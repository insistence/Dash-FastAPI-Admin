from utils.request import api_request


def get_config_list_api(page_obj: dict):

    return api_request(method='post', url='/system/config/get', is_headers=True, json=page_obj)


def query_config_list_api(config_key: str):

    return api_request(method='get', url=f'/common/config/query/{config_key}', headers={'is_token': False})


def add_config_api(page_obj: dict):

    return api_request(method='post', url='/system/config/add', is_headers=True, json=page_obj)


def edit_config_api(page_obj: dict):

    return api_request(method='patch', url='/system/config/edit', is_headers=True, json=page_obj)


def delete_config_api(page_obj: dict):

    return api_request(method='post', url='/system/config/delete', is_headers=True, json=page_obj)


def get_config_detail_api(config_id: int):

    return api_request(method='get', url=f'/system/config/{config_id}', is_headers=True)


def export_config_list_api(page_obj: dict):

    return api_request(method='post', url='/system/config/export', is_headers=True, json=page_obj, stream=True)


def refresh_config_api(page_obj: dict):

    return api_request(method='post', url='/system/config/refresh', is_headers=True, json=page_obj)
