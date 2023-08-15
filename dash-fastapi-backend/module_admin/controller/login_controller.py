import uuid
from fastapi import APIRouter
from module_admin.service.login_service import *
from module_admin.entity.vo.login_vo import *
from module_admin.dao.login_dao import *
from config.env import JwtConfig
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator
from datetime import timedelta


loginController = APIRouter()


@loginController.post("/loginByAccount", response_model=Token)
@log_decorator(title='用户登录', business_type=0, log_type='login')
async def login(request: Request, user: UserLogin, query_db: Session = Depends(get_db)):
    try:
        result = await authenticate_user(request, query_db, user)
        if result in ['用户不存在', '密码错误', '用户已停用', '验证码已失效', '验证码错误']:
            logger.warning(result)
            return response_400(data="", message=result)

        else:
            access_token_expires = timedelta(minutes=JwtConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
            try:
                session_id = str(uuid.uuid4())
                access_token = create_access_token(
                    data={
                        "user_id": str(result[0].user_id),
                        "user_name": result[0].user_name,
                        "dept_name": result[1].dept_name,
                        "session_id": session_id,
                        "login_info": user.login_info
                    },
                    expires_delta=access_token_expires
                )
                await request.app.state.redis.set(f'access_token:{session_id}', access_token, ex=timedelta(minutes=30))
                # 此方法可实现同一账号同一时间只能登录一次
                # await request.app.state.redis.set(f'{result.user_id}_access_token', access_token, ex=timedelta(minutes=30))
                # await request.app.state.redis.set(f'{result.user_id}_session_id', session_id, ex=timedelta(minutes=30))
                logger.info('登录成功')
                return response_200(
                    data={'token': access_token},
                    message='登录成功'
                )
            except Exception as e:
                logger.exception(e)
                return response_500(data="", message="生成token失败")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@loginController.post("/getLoginUserInfo", response_model=CurrentUserInfoServiceResponse, dependencies=[Depends(get_current_user), Depends(CheckUserInterfaceAuth('common'))])
async def get_login_user_info(request: Request, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        logger.info('获取成功')
        return response_200(data=current_user, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@loginController.post("/logout", dependencies=[Depends(get_current_user), Depends(CheckUserInterfaceAuth('common'))])
async def logout(request: Request, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token[6:], JwtConfig.SECRET_KEY, algorithms=[JwtConfig.ALGORITHM])
        session_id: str = payload.get("session_id")
        await logout_services(request, session_id)
        logger.info('退出成功')
        return response_200(data="", message="退出成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
