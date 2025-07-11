from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import redis
import json
import os
import sys

# Fix import path for models
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# AI models
from transformers.pipelines import pipeline
import spacy
from models.intent import detect_intent

emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
nlp = spacy.load("en_core_web_lg")

# Redis config
r = redis.Redis(
    host='redis-16244.c80.us-east-1-2.ec2.redns.redis-cloud.com',
    port=16244,
    username='default',
    password='dZth7NbWs6puJxaqizIprq9yRQgRLtIM',
    decode_responses=True
)

try:
    r.ping()
    print("✅ Connected to Redis")
except Exception as e:
    print(f"❌ Redis error: {e}")

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello from EmpathyBot!"}

# Request & Response Models
class Message(BaseModel):
    text: str
    user_id: str | None = None

class EnhancedResponse(BaseModel):
    text: str
    emotion: str
    intent: str
    crisis_alert: bool
    suggested_action: str | None = None

# Utilities
def crisis_check(text: str) -> bool:
    red_flags = ["kill myself", "want to die", "end it all", "suicide", "can’t go on"]
    return any(flag in text.lower() for flag in red_flags)

def update_mood_history(user_id: str, emotion: str):
    timestamp = datetime.now().isoformat()
    r.rpush(f"user:{user_id}:moods", f"{timestamp}|{emotion}")

def generate_response(emotion: str, intent: str) -> str:
    response_map = {
        "sadness": {
            "venting": "It's okay to feel sad. Do you want to talk about what's bothering you?",
            "comfort": "I'm here for you. You're not alone.",
            "advice": "Sometimes writing down your feelings can help. Want to try that?",
        },
        "anger": {
            "venting": "Let it out — what's making you feel this way?",
            "comfort": "Take a deep breath. I'm here with you.",
            "advice": "Would a calming technique help right now?",
        },
        "joy": {
            "gratitude": "I'm happy you're feeling good. Want to share more?",
            "smalltalk": "That’s great to hear! 😊",
        },
        "fear": {
            "comfort": "It’s okay to be scared. I'm right here.",
            "advice": "Try grounding yourself — notice 5 things you can see.",
        },
        "love": {
            "gratitude": "That’s beautiful to hear 💖",
            "comfort": "Love is powerful. Hold onto it.",
        },
        "surprise": {
            "smalltalk": "Whoa! That sounds unexpected. Want to talk about it?",
        },
        "neutral": {
            "smalltalk": "I'm listening. What’s on your mind?",
        },
        "crisis": {
            "crisis": "I'm really sorry you're feeling this way. You're not alone. Please reach out to a mental health professional or call a local helpline. 💙"
        }
    }

    emotion = emotion.lower()
    intent = intent.lower()

    # Try exact match
    if intent in response_map.get(emotion, {}):
        return response_map[emotion][intent]

    # Fallback to neutral
    if intent in response_map.get("neutral", {}):
        return response_map["neutral"][intent]

    # Absolute fallback
    return "I'm here for you — talk to me about whatever’s on your mind."

@app.post("/chat")
async def chat(message: Message) -> EnhancedResponse:
    # Emotion detection
    emotion_raw = emotion_model(message.text)
    emotion = emotion_raw[0]['label'] if emotion_raw else "neutral"

    # Intent detection
    intent = detect_intent(message.text)

    print(f"[DEBUG] Emotion: {emotion}, Intent: {intent}")

    # Crisis check
    crisis_alert = crisis_check(message.text)

    # Build response
    reply = generate_response(emotion, intent)

    # Store memory
    if message.user_id:
        update_mood_history(message.user_id, emotion)
        r.rpush(f"user:{message.user_id}:convo", json.dumps({
            "text": message.text,
            "emotion": emotion,
            "intent": intent,
            "timestamp": datetime.now().isoformat()
        }))

    return EnhancedResponse(
        text=reply,
        emotion=emotion,
        intent=intent,
        crisis_alert=crisis_alert,
        suggested_action="Try deep breathing" if emotion == "fear" else None
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = await chat(Message(text=data))
        await websocket.send_json(response.dict())
