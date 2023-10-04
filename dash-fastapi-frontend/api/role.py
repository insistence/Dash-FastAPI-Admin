from utils.request import api_request


def get_role_select_option_api():

    return api_request(method='post', url='/system/role/forSelectOption', is_headers=True)


def get_role_list_api(page_obj: dict):

    return api_request(method='post', url='/system/role/get', is_headers=True, json=page_obj)


def add_role_api(page_obj: dict):

    return api_request(method='post', url='/system/role/add', is_headers=True, json=page_obj)


def edit_role_api(page_obj: dict):

    return api_request(method='patch', url='/system/role/edit', is_headers=True, json=page_obj)


def role_datascope_api(page_obj: dict):

    return api_request(method='patch', url='/system/role/dataScope', is_headers=True, json=page_obj)


def delete_role_api(page_obj: dict):

    return api_request(method='post', url='/system/role/delete', is_headers=True, json=page_obj)


def get_role_detail_api(role_id: int):

    return api_request(method='get', url=f'/system/role/{role_id}', is_headers=True)


def export_role_list_api(page_obj: dict):

    return api_request(method='post', url='/system/role/export', is_headers=True, json=page_obj, stream=True)


def get_allocated_user_list_api(page_obj: dict):

    return api_request(method='post', url='/system/role/authUser/allocatedList', is_headers=True, json=page_obj)


def get_unallocated_user_list_api(page_obj: dict):

    return api_request(method='post', url='/system/role/authUser/unallocatedList', is_headers=True, json=page_obj)


def auth_user_select_all_api(page_obj: dict):

    return api_request(method='post', url='/system/role/authUser/selectAll', is_headers=True, json=page_obj)


def auth_user_cancel_api(page_obj: dict):

    return api_request(method='post', url='/system/role/authUser/cancel', is_headers=True, json=page_obj)
