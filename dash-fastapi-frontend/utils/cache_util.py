from cachebox import LRUCache, TTLCache
from flask import session
from typing import Any, Dict


cache_manager = LRUCache(maxsize=10000, iterable=None, capacity=10000)
ttl_manager = TTLCache(maxsize=0, ttl=600)


class CacheManager:
    """
    缓存管理器
    """

    @classmethod
    def get(cls, target_key: str):
        """
        获取缓存值

        :param target_key: 缓存key
        :return: 缓存值
        """
        cache_value = (
            cache_manager.get(session.get('Authorization')).get(target_key)
            if cache_manager.get(session.get('Authorization'))
            else None
        )
        return cache_value

    @classmethod
    def set(cls, target_obj: Dict):
        """
        设置缓存值

        :param target_obj: 缓存值
        :return:
        """
        cache = cache_manager.get(session.get('Authorization'))
        if cache:
            cache.update(target_obj)
        else:
            cache = target_obj
        cache_manager.insert(session.get('Authorization'), cache)

    @classmethod
    def delete(cls, target_key: str):
        """
        删除缓存值

        :param target_key: 缓存key
        :return:
        """
        cache = cache_manager.get(session.get('Authorization'))
        cache.pop(target_key, None)
        cache_manager.insert(session.get('Authorization'), cache)


class TTLCacheManager:
    """
    TTL缓存管理器
    """

    @classmethod
    def get(cls, target_key: str):
        """
        获取缓存值

        :param target_key: 缓存key
        :return: 缓存值
        """
        return ttl_manager.get(target_key)

    @classmethod
    def set(cls, target_key: str, target_value: Any):
        """
        设置缓存值

        :param target_key: 缓存key
        :param target_value: 缓存值
        :return:
        """
        ttl_manager.insert(target_key, target_value)

    @classmethod
    def delete(cls, target_keys: str):
        """
        删除缓存值

        :param target_keys: 缓存keys
        :return:
        """
        target_key_list = target_keys.split(',')
        for target_key in target_key_list:
            if ttl_manager.get(target_key) is not None:
                del ttl_manager[target_key]
