from fastapi import Request
from module_admin.entity.vo.cache_vo import *


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
