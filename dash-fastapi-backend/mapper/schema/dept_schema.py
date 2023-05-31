from pydantic import BaseModel
from typing import Union, Optional, List
from mapper.schema.user_schema import DeptModel


class DeptPageObject(DeptModel):
    """
    部门管理分页查询模型
    """
    page_num: Optional[int]
    page_size: Optional[int]


class DeptTree(BaseModel):
    """
    部门树响应模型
    """
    dept_tree: Union[List, None]
