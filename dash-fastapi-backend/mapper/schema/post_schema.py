from pydantic import BaseModel
from typing import Union, Optional
from mapper.schema.user_schema import PostModel


class PostPageObject(PostModel):
    """
    岗位管理分页查询模型
    """
    page_num: Optional[int]
    page_size: Optional[int]


class PostSelectOptionResponseModel(BaseModel):
    """
    岗位管理不分页查询模型
    """
    post: list[PostModel]
