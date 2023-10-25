from fastapi import Request
from module_admin.entity.vo.cache_vo import *
from config.env import RedisInitKeyConfig


class CacheService:
    """
    缓存监控模块服务层
    """

    @classmethod
    async def get_cache_monitor_statistical_info_services(cls, request: Request):
        """
        获取缓存监控信息service
        :param request: Request对象
        :return: 缓存监控信息
        """
        info = await request.app.state.redis.info()
        db_size = await request.app.state.redis.dbsize()
        command_stats_dict = await request.app.state.redis.info('commandstats')
        command_stats = [dict(name=key.split('_')[1], value=str(value.get('calls'))) for key, value in
                         command_stats_dict.items()]
        result = dict(command_stats=command_stats, db_size=db_size, info=info)

        return CacheMonitorModel(**result)

    @classmethod
    def get_cache_monitor_cache_name_services(cls):
        """
        获取缓存名称列表信息service
        :return: 缓存名称列表信息
        """
        name_list = []
        for attr_name in dir(RedisInitKeyConfig):
            if not attr_name.startswith('__') and isinstance(getattr(RedisInitKeyConfig, attr_name), dict):
                name_list.append(
                    CacheInfoModel(
                        cache_key="",
                        cache_name=getattr(RedisInitKeyConfig, attr_name).get('key'),
                        cache_value="",
                        remark=getattr(RedisInitKeyConfig, attr_name).get('remark')
                    )
                )

        return name_list

    @classmethod
    async def get_cache_monitor_cache_key_services(cls, request: Request, cache_name: str):
        """
        获取缓存键名列表信息service
        :param request: Request对象
        :param cache_name: 缓存名称
        :return: 缓存键名列表信息
        """
        cache_keys = await request.app.state.redis.keys(f"{cache_name}*")
        cache_key_list = [key.split(':', 1)[1] for key in cache_keys if key.startswith(f"{cache_name}:")]

        return cache_key_list

    @classmethod
    async def get_cache_monitor_cache_value_services(cls, request: Request, cache_name: str, cache_key: str):
        """
        获取缓存内容信息service
        :param request: Request对象
        :param cache_name: 缓存名称
        :param cache_key: 缓存键名
        :return: 缓存内容信息
        """
        cache_value = await request.app.state.redis.get(f"{cache_name}:{cache_key}")

        return CacheInfoModel(cache_key=cache_key, cache_name=cache_name, cache_value=cache_value, remark="")
