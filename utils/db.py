import os
import redis
import json

# Lazy Redis connection - only connect when needed
_redis_client = None

def get_redis_client():
    """Get or create Redis client connection"""
    global _redis_client
    if _redis_client is None:
        redis_url = os.environ.get("dvgbot_REDIS_URL")
        if not redis_url:
            raise ValueError("dvgbot_REDIS_URL environment variable not set")
        _redis_client = redis.from_url(redis_url, decode_responses=True)
    return _redis_client

def save_catalog(data):
    """Save catalog to Redis"""
    try:
        r = get_redis_client()
        r.set("dvg:catalog", json.dumps(data))
    except Exception as e:
        print(f"Redis save error: {e}")
        raise

def get_catalog():
    """Get catalog from Redis"""
    try:
        r = get_redis_client()
        data = r.get("dvg:catalog")
        return json.loads(data) if data else []
    except Exception as e:
        print(f"Redis get error: {e}")
        return []
