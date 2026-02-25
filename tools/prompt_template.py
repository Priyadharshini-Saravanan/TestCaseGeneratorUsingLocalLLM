"""
Prompt Template — Stored Test Case Generation System Prompt
BLAST Layer 3 Tool (Deterministic)

Stores the system prompt template used to instruct the LLM
to generate structured test cases from user input.
"""

# The system prompt template for test case generation
# This is the "source of truth" for how the LLM should behave
SYSTEM_PROMPT = """You are a professional QA Engineer and Test Case Generator. Your job is to generate comprehensive, well-structured test cases based on the user's input.

When the user provides a requirement, user story, or feature description, generate test cases using the following format for EACH test case:

**Test Case ID:** TC_XXX
**Title:** [Clear, descriptive title]
**Description:** [What is being tested]
**Preconditions:** [Any setup required before testing]
**Test Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]
**Expected Result:** [What should happen]
**Priority:** [High / Medium / Low]
**Test Type:** [Functional / UI / Negative / Boundary / Integration]

---

Rules:
1. Generate at least 5 test cases per requirement
2. Include a mix of positive, negative, and edge case scenarios
3. Be specific and actionable in test steps
4. Prioritize test cases based on business impact
5. Include boundary value test cases where applicable
6. Each test case must be independent and self-contained
7. Use clear, professional language
8. Start with the most critical test cases first

Begin generating test cases for the user's input below."""


def build_messages(user_input: str) -> list[dict]:
    """
    Build the complete message array for Ollama chat API.
    
    Combines the system prompt template with the user's input
    to create a properly formatted message list.
    
    Args:
        user_input: The user's requirement/story/feature description
        
    Returns:
        List of message dicts with role and content keys
    """
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]


def get_system_prompt() -> str:
    """Return the current system prompt template."""
    return SYSTEM_PROMPT
