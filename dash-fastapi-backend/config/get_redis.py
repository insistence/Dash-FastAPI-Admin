import aioredis
from config.env import RedisConfig
from utils.log_util import logger


async def create_redis_pool() -> aioredis.Redis:
    """
    应用启动时初始化redis连接
    :return: Redis连接对象
    """
    logger.info("开始连接redis...")
    redis = await aioredis.from_url(
        url=f"redis://{RedisConfig.HOST}",
        port=RedisConfig.PORT,
        username=RedisConfig.USERNAME,
        password=RedisConfig.PASSWORD,
        db=RedisConfig.DB,
        encoding="utf-8",
        decode_responses=True
    )
    logger.info("redis连接成功")
    return redis


async def close_redis_pool(app):
    """
    应用关闭时关闭redis连接
    :param app: fastapi对象
    :return: Redis连接对象
    """
    await app.state.redis.close()
    logger.info("关闭redis连接成功")
