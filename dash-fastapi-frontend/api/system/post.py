from utils.request import api_request


class PostApi:
    """
    岗位管理模块相关接口
    """

    @classmethod
    def list_post(cls, query: dict):
        """
        查询岗位列表接口

        :param query: 查询岗位参数
        :return:
        """
        return api_request(
            url='/system/post/list',
            method='get',
            params=query,
        )

    @classmethod
    def get_post(cls, post_id: int):
        """
        查询岗位详情接口

        :param post_id: 岗位id
        :return:
        """
        return api_request(
            url=f'/system/post/{post_id}',
            method='get',
        )

    @classmethod
    def add_post(cls, json: dict):
        """
        新增岗位接口

        :param json: 新增岗位参数
        :return:
        """
        return api_request(
            url='/system/post',
            method='post',
            json=json,
        )

    @classmethod
    def update_post(cls, json: dict):
        """
        修改岗位接口

        :param json: 修改岗位参数
        :return:
        """
        return api_request(
            url='/system/post',
            method='put',
            json=json,
        )

    @classmethod
    def del_post(cls, post_id: str):
        """
        删除岗位接口

        :param post_id: 岗位id
        :return:
        """
        return api_request(
            url=f'/system/post/{post_id}',
            method='delete',
        )

    @classmethod
    def export_post(cls, data: dict):
        """
        导出岗位接口

        :param data: 导出岗位参数
        :return:
        """
        return api_request(
            url='/system/post/export',
            method='post',
            data=data,
            stream=True,
        )
