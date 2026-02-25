# 🔍 Findings — Local LLM Test Case Generator

## Research

### Ollama API
- **Ollama Version Installed:** 0.16.2
- **Models Pulled:** None yet — need to run `ollama pull llama3.2`
- **Python Library:** `pip install ollama`
- **Key API:** `ollama.chat(model='llama3.2', messages=[...])` for chat-style completions
- **Message format:** `{"role": "system/user/assistant", "content": "..."}`
- **Streaming:** Supported via `stream=True` parameter

## Discoveries
- Ollama is already installed on the system (v0.16.2)
- llama3.2 model needs to be pulled before first use
- Ollama runs on `http://localhost:11434` by default

## Constraints
- Must use **local** LLM via Ollama (no cloud API calls)
- User will provide the test case generation prompt template
- System must be deterministic where possible (BLAST rule)
- Model: llama3.2 (open source, ~2GB download)

## Resources
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [Ollama API Docs](https://ollama.com/docs)
