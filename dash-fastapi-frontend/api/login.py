from config.enums import ApiMethod
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
            method=ApiMethod.POST,
            headers={'is_token': False},
            data=data,
        )

    @classmethod
    def get_info(cls):
        """
        获取登录用户信息接口

        :return:
        """
        return api_request(
            url='/getInfo',
            method=ApiMethod.GET,
        )

    @classmethod
    def logout(cls):
        """
        退出登录接口

        :return:
        """
        return api_request(
            url='/logout',
            method=ApiMethod.POST,
        )

    @classmethod
    def get_code_img(cls):
        """
        获取图片验证码接口

        :return:
        """
        return api_request(
            url='/captchaImage',
            method=ApiMethod.GET,
            headers={'is_token': False},
        )
