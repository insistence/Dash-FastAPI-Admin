from utils.request import api_request


def get_cache_statistical_info_api():

    return api_request(method='post', url='/monitor/cache/statisticalInfo', is_headers=True)
