from pydantic import BaseModel
from typing import Union, Optional, List
from mapper.schema.user_schema import RoleModel
from mapper.schema.menu_schema import MenuModel


class RoleMenuModel(BaseModel):
    """
    角色和菜单关联表对应pydantic模型
    """
    role_id: Optional[int]
    menu_id: Optional[int]

    class Config:
        orm_mode = True


class RolePageObject(RoleModel):
    """
    角色管理分页查询模型
    """
    create_time_start: Optional[str]
    create_time_end: Optional[str]
    page_num: Optional[int]
    page_size: Optional[int]
    
    
class RolePageObjectResponse(BaseModel):
    """
    角色管理列表分页查询返回模型
    """
    rows: List[Union[RoleModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class RoleSelectOptionResponseModel(BaseModel):
    """
    角色管理不分页查询模型
    """
    role: List[Union[RoleModel, None]]
    
    
class CrudRoleResponse(BaseModel):
    """
    操作角色响应模型
    """
    is_success: bool
    message: str
    
    
class AddRoleModel(RoleModel):
    """
    新增角色模型
    """
    menu_id: Optional[str]


class DeleteRoleModel(BaseModel):
    """
    删除角色模型
    """
    role_ids: str
    update_by: Optional[str]
    update_time: Optional[str]
    
    
class RoleDetailModel(BaseModel):
    """
    获取角色详情信息响应模型
    """
    role: Union[RoleModel, None]
    menu: List[Union[MenuModel, None]]
