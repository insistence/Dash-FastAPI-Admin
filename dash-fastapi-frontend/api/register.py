from utils.request import api_request


class RegisterApi:
    """
    注册模块相关接口
    """

    @classmethod
    def register(cls, json: dict):
        """
        注册接口

        :param data: 注册参数
        :return:
        """
        return api_request(
            url='/register',
            method='post',
            headers={'is_token': False},
            json=json,
        )
