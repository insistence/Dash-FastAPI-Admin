from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class OnlineModel(BaseModel):
    """
    在线用户对应pydantic模型
    """

    token_id: Optional[str] = Field(default=None, description='会话编号')
    user_name: Optional[str] = Field(default=None, description='部门名称')
    dept_name: Optional[str] = Field(default=None, description='用户名称')
    ipaddr: Optional[str] = Field(default=None, description='登录IP地址')
    login_location: Optional[str] = Field(default=None, description='登录地址')
    browser: Optional[str] = Field(default=None, description='浏览器类型')
    os: Optional[str] = Field(default=None, description='操作系统')
    login_time: Optional[datetime] = Field(default=None, description='登录时间')


class OnlineQueryModel(OnlineModel):
    """
    在线用户不分页查询模型
    """

    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


class OnlinePageQueryModel(OnlineQueryModel):
    """
    在线用户分页查询模型
    """

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteOnlineModel(BaseModel):
    """
    强退在线用户模型
    """

    token_ids: str = Field(description='需要强退的会话编号')
