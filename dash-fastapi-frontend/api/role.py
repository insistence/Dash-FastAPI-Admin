from utils.request import api_request


def get_role_select_option_api():

    return api_request(method='post', url='/system/role/forSelectOption', is_headers=True)


def get_role_list_api(page_obj: dict):

    return api_request(method='post', url='/system/role/get', is_headers=True, json=page_obj)


def add_role_api(page_obj: dict):

    return api_request(method='post', url='/system/role/add', is_headers=True, json=page_obj)


def edit_role_api(page_obj: dict):

    return api_request(method='post', url='/system/role/edit', is_headers=True, json=page_obj)


def delete_role_api(page_obj: dict):

    return api_request(method='post', url='/system/role/delete', is_headers=True, json=page_obj)


def get_role_detail_api(role_id: int):

    return api_request(method='get', url=f'/system/role/{role_id}', is_headers=True)
