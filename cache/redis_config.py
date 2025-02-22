"""Redis configuration and utilities."""
import os
import json
from typing import Any, Optional
from functools import wraps
from redis import Redis
from flask import request
from metrics.prometheus_metrics import cache_hits_total, cache_misses_total

# Redis configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

# Cache expiration times (in seconds)
CACHE_TIMES = {
    'server': 300,  # 5 minutes
    'metrics': 60,  # 1 minute
    'server_metrics': 120,  # 2 minutes
}

# Initialize Redis client
redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    password=REDIS_PASSWORD,
    decode_responses=True
)

def get_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments."""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ':'.join(key_parts)

def cache_response(prefix: str, expire: int = 300):
    """Decorator to cache API responses."""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Generate cache key
            cache_key = f"{prefix}:{get_cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_data = redis_client.get(cache_key)
            if cached_data:
                cache_hits_total.labels(cache_type=prefix).inc()
                return json.loads(cached_data)
            
            cache_misses_total.labels(cache_type=prefix).inc()
            
            # Get fresh data
            data = f(*args, **kwargs)
            
            # Cache the response
            redis_client.setex(
                cache_key,
                expire,
                json.dumps(data)
            )
            
            return data
        return decorated
    return decorator

def invalidate_cache_prefix(prefix: str) -> None:
    """Invalidate all cache keys with given prefix."""
    pattern = f"{prefix}:*"
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)

def set_cache(key: str, value: Any, expire: int = 300) -> None:
    """Set a value in cache."""
    redis_client.setex(key, expire, json.dumps(value))

def get_cache(key: str) -> Optional[Any]:
    """Get a value from cache."""
    data = redis_client.get(key)
    return json.loads(data) if data else None

def delete_cache(key: str) -> None:
    """Delete a value from cache."""
    redis_client.delete(key) 