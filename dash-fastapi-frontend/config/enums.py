from enum import Enum


class ApiMethod(Enum):
    """
    Api请求方法

    GET: get方法
    POST: post方法
    DELETE: delete方法
    PUT: put方法
    PATCH: patch方法
    """

    GET = 'get'
    POST = 'post'
    DELETE = 'delete'
    PUT = 'put'
    PATCH = 'patch'
