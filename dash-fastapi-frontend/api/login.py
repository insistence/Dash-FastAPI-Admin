from utils.request import api_request


def login_api(page_obj: dict):

    return api_request(method='post', url='/login/loginByAccount', is_headers=False, json=page_obj)


def get_current_user_info_api():

    return api_request(method='post', url='/login/getLoginUserInfo', is_headers=True)
