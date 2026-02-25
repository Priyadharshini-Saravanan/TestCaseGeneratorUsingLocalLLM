"""
Flask Backend — Navigation/Routing Layer (BLAST Layer 2)

Orchestrates the test case generation workflow:
User Input --> Validate --> Build Prompt --> Call Ollama --> Stream Response --> UI
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from dotenv import load_dotenv

load_dotenv()

# Add tools to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.ollama_client import generate_response, generate_response_stream, check_health
from tools.prompt_template import build_messages

app = Flask(__name__)

# --- Configuration ---
MAX_INPUT_LENGTH = 5000


# --- Routes ---

@app.route("/")
def index():
    """Serve the chat UI."""
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    """Check Ollama server and model health."""
    status = check_health()
    code = 200 if status["healthy"] else 503
    return jsonify(status), code


@app.route("/api/generate", methods=["POST"])
def generate():
    """
    Generate test cases from user input.
    
    Expects JSON: {"user_input": "..."}
    Returns JSON: {"response": "...", "success": true}
    """
    data = request.get_json()
    
    if not data or "user_input" not in data:
        return jsonify({"success": False, "error": "Missing 'user_input' field"}), 400
    
    user_input = data["user_input"].strip()
    
    # Validate input
    if not user_input:
        return jsonify({"success": False, "error": "Input cannot be empty"}), 400
    
    if len(user_input) > MAX_INPUT_LENGTH:
        return jsonify({
            "success": False, 
            "error": f"Input too long ({len(user_input)} chars). Maximum is {MAX_INPUT_LENGTH} characters."
        }), 400
    
    try:
        messages = build_messages(user_input)
        response_text = generate_response(messages)
        return jsonify({"success": True, "response": response_text})
    except ConnectionError as e:
        return jsonify({"success": False, "error": str(e)}), 503
    except RuntimeError as e:
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"success": False, "error": f"Unexpected error: {str(e)}"}), 500


@app.route("/api/generate/stream", methods=["POST"])
def generate_stream():
    """
    Generate test cases with streaming response.
    
    Expects JSON: {"user_input": "..."}
    Returns: Server-Sent Events (SSE) stream
    """
    data = request.get_json()
    
    if not data or "user_input" not in data:
        return jsonify({"success": False, "error": "Missing 'user_input' field"}), 400
    
    user_input = data["user_input"].strip()
    
    if not user_input:
        return jsonify({"success": False, "error": "Input cannot be empty"}), 400
    
    if len(user_input) > MAX_INPUT_LENGTH:
        return jsonify({
            "success": False,
            "error": f"Input too long. Maximum is {MAX_INPUT_LENGTH} characters."
        }), 400
    
    def stream():
        try:
            messages = build_messages(user_input)
            for chunk in generate_response_stream(messages):
                yield f"data: {chunk}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
    
    return Response(
        stream_with_context(stream()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    
    print(f"Starting Test Case Generator on http://localhost:{port}")
    print(f"Model: {os.getenv('OLLAMA_MODEL', 'llama3.2')}")
    
    # Check health on startup
    status = check_health()
    if status["healthy"]:
        print(f"Ollama: {status['message']}")
    else:
        print(f"WARNING: {status['message']}")
    
    print()
    app.run(host="0.0.0.0", port=port, debug=debug)
