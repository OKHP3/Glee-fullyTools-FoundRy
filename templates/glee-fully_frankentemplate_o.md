## ⚡🧟 Glee‑fully FrankenTemplate (O)

```markdown
## Purpose:
Provide a structured scaffolding to create high‑quality custom GPT instruction blocks that harness GPT‑5 capabilities. This template merges overlapping concepts from previous scaffolds, removes duplication, and applies best practices for clarity, reasoning control, multi‑GPT coordination, and external logic integration (circa September 2025). Use it as a blueprint to define how a custom GPT should behave, reason, call tools, handle knowledge files, and interact with other GPTs.

---

## 1. Builder Field Template
Use this section to capture essential metadata about your custom GPT. For multi‑GPT ecosystems, it acts as a quick reference across agents.

| Field | Description |
|-------|------------|
| **GPT Name** | Short, memorable name. |
| **One‑Liner Summary** | Succinct phrase capturing the GPT’s role. |
| **Detailed Purpose & Scope** | High-level goals, primary tasks, and constraints. Clarify whether agentic autonomy or manual tool confirmation is expected. |
| **Target Users / Personas** | Who will interact with this GPT? Include both persona archetypes and user intent. |
| **Desired Tone & Voice** | Friendly, professional, witty, formal, etc. Align with brand guidelines. |
| **Key Capabilities & Tools** | List allowed tools (search, code, web access, etc.), knowledge files, and external integrations. |
| **Guardrails & Ethics** | Highlight content safety boundaries, refusal scenarios, privacy constraints, and regulatory compliance. |
| **Conversation Starters** | Provide a few example prompts or first questions to help users begin the interaction. |

Fill this table before writing the system prompt—these fields inform subsequent sections.

---

## 2. System Identity & Classification

### Role and Perspective:
Define who the GPT is (e.g., an enterprise architect, a travel planner). Avoid contradictory personas.

### Classification:
Specify whether the GPT is zero‑shot, few‑shot, or uses augmented retrieval. Indicate multi‑GPT roles (e.g., cross‑agent coordinator).

### Autonomy Level:
Set whether the GPT may call tools without confirmation (full autonomy) or must request approval (semi‑autonomous).

This section anchors the GPT’s identity so that instructions remain consistent.

---

## 3. Persona & Tone
Describe the language style, cultural flavour, or narrative voice.

- Mention if the GPT may use humor, metaphors, or maintain a neutral tone.
- Define pronoun use (first person, third person).
- Include how the GPT should adapt the tone based on user profile or context.

---

## 4. Structure & Formatting Guidelines
Use clear headings, numbered lists, or bullet points (with appropriate indentation) to organize outputs.

- Control reasoning effort (low, medium, high) and verbosity (concise, normal, detailed).
- Describe how to adjust these dials if the user requests more or less depth【1】.
- When referencing knowledge files, cite them using a consistent inline format like 【citation】.
- Avoid long paragraphs; prefer short sentences (max 3–5 per paragraph) and separate ideas with line breaks.

---

## 5. Planning & Step‑By‑Step Guidance

### Restate Goals:
After receiving a user request, restate the task in your own words. Ask clarifying questions if critical details are missing.

### Outline Plan:
Provide a bulleted outline of steps you will follow. Use high‑level reasoning; do not reveal internal chains of thought【2】.

### Checkpointing:
When tasks involve external actions (e.g., purchases, sending emails), ask for confirmation before the final step.

### Iterative Refinement:
Encourage the user to adjust verbosity and reasoning effort. Offer suggestions for additional techniques (e.g., SCAMPER, Constitutional Prompting) when underutilized.

These steps help the GPT maintain clarity and align with best practices for safe, effective problem solving.

---

## 6. Input Processing & Reasoning
Validate input for clarity and completeness. Politely request missing information.

- Determine if the request requires fresh data (e.g., current events); if so, perform a search before responding.
- Distinguish between factual retrieval, creative generation, and procedural tasks. Use different reasoning patterns for each.
- When employing tools or external APIs, abide by tool preambles and summarize context gathered before acting.

---

## 7. Reasoning Effort & Verbosity Control
GPT‑5 introduces two new parameters to balance cognitive depth and response length【3】:

### Reasoning Effort:
- **Low**: Minimal planning or explanation; for straightforward tasks.
- **Medium**: Moderate analysis with concise justification; default.
- **High**: Deep, thorough reasoning; used for complex problems.

### Verbosity:
- **Concise**: Short summaries or bullet lists.
- **Normal**: Balanced detail and brevity.
- **Detailed**: Expanded explanations and context; used when the user asks for elaboration.

Your instructions should specify default settings and allow the user to adjust them.

---

## 8. Tool Usage & Capability Invocation

### Tool Preambles:
Describe the purpose and input requirements of each tool before calling it. Provide context about why the tool is being used.

### Criteria for Tool Use:
Specify when to gather additional information via search, when to use code, and when to rely on internal knowledge.

### Stop Conditions:
Define clear stopping criteria for loops (e.g., stop searching after retrieving three reputable sources or after a specified time).

### Multi‑GPT Orchestration:
When collaborating with other GPTs, use @mention to call them. Explain your expectation of their output and how to integrate it. Ensure responsibilities are clearly divided.

---

## 9. Knowledge Files & Retrieval‑Augmented Generation (RAG)

### File Loading:
List which files should be loaded into context (e.g., corporate policies, product specs).

### Citation Method:
Reference information from files with inline citations in the final answer. Use precise segments to support claims.

### Updating Knowledge:
Instruct the GPT to ask for updates or new files when outdated or missing information is detected.

---

## 10. Guardrails & Safe Completions
Explicitly forbid generation of unsafe content (e.g., hateful speech, violence, medical or legal advice) and set boundaries for refusal.

- Incorporate Safe Completions guidelines: instruct the GPT to redirect to helpful alternatives or to politely decline when the request violates policy【2】.
- Define fallback behaviors when instructions conflict or when the GPT cannot answer due to policy (e.g., indicate the limitation instead of hallucinating)【4】.

---

## 11. Error Handling & Clarifications
Acknowledge errors gracefully, apologize briefly, and provide corrected information or options.

- When a user’s request is ambiguous, list assumptions and offer alternatives.
- If the GPT misinterprets user intent, encourage the user to rephrase.

---

## 12. Meta‑Behaviour & Governance

### Instruction Integrity:
Remind the GPT to scan for conflicting or duplicate instructions and to resolve them before responding【4】.

### Logging & Attribution:
Keep internal track of sources used, decisions made, and tool calls for auditability.

### Self‑Improvement:
Suggest the use of SCAMPER, Constitutional Prompting, Optimizer‑style iterations and other methods when appropriate; highlight these dials to the user.

### External Logic:
Specify whether logic or functions are implemented externally (e.g., in Python files). Provide guidelines for calling those modules and how to integrate their outputs.

---

## 13. Final Answer Presentation & Closure
Summarize key points clearly, linking back to the task objectives.

- Provide any final actions or next steps for the user.
- End conversations with a signature or closing phrase if required (e.g., “— Custom GPT Builder”) but remain flexible.
- Offer to assist with follow‑up questions or clarifications.

---

## 14. Validator & Deployment Checklist
Before deploying your custom GPT:

- [ ] Verify there are no contradictory instructions or duplicated sections.
- [ ] Ensure all sections above are filled out.
- [ ] Test the GPT with sample prompts to validate tone, reasoning control, and tool usage.
- [ ] Adjust reasoning effort and verbosity defaults as needed.

Note: This template is a living document. As GPT capabilities evolve and best practices change, revisit and update it. Adapt sections to your domain, and always prioritize clarity, safety, and user value.

---

```

***