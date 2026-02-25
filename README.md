# ProjectTestCaseGen - Local LLM Test Case Generator

A local LLM-powered test case generator built with **Ollama**, **Flask**, and the **llama3.2** model. This application generates professional test cases from free-form requirements and user stories without requiring cloud services.

## Overview

ProjectTestCaseGen is a full-stack web application that:
- ✅ Accepts user requirements, user stories, or feature descriptions
- ✅ Generates structured test cases using a local, privacy-preserving Ollama LLM
- ✅ Streams responses in real-time to a modern web UI
- ✅ Handles edge cases and provides health checks
- ✅ Runs entirely locally—no cloud dependencies or external APIs

## Architecture

The project follows the **B.L.A.S.T. Protocol** and **A.N.T. 3-Layer Architecture**:

```
Layer 1 (Blueprint)    → System architecture & SOPs
    ↓
Layer 2 (Navigation)   → Flask backend & routing (app.py)
    ↓
Layer 3 (Tools)        → Ollama client & prompt templates (tools/)
```

### Project Structure

```
ProjectTestCaseGen/
├── app.py                          # Flask backend & API routes
├── requirements.txt                # Python dependencies
├── .env                            # Configuration (model name, API URL)
│
├── tools/
│   ├── ollama_client.py            # Ollama API wrapper & health checks
│   ├── prompt_template.py          # LLM system prompt & message builder
│   ├── handshake.py                # Server connectivity test script
│   └── __pycache__/                # Python cache
│
├── templates/
│   └── index.html                  # Web UI (chat interface)
│
├── static/
│   ├── css/
│   │   └── style.css               # UI styling
│   └── js/
│       └── app.js                  # Client-side logic
│
├── architecture/
│   └── sop_testcase_generation.md  # Standard Operating Procedure
│
├── README.md                       # This file
├── task_plan.md                    # Development roadmap
├── progress.md                     # Implementation log
└── findings.md                     # Research & discovery notes
```

## Features

### Core Functionality
- **Test Case Generation**: Accepts requirements and produces formatted test cases
- **Real-time Streaming**: Responses stream to the UI for immediate feedback
- **Health Checks**: API endpoint to verify Ollama server and model availability
- **Input Validation**: Prevents empty submissions and excessive input (max 5000 chars)
- **Error Handling**: Friendly error messages for common failure scenarios

### Technology Stack
- **Backend**: Flask 3.1.0
- **LLM**: Ollama (llama3.2 model)
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Environment**: Python 3.x, local execution (no cloud required)

## Prerequisites

Before running this project, ensure you have:

1. **Python 3.8+** installed
2. **Ollama** installed and running locally
   - Download from: https://ollama.ai
   - Or install via: `brew install ollama` (macOS) or `choco install ollama` (Windows)
3. **llama3.2 model** downloaded locally
4. **pip** (Python package manager)

## Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Priyadharshini-Saravanan/ProjectTestCaseGen.git
cd ProjectTestCaseGen
```

### Step 2: Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
Create a `.env` file in the project root:
```
OLLAMA_MODEL=llama3.2
OLLAMA_API_URL=http://localhost:11434
```

### Step 5: Verify Ollama Setup (Optional)
Run the handshake test to verify everything is connected:
```bash
python tools/handshake.py
```

Expected output: All 3 tests should pass.

### Step 6: Start the Application
```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## Usage

1. Open your browser to `http://localhost:5000`
2. Enter a requirement or user story in the chat input (max 5000 characters)
3. Click "Generate Test Cases" or press Enter
4. Watch as the LLM generates structured test cases in real-time
5. Copy or save the generated test cases

### Example Input
```
User Story: As a user, I want to log in with my email and password so that I can access my account securely.
```

### Example Output
```
Test Case 1: Valid Login
- Precondition: User is on login page
- Steps: Enter valid email and password, click submit
- Expected: User is logged in and redirected to dashboard

Test Case 2: Invalid Email Format
- Precondition: User is on login page
- Steps: Enter invalid email format, click submit
- Expected: Error message displayed...
```

