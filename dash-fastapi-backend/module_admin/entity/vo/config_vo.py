from pydantic import BaseModel
from typing import Union, Optional, List


class ConfigModel(BaseModel):
    """
    参数配置表对应pydantic模型
    """
    config_id: Optional[int]
    config_name: Optional[str]
    config_key: Optional[str]
    config_value: Optional[str]
    config_type: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True


class ConfigQueryModel(ConfigModel):
    """
    参数配置管理不分页查询模型
    """
    create_time_start: Optional[str]
    create_time_end: Optional[str]


class ConfigPageObject(ConfigQueryModel):
    """
    参数配置管理分页查询模型
    """
    page_num: int
    page_size: int


class ConfigPageObjectResponse(BaseModel):
    """
    参数配置管理列表分页查询返回模型
    """
    rows: List[Union[ConfigModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeleteConfigModel(BaseModel):
    """
    删除参数配置模型
    """
    config_ids: str


class CrudConfigResponse(BaseModel):
    """
    操作参数配置响应模型
    """
    is_success: bool
    message: str
