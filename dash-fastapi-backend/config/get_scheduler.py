from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from config.database import engine, SQLALCHEMY_DATABASE_URL
from config.get_db import SessionLocal
from module_admin.dao.job_dao import Session, get_job_list_for_scheduler
from utils.log_util import logger
from utils.scheduler_util import *


# 重写Cron定时
class MyCronTrigger(CronTrigger):
    @classmethod
    def from_crontab(cls, expr, timezone=None):
        values = expr.split()
        if len(values) != 7:
            raise ValueError('Wrong number of fields; got {}, expected 7'.format(len(values)))

        return cls(second=values[0], minute=values[1], hour=values[2], day=values[3], month=values[4],
                   day_of_week=values[5], year=values[6], timezone=timezone)


job_stores = {
    'default': SQLAlchemyJobStore(url=SQLALCHEMY_DATABASE_URL, engine=engine)
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instance': 1
}
scheduler = BackgroundScheduler()
scheduler.configure(jobstores=job_stores, executors=executors, job_defaults=job_defaults)


async def init_system_scheduler(result_db: Session = SessionLocal()):
    """
    应用启动时初始化定时任务
    :return:
    """
    logger.info("开始启动定时任务...")
    scheduler.start()
    job_list = get_job_list_for_scheduler(result_db)
    for item in job_list:
        if item.status == '0':
            try:
                scheduler.remove_job(job_id=str(item.job_id))
            except Exception as e:
                print(e)
            finally:
                scheduler.add_job(
                    func=eval(item.invoke_target),
                    trigger=MyCronTrigger.from_crontab(item.cron_expression),
                    id=str(item.job_id),
                    name=item.job_name,
                    misfire_grace_time=1000000000000 if item.misfire_policy == '3' else None,
                    coalesce=True if item.misfire_policy == '2' else False,
                    max_instances=3 if item.concurrent == '0' else 1
                )
        else:
            continue
    logger.info("系统初始定时任务加载成功")


async def close_system_scheduler():
    """
    应用关闭时关闭定时任务
    :return:
    """
    scheduler.shutdown()
    logger.info("关闭定时任务成功")


def add_scheduler_job(job_info):

    scheduler.add_job(
        func=eval(job_info.invoke_target),
        trigger=MyCronTrigger.from_crontab(job_info.cron_expression),
        id=str(job_info.job_id),
        name=job_info.job_name,
        misfire_grace_time=1000000000000 if job_info.misfire_policy == '3' else None,
        coalesce=True if job_info.misfire_policy == '2' else False,
        max_instances=3 if job_info.concurrent == '0' else 1
    )


def remove_scheduler_job(job_id):

    scheduler.remove_job(job_id=str(job_id))
