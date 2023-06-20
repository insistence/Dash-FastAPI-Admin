from pydantic import BaseModel
from typing import Union, Optional, List


class MenuModel(BaseModel):
    """
    菜单表对应pydantic模型
    """
    menu_id: Optional[int]
    menu_name: Optional[str]
    parent_id: Optional[int]
    order_num: Optional[int]
    path: Optional[str]
    component: Optional[str]
    query: Optional[str]
    is_frame: Optional[int]
    is_cache: Optional[int]
    menu_type: Optional[str]
    visible: Optional[str]
    status: Optional[str]
    perms: Optional[str]
    icon: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True
        
        
class MenuTreeModel(MenuModel):
    """
    菜单树查询模型
    """
    type: Optional[str]


class MenuPageObject(MenuModel):
    """
    菜单管理分页查询模型
    """
    page_num: int
    page_size: int


class MenuPageObjectResponse(BaseModel):
    """
    菜单管理列表分页查询返回模型
    """
    rows: List[Union[MenuModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class MenuResponse(BaseModel):
    """
    菜单管理列表不分页查询返回模型
    """
    rows: List[Union[MenuModel, None]] = []


class MenuTree(BaseModel):
    """
    菜单树响应模型
    """
    menu_tree: Union[List, None]


class CrudMenuResponse(BaseModel):
    """
    操作菜单响应模型
    """
    is_success: bool
    message: str


class DeleteMenuModel(BaseModel):
    """
    删除菜单模型
    """
    menu_ids: str
