from config.enums import ApiMethod
from utils.request import api_request


class RouterApi:
    """
    路由模块相关接口
    """

    @classmethod
    def get_routers(cls):
        """
        获取路由信息接口

        :return:
        """
        return api_request(
            url='/getRouters',
            method=ApiMethod.GET,
        )
