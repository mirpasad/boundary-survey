import redis
from core.config import settings
from tenacity import retry, stop_after_attempt, wait_random_exponential, retry_if_exception_type

class RedisCache:
    def __init__(self):
        self.client = None
    async def connect(self):
        self.client = redis.asyncio.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            decode_responses=False,
        )
        
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(multiplier=0.5, max=2),
        retry=retry_if_exception_type(redis.exceptions.ConnectionError)
    )
    async def get(self, key: str):
        if not self.client:
            await self.connect()
        return await self.client.get(key)
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(multiplier=0.5, max=2),
        retry=retry_if_exception_type(redis.exceptions.ConnectionError)
    )
    async def setex(self, key: str, ttl: int, value: str):
        if not self.client:
            await self.connect()
        return await self.client.setex(key, ttl, value)

# Singleton instance
redis_client = RedisCache()