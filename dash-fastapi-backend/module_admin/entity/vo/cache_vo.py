from pydantic import BaseModel
from typing import Optional, List, Any


class CacheMonitorModel(BaseModel):
    """
    缓存监控信息对应pydantic模型
    """
    command_stats: Optional[List]
    db_size: Optional[int]
    info: Optional[dict]


class CacheInfoModel(BaseModel):
    """
    缓存监控对象对应pydantic模型
    """
    cache_key: Optional[str]
    cache_name: Optional[str]
    cache_value: Optional[Any]
    remark: Optional[str]


class CrudCacheResponse(BaseModel):
    """
    操作缓存响应模型
    """
    is_success: bool
    message: str
