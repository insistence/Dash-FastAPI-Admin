from fastapi import APIRouter
from fastapi import Depends
from config.get_db import get_db
from module_admin.service.login_service import get_current_user, CurrentUserInfoServiceResponse
from module_admin.service.dict_service import *
from module_admin.entity.vo.dict_vo import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from utils.common_util import bytes2file_response
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


dictController = APIRouter(dependencies=[Depends(get_current_user)])


@dictController.post("/dictType/get", response_model=DictTypePageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:list'))])
async def get_system_dict_type_list(request: Request, dict_type_page_query: DictTypePageObject, query_db: Session = Depends(get_db)):
    try:
        dict_type_query = DictTypeQueryModel(**dict_type_page_query.dict())
        # 获取全量数据
        dict_type_query_result = DictTypeService.get_dict_type_list_services(query_db, dict_type_query)
        # 分页操作
        dict_type_page_query_result = get_page_obj(dict_type_query_result, dict_type_page_query.page_num, dict_type_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=dict_type_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictType/all", dependencies=[Depends(CheckUserInterfaceAuth('system:dict:list'))])
async def get_system_all_dict_type(request: Request, dict_type_query: DictTypeQueryModel, query_db: Session = Depends(get_db)):
    try:
        dict_type_query_result = DictTypeService.get_all_dict_type_services(query_db)
        logger.info('获取成功')
        return response_200(data=dict_type_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictType/add", response_model=CrudDictResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:add'))])
@log_decorator(title='字典管理', business_type=1)
async def add_system_dict_type(request: Request, add_dict_type: DictTypeModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        add_dict_type.create_by = current_user.user.user_name
        add_dict_type.update_by = current_user.user.user_name
        add_dict_type_result = await DictTypeService.add_dict_type_services(request, query_db, add_dict_type)
        if add_dict_type_result.is_success:
            logger.info(add_dict_type_result.message)
            return response_200(data=add_dict_type_result, message=add_dict_type_result.message)
        else:
            logger.warning(add_dict_type_result.message)
            return response_400(data="", message=add_dict_type_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.patch("/dictType/edit", response_model=CrudDictResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:edit'))])
@log_decorator(title='字典管理', business_type=2)
async def edit_system_dict_type(request: Request, edit_dict_type: DictTypeModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_dict_type.update_by = current_user.user.user_name
        edit_dict_type.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_dict_type_result = await DictTypeService.edit_dict_type_services(request, query_db, edit_dict_type)
        if edit_dict_type_result.is_success:
            logger.info(edit_dict_type_result.message)
            return response_200(data=edit_dict_type_result, message=edit_dict_type_result.message)
        else:
            logger.warning(edit_dict_type_result.message)
            return response_400(data="", message=edit_dict_type_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictType/delete", response_model=CrudDictResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:remove'))])
@log_decorator(title='字典管理', business_type=3)
async def delete_system_dict_type(request: Request, delete_dict_type: DeleteDictTypeModel, query_db: Session = Depends(get_db)):
    try:
        delete_dict_type_result = await DictTypeService.delete_dict_type_services(request, query_db, delete_dict_type)
        if delete_dict_type_result.is_success:
            logger.info(delete_dict_type_result.message)
            return response_200(data=delete_dict_type_result, message=delete_dict_type_result.message)
        else:
            logger.warning(delete_dict_type_result.message)
            return response_400(data="", message=delete_dict_type_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.get("/dictType/{dict_id}", response_model=DictTypeModel, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:query'))])
async def query_detail_system_dict_type(request: Request, dict_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_dict_type_result = DictTypeService.detail_dict_type_services(query_db, dict_id)
        logger.info(f'获取dict_id为{dict_id}的信息成功')
        return response_200(data=detail_dict_type_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictType/export", dependencies=[Depends(CheckUserInterfaceAuth('system:dict:export'))])
@log_decorator(title='字典管理', business_type=5)
async def export_system_dict_type_list(request: Request, dict_type_query: DictTypeQueryModel, query_db: Session = Depends(get_db)):
    try:
        # 获取全量数据
        dict_type_query_result = DictTypeService.get_dict_type_list_services(query_db, dict_type_query)
        dict_type_export_result = DictTypeService.export_dict_type_list_services(dict_type_query_result)
        logger.info('导出成功')
        return streaming_response_200(data=bytes2file_response(dict_type_export_result))
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictType/refresh", response_model=CrudDictResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:edit'))])
@log_decorator(title='字典管理', business_type=2)
async def refresh_system_dict(request: Request, query_db: Session = Depends(get_db)):
    try:
        refresh_dict_result = await DictTypeService.refresh_sys_dict_services(request, query_db)
        if refresh_dict_result.is_success:
            logger.info(refresh_dict_result.message)
            return response_200(data=refresh_dict_result, message=refresh_dict_result.message)
        else:
            logger.warning(refresh_dict_result.message)
            return response_400(data="", message=refresh_dict_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictData/get", response_model=DictDataPageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:list'))])
async def get_system_dict_data_list(request: Request, dict_data_page_query: DictDataPageObject, query_db: Session = Depends(get_db)):
    try:
        dict_data_query = DictDataModel(**dict_data_page_query.dict())
        # 获取全量数据
        dict_data_query_result = DictDataService.get_dict_data_list_services(query_db, dict_data_query)
        # 分页操作
        dict_data_page_query_result = get_page_obj(dict_data_query_result, dict_data_page_query.page_num, dict_data_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=dict_data_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.get("/dictData/query/{dict_type}", dependencies=[Depends(CheckUserInterfaceAuth('system:dict:list'))])
async def query_system_dict_data_list(request: Request, dict_type: str, query_db: Session = Depends(get_db)):
    try:
        # 获取全量数据
        dict_data_query_result = await DictDataService.query_dict_data_list_from_cache_services(request.app.state.redis, dict_type)
        logger.info('获取成功')
        return response_200(data=dict_data_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictData/add", response_model=CrudDictResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:add'))])
@log_decorator(title='字典管理', business_type=1)
async def add_system_dict_data(request: Request, add_dict_data: DictDataModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        add_dict_data.create_by = current_user.user.user_name
        add_dict_data.update_by = current_user.user.user_name
        add_dict_data_result = await DictDataService.add_dict_data_services(request, query_db, add_dict_data)
        if add_dict_data_result.is_success:
            logger.info(add_dict_data_result.message)
            return response_200(data=add_dict_data_result, message=add_dict_data_result.message)
        else:
            logger.warning(add_dict_data_result.message)
            return response_400(data="", message=add_dict_data_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.patch("/dictData/edit", response_model=CrudDictResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:edit'))])
@log_decorator(title='字典管理', business_type=2)
async def edit_system_dict_data(request: Request, edit_dict_data: DictDataModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_dict_data.update_by = current_user.user.user_name
        edit_dict_data.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_dict_data_result = await DictDataService.edit_dict_data_services(request, query_db, edit_dict_data)
        if edit_dict_data_result.is_success:
            logger.info(edit_dict_data_result.message)
            return response_200(data=edit_dict_data_result, message=edit_dict_data_result.message)
        else:
            logger.warning(edit_dict_data_result.message)
            return response_400(data="", message=edit_dict_data_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictData/delete", response_model=CrudDictResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:remove'))])
@log_decorator(title='字典管理', business_type=3)
async def delete_system_dict_data(request: Request, delete_dict_data: DeleteDictDataModel, query_db: Session = Depends(get_db)):
    try:
        delete_dict_data_result = await DictDataService.delete_dict_data_services(request, query_db, delete_dict_data)
        if delete_dict_data_result.is_success:
            logger.info(delete_dict_data_result.message)
            return response_200(data=delete_dict_data_result, message=delete_dict_data_result.message)
        else:
            logger.warning(delete_dict_data_result.message)
            return response_400(data="", message=delete_dict_data_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.get("/dictData/{dict_code}", response_model=DictDataModel, dependencies=[Depends(CheckUserInterfaceAuth('system:dict:query'))])
async def query_detail_system_dict_data(request: Request, dict_code: int, query_db: Session = Depends(get_db)):
    try:
        detail_dict_data_result = DictDataService.detail_dict_data_services(query_db, dict_code)
        logger.info(f'获取dict_code为{dict_code}的信息成功')
        return response_200(data=detail_dict_data_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@dictController.post("/dictData/export", dependencies=[Depends(CheckUserInterfaceAuth('system:dict:export'))])
@log_decorator(title='字典管理', business_type=5)
async def export_system_dict_data_list(request: Request, dict_data_query: DictDataModel, query_db: Session = Depends(get_db)):
    try:
        # 获取全量数据
        dict_data_query_result = DictDataService.get_dict_data_list_services(query_db, dict_data_query)
        dict_data_export_result = DictDataService.export_dict_data_list_services(dict_data_query_result)
        logger.info('导出成功')
        return streaming_response_200(data=bytes2file_response(dict_data_export_result))
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
