from config.enums import ApiMethod
from utils.request import api_request


class JobLogApi:
    """
    调度日志管理模块相关接口
    """

    @classmethod
    def list_job_log(cls, query: dict):
        """
        查询调度日志列表接口

        :param query: 查询调度日志参数
        :return:
        """
        return api_request(
            url='/monitor/jobLog/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def del_job_log(cls, job_log_id: str):
        """
        删除调度日志接口

        :param job_log_id: 调度日志id
        :return:
        """
        return api_request(
            url=f'/monitor/jobLog/{job_log_id}',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def clean_job_log(cls):
        """
        清空调度日志接口

        :return:
        """
        return api_request(
            url='/monitor/jobLog/clean',
            method=ApiMethod.DELETE,
        )

    @classmethod
    def export_job_log(cls, data: dict):
        """
        导出调度日志接口

        :param data: 导出调度日志参数
        :return:
        """
        return api_request(
            url='/monitor/jobLog/export',
            method=ApiMethod.POST,
            data=data,
            stream=True,
        )
