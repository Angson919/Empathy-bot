from datetime import datetime
import matplotlib.pyplot as plt
import aioredis

import asyncio

r = None  # Will be initialized asynchronously

async def generate_mood_chart(user_id: str):
    global r
    if r is None:
        r = await aioredis.from_url(
    "redis://default:dZth7NbWs6puJxaqizIprq9yRQgRLtIM@redis-16244.c80.us-east-1-2.ec2.redns.redis-cloud.com:16244"
)
    # Fetch mood history from Redis
    if not await r.exists(f"user:{user_id}:moods"):
        return "No mood history available for this user."
    moods = await r.lrange(f"user:{user_id}:moods", 0, -1)
    timestamps = []
    emotions = []
    
    for entry in moods:
        if isinstance(entry, bytes):
            entry = entry.decode()
        time, emotion = entry.split("|")
        timestamps.append(datetime.fromisoformat(time))
        emotions.append(emotion)
    
    plt.figure(figsize=(10, 4))
    plt.plot(timestamps, emotions, marker='o')
    plt.title("Your Mood Over Time")
    plt.savefig(f"mood_chart_{user_id}.png")
    return f"mood_chart_{user_id}.png"
