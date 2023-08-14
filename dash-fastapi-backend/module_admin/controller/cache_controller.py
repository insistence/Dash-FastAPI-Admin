from fastapi import APIRouter, Request
from fastapi import Depends, Header
from config.get_db import get_db
from module_admin.service.login_service import get_current_user, Session
from module_admin.service.cache_service import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


cacheController = APIRouter(prefix='/cache', dependencies=[Depends(get_current_user)])


@cacheController.post("/statisticalInfo", response_model=CacheMonitorModel, dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def get_monitor_cache_info(request: Request):
    try:
        # 获取全量数据
        cache_info_query_result = await get_cache_monitor_statistical_info_services(request)
        logger.info('获取成功')
        return response_200(data=cache_info_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
