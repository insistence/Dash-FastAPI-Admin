from utils.request import api_request


def get_notice_list_api(page_obj: dict):

    return api_request(method='post', url='/system/notice/get', is_headers=True, json=page_obj)


def add_notice_api(page_obj: dict):

    return api_request(method='post', url='/system/notice/add', is_headers=True, json=page_obj)


def edit_notice_api(page_obj: dict):

    return api_request(method='patch', url='/system/notice/edit', is_headers=True, json=page_obj)


def delete_notice_api(page_obj: dict):

    return api_request(method='post', url='/system/notice/delete', is_headers=True, json=page_obj)


def get_notice_detail_api(notice_id: int):

    return api_request(method='get', url=f'/system/notice/{notice_id}', is_headers=True)
