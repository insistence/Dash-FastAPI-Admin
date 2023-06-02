from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from config.get_db import get_db
from service.login_service import get_current_user, get_password_hash
from service.dept_service import *
from mapper.schema.dept_schema import *
from mapper.crud.dept_crud import *
from utils.response_tool import *
from utils.log_tool import *


deptController = APIRouter()


@deptController.post("/dept/tree", response_model=DeptTree)
async def get_system_dept_tree(request: Request, dept_query: DeptModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        if current_user == "用户token已失效，请重新登录" or current_user == "用户token不合法":
            logger.warning(current_user)
            return response_401(data="", message=current_user)
        else:
            dept_query_result = get_dept_tree_services(query_db, dept_query)
            logger.info('获取成功')
            return response_200(data=dept_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@deptController.post("/dept/get", response_model=DeptResponse)
async def get_system_dept_list(request: Request, dept_query: DeptModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        if current_user == "用户token已失效，请重新登录" or current_user == "用户token不合法":
            logger.warning(current_user)
            return response_401(data="", message=current_user)
        else:
            dept_query_result = get_dept_list_services(query_db, dept_query)
            logger.info('获取成功')
            return response_200(data=dept_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
