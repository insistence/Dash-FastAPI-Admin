from fastapi import APIRouter, Request
from fastapi import Depends, Header
from config.get_db import get_db
from module_admin.service.login_service import get_current_user, get_password_hash
from module_admin.service.user_service import *
from module_admin.entity.vo.user_vo import *
from module_admin.dao.user_dao import *
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


userController = APIRouter(dependencies=[Depends(get_current_user)])


@userController.post("/user/get", response_model=UserPageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:list'))])
async def get_system_user_list(request: Request, user_query: UserPageObject, query_db: Session = Depends(get_db)):
    try:
        user_query_result = get_user_list_services(query_db, user_query)
        logger.info('获取成功')
        return response_200(data=user_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@userController.post("/user/add", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:add'))])
@log_decorator(title='用户管理', business_type=1)
async def add_system_user(request: Request, add_user: AddUserModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        add_user.password = get_password_hash(add_user.password)
        add_user.create_by = current_user.user.user_name
        add_user.update_by = current_user.user.user_name
        add_user_result = add_user_services(query_db, add_user)
        logger.info(add_user_result.message)
        if add_user_result.is_success:
            return response_200(data=add_user_result, message=add_user_result.message)
        else:
            return response_400(data="", message=add_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@userController.patch("/user/edit", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:edit'))])
@log_decorator(title='用户管理', business_type=2)
async def edit_system_user(request: Request, edit_user: AddUserModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        edit_user.update_by = current_user.user.user_name
        edit_user.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_user_result = edit_user_services(query_db, edit_user)
        if edit_user_result.is_success:
            logger.info(edit_user_result.message)
            return response_200(data=edit_user_result, message=edit_user_result.message)
        else:
            logger.warning(edit_user_result.message)
            return response_400(data="", message=edit_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@userController.post("/user/delete", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:remove'))])
@log_decorator(title='用户管理', business_type=3)
async def delete_system_user(request: Request, delete_user: DeleteUserModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        delete_user.update_by = current_user.user.user_name
        delete_user.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delete_user_result = delete_user_services(query_db, delete_user)
        if delete_user_result.is_success:
            logger.info(delete_user_result.message)
            return response_200(data=delete_user_result, message=delete_user_result.message)
        else:
            logger.warning(delete_user_result.message)
            return response_400(data="", message=delete_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@userController.get("/user/{user_id}", response_model=UserDetailModel, dependencies=[Depends(CheckUserInterfaceAuth('system:user:edit'))])
async def query_detail_system_user(request: Request, user_id: int, query_db: Session = Depends(get_db)):
    try:
        delete_user_result = detail_user_services(query_db, user_id)
        logger.info(f'获取user_id为{user_id}的信息成功')
        return response_200(data=delete_user_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
