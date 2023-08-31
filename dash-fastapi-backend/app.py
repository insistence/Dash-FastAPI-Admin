from fastapi import FastAPI, Request
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from module_admin.controller.login_controller import loginController
from module_admin.controller.captcha_controller import captchaController
from module_admin.controller.user_controller import userController
from module_admin.controller.menu_controller import menuController
from module_admin.controller.dept_controller import deptController
from module_admin.controller.role_controller import roleController
from module_admin.controller.post_controler import postController
from module_admin.controller.dict_controller import dictController
from module_admin.controller.config_controller import configController
from module_admin.controller.notice_controller import noticeController
from module_admin.controller.log_controller import logController
from module_admin.controller.online_controller import onlineController
from module_admin.controller.job_controller import jobController
from module_admin.controller.server_controller import serverController
from module_admin.controller.cache_controller import cacheController
from module_admin.controller.common_controller import commonController
from config.get_redis import RedisUtil
from config.get_db import init_create_table
from config.get_scheduler import SchedulerUtil
from utils.response_util import *
from utils.log_util import logger
from utils.common_util import worship

app = FastAPI(
    title='Dash-FastAPI',
    description='Dash-FastAPI接口文档',
    version='1.0.0',
)

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


@app.on_event("startup")
async def startup_event():
    logger.info("Dash-FastAPI开始启动")
    worship()
    await init_create_table()
    app.state.redis = await RedisUtil.create_redis_pool()
    await RedisUtil.init_sys_dict(app.state.redis)
    await RedisUtil.init_sys_config(app.state.redis)
    await SchedulerUtil.init_system_scheduler()
    logger.info("Dash-FastAPI启动成功")


@app.on_event("shutdown")
async def shutdown_event():
    await RedisUtil.close_redis_pool(app)
    await SchedulerUtil.close_system_scheduler()


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


app.include_router(loginController, prefix="/login", tags=['登录模块'])
app.include_router(captchaController, prefix="/captcha", tags=['验证码模块'])
app.include_router(userController, prefix="/system", tags=['系统管理-用户管理'])
app.include_router(menuController, prefix="/system", tags=['系统管理-菜单管理'])
app.include_router(deptController, prefix="/system", tags=['系统管理-部门管理'])
app.include_router(roleController, prefix="/system", tags=['系统管理-角色管理'])
app.include_router(postController, prefix="/system", tags=['系统管理-岗位管理'])
app.include_router(dictController, prefix="/system", tags=['系统管理-字典管理'])
app.include_router(configController, prefix="/system", tags=['系统管理-参数管理'])
app.include_router(noticeController, prefix="/system", tags=['系统管理-通知公告管理'])
app.include_router(logController, prefix="/system", tags=['系统管理-日志管理'])
app.include_router(onlineController, prefix="/monitor", tags=['系统监控-在线用户'])
app.include_router(jobController, prefix="/monitor", tags=['系统监控-定时任务'])
app.include_router(serverController, prefix="/monitor", tags=['系统监控-服务监控'])
app.include_router(cacheController, prefix="/monitor", tags=['系统监控-缓存监控'])
app.include_router(commonController, prefix="/common", tags=['通用模块'])

if __name__ == '__main__':
    uvicorn.run(app='app:app', host="127.0.0.1", port=9099, reload=True)
