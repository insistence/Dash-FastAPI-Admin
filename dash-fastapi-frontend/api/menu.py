from utils.request import api_request


def get_menu_tree_api(page_obj: dict):

    return api_request(method='post', url='/system/menu/tree', is_headers=True, json=page_obj)


def get_menu_tree_for_edit_option_api(page_obj: dict):

    return api_request(method='post', url='/system/menu/forEditOption', is_headers=True, json=page_obj)


def get_menu_list_api(page_obj: dict):

    return api_request(method='post', url='/system/menu/get', is_headers=True, json=page_obj)


def add_menu_api(page_obj: dict):

    return api_request(method='post', url='/system/menu/add', is_headers=True, json=page_obj)


def edit_menu_api(page_obj: dict):

    return api_request(method='post', url='/system/menu/edit', is_headers=True, json=page_obj)


def delete_menu_api(page_obj: dict):

    return api_request(method='post', url='/system/menu/delete', is_headers=True, json=page_obj)


def get_menu_detail_api(menu_id: int):

    return api_request(method='get', url=f'/system/menu/{menu_id}', is_headers=True)
