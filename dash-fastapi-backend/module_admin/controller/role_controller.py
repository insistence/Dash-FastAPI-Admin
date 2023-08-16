from fastapi import APIRouter, Request
from fastapi import Depends, Header
from config.get_db import get_db
from module_admin.service.login_service import get_current_user
from module_admin.service.role_service import *
from module_admin.entity.vo.role_vo import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from utils.common_util import bytes2file_response
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


roleController = APIRouter(dependencies=[Depends(get_current_user)])


@roleController.post("/role/forSelectOption", response_model=RoleSelectOptionResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_role_select(request: Request, query_db: Session = Depends(get_db)):
    try:
        role_query_result = get_role_select_option_services(query_db)
        logger.info('获取成功')
        return response_200(data=role_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
    
    
@roleController.post("/role/get", response_model=RolePageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:role:list'))])
async def get_system_role_list(request: Request, role_page_query: RolePageObject, query_db: Session = Depends(get_db)):
    try:
        role_query = RoleQueryModel(**role_page_query.dict())
        role_query_result = get_role_list_services(query_db, role_query)
        # 分页操作
        role_page_query_result = get_page_obj(role_query_result, role_page_query.page_num, role_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=role_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
    
    
@roleController.post("/role/add", response_model=CrudRoleResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:role:add'))])
@log_decorator(title='角色管理', business_type=1)
async def add_system_role(request: Request, add_role: AddRoleModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        add_role.create_by = current_user.user.user_name
        add_role.update_by = current_user.user.user_name
        add_role_result = add_role_services(query_db, add_role)
        logger.info(add_role_result.message)
        if add_role_result.is_success:
            return response_200(data=add_role_result, message=add_role_result.message)
        else:
            return response_400(data="", message=add_role_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
    
    
@roleController.patch("/role/edit", response_model=CrudRoleResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:role:edit'))])
@log_decorator(title='角色管理', business_type=2)
async def edit_system_role(request: Request, edit_role: AddRoleModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        edit_role.update_by = current_user.user.user_name
        edit_role.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_role_result = edit_role_services(query_db, edit_role)
        if edit_role_result.is_success:
            logger.info(edit_role_result.message)
            return response_200(data=edit_role_result, message=edit_role_result.message)
        else:
            logger.warning(edit_role_result.message)
            return response_400(data="", message=edit_role_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
    
    
@roleController.post("/role/delete", response_model=CrudRoleResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:role:remove'))])
@log_decorator(title='角色管理', business_type=3)
async def delete_system_role(request: Request, delete_role: DeleteRoleModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        delete_role.update_by = current_user.user.user_name
        delete_role.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delete_role_result = delete_role_services(query_db, delete_role)
        if delete_role_result.is_success:
            logger.info(delete_role_result.message)
            return response_200(data=delete_role_result, message=delete_role_result.message)
        else:
            logger.warning(delete_role_result.message)
            return response_400(data="", message=delete_role_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
    
    
@roleController.get("/role/{role_id}", response_model=RoleDetailModel, dependencies=[Depends(CheckUserInterfaceAuth('system:role:edit'))])
async def query_detail_system_role(request: Request, role_id: int, query_db: Session = Depends(get_db)):
    try:
        delete_role_result = detail_role_services(query_db, role_id)
        logger.info(f'获取role_id为{role_id}的信息成功')
        return response_200(data=delete_role_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@roleController.post("/role/export", dependencies=[Depends(CheckUserInterfaceAuth('system:role:export'))])
@log_decorator(title='角色管理', business_type=5)
async def export_system_role_list(request: Request, role_query: RoleQueryModel, query_db: Session = Depends(get_db)):
    try:
        # 获取全量数据
        role_query_result = get_role_list_services(query_db, role_query)
        role_export_result = export_role_list_services(role_query_result)
        logger.info('导出成功')
        return streaming_response_200(data=bytes2file_response(role_export_result))
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
