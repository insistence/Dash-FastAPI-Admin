import requests
from typing import Optional
from flask import session, request
from config.global_config import ApiBaseUrlConfig
from server import logger


def api_request(method: str, url: str, is_headers: bool, params: Optional[dict] = None, data: Optional[dict] = None,
                json: Optional[dict] = None, timeout: Optional[int] = None):
    api_url = ApiBaseUrlConfig.BaseUrl + url
    method = method.lower().strip()
    api_headers = None
    if is_headers:
        api_headers = {'token': 'Bearer' + session.get('token')}
    try:
        if method == 'get':
            response = requests.get(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                    timeout=timeout)
        elif method == 'post':
            response = requests.post(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                     timeout=timeout)
        elif method == 'delete':
            response = requests.delete(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                       timeout=timeout)
        elif method == 'put':
            response = requests.put(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                    timeout=timeout)
        elif method == 'patch':
            response = requests.patch(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                    timeout=timeout)
        else:
            raise ValueError(f'Unsupported HTTP method: {method}')

        data_list = [params, data, json]
        response_code = response.json().get('code')
        response_message = response.json().get('message')
        session['code'] = response_code
        session['message'] = response_message
        if response_code == 200:
            logger.info("[api]请求人:{}||请求IP:{}||请求方法:{}||请求Api:{}||请求参数:{}||请求结果:{}",
                        session.get('user_info').get('user_name') if session.get('user_info') else None,
                        request.remote_addr, method, url,
                        ','.join([str(x) for x in data_list if x]),
                        response_message)
        else:
            logger.warning("[api]请求人:{}||请求IP:{}||请求方法:{}||请求Api:{}||请求参数:{}||请求结果:{}",
                           session.get('user_info').get('user_name') if session.get('user_info') else None,
                           request.remote_addr, method, url,
                           ','.join([str(x) for x in data_list if x]),
                           response_message)

        return response.json()
    except Exception as e:
        logger.error("[api]请求人:{}||请求IP:{}||请求方法:{}||请求Api:{}||请求结果:{}",
                     session.get('user')['user_name'], request.remote_addr, method, url, str(e))

        raise Exception
