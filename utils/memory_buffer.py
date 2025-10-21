# ============================================
# utils/memory_buffer.py
# ============================================
import os
import redis
import json
from dotenv import load_dotenv

load_dotenv()
REDIS_URL = os.getenv("REDIS_URL")

try:
    r = redis.from_url(REDIS_URL, decode_responses=True)
    r.ping()  # Test connection
    REDIS_AVAILABLE = True
except:
    REDIS_AVAILABLE = False
    print("⚠️  Redis not available, using in-memory storage")
    _memory_store = {}
    _history_store = {}

def store_eval(key: str, payload: dict, ttl: int = 3600):
    """Store evaluation result"""
    if REDIS_AVAILABLE:
        r.set(key, json.dumps(payload), ex=ttl)
    else:
        _memory_store[key] = payload

def get_eval(key: str):
    """Retrieve evaluation result"""
    if REDIS_AVAILABLE:
        v = r.get(key)
        return json.loads(v) if v else None
    else:
        return _memory_store.get(key)

def append_history(agent_id: str, record: dict):
    """Append to evaluation history"""
    key = f"history:{agent_id}"
    if REDIS_AVAILABLE:
        r.rpush(key, json.dumps(record))
    else:
        if key not in _history_store:
            _history_store[key] = []
        _history_store[key].append(record)

def get_history(agent_id: str, limit: int = 10):
    """Get evaluation history"""
    key = f"history:{agent_id}"
    if REDIS_AVAILABLE:
        history = r.lrange(key, -limit, -1)
        return [json.loads(h) for h in history]
    else:
        return _history_store.get(key, [])[-limit:]
