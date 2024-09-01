import requests
from typing import Dict, Literal, Optional
from flask import session, request
from config.env import AppConfig
from config.global_config import ApiBaseUrlConfig
from server import logger


def api_request(
    url: str,
    method: Literal['get', 'post', 'delete', 'put', 'patch'],
    headers: Optional[Dict] = {},
    params: Optional[Dict] = None,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None,
    timeout: Optional[int] = None,
    stream: Optional[bool] = False,
):
    """
    Api请求方法

    :param url: 请求url
    :param method: 请求方法
    :param headers: 请求头
    :param params: 查询参数
    :param data: 表单参数
    :param json: 请求体
    :param timeout: 请求超时时间
    :param stream: 是否为流式请求
    :return: 请求结果
    """
    api_url = ApiBaseUrlConfig.BaseUrl + url
    api_method = method.lower().strip()
    user_agent = request.headers.get('User-Agent')
    authorization = (
        session.get('Authorization') if session.get('Authorization') else ''
    )
    remote_addr = (
        request.headers.get('X-Forwarded-For')
        if AppConfig.app_env == 'prod'
        else request.remote_addr
    )
    merged_headers = {'is_token': True, **headers}
    is_token = merged_headers.get('is_token')
    api_headers = {
        k: v for k, v in merged_headers.items() if isinstance(v, (str, bytes))
    }
    api_headers.update(
        {
            'remote_addr': remote_addr,
            'User-Agent': user_agent,
            'is_browser': 'no',
        }
    )
    if is_token:
        api_headers.update({'Authorization': 'Bearer ' + authorization})
    try:
        if api_method == 'get':
            response = requests.get(
                url=api_url,
                params=params,
                data=data,
                json=json,
                headers=api_headers,
                timeout=timeout,
                stream=stream,
            )
        elif api_method == 'post':
            response = requests.post(
                url=api_url,
                params=params,
                data=data,
                json=json,
                headers=api_headers,
                timeout=timeout,
                stream=stream,
            )
        elif api_method == 'delete':
            response = requests.delete(
                url=api_url,
                params=params,
                data=data,
                json=json,
                headers=api_headers,
                timeout=timeout,
                stream=stream,
            )
        elif api_method == 'put':
            response = requests.put(
                url=api_url,
                params=params,
                data=data,
                json=json,
                headers=api_headers,
                timeout=timeout,
                stream=stream,
            )
        elif api_method == 'patch':
            response = requests.patch(
                url=api_url,
                params=params,
                data=data,
                json=json,
                headers=api_headers,
                timeout=timeout,
                stream=stream,
            )

        data_list = [params, data, json]
        if stream:
            response_code = response.status_code
            response_message = (
                '获取成功' if response_code == 200 else '获取失败'
            )
        else:
            response_code = response.json().get('code')
            response_message = response.json().get('msg')
        session['code'] = response_code
        session['message'] = response_message
        if response_code == 200:
            logger.info(
                '[api]请求人:{}||请求IP:{}||请求方法:{}||请求Api:{}||请求参数:{}||请求结果:{}',
                session.get('user_info').get('user_name')
                if session.get('user_info')
                else None,
                remote_addr,
                method,
                url,
                ','.join([str(x) for x in data_list if x]),
                response_message,
            )
        else:
            logger.warning(
                '[api]请求人:{}||请求IP:{}||请求方法:{}||请求Api:{}||请求参数:{}||请求结果:{}',
                session.get('user_info').get('user_name')
                if session.get('user_info')
                else None,
                remote_addr,
                method,
                url,
                ','.join([str(x) for x in data_list if x]),
                response_message,
            )

        return response if stream else response.json()
    except Exception as e:
        logger.error(
            '[api]请求人:{}||请求IP:{}||请求方法:{}||请求Api:{}||请求结果:{}',
            session.get('user_info').get('user_name')
            if session.get('user_info')
            else None,
            remote_addr,
            method,
            url,
            str(e),
        )
        session['code'] = 500
        session['msg'] = str(e)

        return dict(code=500, data='', message=str(e))
