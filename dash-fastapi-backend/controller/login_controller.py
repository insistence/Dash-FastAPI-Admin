import uuid
from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from config.get_db import get_db
from service.login_service import *
from mapper.schema.login_schema import *
from mapper.crud.login_crud import *
from config.env import JwtConfig
from utils.response_tool import *
from utils.log_tool import *
from datetime import datetime, timedelta


loginController = APIRouter()


@loginController.post("/loginByAccount", response_model=Token)
async def login(request: Request, user: UserLogin, query_db: Session = Depends(get_db)):
    try:
        result = authenticate_user(query_db, user.user_name, user.password)
        if result == '用户不存在' or result == '密码错误' or result == '用户已停用':
            logger.warning(result)
            return response_400(data="", message=result)

        else:
            access_token_expires = timedelta(minutes=JwtConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
            try:
                session_id = str(uuid.uuid4())
                access_token = create_access_token(
                    data={"user_id": str(result.user_id), "session_id": session_id}, expires_delta=access_token_expires
                )
                await request.app.state.redis.set(f'{result.user_id}_access_token', access_token, ex=timedelta(minutes=30))
                await request.app.state.redis.set(f'{result.user_id}_session_id', session_id, ex=timedelta(minutes=30))
                logger.info('登录成功')
                return response_200(
                    data={
                        'token': access_token,
                        'session_id': session_id,
                    },
                    message='登录成功'
                )
            except Exception as e:
                logger.exception(e)
                return response_500(data="", message="生成token失败")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@loginController.post("/getLoginUserInfo", response_model=CurrentUserInfoServiceResponse, dependencies=[Depends(get_current_user)])
async def get_login_user_info(request: Request, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        logger.info('获取成功')
        return response_200(data=current_user, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@loginController.post("/logout", dependencies=[Depends(get_current_user)])
async def logout(request: Request, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        await logout_services(request, current_user)
        logger.info('退出成功')
        return response_200(data="", message="退出成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
