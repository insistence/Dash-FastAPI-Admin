from fastapi import FastAPI, Request
import uvicorn
import aioredis
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from controller.login_controller import loginController
from controller.user_controller import userController
from controller.menu_controller import menuController
from controller.dept_controller import deptController
from controller.role_controller import roleController
from controller.post_controler import postController
from config.env import RedisConfig


app = FastAPI()

# 前端页面url
origins = [
    "http://localhost:8088",
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


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        content=jsonable_encoder({"message": exc.detail, "code": exc.status_code}),
        status_code=exc.status_code
    )


app.include_router(loginController, prefix="/login", tags=['login'])
app.include_router(userController, prefix="/system", tags=['system/user'])
app.include_router(menuController, prefix="/system", tags=['system/menu'])
app.include_router(deptController, prefix="/system", tags=['system/dept'])
app.include_router(roleController, prefix="/system", tags=['system/role'])
app.include_router(postController, prefix="/system", tags=['system/post'])


if __name__ == '__main__':
    uvicorn.run(app='app:app', host="127.0.0.1", port=9099, reload=True)
