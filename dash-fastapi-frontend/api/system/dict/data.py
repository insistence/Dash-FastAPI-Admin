from utils.request import api_request


class DictDataApi:
    """
    字典数据管理模块相关接口
    """

    @classmethod
    def list_data(cls, query: dict):
        """
        查询字典数据列表接口

        :param query: 查询字典数据参数
        :return:
        """
        return api_request(
            url='/system/dict/data/list',
            method='get',
            params=query,
        )

    @classmethod
    def get_data(cls, dict_code: str):
        """
        查询字典数据详情接口

        :param dict_code: 字典数据id
        :return:
        """
        return api_request(
            url=f'/system/dict/data/{dict_code}',
            method='get',
        )

    @classmethod
    def get_dicts(cls, dict_type: str):
        """
        根据字典类型查询字典数据信息接口

        :param dict_type: 字典类型
        :return:
        """
        return api_request(
            url=f'/system/dict/data/type/{dict_type}',
            method='get',
        )

    @classmethod
    def add_data(cls, json: dict):
        """
        新增字典数据接口

        :param json: 新增字典数据参数
        :return:
        """
        return api_request(
            url='/system/dict/data',
            method='post',
            json=json,
        )

    @classmethod
    def update_data(cls, json: dict):
        """
        修改字典数据接口

        :param json: 修改字典数据参数
        :return:
        """
        return api_request(
            url='/system/dict/data',
            method='put',
            json=json,
        )

    @classmethod
    def del_data(cls, dict_code: str):
        """
        删除字典数据接口

        :param dict_code: 字典数据id
        :return:
        """
        return api_request(
            url=f'/system/dict/data/{dict_code}',
            method='delete',
        )
        
    @classmethod
    def export_data(cls, data: dict):
        """
        导出字典数据接口

        :param data: 导出字典数据参数
        :return:
        """
        return api_request(
            url='/system/dict/data/export',
            method='post',
            data=data,
            stream=True,
        )
