"""
Ollama Client — Wrapper for Ollama Chat API
BLAST Layer 3 Tool (Deterministic)

Handles all communication with the local Ollama server.
Provides error handling, streaming support, and health checks.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

import ollama


def get_model_name() -> str:
    """Get the configured model name from environment."""
    return os.getenv("OLLAMA_MODEL", "llama3.2")


def check_health() -> dict:
    """
    Check if Ollama server is running and model is available.
    
    Returns:
        dict with 'healthy' (bool), 'message' (str), 'models' (list)
    """
    try:
        models = ollama.list()
        model_names = [m.model for m in models.models]
        target = get_model_name()
        model_found = any(name.startswith(target) for name in model_names)
        
        return {
            "healthy": model_found,
            "message": f"Model '{target}' is ready" if model_found else f"Model '{target}' not found",
            "models": model_names
        }
    except Exception as e:
        return {
            "healthy": False,
            "message": f"Ollama connection failed: {str(e)}",
            "models": []
        }


def generate_response(messages: list[dict]) -> str:
    """
    Send messages to Ollama and get a complete response.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        
    Returns:
        The assistant's response content as a string
        
    Raises:
        ConnectionError: If Ollama server is not reachable
        RuntimeError: If model fails to respond
    """
    try:
        model = get_model_name()
        response = ollama.chat(
            model=model,
            messages=messages
        )
        return response["message"]["content"]
    except ollama.ResponseError as e:
        raise RuntimeError(f"Ollama model error: {str(e)}")
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Ollama: {str(e)}")


def generate_response_stream(messages: list[dict]):
    """
    Send messages to Ollama and stream the response chunks.
    
    Yields response text chunks as they arrive for real-time display.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        
    Yields:
        str: Response text chunks
        
    Raises:
        ConnectionError: If Ollama server is not reachable
        RuntimeError: If model fails to respond
    """
    try:
        model = get_model_name()
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )
        for chunk in stream:
            content = chunk["message"]["content"]
            if content:
                yield content
    except ollama.ResponseError as e:
        raise RuntimeError(f"Ollama model error: {str(e)}")
    except Exception as e:
        raise ConnectionError(f"Failed to connect to Ollama: {str(e)}")
