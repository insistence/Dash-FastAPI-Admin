import uuid
from fastapi import APIRouter, Request
from config.env import RedisInitKeyConfig
from module_admin.service.captcha_service import *
from utils.response_util import *
from utils.log_util import *
from datetime import timedelta


captchaController = APIRouter()


@captchaController.post("/captchaImage")
async def get_captcha_image(request: Request):
    try:
        session_id = str(uuid.uuid4())
        captcha_result = CaptchaService.create_captcha_image_service()
        image = captcha_result[0]
        computed_result = captcha_result[1]
        await request.app.state.redis.set(f"{RedisInitKeyConfig.CAPTCHA_CODES.get('key')}:{session_id}", computed_result, ex=timedelta(minutes=2))
        logger.info(f'编号为{session_id}的会话获取图片验证码成功')
        return response_200(data={'image': image, 'session_id': session_id}, message='获取验证码成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message=str(e))
