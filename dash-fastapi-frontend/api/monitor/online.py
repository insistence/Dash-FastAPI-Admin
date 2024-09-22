from config.enums import ApiMethod
from utils.request import api_request


class OnlineApi:
    """
    在线用户管理模块相关接口
    """

    @classmethod
    def list_online(cls, query: dict):
        """
        查询在线用户列表接口

        :param query: 查询在线用户参数
        :return:
        """
        return api_request(
            url='/monitor/online/list/page',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def force_logout(cls, token_id: str):
        """
        强退用户接口

        :param token_id: 在线用户token
        :return:
        """
        return api_request(
            url=f'/monitor/online/{token_id}',
            method=ApiMethod.DELETE,
        )
