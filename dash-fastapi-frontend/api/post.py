from utils.request import api_request


def get_post_select_option_api():

    return api_request(method='post', url='/system/post/forSelectOption', is_headers=True)
