import os, redis
from dotenv import load_dotenv

load_dotenv()
r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
r.set("ping", "pong")
print(r.get("ping"))