from utils.request import api_request


def change_password_api(page_obj: dict):

    return api_request(method='post', url='/login/loginByAccount', is_headers=False, json=page_obj)


def get_user_list_api(page_obj: dict):

    return api_request(method='post', url='/system/user/get', is_headers=True, json=page_obj)


def add_user_api(page_obj: dict):

    return api_request(method='post', url='/system/user/add', is_headers=True, json=page_obj)


def edit_user_api(page_obj: dict):

    return api_request(method='post', url='/system/user/edit', is_headers=True, json=page_obj)


def delete_user_api(page_obj: dict):

    return api_request(method='post', url='/system/user/delete', is_headers=True, json=page_obj)


def get_user_detail_api(user_id: int):

    return api_request(method='get', url=f'/system/user/{user_id}', is_headers=True)
