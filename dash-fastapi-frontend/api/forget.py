from config.enums import ApiMethod
from utils.request import api_request


class ForgetApi:
    """
    忘记密码模块相关接口
    """

    @classmethod
    def forget_password(cls, json: dict):
        """
        忘记密码接口

        :param data: 忘记密码参数
        :return:
        """
        return api_request(
            url='/forgetPwd',
            method=ApiMethod.POST,
            headers={'is_token': False},
            json=json,
        )

    @classmethod
    def send_message(cls, json: dict):
        """
        发送短信验证码接口

        :param data: 发送短信验证码参数
        :return:
        """
        return api_request(
            url='/getSmsCode',
            method=ApiMethod.POST,
            headers={'is_token': False},
            json=json,
        )
