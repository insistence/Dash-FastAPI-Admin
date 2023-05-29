from fastapi import status
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from typing import Union
from datetime import datetime


def response_200(*, data: Union[list, dict, str], message="获取成功") -> Response:
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


def response_400(*, data: str = None, message: str = "获取失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=(
            {
                'code': 400,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def response_401(*, data: str = None, message: str = "获取失败") -> Response:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=(
            {
                'code': 401,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )


def response_500(*, data: str = None, message: str = "接口异常") -> Response:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=(
            {
                'code': 500,
                'message': message,
                'data': data,
                'success': 'false',
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
    )
