from typing import Dict, List

INTENT_DETAILS: Dict[str, Dict] = {
    "venting": {
        "description": "User wants to express feelings or frustrations.",
        "examples": [
            "I just need to get this off my chest.",
            "Can I vent for a moment?",
            "I'm so frustrated right now."
        ],
        "synonyms": ["rant", "complain", "express", "talk about", "share feelings"]
    },
    "comfort": {
        "description": "User is seeking comfort or reassurance.",
        "examples": [
            "I need some comfort.",
            "Can you reassure me?",
            "I feel alone."
        ],
        "synonyms": ["reassure", "console", "soothe", "support"]
    },
    "advice": {
        "description": "User is seeking advice or guidance.",
        "examples": [
            "What should I do?",
            "Do you have any advice?",
            "Can you help me decide?"
        ],
        "synonyms": ["guidance", "suggestion", "recommendation", "help"]
    },
    "gratitude": {
        "description": "User is expressing thanks or appreciation.",
        "examples": [
            "Thank you so much.",
            "I appreciate your help.",
            "You're the best!"
        ],
        "synonyms": ["thanks", "appreciation", "grateful", "gratitude"]
    },
    "greeting": {
        "description": "User is greeting the bot.",
        "examples": [
            "Hello!",
            "Hi there!",
            "Hey!"
        ],
        "synonyms": ["hello", "hi", "hey", "greetings"]
    },
    "goodbye": {
        "description": "User is ending the conversation.",
        "examples": [
            "Goodbye.",
            "See you later.",
            "Bye!"
        ],
        "synonyms": ["bye", "see you", "farewell", "later"]
    },
    "crisis": {
        "description": "User may be in crisis or expressing harmful intent.",
        "examples": [
            "I want to hurt myself.",
            "I can't go on.",
            "Everything feels hopeless."
        ],
        "synonyms": ["suicide", "self-harm", "hopeless", "crisis"]
    },
    "question": {
        "description": "User is asking a general question.",
        "examples": [
            "What is empathy?",
            "How do I cope with stress?",
            "Can you tell me about anxiety?"
        ],
        "synonyms": ["ask", "question", "wonder", "curious"]
    },
    "smalltalk": {
        "description": "User is making small talk or casual conversation.",
        "examples": [
            "How's the weather?",
            "What's your favorite color?",
            "Do you like music?"
        ],
        "synonyms": ["chitchat", "casual", "small talk", "banter"]
    }
}

INTENT_NORMALIZATION: Dict[str, str] = {}
for intent, details in INTENT_DETAILS.items():
    INTENT_NORMALIZATION[intent] = intent
    for synonym in details["synonyms"]:
        INTENT_NORMALIZATION[synonym.lower()] = intent

def normalize_intent(intent_label: str) -> str:
    """Normalize an intent or synonym to a main intent category."""
    return INTENT_NORMALIZATION.get(intent_label.lower(), "smalltalk")

def get_intent_details(intent_label: str) -> Dict:
    """Return details for a given intent label."""
    normalized = normalize_intent(intent_label)
    return INTENT_DETAILS.get(normalized, INTENT_DETAILS["smalltalk"])

def detect_intent(text: str) -> str:
    """Detect user intent from text using keyword matching."""
    text_lower = text.lower()
    for intent, details in INTENT_DETAILS.items():
        for keyword in details["synonyms"] + details["examples"]:
            if keyword.lower() in text_lower:
                return intent
if any(word in text_lower for word in ["hello", "hi", "hey"]):
        return "greeting"
    if any(word in text_lower for word in ["bye", "goodbye", "see you"]):
        return "goodbye"
    return "smalltalk"

def list_intents() -> List[str]:
    return list(INTENT_DETAILS.keys())

if __name__ == "__main__":
    test_texts = [
        "Can I vent for a moment?",
        "Thank you so much!",
        "Do you have any advice?",
        "I want to hurt myself.",
        "Hello!",
        "Bye for now.",
        "What's your favorite color?"
    ]
    for text in test_texts:
        intent = detect_intent(text)
        details = get_intent_details(intent)
        print(f"Text: {text}\nDetected intent: {intent}\nDescription: {details['description']}\n")
