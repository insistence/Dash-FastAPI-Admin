from fastapi import APIRouter
from module_admin.service.login_service import *
from module_admin.entity.vo.login_vo import *
from module_admin.dao.login_dao import *
from config.env import JwtConfig, RedisInitKeyConfig
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator
from datetime import timedelta


loginController = APIRouter()


@loginController.post("/loginByAccount", response_model=Token)
@log_decorator(title='用户登录', business_type=0, log_type='login')
async def login(request: Request, form_data: CustomOAuth2PasswordRequestForm = Depends(), query_db: Session = Depends(get_db)):
    captcha_enabled = True if await request.app.state.redis.get(f"{RedisInitKeyConfig.SYS_CONFIG.get('key')}:sys.account.captchaEnabled") == 'true' else False
    user = UserLogin(
        **dict(
            user_name=form_data.username,
            password=form_data.password,
            captcha=form_data.captcha,
            session_id=form_data.session_id,
            login_info=form_data.login_info,
            captcha_enabled=captcha_enabled
        )
    )
    try:
        result = await authenticate_user(request, query_db, user)
    except LoginException as e:
        return response_400(data="", message=e.message)
    try:
        access_token_expires = timedelta(minutes=JwtConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        session_id = str(uuid.uuid4())
        access_token = create_access_token(
            data={
                "user_id": str(result[0].user_id),
                "user_name": result[0].user_name,
                "dept_name": result[1].dept_name if result[1] else None,
                "session_id": session_id,
                "login_info": user.login_info
            },
            expires_delta=access_token_expires
        )
        await request.app.state.redis.set(f"{RedisInitKeyConfig.ACCESS_TOKEN.get('key')}:{session_id}", access_token,
                                          ex=timedelta(minutes=JwtConfig.REDIS_TOKEN_EXPIRE_MINUTES))
        # 此方法可实现同一账号同一时间只能登录一次
        # await request.app.state.redis.set(f"{RedisInitKeyConfig.ACCESS_TOKEN.get('key')}:{result[0].user_id}", access_token,
        #                                   ex=timedelta(minutes=JwtConfig.REDIS_TOKEN_EXPIRE_MINUTES))
        logger.info('登录成功')
        # 判断请求是否来自于api文档，如果是返回指定格式的结果，用于修复api文档认证成功后token显示undefined的bug
        request_from_swagger = request.headers.get('referer').endswith('docs') if request.headers.get('referer') else False
        request_from_redoc = request.headers.get('referer').endswith('redoc') if request.headers.get('referer') else False
        if request_from_swagger or request_from_redoc:
            return {'access_token': access_token, 'token_type': 'Bearer'}
        return response_200(
            data={'access_token': access_token, 'token_type': 'Bearer'},
            message='登录成功'
        )
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@loginController.post("/getSmsCode", response_model=SmsCode)
async def get_sms_code(request: Request, user: ResetUserModel, query_db: Session = Depends(get_db)):
    try:
        sms_result = await get_sms_code_services(request, query_db, user)
        if sms_result.is_success:
            logger.info('获取成功')
            return response_200(data=sms_result, message='获取成功')
        else:
            logger.warning(sms_result.message)
            return response_400(data='', message=sms_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@loginController.post("/forgetPwd", response_model=CrudUserResponse)
async def forget_user_pwd(request: Request, forget_user: ResetUserModel, query_db: Session = Depends(get_db)):
    try:
        forget_user_result = await forget_user_services(request, query_db, forget_user)
        if forget_user_result.is_success:
            logger.info(forget_user_result.message)
            return response_200(data=forget_user_result, message=forget_user_result.message)
        else:
            logger.warning(forget_user_result.message)
            return response_400(data="", message=forget_user_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@loginController.post("/getLoginUserInfo", response_model=CurrentUserInfoServiceResponse, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_login_user_info(request: Request, current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
    try:
        logger.info('获取成功')
        return response_200(data=current_user, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))


@loginController.post("/logout", dependencies=[Depends(get_current_user), Depends(CheckUserInterfaceAuth('common'))])
async def logout(request: Request, token: Optional[str] = Depends(oauth2_scheme), query_db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JwtConfig.SECRET_KEY, algorithms=[JwtConfig.ALGORITHM])
        session_id: str = payload.get("session_id")
        await logout_services(request, session_id)
        logger.info('退出成功')
        return response_200(data="", message="退出成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
