# utils/memory_buffer.py
import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(REDIS_URL)

def store_eval(key: str, payload: dict, ttl: int = 3600):
    r.set(key, json.dumps(payload), ex=ttl)

def get_eval(key: str):
    v = r.get(key)
    return json.loads(v) if v else None

def append_history(agent_id: str, record: dict):
    key = f"history:{agent_id}"
    r.rpush(key, json.dumps(record))
