EMOTION_DETAILS = {
    "sadness": {"description": "Feeling down or unhappy", "emoji": "😢", "synonyms": ["unhappy", "blue", "down", "depressed", "hopeless", "miserable"]},
    "joy": {"description": "Feeling happy or delighted", "emoji": "😊", "synonyms": ["happy", "delighted", "cheerful", "content", "elated", "excited"]},
    "anger": {"description": "Feeling mad or frustrated", "emoji": "😠", "synonyms": ["mad", "frustrated", "irritated", "annoyed", "resentful", "furious"]},
    "fear": {"description": "Feeling scared or anxious", "emoji": "😨", "synonyms": ["scared", "anxious", "nervous", "worried", "afraid", "terrified"]},
    "surprise": {"description": "Feeling surprised or shocked", "emoji": "😲", "synonyms": ["shocked", "amazed", "astonished", "startled"]},
    "love": {"description": "Feeling love or affection", "emoji": "❤️", "synonyms": ["affection", "fondness", "caring", "compassion", "tenderness"]},
    "disgust": {"description": "Feeling disgusted or repulsed", "emoji": "🤢", "synonyms": ["repulsed", "sickened", "revolted", "nauseated"]},
    "trust": {"description": "Feeling trust or confidence", "emoji": "🤝", "synonyms": ["confidence", "faith", "secure", "safe"]},
    "anticipation": {"description": "Feeling anticipation or excitement", "emoji": "🤩", "synonyms": ["excitement", "expectation", "eager", "hopeful"]},
    "boredom": {"description": "Feeling uninterested or bored", "emoji": "🥱", "synonyms": ["uninterested", "apathetic", "indifferent", "weary"]},
    "shame": {"description": "Feeling ashamed or embarrassed", "emoji": "😳", "synonyms": ["embarrassed", "humiliated", "guilty"]},
    "pride": {"description": "Feeling proud or accomplished", "emoji": "🏅", "synonyms": ["accomplished", "satisfied", "fulfilled"]},
    "envy": {"description": "Feeling envious or jealous", "emoji": "😒", "synonyms": ["jealous", "covetous"]},
    "relief": {"description": "Feeling relieved or at ease", "emoji": "😌", "synonyms": ["at ease", "comforted"]},
    "neutral": {"description": "No strong emotion", "emoji": "😐", "synonyms": ["calm", "indifferent", "okay"]},
}

EMOTION_NORMALIZATION = {}
for main, details in EMOTION_DETAILS.items():
    EMOTION_NORMALIZATION[main] = main
    for synonym in details["synonyms"]:
        EMOTION_NORMALIZATION[synonym.lower()] = main

def get_emotion_details(emotion_label: str):
    normalized = normalize_emotion(emotion_label)
    return EMOTION_DETAILS.get(normalized, EMOTION_DETAILS["neutral"])

def normalize_emotion(emotion_label: str) -> str:
    return EMOTION_NORMALIZATION.get(emotion_label.lower(), "neutral")
