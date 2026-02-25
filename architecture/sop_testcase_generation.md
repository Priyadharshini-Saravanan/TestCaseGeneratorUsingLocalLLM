# SOP: Test Case Generation Workflow

## Goal
Accept user input (requirement, user story, or feature description) and generate structured, professional test cases using the local Ollama LLM (llama3.2).

---

## Workflow

```
User Input (text) 
    --> Validate Input (non-empty, reasonable length)
    --> Build Prompt (system template + user input)
    --> Send to Ollama (llama3.2 via chat API)
    --> Receive LLM Response (raw text)
    --> Return Response to UI
```

---

## Input
- **Source:** Chat UI text input
- **Format:** Free-form text (requirement, user story, feature description)
- **Validation:**
  - Must not be empty or whitespace-only
  - Max length: 5000 characters (prevents excessive token usage)

## Output
- **Format:** LLM-generated test cases as formatted text/markdown
- **Delivery:** Displayed in the chat UI as an assistant message

---

## Tool Logic

### 1. `prompt_template.py`
- Stores the system prompt that instructs LLM to generate test cases
- Function `build_messages(user_input)` returns the full message array:
  - `[{role: "system", content: <template>}, {role: "user", content: <user_input>}]`

### 2. `ollama_client.py`
- Wraps `ollama.chat()` with:
  - Model name from `.env`
  - Error handling (connection errors, timeouts)
  - Streaming support for real-time response display

---

## Edge Cases
| Scenario | Handling |
|----------|----------|
| Empty input | Return validation error before calling LLM |
| Very long input (>5000 chars) | Truncate and warn user |
| Ollama server not running | Return friendly error message |
| Model not found | Return error with install instructions |
| LLM timeout / slow response | Streaming with visual indicator |

---

## Golden Rule
If this workflow logic changes, **update this SOP before updating any code**.
