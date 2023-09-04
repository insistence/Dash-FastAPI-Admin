from pydantic import BaseModel
from typing import Optional, List


class CacheMonitorModel(BaseModel):
    """
    缓存监控信息对应pydantic模型
    """
    command_stats: Optional[List]
    db_size: Optional[int]
    info: Optional[dict]
