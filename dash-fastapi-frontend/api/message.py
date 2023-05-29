from utils.request import api_request


def send_message_api(page_obj: dict):

    return api_request(method='post', url='/login/loginByAccount', is_headers=False, json=page_obj)