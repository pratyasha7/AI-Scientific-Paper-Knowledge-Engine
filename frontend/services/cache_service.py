import time
from typing import Any, Dict, Optional

class CacheService:
    """
    Manages frontend data caching with TTL (Time To Live) and invalidation logic.
    """
    
    _cache: Dict[str, Dict[str, Any]] = {}
    
    @staticmethod
    def set(key: str, value: Any, ttl_seconds: int = 3600):
        CacheService._cache[key] = {
            "value": value,
            "expiry": time.time() + ttl_seconds
        }

    @staticmethod
    def get(key: str) -> Optional[Any]:
        if key not in CacheService._cache:
            return None
            
        data = CacheService._cache[key]
        if time.time() > data["expiry"]:
            del CacheService._cache[key]
            return None
            
        return data["value"]

    @staticmethod
    def invalidate(key: str):
        if key in CacheService._cache:
            del CacheService._cache[key]

    @staticmethod
    def clear_all():
        CacheService._cache = {}

    @staticmethod
    def is_valid(key: str) -> bool:
        if key not in CacheService._cache:
            return False
        return time.time() <= CacheService._cache[key]["expiry"]
