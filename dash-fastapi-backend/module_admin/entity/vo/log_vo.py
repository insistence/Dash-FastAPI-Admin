from pydantic import BaseModel
from typing import Union, Optional, List


class OperLogModel(BaseModel):
    """
    操作日志表对应pydantic模型
    """
    oper_id: Optional[int]
    title: Optional[str]
    business_type: Optional[int]
    method: Optional[str]
    request_method: Optional[str]
    operator_type: Optional[int]
    oper_name: Optional[str]
    dept_name: Optional[str]
    oper_url: Optional[str]
    oper_ip: Optional[str]
    oper_location: Optional[str]
    oper_param: Optional[str]
    json_result: Optional[str]
    status: Optional[int]
    error_msg: Optional[str]
    oper_time: Optional[str]
    cost_time: Optional[int]

    class Config:
        orm_mode = True


class LogininforModel(BaseModel):
    """
    登录日志表对应pydantic模型
    """
    info_id: Optional[int]
    user_name: Optional[str]
    ipaddr: Optional[str]
    login_location: Optional[str]
    browser: Optional[str]
    os: Optional[str]
    status: Optional[str]
    msg: Optional[str]
    login_time: Optional[str]

    class Config:
        orm_mode = True


class OperLogQueryModel(OperLogModel):
    """
    操作日志管理不分页查询模型
    """
    oper_time_start: Optional[str]
    oper_time_end: Optional[str]


class OperLogPageObject(OperLogQueryModel):
    """
    操作日志管理分页查询模型
    """
    page_num: int
    page_size: int


class OperLogPageObjectResponse(BaseModel):
    """
    操作日志列表分页查询返回模型
    """
    rows: List[Union[OperLogModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeleteOperLogModel(BaseModel):
    """
    删除操作日志模型
    """
    oper_ids: str


class ClearOperLogModel(BaseModel):
    """
    清除操作日志模型
    """
    oper_type: str


class LoginLogQueryModel(LogininforModel):
    """
    登录日志管理不分页查询模型
    """
    login_time_start: Optional[str]
    login_time_end: Optional[str]


class LoginLogPageObject(LoginLogQueryModel):
    """
    登录日志管理分页查询模型
    """
    page_num: int
    page_size: int


class LoginLogPageObjectResponse(BaseModel):
    """
    登录日志列表分页查询返回模型
    """
    rows: List[Union[LogininforModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class DeleteLoginLogModel(BaseModel):
    """
    删除登录日志模型
    """
    info_ids: str


class ClearLoginLogModel(BaseModel):
    """
    清除登录日志模型
    """
    oper_type: str


class UnlockUser(BaseModel):
    """
    解锁用户模型
    """
    user_name: str


class CrudLogResponse(BaseModel):
    """
    操作各类日志响应模型
    """
    is_success: bool
    message: str
