from utils.request import api_request


def login_api(page_obj: dict):

    return api_request(method='post', url='/login/loginByAccount', is_headers=False, json=page_obj)


def get_captcha_image_api():

    return api_request(method='post', url='/captcha/captchaImage', is_headers=False)


def get_current_user_info_api():

    return api_request(method='post', url='/login/getLoginUserInfo', is_headers=True)


def logout_api():
    return api_request(method='post', url='/login/logout', is_headers=True)
