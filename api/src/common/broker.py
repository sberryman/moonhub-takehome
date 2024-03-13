from faststream.redis.fastapi import RedisRouter

from src.common.config import settings

router = RedisRouter(
    url=settings.redis_url,
)

broker = router.broker
