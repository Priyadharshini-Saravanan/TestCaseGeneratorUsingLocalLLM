# 📜 Project Constitution — Local LLM Test Case Generator

## Discovery Answers
- **North Star:** Local LLM Test Case Generator based on user input with a proper template, using Ollama API (llama3.2)
- **Integrations:** Ollama (local only)
- **Source of Truth:** N/A — user provides input directly via chat UI
- **Delivery Payload:** Chat UI where user enters input and sees generated test cases
- **Behavioral Rules:** User enters input → system generates test cases using local LLM via Ollama

---

## Data Schemas

### Input Schema (User → System)
```json
{
  "user_input": "string — requirement, user story, or feature description",
  "session_id": "string — unique chat session identifier"
}
```

### System Prompt Template (Stored in Code)
```json
{
  "role": "system",
  "content": "Test case generation system prompt with template (to be provided by user)"
}
```

### Output Schema (LLM → User)
```json
{
  "test_cases": [
    {
      "id": "string — TC_001",
      "title": "string — test case title",
      "description": "string — what is being tested",
      "preconditions": "string — setup requirements",
      "steps": ["string — step 1", "string — step 2"],
      "expected_result": "string — expected outcome",
      "priority": "string — High/Medium/Low"
    }
  ],
  "summary": "string — brief summary of generated test cases",
  "total_count": "number — total test cases generated"
}
```

---

## Behavioral Rules
1. All LLM calls are **local only** via Ollama — no external API calls.
2. Business logic must be **deterministic** — LLM is used only for generation.
3. Test case prompt template is **stored in code**, not user-configurable.
4. All intermediate files go in `.tmp/`.
5. Environment config goes in `.env`.
6. Model: **llama3.2** (open source).

---

## Architectural Invariants
1. **3-Layer Architecture (A.N.T.)**:
   - `architecture/` — Technical SOPs (Markdown)
   - Navigation — Routing/orchestration layer (Python backend)
   - `tools/` — Deterministic Python scripts (atomic, testable)
2. If logic changes → Update SOP **before** updating code.
3. No code in `tools/` until Discovery is complete and Data Schema is approved.

---

## Technology Stack
- **LLM Runtime:** Ollama (local)
- **Model:** llama3.2
- **Backend:** Python (Flask)
- **Frontend:** HTML/CSS/JS (Chat UI)
- **Communication:** Ollama Python library (`pip install ollama`)
