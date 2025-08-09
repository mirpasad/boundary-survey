import redis.asyncio as redis
from core.config import settings

class RedisCache:
    def __init__(self):
        self.client = None
        
    async def connect(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=False,
        )
        
    async def get(self, key: str):
        if not self.client:
            await self.connect()
        return await self.client.get(key)
    
    async def setex(self, key: str, ttl: int, value: str):
        if not self.client:
            await self.connect()
        return await self.client.setex(key, ttl, value)

# Singleton instance
redis_client = RedisCache()