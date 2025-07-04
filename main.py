from transformers.pipelines import pipeline
import spacy
from typing import Literal
from pydantic import BaseModel
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import redis
import json
from datetime import datetime

# Load AI models
emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
nlp = spacy.load("en_core_web_lg")  # For intent/entity detection


import redis

r = redis.Redis(
    host='redis-16244.c80.us-east-1-2.ec2.redns.redis-cloud.com',  
    port=16244,                                              
    username='default',                                         
    password='dZth7NbWs6puJxaqizIprq9yRQgRLtIM',                  
    decode_responses=True                                       
)

try:
    r.ping() 
    print("✅ Successfully connected to Redis!")
except Exception as e:
    print(f"❌ Redis connection failed: {e}")
    
# FastAPI app setup
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class Message(BaseModel):
    text: str
    user_id: str | None = None  # For personalized memory

class EnhancedResponse(BaseModel):
    text: str
    emotion: str
    intent: str
    suggested_action: str | None = None
    crisis_alert: bool = False

# Track emotion trends
def update_mood_history(user_id: str, emotion: str):
    timestamp = datetime.now().isoformat()
    r.rpush(f"user:{user_id}:moods", f"{timestamp}|{emotion}")

# Detect harmful content
def crisis_check(text: str) -> bool:
    red_flags = ["kill myself", "want to die", "end it all"]
    return any(flag in text.lower() for flag in red_flags)

# Generate therapist-like responses
def generate_response(emotion: str, intent: str) -> str:
    responses = {
        "sadness": {
            "venting": "It sounds like you're carrying a heavy weight. Would you like to talk more about what's hurting?",
            "comfort": "I hear your pain. You're not alone in this.",
        },
        "anger": {
            "venting": "Anger is a natural emotion. What's making you feel this way?",
        }
    }
    return responses.get(emotion, {}).get(intent, "I appreciate you sharing that.")

@app.post("/chat")
async def chat(message: Message) -> EnhancedResponse:
    # Detect emotion and intent
    emotion_raw = emotion_model(message.text)
    if emotion_raw is None:
        emotion_results = []
    else:
        emotion_results = list(emotion_raw)
    if not emotion_results:
        emotion = "neutral"
    else:
        first_result = emotion_results[0]
        if isinstance(first_result, dict) and "label" in first_result:
            label = first_result.get("label")
            emotion = str(label) if label is not None else "neutral"
        else:
            emotion = "neutral"
    intent = "venting" if "frustrated" in message.text else "other"  # (Expand this logic)
    
    # Ensure emotion is a string
    emotion = str(emotion)
    
    # Check for crisis
    crisis_alert = crisis_check(message.text)
    
    # Generate response
    reply = generate_response(emotion, intent)
    
    # Store in memory (if user_id provided)
    if message.user_id:
        update_mood_history(message.user_id, emotion)
        r.rpush(f"user:{message.user_id}:convo", json.dumps({
            "text": message.text,
            "emotion": emotion,
            "timestamp": datetime.now().isoformat()
        }))
    
    return EnhancedResponse(
        text=reply,
        emotion=emotion,
        intent=intent,
        crisis_alert=crisis_alert,
        suggested_action="Try deep breathing" if emotion == "anxiety" else None
    )

# WebSocket for real-time voice
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = await chat(Message(text=data))
        await websocket.send_json(response.dict())
