from fastapi import APIRouter, Request
from fastapi import Depends
from config.get_db import get_db
from module_admin.service.login_service import get_current_user, CurrentUserInfoServiceResponse
from module_admin.service.job_service import *
from module_admin.service.job_log_service import *
from module_admin.entity.vo.job_vo import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from utils.common_util import bytes2file_response
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


jobController = APIRouter(dependencies=[Depends(get_current_user)])


@jobController.post("/job/get", response_model=JobPageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:list'))])
async def get_system_job_list(request: Request, job_page_query: JobPageObject, query_db: Session = Depends(get_db)):
    try:
        job_query = JobModel(**job_page_query.dict())
        # 获取全量数据
        job_query_result = JobService.get_job_list_services(query_db, job_query)
        # 分页操作
        notice_page_query_result = get_page_obj(job_query_result, job_page_query.page_num, job_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=notice_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.post("/job/add", response_model=CrudJobResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:add'))])
@log_decorator(title='定时任务管理', business_type=1)
async def add_system_job(request: Request, add_job: JobModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        add_job.create_by = current_user.user.user_name
        add_job.update_by = current_user.user.user_name
        add_job_result = JobService.add_job_services(query_db, add_job)
        if add_job_result.is_success:
            logger.info(add_job_result.message)
            return response_200(data=add_job_result, message=add_job_result.message)
        else:
            logger.warning(add_job_result.message)
            return response_400(data="", message=add_job_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.patch("/job/edit", response_model=CrudJobResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:edit'))])
@log_decorator(title='定时任务管理', business_type=2)
async def edit_system_job(request: Request, edit_job: EditJobModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_job.update_by = current_user.user.user_name
        edit_job.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_job_result = JobService.edit_job_services(query_db, edit_job)
        if edit_job_result.is_success:
            logger.info(edit_job_result.message)
            return response_200(data=edit_job_result, message=edit_job_result.message)
        else:
            logger.warning(edit_job_result.message)
            return response_400(data="", message=edit_job_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.post("/job/changeStatus", response_model=CrudJobResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:changeStatus'))])
@log_decorator(title='定时任务管理', business_type=2)
async def execute_system_job(request: Request, execute_job: JobModel, query_db: Session = Depends(get_db)):
    try:
        execute_job_result = JobService.execute_job_once_services(query_db, execute_job)
        if execute_job_result.is_success:
            logger.info(execute_job_result.message)
            return response_200(data=execute_job_result, message=execute_job_result.message)
        else:
            logger.warning(execute_job_result.message)
            return response_400(data="", message=execute_job_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.post("/job/delete", response_model=CrudJobResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:remove'))])
@log_decorator(title='定时任务管理', business_type=3)
async def delete_system_job(request: Request, delete_job: DeleteJobModel, query_db: Session = Depends(get_db)):
    try:
        delete_job_result = JobService.delete_job_services(query_db, delete_job)
        if delete_job_result.is_success:
            logger.info(delete_job_result.message)
            return response_200(data=delete_job_result, message=delete_job_result.message)
        else:
            logger.warning(delete_job_result.message)
            return response_400(data="", message=delete_job_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.get("/job/{job_id}", response_model=JobModel, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:query'))])
async def query_detail_system_job(request: Request, job_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_job_result = JobService.detail_job_services(query_db, job_id)
        logger.info(f'获取job_id为{job_id}的信息成功')
        return response_200(data=detail_job_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.post("/job/export", dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:export'))])
@log_decorator(title='定时任务管理', business_type=5)
async def export_system_job_list(request: Request, job_query: JobModel, query_db: Session = Depends(get_db)):
    try:
        # 获取全量数据
        job_query_result = JobService.get_job_list_services(query_db, job_query)
        job_export_result = await JobService.export_job_list_services(request, job_query_result)
        logger.info('导出成功')
        return streaming_response_200(data=bytes2file_response(job_export_result))
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.post("/jobLog/get", response_model=JobLogPageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:list'))])
async def get_system_job_log_list(request: Request, job_log_page_query: JobLogPageObject, query_db: Session = Depends(get_db)):
    try:
        job_log_query = JobLogQueryModel(**job_log_page_query.dict())
        # 获取全量数据
        job_log_query_result = JobLogService.get_job_log_list_services(query_db, job_log_query)
        # 分页操作
        notice_page_query_result = get_page_obj(job_log_query_result, job_log_page_query.page_num, job_log_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=notice_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.post("/jobLog/delete", response_model=CrudJobResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:remove'))])
@log_decorator(title='定时任务日志管理', business_type=3)
async def delete_system_job_log(request: Request, delete_job_log: DeleteJobLogModel, query_db: Session = Depends(get_db)):
    try:
        delete_job_log_result = JobLogService.delete_job_log_services(query_db, delete_job_log)
        if delete_job_log_result.is_success:
            logger.info(delete_job_log_result.message)
            return response_200(data=delete_job_log_result, message=delete_job_log_result.message)
        else:
            logger.warning(delete_job_log_result.message)
            return response_400(data="", message=delete_job_log_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.post("/jobLog/clear", response_model=CrudJobResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:remove'))])
@log_decorator(title='定时任务日志管理', business_type=9)
async def clear_system_job_log(request: Request, clear_job_log: ClearJobLogModel, query_db: Session = Depends(get_db)):
    try:
        clear_job_log_result = JobLogService.clear_job_log_services(query_db, clear_job_log)
        if clear_job_log_result.is_success:
            logger.info(clear_job_log_result.message)
            return response_200(data=clear_job_log_result, message=clear_job_log_result.message)
        else:
            logger.warning(clear_job_log_result.message)
            return response_400(data="", message=clear_job_log_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.get("/jobLog/{job_log_id}", response_model=JobLogModel, dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:query'))])
async def query_detail_system_job_log(request: Request, job_log_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_job_log_result = JobLogService.detail_job_log_services(query_db, job_log_id)
        logger.info(f'获取job_log_id为{job_log_id}的信息成功')
        return response_200(data=detail_job_log_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@jobController.post("/jobLog/export", dependencies=[Depends(CheckUserInterfaceAuth('monitor:job:export'))])
@log_decorator(title='定时任务日志管理', business_type=5)
async def export_system_job_log_list(request: Request, job_log_query: JobLogQueryModel, query_db: Session = Depends(get_db)):
    try:
        # 获取全量数据
        job_log_query_result = JobLogService.get_job_log_list_services(query_db, job_log_query)
        job_log_export_result = JobLogService.export_job_log_list_services(query_db, job_log_query_result)
        logger.info('导出成功')
        return streaming_response_200(data=bytes2file_response(job_log_export_result))
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
