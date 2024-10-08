from dash import Dash
from flask import request, session
from user_agents import parse
from config.env import AppConfig
from config.exception import global_exception_handler
from utils.log_util import logger


app = Dash(
    __name__,
    compress=True,
    suppress_callback_exceptions=True,
    update_title=None,
    on_error=global_exception_handler,
)

server = app.server

app.title = AppConfig.app_name

# 配置密钥
app.server.secret_key = AppConfig.app_secret_key
app.server.config['COMPRESS_ALGORITHM'] = AppConfig.app_compress_algorithm
app.server.config['COMPRESS_BR_LEVEL'] = AppConfig.app_compress_br_level


# 获取用户浏览器信息
@server.before_request
def get_user_agent_info():
    request_addr = (
        request.headers.get('X-Forwarded-For')
        if AppConfig.app_env == 'prod'
        else request.remote_addr
    )
    user_string = str(request.user_agent)
    user_agent = parse(user_string)
    bw = user_agent.browser.family
    if user_agent.browser.version != ():
        bw_version = user_agent.browser.version[0]
        if bw == 'IE':
            logger.warning(
                '[sys]请求人:{}||请求IP:{}||请求方法:{}||请求Data:{}',
                session.get('name'),
                request_addr,
                request.method,
                '用户使用IE内核',
            )
            return "<h1 style='color: red'>请不要使用IE浏览器或360浏览器兼容模式</h1>"
        if bw == 'Chrome' and bw_version < 71:
            logger.warning(
                '[sys]请求人:{}||请求IP:{}||请求方法:{}||请求Data:{}',
                session.get('name'),
                request_addr,
                request.method,
                '用户Chrome内核版本太低',
            )
            return (
                "<h1 style='color: red'>Chrome内核版本号太低，请升级浏览器</h1>"
                "<h1 style='color: red'><a href='https://www.google.cn/chrome/'>点击此处</a>可下载最新版Chrome浏览器</h1>"
            )


# 配置系统日志
# @server.after_request
# def get_callbacks_log(response):
#     logger.info("[sys]请求人:{}||请求IP:{}||请求方法:{}||请求Data:{}",
#                 session.get('name'), request.remote_addr, request.method, request.data.decode("utf-8"))
#
#     return response
