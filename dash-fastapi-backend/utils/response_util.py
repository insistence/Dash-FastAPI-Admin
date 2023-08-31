from fastapi import status
from fastapi.responses import JSONResponse, Response, StreamingResponse
from fastapi.encoders import jsonable_encoder
from typing import Union, Any
from datetime import datetime


def response_200(*, data: Any = None, message="获取成功") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder(
            {
                'code': 200,
                'message': message,
                'data': data,
                'success': 'true',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def response_400(*, data: Any = None, message: str = "获取失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {
                'code': 400,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def response_401(*, data: Any = None, message: str = "获取失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=jsonable_encoder(
            {
                'code': 401,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def response_500(*, data: Any = None, message: str = "接口异常") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder(
            {
                'code': 500,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def streaming_response_200(*, data: Any = None):
    return StreamingResponse(
        status_code=status.HTTP_200_OK,
        content=data,
    )
    
    
class AuthException(Exception):
    """
    自定义令牌异常AuthException
    """
    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class LoginException(Exception):
    """
    自定义登录异常LoginException
    """
    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message
