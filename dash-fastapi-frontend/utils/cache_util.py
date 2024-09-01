from cachebox import LRUCache
from flask import session
from typing import Dict


cache_manager = LRUCache(maxsize=10000, iterable=None, capacity=10000)


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
        cache_value = cache_manager.get(session.get('Authorization')).get(
            target_key
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
