from utils.request import api_request


def get_online_list_api(page_obj: dict):

    return api_request(method='post', url='/monitor/online/get', is_headers=True, json=page_obj)


def force_logout_online_api(page_obj: dict):

    return api_request(method='post', url='/monitor/online/forceLogout', is_headers=True, json=page_obj)


def batch_logout_online_api(page_obj: dict):

    return api_request(method='post', url='/monitor/online/batchLogout', is_headers=True, json=page_obj)
