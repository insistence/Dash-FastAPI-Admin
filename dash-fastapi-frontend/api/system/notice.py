from config.enums import ApiMethod
from utils.request import api_request


class NoticeApi:
    """
    通知公告管理模块相关接口
    """

    @classmethod
    def list_notice(cls, query: dict):
        """
        查询通知公告列表接口

        :param query: 查询通知公告参数
        :return:
        """
        return api_request(
            url='/system/notice/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def get_notice(cls, notice_id: int):
        """
        查询通知公告详情接口

        :param notice_id: 通知公告id
        :return:
        """
        return api_request(
            url=f'/system/notice/{notice_id}',
            method=ApiMethod.GET,
        )

    @classmethod
    def add_notice(cls, json: dict):
        """
        新增通知公告接口

        :param json: 新增通知公告参数
        :return:
        """
        return api_request(
            url='/system/notice',
            method=ApiMethod.POST,
            json=json,
        )

    @classmethod
    def update_notice(cls, json: dict):
        """
        修改通知公告接口

        :param json: 修改通知公告参数
        :return:
        """
        return api_request(
            url='/system/notice',
            method=ApiMethod.PUT,
            json=json,
        )

    @classmethod
    def del_notice(cls, notice_id: str):
        """
        删除通知公告接口

        :param notice_id: 通知公告id
        :return:
        """
        return api_request(
            url=f'/system/notice/{notice_id}',
            method=ApiMethod.DELETE,
        )
