from __future__ import annotations

import json
import socket
import tempfile
import threading
import unittest
from pathlib import Path

from app.server import FoundryServer


class HttpContractEdgeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(__file__).resolve().parents[2]
        self.server = FoundryServer(("127.0.0.1", 0), self.root, Path(self.tmp.name))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def request(self, method, path, headers=None):
        import http.client

        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.request(method, path, headers=headers or {})
        response = connection.getresponse()
        raw = response.read()
        content_type = response.getheader("Content-Type", "")
        connection.close()
        return response.status, content_type, raw

    def raw_request(self, request):
        connection = socket.create_connection(("127.0.0.1", self.port), timeout=2)
        connection.settimeout(2)
        try:
            connection.sendall(request)
            connection.shutdown(socket.SHUT_WR)
            chunks = []
            while True:
                chunk = connection.recv(65535)
                if not chunk:
                    break
                chunks.append(chunk)
        finally:
            connection.close()
        return b"".join(chunks)

    def test_malformed_content_length_returns_json_400(self):
        prefix = (
            "POST /api/projects HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{self.port}\r\n"
            "Content-Type: application/json\r\n"
            "X-Foundry-Request: 1\r\n"
        ).encode()
        for value in (b"nope", b"-1"):
            with self.subTest(content_length=value):
                response = self.raw_request(
                    prefix + b"Content-Length: " + value + b"\r\n\r\n{}"
                )
                header, body = response.split(b"\r\n\r\n", 1)
                self.assertIn(b"400 Bad Request", header)
                self.assertIn(b"Content-Type: application/json; charset=utf-8", header)
                self.assertIsInstance(json.loads(body), dict)
                self.assertIn("error", json.loads(body))

    def test_malformed_json_body_returns_json_400(self):
        response = self.raw_request(
            (
                "POST /api/projects HTTP/1.1\r\n"
                f"Host: 127.0.0.1:{self.port}\r\n"
                "Content-Type: application/json\r\n"
                "X-Foundry-Request: 1\r\n"
                "Content-Length: 1\r\n\r\n"
                "x"
            ).encode()
        )
        header, body = response.split(b"\r\n\r\n", 1)
        self.assertIn(b"400 Bad Request", header)
        self.assertIn(b"Content-Type: application/json; charset=utf-8", header)
        self.assertEqual(json.loads(body), {"error": "invalid or excessively nested JSON"})

    def test_loopback_host_alias_is_allowed_but_malformed_hosts_are_rejected(self):
        status, content_type, raw = self.request(
            "GET",
            "/api/health",
            {"Host": f"localhost:{self.port}", "Origin": f"http://localhost:{self.port}"},
        )
        self.assertEqual(status, 200)
        self.assertTrue(content_type.startswith("application/json"))
        self.assertEqual(json.loads(raw), {"status": "ok"})

        for headers in (
            {"Host": f"127.0.0.1:not-a-port"},
            {"Host": f"127.0.0.1:{self.port}", "Origin": f"http://127.0.0.1:not-a-port"},
        ):
            with self.subTest(headers=headers):
                status, content_type, raw = self.request("GET", "/api/health", headers)
                self.assertEqual(status, 403)
                self.assertTrue(content_type.startswith("application/json"))
                self.assertEqual(json.loads(raw), {"error": "foreign Host or Origin"})

    def test_explicitly_unsupported_methods_return_json_405(self):
        for method in ("DELETE", "PATCH"):
            with self.subTest(method=method):
                status, content_type, raw = self.request(method, "/api/health")
                self.assertEqual(status, 405)
                self.assertTrue(content_type.startswith("application/json"))
                self.assertEqual(json.loads(raw), {"error": "method not allowed"})

    def test_trace_and_connect_return_json_501(self):
        for method in ("TRACE", "CONNECT"):
            with self.subTest(method=method):
                status, content_type, raw = self.request(method, "/api/health")
                self.assertEqual(status, 501)
                self.assertTrue(content_type.startswith("application/json"))
                self.assertEqual(json.loads(raw), {"error": "method not implemented"})


if __name__ == "__main__":
    unittest.main()
