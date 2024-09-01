from utils.request import api_request


class LoginApi:
    """
    登录模块相关接口
    """

    @classmethod
    def login(cls, data: dict):
        """
        登录接口

        :param data: 登录参数
        :return:
        """
        return api_request(
            url='/login',
            method='post',
            headers={'is_token': False},
            data=data,
        )

    @classmethod
    def register(json: dict):
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

    @classmethod
    def get_info(cls):
        """
        获取登录用户信息接口

        :return:
        """
        return api_request(
            url='/getInfo',
            method='get',
        )

    @classmethod
    def logout(cls):
        """
        退出登录接口

        :return:
        """
        return api_request(
            url='/logout',
            method='post',
        )

    @classmethod
    def get_code_img(cls):
        """
        获取图片验证码接口

        :return:
        """
        return api_request(
            url='/captchaImage',
            method='get',
            headers={'is_token': False},
        )
