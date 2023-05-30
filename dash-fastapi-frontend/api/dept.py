from utils.request import api_request


def get_dept_tree_api(page_obj: dict):

    return api_request(method='post', url='/system/dept/tree', is_headers=True, json=page_obj)
