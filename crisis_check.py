import re

CRISIS_PATTERNS = [
    r"\b(kill|end|harm) (my|me|self)\b",
    r"\b(don't|do not) want to live\b",
    r"\b(nobody cares|worthless|hopeless)\b"
]

def is_crisis(text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in CRISIS_PATTERNS)

def crisis_protocol():
    return {
        "response": "I'm deeply concerned about what you're saying. Please call a helpline.",
        "resources": [
            "National Suicide Prevention Lifeline: 988",
            "Crisis Text Line: Text HOME to 741741"
        ]
    }
