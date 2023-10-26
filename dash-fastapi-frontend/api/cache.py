from utils.request import api_request


def get_cache_statistical_info_api():

    return api_request(method='post', url='/monitor/cache/statisticalInfo', is_headers=True)


def get_cache_name_list_api():

    return api_request(method='post', url='/monitor/cache/getNames', is_headers=True)


def get_cache_key_list_api(cache_name: str):

    return api_request(method='post', url=f'/monitor/cache/getKeys/{cache_name}', is_headers=True)


def get_cache_value_api(cache_name: str, cache_key: str):

    return api_request(method='post', url=f'/monitor/cache/getValue/{cache_name}/{cache_key}', is_headers=True)


def clear_cache_name_api(cache_name: str):

    return api_request(method='post', url=f'/monitor/cache/clearCacheName/{cache_name}', is_headers=True)


def clear_cache_key_api(cache_name: str, cache_key: str):

    return api_request(method='post', url=f'/monitor/cache/clearCacheKey/{cache_name}/{cache_key}', is_headers=True)


def clear_all_cache_api():

    return api_request(method='post', url='/monitor/cache/clearCacheAll', is_headers=True)
