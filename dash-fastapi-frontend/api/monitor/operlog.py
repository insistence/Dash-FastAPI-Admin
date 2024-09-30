from config.enums import ApiMethod
from utils.request import api_request


class OperlogApi:
    """
    操作日志管理模块相关接口
    """

    @classmethod
    def list_operlog(cls, query: dict):
        """
        查询操作日志列表接口

        :param query: 查询操作日志参数
        :return:
        """
        return api_request(
            url='/monitor/operlog/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def del_operlog(cls, oper_id: str):
        """
        删除操作日志接口

        :param oper_id: 操作日志id
        :return:
        """
        return api_request(
            url=f'/monitor/operlog/{oper_id}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def clean_operlog(cls):
        """
        清空操作日志接口

        :return:
        """
        return api_request(
            url='/monitor/operlog/clean',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def export_operlog(cls, data: dict):
        """
        导出操作日志接口

        :param data: 导出操作日志参数
        :return:
        """
        return api_request(
            url='/monitor/operlog/export',
            method=ApiMethod.POST,
            data=data,
            stream=True,
        )