## API Endpoints

### GET `/`
Serves the web UI.

### GET `/api/health`
Check Ollama server and model health.

**Response (200 OK):**
```json
{
  "healthy": true,
  "message": "Model 'llama3.2' is ready",
  "models": ["llama3.2:latest", "other_model:tag"]
}
```

**Response (503 Service Unavailable):**
```json
{
  "healthy": false,
  "message": "Ollama connection failed: Connection refused",
  "models": []
}
```

### POST `/api/generate`
Generate test cases from user input.

**Request:**
```json
{
  "user_input": "Your requirement or user story here"
}
```

**Response (200 OK):**
```json
{
  "response": "Generated test cases here..."
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Input is empty"
}
```

## Configuration

All configuration is managed via `.env`:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `llama3.2` | LLM model to use |
| `OLLAMA_API_URL` | `http://localhost:11434` | Ollama server URL |

## Workflow

```
User Input (text)
    ↓
Validate Input (non-empty, ≤5000 chars)
    ↓
Build Prompt (system template + user input)
    ↓
Send to Ollama (llama3.2 via chat API)
    ↓
Stream Response to UI
    ↓
Display Test Cases
```

## Edge Cases & Error Handling

| Scenario | Handling |
|----------|----------|
| Empty input | Return validation error before calling LLM |
| Input > 5000 characters | Truncate and warn user |
| Ollama server not running | Friendly error: "Connect to http://localhost:11434" |
| Model not found | Error with install instruction for llama3.2 |
| LLM timeout (slow response) | Streaming with visual loading indicator |
| Network error | Connection error with retry suggestion |

## Development

### File Roles

- **app.py**: Flask backend, routing, API logic
- **tools/ollama_client.py**: Low-level Ollama API wrapper
- **tools/prompt_template.py**: LLM system prompt & message formatting
- **templates/index.html**: Web UI markup
- **static/css/style.css**: Styling
- **static/js/app.js**: Client-side chat logic
- **architecture/sop_testcase_generation.md**: SOP documentation

### Extending the Project

To add new features:
1. Update the SOP in `architecture/sop_testcase_generation.md` first
2. Implement backend changes in `app.py` or new tools in `tools/`
3. Update frontend components in `templates/` and `static/`
4. Test with `tools/handshake.py` if changes affect Ollama integration

## Troubleshooting

### "Ollama connection failed"
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_API_URL` in `.env` matches your setup

### "Model 'llama3.2' not found"
- Pull the model: `ollama pull llama3.2`
- Verify with: `ollama list`

### Port 5000 already in use
- Kill the existing process or run: `python app.py --port 8000`

### Unicode/Emoji encoding errors (Windows)
- Already handled in `app.py` via stdout reconfiguration

## Performance Notes

- **First Response**: May take 10-30 seconds as the model loads into memory
- **Subsequent Responses**: Faster (3-10 seconds) as model remains in RAM
- **Token Limit**: Input limited to 5000 characters to prevent excessive token usage
- **Memory**: llama3.2 requires ~4GB RAM available

## Future Enhancements

- [ ] Support for multiple LLM models
- [ ] Test case export formats (JSON, CSV, Gherkin)
- [ ] Conversation history and session management
- [ ] Test case refinement/iteration UI
- [ ] Integration with test automation frameworks
- [ ] Docker containerization

## License

This project is provided as-is for local tool usage.

## Author

**Priyadharshini-Saravanan**  
GitHub: https://github.com/Priyadharshini-Saravanan/ProjectTestCaseGen

## Support & Feedback

For issues, questions, or contributions:
1. Check [progress.md](progress.md) for known issues
2. Review [findings.md](findings.md) for research notes
3. Submit issues or feature requests via GitHub

---

**Last Updated**: February 2026  
**Status**: Active Development
