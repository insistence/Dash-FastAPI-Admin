from sqlalchemy.orm import Session
from module_admin.entity.do.job_do import SysJobLog
from module_admin.entity.vo.job_vo import JobLogModel, JobLogQueryModel
from utils.time_format_util import list_format_datetime, object_format_datetime
from datetime import datetime, time


class JobLogDao:
    """
    定时任务日志管理模块数据库操作层
    """

    @classmethod
    def get_job_log_detail_by_id(cls, db: Session, job_log_id: int):
        """
        根据定时任务日志id获取定时任务日志详细信息
        :param db: orm对象
        :param job_log_id: 定时任务日志id
        :return: 定时任务日志信息对象
        """
        job_log_info = db.query(SysJobLog) \
            .filter(SysJobLog.job_log_id == job_log_id) \
            .first()

        return object_format_datetime(job_log_info)

    @classmethod
    def get_job_log_list(cls, db: Session, query_object: JobLogQueryModel):
        """
        根据查询参数获取定时任务日志列表信息
        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 定时任务日志列表信息对象
        """
        job_log_list = db.query(SysJobLog) \
            .filter(SysJobLog.job_name.like(f'%{query_object.job_name}%') if query_object.job_name else True,
                    SysJobLog.job_group == query_object.job_group if query_object.job_group else True,
                    SysJobLog.status == query_object.status if query_object.status else True,
                    SysJobLog.create_time.between(
                        datetime.combine(datetime.strptime(query_object.create_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                        datetime.combine(datetime.strptime(query_object.create_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                    if query_object.create_time_start and query_object.create_time_end else True
                    ) \
            .distinct().all()

        return list_format_datetime(job_log_list)

    @classmethod
    def add_job_log_dao(cls, db: Session, job_log: JobLogModel):
        """
        新增定时任务日志数据库操作
        :param db: orm对象
        :param job_log: 定时任务日志对象
        :return:
        """
        db_job_log = SysJobLog(**job_log.dict())
        db.add(db_job_log)
        db.flush()

        return db_job_log

    @classmethod
    def delete_job_log_dao(cls, db: Session, job_log: JobLogModel):
        """
        删除定时任务日志数据库操作
        :param db: orm对象
        :param job_log: 定时任务日志对象
        :return:
        """
        db.query(SysJobLog) \
            .filter(SysJobLog.job_log_id == job_log.job_log_id) \
            .delete()

    @classmethod
    def clear_job_log_dao(cls, db: Session):
        """
        清除定时任务日志数据库操作
        :param db: orm对象
        :return:
        """
        db.query(SysJobLog) \
            .delete()
