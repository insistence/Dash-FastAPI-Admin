from pydantic import BaseModel
from typing import Union, Optional, List
from module_admin.entity.vo.user_vo import PostModel


class PostPageObject(PostModel):
    """
    岗位管理分页查询模型
    """
    page_num: int
    page_size: int


class PostPageObjectResponse(BaseModel):
    """
    岗位管理列表分页查询返回模型
    """
    rows: List[Union[PostModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class PostSelectOptionResponseModel(BaseModel):
    """
    岗位管理不分页查询模型
    """
    post: List[Union[PostModel, None]]


class CrudPostResponse(BaseModel):
    """
    操作岗位响应模型
    """
    is_success: bool
    message: str


class DeletePostModel(BaseModel):
    """
    删除岗位模型
    """
    post_ids: str
