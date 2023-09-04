from pydantic import BaseModel
from typing import Union, Optional, List


class NoticeModel(BaseModel):
    """
    通知公告表对应pydantic模型
    """
    notice_id: Optional[int]
    notice_title: Optional[str]
    notice_type: Optional[str]
    notice_content: Optional[bytes]
    status: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True


class NoticeQueryModel(NoticeModel):
    """
    通知公告管理不分页查询模型
    """
    create_time_start: Optional[str]
    create_time_end: Optional[str]


class NoticePageObject(NoticeQueryModel):
    """
    通知公告管理分页查询模型
    """
    page_num: int
    page_size: int


class NoticePageObjectResponse(BaseModel):
    """
    通知公告管理列表分页查询返回模型
    """
    rows: List[Union[NoticeModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class CrudNoticeResponse(BaseModel):
    """
    操作通知公告响应模型
    """
    is_success: bool
    message: str


class DeleteNoticeModel(BaseModel):
    """
    删除通知公告模型
    """
    notice_ids: str
