import os


class PathConfig:

    # 项目绝对根目录
    ABS_ROOT_PATH = os.path.abspath(os.getcwd())


class RouterConfig:

    # 合法pathname列表
    BASIC_VALID_PATHNAME = [
        '/', '/login', '/forget'
    ]


class ApiBaseUrlConfig:

    # api基本url
    BaseUrl = 'http://127.0.0.1:9099'
