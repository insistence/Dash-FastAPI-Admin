from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from config.get_db import get_db
from service.login_service import get_current_user, get_password_hash
from service.post_service import *
from mapper.schema.post_schema import *
from utils.response_tool import *
from utils.log_tool import *


postController = APIRouter()


@postController.post("/post/forSelectOption", response_model=PostSelectOptionResponseModel)
async def get_system_post_select(request: Request, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        if current_user == "用户token已失效，请重新登录" or current_user == "用户token不合法":
            logger.warning(current_user)
            return response_401(data="", message=current_user)
        else:
            role_query_result = get_post_select_option_services(query_db)
            logger.info('获取成功')
            return response_200(data=role_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
