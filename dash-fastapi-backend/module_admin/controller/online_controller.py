from fastapi import APIRouter, Request
from fastapi import Depends
from config.get_db import get_db
from module_admin.service.login_service import get_current_user, Session
from module_admin.service.online_service import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


onlineController = APIRouter(prefix='/online', dependencies=[Depends(get_current_user)])


@onlineController.post("/get", response_model=OnlinePageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:online:list'))])
async def get_monitor_online_list(request: Request, online_page_query: OnlinePageObject):
    try:
        # 获取全量数据
        online_query_result = await OnlineService.get_online_list_services(request, online_page_query)
        # 分页操作
        online_page_query_result = get_page_obj(online_query_result, online_page_query.page_num, online_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=online_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@onlineController.post("/forceLogout", response_model=CrudOnlineResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:online:forceLogout'))])
@log_decorator(title='在线用户', business_type=7)
async def delete_monitor_online(request: Request, delete_online: DeleteOnlineModel, query_db: Session = Depends(get_db)):
    try:
        delete_online_result = await OnlineService.delete_online_services(request, delete_online)
        if delete_online_result.is_success:
            logger.info(delete_online_result.message)
            return response_200(data=delete_online_result, message=delete_online_result.message)
        else:
            logger.warning(delete_online_result.message)
            return response_400(data="", message=delete_online_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@onlineController.post("/batchLogout", response_model=CrudOnlineResponse, dependencies=[Depends(CheckUserInterfaceAuth('monitor:online:batchLogout'))])
@log_decorator(title='在线用户', business_type=7)
async def delete_monitor_online(request: Request, delete_online: DeleteOnlineModel, query_db: Session = Depends(get_db)):
    try:
        delete_online_result = await OnlineService.delete_online_services(request, delete_online)
        if delete_online_result.is_success:
            logger.info(delete_online_result.message)
            return response_200(data=delete_online_result, message=delete_online_result.message)
        else:
            logger.warning(delete_online_result.message)
            return response_400(data="", message=delete_online_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
