from utils.request import api_request


class JobApi:
    """
    定时任务调度管理模块相关接口
    """

    @classmethod
    def list_job(cls, query: dict):
        """
        查询定时任务调度列表接口

        :param query: 查询定时任务调度参数
        :return:
        """
        return api_request(
            url='/monitor/job/list',
            method='get',
            params=query,
        )

    @classmethod
    def get_job(cls, job_id: int):
        """
        查询定时任务调度详情接口

        :param job_id: 定时任务调度id
        :return:
        """
        return api_request(
            url=f'/monitor/job/{job_id}',
            method='get',
        )

    @classmethod
    def add_job(cls, json: dict):
        """
        新增定时任务调度接口

        :param json: 新增定时任务调度参数
        :return:
        """
        return api_request(
            url='/monitor/job',
            method='post',
            json=json,
        )

    @classmethod
    def update_job(cls, json: dict):
        """
        修改定时任务调度接口

        :param json: 修改定时任务调度参数
        :return:
        """
        return api_request(
            url='/monitor/job',
            method='put',
            json=json,
        )

    @classmethod
    def del_job(cls, job_id: str):
        """
        删除定时任务调度接口

        :param job_id: 定时任务调度id
        :return:
        """
        return api_request(
            url=f'/monitor/job/{job_id}',
            method='delete',
        )

    @classmethod
    def export_job(cls, data: dict):
        """
        导出定时任务调度接口

        :param data: 导出定时任务调度参数
        :return:
        """
        return api_request(
            url='/monitor/job/export',
            method='post',
            data=data,
            stream=True,
        )

    @classmethod
    def change_job_status(cls, job_id: int, status: str):
        """
        定时任务调度状态修改接口

        :param job_id: 定时任务id
        :param status: 定时任务状态
        :return:
        """
        return api_request(
            url='/monitor/job/changeStatus',
            method='put',
            json=dict(job_id=job_id, status=status),
        )

    @classmethod
    def run_job(cls, job_id: int, job_group: str):
        """
        定时任务立即执行一次接口

        :param job_id: 定时任务id
        :param job_group: 定时任务分组
        :return:
        """
        return api_request(
            url='/monitor/job/run',
            method='put',
            json=dict(job_id=job_id, job_group=job_group),
        )
