from fastapi import APIRouter, Request
from fastapi import Depends, Header
from config.get_db import get_db
from module_admin.service.login_service import get_current_user
from module_admin.service.dept_service import *
from module_admin.entity.vo.dept_vo import *
from module_admin.dao.dept_dao import *
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


deptController = APIRouter(dependencies=[Depends(get_current_user)])


@deptController.post("/dept/tree", response_model=DeptTree, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_dept_tree(request: Request, dept_query: DeptModel, query_db: Session = Depends(get_db)):
    try:
        dept_query_result = get_dept_tree_services(query_db, dept_query)
        logger.info('获取成功')
        return response_200(data=dept_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@deptController.post("/dept/forEditOption", response_model=DeptTree, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_dept_tree_for_edit_option(request: Request, dept_query: DeptModel, query_db: Session = Depends(get_db)):
    try:
        dept_query_result = get_dept_tree_for_edit_option_services(query_db, dept_query)
        logger.info('获取成功')
        return response_200(data=dept_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@deptController.post("/dept/get", response_model=DeptResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dept:list'))])
async def get_system_dept_list(request: Request, dept_query: DeptModel, query_db: Session = Depends(get_db)):
    try:
        dept_query_result = get_dept_list_services(query_db, dept_query)
        logger.info('获取成功')
        return response_200(data=dept_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@deptController.post("/dept/add", response_model=CrudDeptResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dept:add'))])
@log_decorator(title='部门管理', business_type=1)
async def add_system_dept(request: Request, add_dept: DeptModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        add_dept.create_by = current_user.user.user_name
        add_dept.update_by = current_user.user.user_name
        add_dept_result = add_dept_services(query_db, add_dept)
        logger.info(add_dept_result.message)
        if add_dept_result.is_success:
            return response_200(data=add_dept_result, message=add_dept_result.message)
        else:
            return response_400(data="", message=add_dept_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@deptController.patch("/dept/edit", response_model=CrudDeptResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dept:edit'))])
@log_decorator(title='部门管理', business_type=2)
async def edit_system_dept(request: Request, edit_dept: DeptModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        edit_dept.update_by = current_user.user.user_name
        edit_dept.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_dept_result = edit_dept_services(query_db, edit_dept)
        if edit_dept_result.is_success:
            logger.info(edit_dept_result.message)
            return response_200(data=edit_dept_result, message=edit_dept_result.message)
        else:
            logger.warning(edit_dept_result.message)
            return response_400(data="", message=edit_dept_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@deptController.post("/dept/delete", response_model=CrudDeptResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:dept:remove'))])
@log_decorator(title='部门管理', business_type=3)
async def delete_system_dept(request: Request, delete_dept: DeleteDeptModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        delete_dept.update_by = current_user.user.user_name
        delete_dept.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        delete_dept_result = delete_dept_services(query_db, delete_dept)
        if delete_dept_result.is_success:
            logger.info(delete_dept_result.message)
            return response_200(data=delete_dept_result, message=delete_dept_result.message)
        else:
            logger.warning(delete_dept_result.message)
            return response_400(data="", message=delete_dept_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@deptController.get("/dept/{dept_id}", response_model=DeptModel, dependencies=[Depends(CheckUserInterfaceAuth('system:dept:edit'))])
async def query_detail_system_dept(request: Request, dept_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_dept_result = detail_dept_services(query_db, dept_id)
        logger.info(f'获取dept_id为{dept_id}的信息成功')
        return response_200(data=detail_dept_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
