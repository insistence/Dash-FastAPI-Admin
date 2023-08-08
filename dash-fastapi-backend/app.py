from fastapi import FastAPI, Request
import uvicorn
import aioredis
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from module_admin.controller.login_controller import loginController
# from module_admin.controller.captcha_controller import captchaController
from module_admin.controller.user_controller import userController
from module_admin.controller.menu_controller import menuController
from module_admin.controller.dept_controller import deptController
from module_admin.controller.role_controller import roleController
from module_admin.controller.post_controler import postController
from module_admin.controller.dict_controller import dictController
from module_admin.controller.log_controller import logController
from module_admin.controller.common_controller import commonController
from config.env import RedisConfig
from utils.response_util import response_401, AuthException


app = FastAPI()

# 前端页面url
origins = [
    "http://localhost:8088",
    "http://127.0.0.1:8088",
]

# 后台api允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def create_redis_pool() -> aioredis.Redis:
    redis = await aioredis.from_url(
        url=f"redis://{RedisConfig.HOST}",
        port=RedisConfig.PORT,
        username=RedisConfig.USERNAME,
        password=RedisConfig.PASSWORD,
        db=RedisConfig.DB,
        encoding="utf-8",
        decode_responses=True
    )
    return redis


@app.on_event("startup")
async def startup_event():
    app.state.redis = await create_redis_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()
    
    
# 自定义token检验异常
@app.exception_handler(AuthException)
async def auth_exception_handler(request: Request, exc: AuthException):
    return response_401(data=exc.data, message=exc.message)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.detail, "code": exc.status_code}),
        status_code=exc.status_code
    )


app.include_router(loginController, prefix="/login", tags=['login'])
# app.include_router(captchaController, prefix="/captcha", tags=['captcha'])
app.include_router(userController, prefix="/system", tags=['system/user'])
app.include_router(menuController, prefix="/system", tags=['system/menu'])
app.include_router(deptController, prefix="/system", tags=['system/dept'])
app.include_router(roleController, prefix="/system", tags=['system/role'])
app.include_router(postController, prefix="/system", tags=['system/post'])
app.include_router(dictController, prefix="/system", tags=['system/dict'])
app.include_router(logController, prefix="/system", tags=['system/log'])
app.include_router(commonController, prefix="/common", tags=['common'])


if __name__ == '__main__':
    uvicorn.run(app='app:app', host="127.0.0.1", port=9099, reload=True)
