from fastapi import APIRouter, Request
from fastapi import Depends
from module_admin.service.login_service import get_current_user, Session
from module_admin.service.cache_service import *
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth


cacheController = APIRouter(prefix='/cache', dependencies=[Depends(get_current_user)])


@cacheController.post("/statisticalInfo", response_model=CacheMonitorModel, dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def get_monitor_cache_info(request: Request):
    try:
        # 获取全量数据
        cache_info_query_result = await CacheService.get_cache_monitor_statistical_info_services(request)
        logger.info('获取成功')
        return response_200(data=cache_info_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
