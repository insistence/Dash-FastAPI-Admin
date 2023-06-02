from utils.request import api_request


def get_post_select_option_api():

    return api_request(method='post', url='/system/post/forSelectOption', is_headers=True)


def get_post_list_api(page_obj: dict):

    return api_request(method='post', url='/system/post/get', is_headers=True, json=page_obj)


def add_post_api(page_obj: dict):

    return api_request(method='post', url='/system/post/add', is_headers=True, json=page_obj)


def edit_post_api(page_obj: dict):

    return api_request(method='post', url='/system/post/edit', is_headers=True, json=page_obj)


def delete_post_api(page_obj: dict):

    return api_request(method='post', url='/system/post/delete', is_headers=True, json=page_obj)


def get_post_detail_api(post_id: int):

    return api_request(method='get', url=f'/system/post/{post_id}', is_headers=True)
