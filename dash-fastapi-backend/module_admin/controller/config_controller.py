from fastapi import APIRouter
from fastapi import Depends
from config.get_db import get_db
from module_admin.service.login_service import get_current_user, CurrentUserInfoServiceResponse
from module_admin.service.config_service import *
from module_admin.entity.vo.config_vo import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from utils.common_util import bytes2file_response
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


configController = APIRouter(dependencies=[Depends(get_current_user)])


@configController.post("/config/get", response_model=ConfigPageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:config:list'))])
async def get_system_config_list(request: Request, config_page_query: ConfigPageObject, query_db: Session = Depends(get_db)):
    try:
        config_query = ConfigQueryModel(**config_page_query.dict())
        # 获取全量数据
        config_query_result = ConfigService.get_config_list_services(query_db, config_query)
        # 分页操作
        config_page_query_result = get_page_obj(config_query_result, config_page_query.page_num, config_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=config_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@configController.post("/config/add", response_model=CrudConfigResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:config:add'))])
@log_decorator(title='参数管理', business_type=1)
async def add_system_config(request: Request, add_config: ConfigModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        add_config.create_by = current_user.user.user_name
        add_config.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_config.update_by = current_user.user.user_name
        add_config.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        add_config_result = await ConfigService.add_config_services(request, query_db, add_config)
        if add_config_result.is_success:
            logger.info(add_config_result.message)
            return response_200(data=add_config_result, message=add_config_result.message)
        else:
            logger.warning(add_config_result.message)
            return response_400(data="", message=add_config_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@configController.patch("/config/edit", response_model=CrudConfigResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:config:edit'))])
@log_decorator(title='参数管理', business_type=2)
async def edit_system_config(request: Request, edit_config: ConfigModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_config.update_by = current_user.user.user_name
        edit_config.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_config_result = await ConfigService.edit_config_services(request, query_db, edit_config)
        if edit_config_result.is_success:
            logger.info(edit_config_result.message)
            return response_200(data=edit_config_result, message=edit_config_result.message)
        else:
            logger.warning(edit_config_result.message)
            return response_400(data="", message=edit_config_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@configController.post("/config/delete", response_model=CrudConfigResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:config:remove'))])
@log_decorator(title='参数管理', business_type=3)
async def delete_system_config(request: Request, delete_config: DeleteConfigModel, query_db: Session = Depends(get_db)):
    try:
        delete_config_result = await ConfigService.delete_config_services(request, query_db, delete_config)
        if delete_config_result.is_success:
            logger.info(delete_config_result.message)
            return response_200(data=delete_config_result, message=delete_config_result.message)
        else:
            logger.warning(delete_config_result.message)
            return response_400(data="", message=delete_config_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@configController.get("/config/{config_id}", response_model=ConfigModel, dependencies=[Depends(CheckUserInterfaceAuth('system:config:query'))])
async def query_detail_system_config(request: Request, config_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_config_result = ConfigService.detail_config_services(query_db, config_id)
        logger.info(f'获取config_id为{config_id}的信息成功')
        return response_200(data=detail_config_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@configController.post("/config/export", dependencies=[Depends(CheckUserInterfaceAuth('system:config:export'))])
@log_decorator(title='参数管理', business_type=5)
async def export_system_config_list(request: Request, config_query: ConfigQueryModel, query_db: Session = Depends(get_db)):
    try:
        # 获取全量数据
        config_query_result = ConfigService.get_config_list_services(query_db, config_query)
        config_export_result = ConfigService.export_config_list_services(config_query_result)
        logger.info('导出成功')
        return streaming_response_200(data=bytes2file_response(config_export_result))
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@configController.post("/config/refresh", response_model=CrudConfigResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:config:edit'))])
@log_decorator(title='参数管理', business_type=2)
async def refresh_system_config(request: Request, query_db: Session = Depends(get_db)):
    try:
        refresh_config_result = await ConfigService.refresh_sys_config_services(request, query_db)
        if refresh_config_result.is_success:
            logger.info(refresh_config_result.message)
            return response_200(data=refresh_config_result, message=refresh_config_result.message)
        else:
            logger.warning(refresh_config_result.message)
            return response_400(data="", message=refresh_config_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
