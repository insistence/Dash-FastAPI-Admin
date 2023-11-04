from fastapi import APIRouter, Request
from fastapi import Depends
import base64
from config.get_db import get_db
from module_admin.service.login_service import get_current_user
from module_admin.service.user_service import *
from module_admin.entity.vo.user_vo import *
from module_admin.dao.user_dao import *
from utils.page_util import get_page_obj
from utils.response_util import *
from utils.log_util import *
from utils.common_util import bytes2file_response
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.aspect.data_scope import GetDataScope
from module_admin.annotation.log_annotation import log_decorator


userController = APIRouter(dependencies=[Depends(get_current_user)])


@userController.post("/user/get", response_model=UserPageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:list'))])
async def get_system_user_list(request: Request, user_page_query: UserPageObject, query_db: Session = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysUser'))):
    try:
        user_query = UserQueryModel(**user_page_query.dict())
        # 获取全量数据
        user_query_result = UserService.get_user_list_services(query_db, user_query, data_scope_sql)
        # 分页操作
        user_page_query_result = get_page_obj(user_query_result, user_page_query.page_num, user_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=user_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/add", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:add'))])
@log_decorator(title='用户管理', business_type=1)
async def add_system_user(request: Request, add_user: AddUserModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        add_user.password = PwdUtil.get_password_hash(add_user.password)
        add_user.create_by = current_user.user.user_name
        add_user.update_by = current_user.user.user_name
        add_user_result = UserService.add_user_services(query_db, add_user)
        if add_user_result.is_success:
            logger.info(add_user_result.message)
            return response_200(data=add_user_result, message=add_user_result.message)
        else:
            logger.warning(add_user_result.message)
            return response_400(data="", message=add_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.patch("/user/edit", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:edit'))])
@log_decorator(title='用户管理', business_type=2)
async def edit_system_user(request: Request, edit_user: AddUserModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_user.update_by = current_user.user.user_name
        edit_user.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_user_result = UserService.edit_user_services(query_db, edit_user)
        if edit_user_result.is_success:
            logger.info(edit_user_result.message)
            return response_200(data=edit_user_result, message=edit_user_result.message)
        else:
            logger.warning(edit_user_result.message)
            return response_400(data="", message=edit_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/delete", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:remove'))])
@log_decorator(title='用户管理', business_type=3)
async def delete_system_user(request: Request, delete_user: DeleteUserModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        delete_user.update_by = current_user.user.user_name
        delete_user.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delete_user_result = UserService.delete_user_services(query_db, delete_user)
        if delete_user_result.is_success:
            logger.info(delete_user_result.message)
            return response_200(data=delete_user_result, message=delete_user_result.message)
        else:
            logger.warning(delete_user_result.message)
            return response_400(data="", message=delete_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.get("/user/{user_id}", response_model=UserDetailModel, dependencies=[Depends(CheckUserInterfaceAuth('system:user:query'))])
async def query_detail_system_user(request: Request, user_id: int, query_db: Session = Depends(get_db)):
    try:
        delete_user_result = UserService.detail_user_services(query_db, user_id)
        logger.info(f'获取user_id为{user_id}的信息成功')
        return response_200(data=delete_user_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.patch("/user/profile/changeAvatar", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
@log_decorator(title='个人信息', business_type=2)
async def change_system_user_profile_avatar(request: Request, edit_user: AddUserModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        avatar = edit_user.avatar
        # 去除 base64 字符串中的头部信息（data:image/jpeg;base64, 等等）
        base64_string = avatar.split(',', 1)[1]
        # 解码 base64 字符串
        file_data = base64.b64decode(base64_string)
        dir_path = os.path.join(CachePathConfig.PATH, 'avatar', current_user.user.user_name)
        try:
            os.makedirs(dir_path)
        except FileExistsError:
            pass
        filepath = os.path.join(dir_path, f'{current_user.user.user_name}_avatar.jpeg')
        with open(filepath, 'wb') as f:
            f.write(file_data)
        edit_user.user_id = current_user.user.user_id
        edit_user.avatar = f'/common/{CachePathConfig.PATHSTR}?taskPath=avatar&taskId={current_user.user.user_name}&filename={current_user.user.user_name}_avatar.jpeg'
        edit_user.update_by = current_user.user.user_name
        edit_user.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_user_result = UserService.edit_user_services(query_db, edit_user)
        if edit_user_result.is_success:
            logger.info(edit_user_result.message)
            return response_200(data=edit_user_result, message=edit_user_result.message)
        else:
            logger.warning(edit_user_result.message)
            return response_400(data="", message=edit_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.patch("/user/profile/changeInfo", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
@log_decorator(title='个人信息', business_type=2)
async def change_system_user_profile_info(request: Request, edit_user: AddUserModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        edit_user.user_id = current_user.user.user_id
        edit_user.update_by = current_user.user.user_name
        edit_user.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_user_result = UserService.edit_user_services(query_db, edit_user)
        if edit_user_result.is_success:
            logger.info(edit_user_result.message)
            return response_200(data=edit_user_result, message=edit_user_result.message)
        else:
            logger.warning(edit_user_result.message)
            return response_400(data="", message=edit_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.patch("/user/profile/resetPwd", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
@log_decorator(title='个人信息', business_type=2)
async def reset_system_user_password(request: Request, reset_user: ResetUserModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        if not reset_user.user_id and reset_user.old_password:
            reset_user.user_id = current_user.user.user_id
        reset_user.password = PwdUtil.get_password_hash(reset_user.password)
        reset_user.update_by = current_user.user.user_name
        reset_user.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        reset_user_result = UserService.reset_user_services(query_db, reset_user)
        if reset_user_result.is_success:
            logger.info(reset_user_result.message)
            return response_200(data=reset_user_result, message=reset_user_result.message)
        else:
            logger.warning(reset_user_result.message)
            return response_400(data="", message=reset_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/importData", dependencies=[Depends(CheckUserInterfaceAuth('system:user:import'))])
@log_decorator(title='用户管理', business_type=6)
async def batch_import_system_user(request: Request, user_import: ImportUserModel, query_db: Session = Depends(get_db), current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        batch_import_result = UserService.batch_import_user_services(query_db, user_import, current_user)
        if batch_import_result.is_success:
            logger.info(batch_import_result.message)
            return response_200(data=batch_import_result, message=batch_import_result.message)
        else:
            logger.warning(batch_import_result.message)
            return response_400(data="", message=batch_import_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/importTemplate", dependencies=[Depends(CheckUserInterfaceAuth('system:user:import'))])
async def export_system_user_template(request: Request, query_db: Session = Depends(get_db)):
    try:
        user_import_template_result = UserService.get_user_import_template_services()
        logger.info('获取成功')
        return streaming_response_200(data=bytes2file_response(user_import_template_result))
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/export", dependencies=[Depends(CheckUserInterfaceAuth('system:user:export'))])
@log_decorator(title='用户管理', business_type=5)
async def export_system_user_list(request: Request, user_query: UserQueryModel, query_db: Session = Depends(get_db), data_scope_sql: str = Depends(GetDataScope('SysUser'))):
    try:
        # 获取全量数据
        user_query_result = UserService.get_user_list_services(query_db, user_query, data_scope_sql)
        user_export_result = UserService.export_user_list_services(user_query_result)
        logger.info('导出成功')
        return streaming_response_200(data=bytes2file_response(user_export_result))
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/authRole/allocatedList", response_model=UserRolePageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_allocated_role_list(request: Request, user_role: UserRolePageObject, query_db: Session = Depends(get_db)):
    try:
        user_role_query = UserRoleQueryModel(**user_role.dict())
        user_role_allocated_query_result = UserService.get_user_role_allocated_list_services(query_db, user_role_query)
        # 分页操作
        user_role_allocated_page_query_result = get_page_obj(user_role_allocated_query_result, user_role.page_num, user_role.page_size)
        logger.info('获取成功')
        return response_200(data=user_role_allocated_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/authRole/unallocatedList", response_model=UserRolePageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_unallocated_role_list(request: Request, user_role: UserRolePageObject, query_db: Session = Depends(get_db)):
    try:
        user_role_query = UserRoleQueryModel(**user_role.dict())
        user_role_unallocated_query_result = UserService.get_user_role_unallocated_list_services(query_db, user_role_query)
        # 分页操作
        user_role_unallocated_page_query_result = get_page_obj(user_role_unallocated_query_result, user_role.page_num, user_role.page_size)
        logger.info('获取成功')
        return response_200(data=user_role_unallocated_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/authRole/selectAll", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:edit'))])
@log_decorator(title='用户管理', business_type=4)
async def add_system_role_user(request: Request, add_user_role: CrudUserRoleModel, query_db: Session = Depends(get_db)):
    try:
        add_user_role_result = UserService.add_user_role_services(query_db, add_user_role)
        if add_user_role_result.is_success:
            logger.info(add_user_role_result.message)
            return response_200(data=add_user_role_result, message=add_user_role_result.message)
        else:
            logger.warning(add_user_role_result.message)
            return response_400(data="", message=add_user_role_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@userController.post("/user/authRole/cancel", response_model=CrudUserResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:user:edit'))])
@log_decorator(title='用户管理', business_type=4)
async def cancel_system_role_user(request: Request, cancel_user_role: CrudUserRoleModel, query_db: Session = Depends(get_db)):
    try:
        cancel_user_role_result = UserService.delete_user_role_services(query_db, cancel_user_role)
        if cancel_user_role_result.is_success:
            logger.info(cancel_user_role_result.message)
            return response_200(data=cancel_user_role_result, message=cancel_user_role_result.message)
        else:
            logger.warning(cancel_user_role_result.message)
            return response_400(data="", message=cancel_user_role_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
