import dash
import os
import time
from loguru import logger
from flask import request, session
from user_agents import parse
from config.global_config import PathConfig

app = dash.Dash(
    __name__,
    compress=True,
    suppress_callback_exceptions=True,
    update_title=None
)

server = app.server

app.title = '通用后台管理系统'

# 配置密钥
app.server.secret_key = 'Dash-FastAPI'
app.server.config['COMPRESS_ALGORITHM'] = 'br'
app.server.config['COMPRESS_BR_LEVEL'] = 8

log_time = time.strftime("%Y%m%d", time.localtime())
sys_log_file_path = os.path.join(PathConfig.ABS_ROOT_PATH, 'log', 'sys_log', f'sys_request_log_{log_time}.log')
api_log_file_path = os.path.join(PathConfig.ABS_ROOT_PATH, 'log', 'api_log', f'api_request_log_{log_time}.log')
logger.add(sys_log_file_path, filter=lambda x: '[sys]' in x['message'],
           rotation="50MB", encoding="utf-8", enqueue=True, compression="zip")
logger.add(api_log_file_path, filter=lambda x: '[api]' in x['message'],
           rotation="50MB", encoding="utf-8", enqueue=True, compression="zip")


# 获取用户浏览器信息
@server.before_request
def get_user_agent_info():
    user_string = str(request.user_agent)
    user_agent = parse(user_string)
    bw = user_agent.browser.family
    bw_version = user_agent.browser.version[0]
    if bw == 'IE':
        logger.warning("[sys]请求人:{}||请求IP:{}||请求方法:{}||请求Data:{}",
                session.get('name'), request.remote_addr, request.method, '用户使用IE内核')
        return "<h1 style='color: red'>请不要使用IE浏览器或360浏览器兼容模式</h1>"
    if bw_version < 71:
        logger.warning("[sys]请求人:{}||请求IP:{}||请求方法:{}||请求Data:{}",
                       session.get('name'), request.remote_addr, request.method, '用户Chrome内核版本太低')
        return "<h1 style='color: red'>Chrome内核版本号太低，请升级浏览器</h1>" \
               "<h1 style='color: red'><a href='https://www.google.cn/chrome/'>点击此处</a>可下载最新版Chrome浏览器</h1>"


# 配置系统日志
# @server.after_request
# def get_callbacks_log(response):
#     logger.info("[sys]请求人:{}||请求IP:{}||请求方法:{}||请求Data:{}",
#                 session.get('name'), request.remote_addr, request.method, request.data.decode("utf-8"))
#
#     return response


# 这里的app即为Dash实例
@app.server.route('/upload/', methods=['POST'])
def upload():
    """
    构建文件上传服务
    :return:
    """

    # 获取上传id参数，用于指向保存路径
    upload_id = request.values.get('uploadId')

    # 获取上传的文件名称
    filename = request.files['file'].filename

    # 基于上传id，若本地不存在则会自动创建目录
    try:
        os.mkdir(os.path.join(PathConfig.ABS_ROOT_PATH, 'cache', 'upload', f'{upload_id}'))
    except FileExistsError:
        pass

    # 流式写出文件到指定目录
    with open(os.path.join(PathConfig.ABS_ROOT_PATH, 'cache', 'upload', f'{upload_id}', filename), 'wb') as f:
        # 流式写出大型文件，这里的10代表10MB
        for chunk in iter(lambda: request.files['file'].read(1024 * 1024 * 10), b''):
            f.write(chunk)

    return {'filename': filename}
