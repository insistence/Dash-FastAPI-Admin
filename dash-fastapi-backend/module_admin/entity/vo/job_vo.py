from pydantic import BaseModel
from typing import Union, Optional, List


class JobModel(BaseModel):
    """
    定时任务调度表对应pydantic模型
    """
    job_id: Optional[int]
    job_name: Optional[str]
    job_group: Optional[str]
    invoke_target: Optional[str]
    cron_expression: Optional[str]
    misfire_policy: Optional[str]
    concurrent: Optional[str]
    status: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True


class JobLogModel(BaseModel):
    """
    定时任务调度日志表对应pydantic模型
    """
    job_log_id: Optional[int]
    job_name: Optional[str]
    job_group: Optional[str]
    invoke_target: Optional[str]
    job_message: Optional[str]
    status: Optional[str]
    exception_info: Optional[str]
    create_time: Optional[str]

    class Config:
        orm_mode = True


class JobPageObject(JobModel):
    """
    定时任务管理分页查询模型
    """
    page_num: int
    page_size: int


class JobPageObjectResponse(BaseModel):
    """
    定时任务管理列表分页查询返回模型
    """
    rows: List[Union[JobModel, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class CrudJobResponse(BaseModel):
    """
    操作定时任务响应模型
    """
    is_success: bool
    message: str


class EditJobModel(JobModel):
    """
    编辑定时任务模型
    """
    type: Optional[str]


class DeleteJobModel(BaseModel):
    """
    删除定时任务模型
    """
    job_ids: str
