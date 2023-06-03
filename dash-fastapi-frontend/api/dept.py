from utils.request import api_request


def get_dept_tree_api(page_obj: dict):

    return api_request(method='post', url='/system/dept/tree', is_headers=True, json=page_obj)


def get_dept_tree_for_edit_option_api(page_obj: dict):

    return api_request(method='post', url='/system/dept/forEditOption', is_headers=True, json=page_obj)


def get_dept_list_api(page_obj: dict):

    return api_request(method='post', url='/system/dept/get', is_headers=True, json=page_obj)


def add_dept_api(page_obj: dict):

    return api_request(method='post', url='/system/dept/add', is_headers=True, json=page_obj)


def edit_dept_api(page_obj: dict):

    return api_request(method='post', url='/system/dept/edit', is_headers=True, json=page_obj)


def delete_dept_api(page_obj: dict):

    return api_request(method='post', url='/system/dept/delete', is_headers=True, json=page_obj)


def get_dept_detail_api(dept_id: int):

    return api_request(method='get', url=f'/system/dept/{dept_id}', is_headers=True)
