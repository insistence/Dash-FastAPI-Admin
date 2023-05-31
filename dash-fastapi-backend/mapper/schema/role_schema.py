from pydantic import BaseModel
from typing import Union, Optional, List
from mapper.schema.user_schema import RoleModel


class RolePageObject(RoleModel):
    """
    角色管理分页查询模型
    """
    page_num: Optional[int]
    page_size: Optional[int]


class RoleSelectOptionResponseModel(BaseModel):
    """
    角色管理不分页查询模型
    """
    role: List[Union[RoleModel, None]]
