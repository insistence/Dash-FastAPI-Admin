from pydantic import BaseModel
from typing import Union, Optional, List
from mapper.schema.user_schema import DeptModel


class DeptPageObject(DeptModel):
    """
    部门管理分页查询模型
    """
    page_num: int
    page_size: int


class DeptPageObjectResponse(BaseModel):
    """
    用户管理列表分页查询返回模型
    """
    rows: List[Union[DeptModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeptResponse(BaseModel):
    """
    用户管理列表不分页查询返回模型
    """
    rows: List[Union[DeptModel, None]] = []


class DeptTree(BaseModel):
    """
    部门树响应模型
    """
    dept_tree: Union[List, None]
