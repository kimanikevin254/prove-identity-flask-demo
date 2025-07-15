import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Any, ttl: int) -> None:
        """Set a value in cache with TTL in seconds"""
        expiry = datetime.now() + timedelta(seconds=ttl)
        self._cache[key] = {
            'value': value,
            'expiry': expiry
        }

    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        if key not in self._cache:
            return None

        cached_item = self._cache[key]
        if datetime.now() > cached_item['expiry']:
            del self._cache[key]
            return None

        return cached_item['value']

# Global cache instance
cache = CacheService()