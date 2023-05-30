from utils.request import api_request


def get_role_select_option_api():

    return api_request(method='post', url='/system/role/forSelectOption', is_headers=True)
