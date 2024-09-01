from utils.request import api_request


class DictTypeApi:
    """
    字典类型管理模块相关接口
    """

    @classmethod
    def list_type(cls, query: dict):
        """
        查询字典类型列表接口

        :param query: 查询字典类型参数
        :return:
        """
        return api_request(
            url='/system/dict/type/list',
            method='get',
            params=query,
        )

    @classmethod
    def get_type(cls, dict_id: str):
        """
        查询字典类型详情接口

        :param dict_id: 字典类型id
        :return:
        """
        return api_request(
            url=f'/system/dict/type/{dict_id}',
            method='get',
        )

    @classmethod
    def add_type(cls, json: dict):
        """
        新增字典类型接口

        :param json: 新增字典类型参数
        :return:
        """
        return api_request(
            url='/system/dict/type',
            method='post',
            json=json,
        )

    @classmethod
    def update_type(cls, json: dict):
        """
        修改字典类型接口

        :param json: 修改字典类型参数
        :return:
        """
        return api_request(
            url='/system/dict/type',
            method='put',
            json=json,
        )

    @classmethod
    def del_type(cls, dict_id: str):
        """
        删除字典类型接口

        :param dict_id: 字典类型id
        :return:
        """
        return api_request(
            url=f'/system/dict/type/{dict_id}',
            method='delete',
        )

    @classmethod
    def export_type(cls, data: dict):
        """
        导出字典类型接口

        :param data: 导出字典类型参数
        :return:
        """
        return api_request(
            url='/system/dict/type/export',
            method='post',
            data=data,
            stream=True,
        )

    @classmethod
    def refresh_cache(cls):
        """
        删除字典类型接口

        :return:
        """
        return api_request(
            url='/system/dict/type/refreshCache',
            method='delete',
        )

    @classmethod
    def optionselect(cls):
        """
        查询字典类型详情接口

        :return:
        """
        return api_request(
            url='/system/dict/type/optionselect',
            method='get',
        )
