"""
Ollama Handshake Script — BLAST Phase 2 (Link Verification)
Verifies that Ollama is running and llama3.2 model is accessible.
"""

import sys
import os

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

def verify_ollama_connection():
    """Test 1: Verify Ollama server is running and reachable."""
    try:
        import ollama
        models = ollama.list()
        print("[PASS] Test 1: Ollama server is running")
        print(f"   Available models: {[m.model for m in models.models]}")
        return True
    except Exception as e:
        print(f"[FAIL] Test 1: Cannot connect to Ollama - {e}")
        return False


def verify_model_available():
    """Test 2: Verify llama3.2 model is pulled and available."""
    try:
        import ollama
        model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
        models = ollama.list()
        model_names = [m.model for m in models.models]
        
        found = any(name.startswith(model_name) for name in model_names)
        
        if found:
            print(f"[PASS] Test 2: Model '{model_name}' is available")
            return True
        else:
            print(f"[FAIL] Test 2: Model '{model_name}' not found. Available: {model_names}")
            return False
    except Exception as e:
        print(f"[FAIL] Test 2: Error checking model - {e}")
        return False


def verify_model_responds():
    """Test 3: Verify llama3.2 can generate a response."""
    try:
        import ollama
        model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
        print(f"   Sending test prompt to '{model_name}'... (this may take a moment)")
        
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "user", "content": "Respond with exactly: HANDSHAKE_OK"}
            ]
        )
        
        content = response["message"]["content"]
        print(f"[PASS] Test 3: Model responded successfully")
        print(f"   Response: {content[:100]}")
        return True
    except Exception as e:
        print(f"[FAIL] Test 3: Model did not respond - {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("OLLAMA HANDSHAKE - Link Verification")
    print("=" * 50)
    print()
    
    results = []
    results.append(verify_ollama_connection())
    results.append(verify_model_available())
    results.append(verify_model_responds())
    
    print()
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if all(results):
        print(f"ALL TESTS PASSED ({passed}/{total}) - Link is READY")
    else:
        print(f"SOME TESTS FAILED ({passed}/{total}) - Link is BROKEN")
        print("   Fix the issues above before proceeding to Phase 3.")
    
    print("=" * 50)
    sys.exit(0 if all(results) else 1)
