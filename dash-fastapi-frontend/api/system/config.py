from utils.request import api_request


class ConfigApi:
    """
    参数配置模块相关接口
    """

    @classmethod
    def list_config(cls, query: dict):
        """
        查询参数配置列表接口

        :param query: 查询参数配置参数
        :return:
        """
        return api_request(
            url='/system/config/list',
            method='get',
            params=query,
        )

    @classmethod
    def get_config(cls, config_id: int):
        """
        查询参数配置详情接口

        :param config_id: 参数配置id
        :return:
        """
        return api_request(
            url=f'/system/config/{config_id}',
            method='get',
        )

    @classmethod
    def get_config_key(config_key: str):
        """
        根据参数配置键名查询参数配置值接口

        :param config_key: 参数键名
        :return:
        """
        return api_request(
            url=f'/system/config/configKey/{config_key}',
            method='get',
        )

    @classmethod
    def add_config(cls, json: dict):
        """
        新增参数配置接口

        :param json: 新增参数配置参数
        :return:
        """
        return api_request(
            url='/system/config',
            method='post',
            json=json,
        )

    @classmethod
    def update_config(cls, json: dict):
        """
        修改参数配置接口

        :param json: 修改参数配置参数
        :return:
        """
        return api_request(
            url='/system/config',
            method='put',
            json=json,
        )

    @classmethod
    def del_config(cls, config_id: str):
        """
        删除参数配置接口

        :param config_id: 参数配置id
        :return:
        """
        return api_request(
            url=f'/system/config/{config_id}',
            method='delete',
        )

    @classmethod
    def refresh_cache(cls):
        """
        刷新参数配置缓存接口

        :return:
        """
        return api_request(
            url='/system/config/refreshCache',
            method='delete',
        )

    @classmethod
    def export_config(cls, data: dict):
        """
        导出参数配置接口

        :param data: 导出参数配置参数
        :return:
        """
        return api_request(
            url='/system/config/export',
            method='post',
            data=data,
            stream=True,
        )
