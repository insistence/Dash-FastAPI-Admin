from config.enums import ApiMethod
from utils.request import api_request


class LogininforApi:
    """
    登录日志管理模块相关接口
    """

    @classmethod
    def list_logininfor(cls, query: dict):
        """
        查询登录日志列表接口

        :param query: 查询登录日志参数
        :return:
        """
        return api_request(
            url='/monitor/logininfor/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def del_logininfor(cls, info_id: str):
        """
        删除登录日志接口

        :param info_id: 登录日志id
        :return:
        """
        return api_request(
            url=f'/monitor/logininfor/{info_id}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def unlock_logininfor(cls, user_name: str):
        """
        解锁用户登录状态接口

        :param user_name: 用户名称
        :return:
        """
        return api_request(
            url=f'/monitor/logininfor/unlock/{user_name}',
            method=ApiMethod.GET,
        )

    @classmethod
    def clean_logininfor(cls):
        """
        清空登录日志接口

        :return:
        """
        return api_request(
            url='/monitor/logininfor/clean',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def export_logininfor(cls, data: dict):
        """
        导出登录日志接口

        :param data: 导出登录日志参数
        :return:
        """
        return api_request(
            url='/monitor/logininfor/export',
            method=ApiMethod.POST,
            data=data,
            stream=True,
        )
