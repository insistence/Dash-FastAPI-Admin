from utils.request import api_request


def get_operation_log_list_api(page_obj: dict):

    return api_request(method='post', url='/system/log/operation/get', is_headers=True, json=page_obj)


def delete_operation_log_api(page_obj: dict):

    return api_request(method='post', url='/system/log/operation/delete', is_headers=True, json=page_obj)


def clear_operation_log_api(page_obj: dict):

    return api_request(method='post', url='/system/log/operation/clear', is_headers=True, json=page_obj)


def get_operation_log_detail_api(oper_id: int):

    return api_request(method='get', url=f'/system/log/operation/{oper_id}', is_headers=True)


def get_login_log_list_api(page_obj: dict):

    return api_request(method='post', url='/system/log/login/get', is_headers=True, json=page_obj)


def delete_login_log_api(page_obj: dict):

    return api_request(method='post', url='/system/log/login/delete', is_headers=True, json=page_obj)


def clear_login_log_api(page_obj: dict):

    return api_request(method='post', url='/system/log/login/clear', is_headers=True, json=page_obj)
