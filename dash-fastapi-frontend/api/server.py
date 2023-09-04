from utils.request import api_request


def get_server_statistical_info_api():

    return api_request(method='post', url='/monitor/server/statisticalInfo', is_headers=True)
