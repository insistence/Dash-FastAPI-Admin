from sqlalchemy.orm import Session
from module_admin.entity.do.job_do import SysJob
from module_admin.entity.vo.job_vo import JobModel, CrudJobResponse
from utils.time_format_util import list_format_datetime, object_format_datetime


def get_job_detail_by_id(db: Session, job_id: int):
    job_info = db.query(SysJob) \
        .filter(SysJob.job_id == job_id) \
        .first()

    return object_format_datetime(job_info)


def get_job_list(db: Session, query_object: JobModel):
    """
    根据查询参数获取定时任务列表信息
    :param db: orm对象
    :param query_object: 查询参数对象
    :return: 定时任务列表信息对象
    """
    job_list = db.query(SysJob) \
        .filter(SysJob.job_name.like(f'%{query_object.job_name}%') if query_object.job_name else True,
                SysJob.job_group == query_object.job_group if query_object.job_group else True,
                SysJob.status == query_object.status if query_object.status else True
                ) \
        .distinct().all()

    return list_format_datetime(job_list)


def get_job_list_for_scheduler(db: Session):
    """
    获取定时任务列表信息
    :param db: orm对象
    :return: 定时任务列表信息对象
    """
    job_list = db.query(SysJob) \
        .distinct().all()

    return list_format_datetime(job_list)


def add_job_dao(db: Session, job: JobModel):
    """
    新增定时任务数据库操作
    :param db: orm对象
    :param job: 定时任务对象
    :return: 新增校验结果
    """
    db_job = SysJob(**job.dict())
    db.add(db_job)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_job)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudJobResponse(**result)


def edit_job_dao(db: Session, job: dict):
    """
    编辑定时任务数据库操作
    :param db: orm对象
    :param job: 需要更新的定时任务字典
    :return: 编辑校验结果
    """
    is_job_id = db.query(SysJob).filter(SysJob.job_id == job.get('job_id')).all()
    if not is_job_id:
        result = dict(is_success=False, message='定时任务不存在')
    else:
        db.query(SysJob) \
            .filter(SysJob.job_id == job.get('job_id')) \
            .update(job)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudJobResponse(**result)


def delete_job_dao(db: Session, job: JobModel):
    """
    删除定时任务数据库操作
    :param db: orm对象
    :param job: 定时任务对象
    :return:
    """
    db.query(SysJob) \
        .filter(SysJob.job_id == job.job_id) \
        .delete()
    db.commit()  # 提交保存到数据库中
