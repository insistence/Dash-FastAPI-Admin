import requests
from typing import Optional
from flask import session, request
from config.env import AppConfig
from config.global_config import ApiBaseUrlConfig
from server import logger


def api_request(method: str, url: str, is_headers: bool, params: Optional[dict] = None, data: Optional[dict] = None,
                json: Optional[dict] = None, timeout: Optional[int] = None, stream: Optional[bool] = False):
    api_url = ApiBaseUrlConfig.BaseUrl + url
    method = method.lower().strip()
    user_agent = request.headers.get('User-Agent')
    authorization = session.get('Authorization') if session.get('Authorization') else ''
    remote_addr = request.headers.get("X-Forwarded-For") if AppConfig.app_env == 'prod' else request.remote_addr
    if is_headers:
        api_headers = {'Authorization': 'Bearer ' + authorization, 'remote_addr': remote_addr,
                       'User-Agent': user_agent}
    else:
        api_headers = {'remote_addr': remote_addr, 'User-Agent': user_agent}
    try:
        if method == 'get':
            response = requests.get(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                    timeout=timeout, stream=stream)
        elif method == 'post':
            response = requests.post(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                     timeout=timeout, stream=stream)
        elif method == 'delete':
            response = requests.delete(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                       timeout=timeout, stream=stream)
        elif method == 'put':
            response = requests.put(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                    timeout=timeout, stream=stream)
        elif method == 'patch':
            response = requests.patch(url=api_url, params=params, data=data, json=json, headers=api_headers,
                                      timeout=timeout, stream=stream)
        else:
            raise ValueError(f'Unsupported HTTP method: {method}')

        data_list = [params, data, json]
        if stream:
            response_code = response.status_code
            response_message = '获取成功' if response_code == 200 else '获取失败'
        else:
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

        return response if stream else response.json()
    except Exception as e:
        logger.error("[api]请求人:{}||请求IP:{}||请求方法:{}||请求Api:{}||请求结果:{}",
                     session.get('user_info').get('user_name') if session.get('user_info') else None,
                     request.remote_addr, method, url, str(e))
        session['code'] = 500
        session['message'] = str(e)

        return dict(code=500, data='', message=str(e))
