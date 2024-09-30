from config.enums import ApiMethod
from utils.request import api_request


class ServerApi:
    """
    服务监控模块相关接口
    """

    @classmethod
    def get_server(cls):
        """
        获取服务信息接口

        :return:
        """
        return api_request(
            url='/monitor/server',
            method=ApiMethod.GET,
        )
