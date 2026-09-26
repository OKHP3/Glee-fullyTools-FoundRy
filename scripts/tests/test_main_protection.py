"""Offline contract tests for the live-settings checker."""

import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location(
    "check_main_protection", Path(__file__).resolve().parents[1] / "check-main-protection.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class MainProtectionTests(unittest.TestCase):
    def setUp(self):
        self.protection = {
            "required_pull_request_reviews": {
                "required_approving_review_count": 1,
                "dismiss_stale_reviews": True,
            },
            "required_status_checks": {"contexts": ["Validate manifest"], "strict": True},
            "enforce_admins": {"enabled": True},
            "allow_force_pushes": {"enabled": False},
            "allow_deletions": {"enabled": False},
        }
        self.environment = {
            "name": "github-pages",
            "deployment_branch_policy": {"protected_branches": True, "custom_branch_policies": False},
        }

    def test_expected_safeguards_pass(self):
        self.assertEqual(audit.check(self.protection, self.environment), [])

    def test_missing_and_weakened_reviews_fail(self):
        self.protection["required_pull_request_reviews"] = None
        self.assertTrue(any("reviews" in issue for issue in audit.check(self.protection, self.environment)))
        self.protection["required_pull_request_reviews"] = {
            "required_approving_review_count": 0, "dismiss_stale_reviews": False
        }
        issues = audit.check(self.protection, self.environment)
        self.assertTrue(any("at least one" in issue for issue in issues))
        self.assertTrue(any("stale" in issue for issue in issues))

    def test_other_controls_fail_independently(self):
        alterations = [
            ("required_status_checks", None, "status check"),
            ("required_status_checks", {"contexts": ["Validate manifest"], "strict": False}, "up-to-date"),
            ("enforce_admins", {"enabled": False}, "enforce_admins"),
            ("allow_force_pushes", {"enabled": True}, "allow_force_pushes"),
            ("allow_deletions", {"enabled": True}, "allow_deletions"),
        ]
        for key, changed, phrase in alterations:
            with self.subTest(key=key, changed=changed):
                original = self.protection[key]
                self.protection[key] = changed
                self.assertTrue(any(phrase in issue for issue in audit.check(self.protection, self.environment)))
                self.protection[key] = original
        self.assertTrue(audit.check(self.protection, None))
        self.environment["deployment_branch_policy"] = None
        self.assertTrue(any("restrict" in issue for issue in audit.check(self.protection, self.environment)))

    def test_custom_deployment_policy_must_allow_main(self):
        self.environment["deployment_branch_policy"] = {
            "protected_branches": False, "custom_branch_policies": True
        }
        self.assertEqual(audit.check(self.protection, self.environment, [{"name": "main"}]), [])
        self.assertTrue(any(
            "permit main" in issue
            for issue in audit.check(self.protection, self.environment, [{"name": "release/*"}])
        ))
        self.assertTrue(audit.check(self.protection, self.environment))

    def test_api_error_is_not_a_pass(self):
        with patch.dict(audit.os.environ, {"GITHUB_TOKEN": "test", "REPO_SETTINGS_READ_TOKEN": ""}):
            with patch.object(audit, "fetch", side_effect=RuntimeError("GitHub returned HTTP 403")):
                self.assertEqual(audit.main(), 2)

    def test_main_reads_live_rule_and_environment(self):
        responses = [
            {"full_name": audit.REPOSITORY, "default_branch": "main"},
            self.protection,
            {"total_count": 1, "environments": [{"name": "github-pages"}]},
            self.environment,
        ]
        with patch.dict(audit.os.environ, {"GITHUB_TOKEN": "test", "REPO_SETTINGS_READ_TOKEN": ""}):
            with patch.object(audit, "fetch", side_effect=responses) as fetch:
                self.assertEqual(audit.main(), 0)
        paths = [call.args[0] for call in fetch.call_args_list]
        self.assertEqual(paths, [
            "/repos/OKHP3/Glee-fullyTools-FoundRy",
            "/repos/OKHP3/Glee-fullyTools-FoundRy/branches/main/protection",
            "/repos/OKHP3/Glee-fullyTools-FoundRy/environments?per_page=100",
            "/repos/OKHP3/Glee-fullyTools-FoundRy/environments/github-pages",
        ])

    def test_truncated_environment_list_is_incomplete(self):
        responses = [
            {"full_name": audit.REPOSITORY, "default_branch": "main"},
            self.protection,
            {"total_count": 101, "environments": [{"name": "github-pages"}]},
        ]
        with patch.dict(audit.os.environ, {"GITHUB_TOKEN": "test", "REPO_SETTINGS_READ_TOKEN": ""}):
            with patch.object(audit, "fetch", side_effect=responses):
                self.assertEqual(audit.main(), 2)


if __name__ == "__main__":
    unittest.main()