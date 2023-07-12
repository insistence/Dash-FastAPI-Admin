from functools import wraps
from fastapi import Request
import inspect
import os
import json
import time
from datetime import datetime
import requests
from user_agents import parse
from typing import Optional
from module_admin.service.login_service import get_current_user
from module_admin.service.log_service import add_operation_log_services, add_login_log_services
from module_admin.entity.vo.log_vo import OperLogModel, LogininforModel


def log_decorator(title: str, business_type: int, log_type: Optional[str] = 'operation'):
    """
    日志装饰器
    :param log_type: 日志类型（login表示登录日志，为空表示为操作日志）
    :param title: 当前日志装饰器装饰的模块标题
    :param business_type: 业务类型（0其它 1新增 2修改 3删除 4授权 5导出 6导入 7强退 8生成代码 9清空数据）
    :return:
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            # 获取被装饰函数的文件路径
            file_path = inspect.getfile(func)
            # 获取项目根路径
            project_root = os.getcwd()
            # 处理文件路径，去除项目根路径部分
            relative_path = os.path.relpath(file_path, start=project_root)[0:-2].replace('\\', '.')
            # 获取当前被装饰函数所在路径
            func_path = f'{relative_path}{func.__name__}()'
            # 获取上下文信息
            request: Request = kwargs.get('request')
            token = request.headers.get('token')
            query_db = kwargs.get('query_db')
            request_method = request.method
            operator_type = 0
            user_agent = request.headers.get('User-Agent')
            if "Windows" in user_agent or "Macintosh" in user_agent or "Linux" in user_agent:
                operator_type = 1
            if "Mobile" in user_agent or "Android" in user_agent or "iPhone" in user_agent:
                operator_type = 2
            oper_url = request.url.path
            oper_ip = request.headers.get('remote_addr')
            oper_location = '内网IP'
            try:
                if oper_ip != '127.0.0.1' and oper_ip != 'localhost':
                    ip_result = requests.get(f'https://qifu-api.baidubce.com/ip/geo/v1/district?ip={oper_ip}')
                    if ip_result.status_code == 200:
                        prov = ip_result.json().get('data').get('prov')
                        city = ip_result.json().get('data').get('city')
                        if prov or city:
                            oper_location = f'{prov}-{city}'
                        else:
                            oper_location = '未知'
                    else:
                        oper_location = '未知'
            except Exception as e:
                oper_location = '未知'
                print(e)
            finally:
                payload = await request.body()
                oper_param = json.dumps(json.loads(str(payload, 'utf-8')), ensure_ascii=False)

                # 调用原始函数
                oper_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result = await func(*args, **kwargs)
                cost_time = float(time.time() - start_time) * 100
                result_dict = json.loads(str(result.body, 'utf-8'))
                json_result = json.dumps(dict(code=result_dict.get('code'), message=result_dict.get('message')), ensure_ascii=False)
                status = 1
                error_msg = ''
                if result_dict.get('code') == 200:
                    status = 0
                else:
                    error_msg = result_dict.get('message')
                if log_type == 'login':
                    # print(request.headers)
                    user_agent_info = parse(user_agent)
                    browser = f'{user_agent_info.browser.family} {user_agent_info.browser.version[0]}'
                    system_os = f'{user_agent_info.os.family} {user_agent_info.os.version[0]}'
                    user = kwargs.get('user')
                    user_name = user.user_name
                    login_log = dict(
                        user_name=user_name,
                        ipaddr=oper_ip,
                        login_location=oper_location,
                        browser=browser,
                        os=system_os,
                        status=str(status),
                        msg=result_dict.get('message'),
                        login_time=oper_time
                    )

                    add_login_log_services(query_db, LogininforModel(**login_log))
                else:
                    current_user = await get_current_user(request, token, query_db)
                    oper_name = current_user.user.user_name
                    dept_name = current_user.dept.dept_name
                    operation_log = dict(
                        title=title,
                        business_type=business_type,
                        method=func_path,
                        request_method=request_method,
                        operator_type=operator_type,
                        oper_name=oper_name,
                        dept_name=dept_name,
                        oper_url=oper_url,
                        oper_ip=oper_ip,
                        oper_location=oper_location,
                        oper_param=oper_param,
                        json_result=json_result,
                        status=status,
                        error_msg=error_msg,
                        oper_time=oper_time,
                        cost_time=cost_time
                    )
                    add_operation_log_services(query_db, OperLogModel(**operation_log))

                return result

        return wrapper

    return decorator
