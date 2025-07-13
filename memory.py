import redis
from datetime import datetime
from typing import List, Dict, Optional

r = redis.Redis(
    host='redis-16244.c80.us-east-1-2.ec2.redns.redis-cloud.com',
    port=16244,
    username='default',
    password='dZth7NbWs6puJxaqizIprq9yRQgRLtIM',
    decode_responses=True
)

def save_message(user_id: str, sender: str, text: str, emotion: Optional[str] = None, intent: Optional[str] = None):
    
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "sender": sender,
        "text": text,
        "emotion": emotion,
        "intent": intent
    }
    r.rpush(f"user:{user_id}:history", str(entry))

import asyncio

async def get_history(user_id: str, limit: int = 20) -> List[Dict]:
    
    loop = asyncio.get_event_loop()
    raw_history = await loop.run_in_executor(None, r.lrange, f"user:{user_id}:history", -limit, -1)
    history = []
    for entry in raw_history:
        try:
            history.append(eval(entry))
        except Exception:
            continue
    return history

def save_emotion(user_id: str, emotion: str):
    entry = f"{datetime.utcnow().isoformat()}|{emotion}"
    r.rpush(f"user:{user_id}:moods", entry)

import asyncio

async def get_emotion_history(user_id: str, limit: int = 20) -> List[Dict]:

    loop = asyncio.get_event_loop()
    raw_result = await loop.run_in_executor(None, r.lrange, f"user:{user_id}:moods", -limit, -1)
    result = []
    for entry in raw_result:
        try:
            timestamp, emotion = entry.split("|")
            result.append({"timestamp": timestamp, "emotion": emotion})
        except Exception:
            continue
    return result

def clear_history(user_id: str):

    r.delete(f"user:{user_id}:history")
    r.delete(f"user:{user_id}:moods")

def get_last_emotion(user_id: str) -> Optional[str]:
    
    last = r.lindex(f"user:{user_id}:moods", -1)
    import inspect
    if inspect.isawaitable(last):
        last = asyncio.get_event_loop().run_until_complete(last)
    if last:
        try:
            if isinstance(last, str):
                _, emotion = last.split("|")
                return emotion
        except Exception:
            return None
    return None

import asyncio

async def get_last_intent(user_id: str) -> Optional[str]:
    """
    Get the most recent intent detected for the user.
    """
    history = await get_history(user_id, limit=1)
    if history:
        return history[0].get("intent")
if __name__ == "__main__":
    user = "test_user"
    print("Emotions:", asyncio.run(get_emotion_history(user)))
    save_message(user, "bot", "I'm here for you. Want to talk more?", "sadness", "comfort")
    save_emotion(user, "sadness")
    print("History:", asyncio.run(get_history(user)))
    print("Emotions:", asyncio.run(get_emotion_history(user)))
    print("Last emotion:", get_last_emotion(user))
    print("Last intent:", asyncio.run(get_last_intent(user)))
    clear_history(user)
    print("Last emotion after clearing:", get_last_emotion(user))
    print("Last intent:", get_last_intent(user))
    clear_history(user)
