from config.enums import ApiMethod
from utils.request import api_request


class CacheApi:
    """
    缓存管理模块相关接口
    """

    @classmethod
    def get_cache(cls):
        """
        查询缓存详情接口

        :return:
        """
        return api_request(
            url='/monitor/cache',
            method=ApiMethod.GET,
        )

    @classmethod
    def list_cache_name(cls):
        """
        查询缓存名称列表接口

        :return:
        """
        return api_request(
            url='/monitor/cache/getNames',
            method=ApiMethod.GET,
        )

    @classmethod
    def list_cache_key(cls, cache_name: str):
        """
        查询缓存键名列表接口

        :param cache_name: 缓存名称
        :return:
        """
        return api_request(
            url=f'/monitor/cache/getKeys/{cache_name}',
            method=ApiMethod.GET,
        )

    @classmethod
    def get_cache_value(cls, cache_name: str, cache_key: str):
        """
        查询缓存内容接口

        :param cache_name: 缓存名称
        :param cache_key: 缓存键名
        :return:
        """
        return api_request(
            url=f'/monitor/cache/getValue/{cache_name}/{cache_key}',
            method=ApiMethod.GET,
        )

    @classmethod
    def clear_cache_name(cls, cache_name: str):
        """
        清理指定名称缓存接口

        :param cache_name: 缓存名称
        :return:
        """
        return api_request(
            url=f'/monitor/cache/clearCacheName/{cache_name}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def clear_cache_key(cls, cache_key: str):
        """
        清理指定键名缓存接口

        :param cache_key: 缓存键名
        :return:
        """
        return api_request(
            url=f'/monitor/cache/clearCacheKey/{cache_key}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def clear_cache_all(cls):
        """
        清理全部缓存接口

        :return:
        """
        return api_request(
            url='/monitor/cache/clearCacheAll',
            method=ApiMethod.DELETE,
        )
