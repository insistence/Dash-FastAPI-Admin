import os
import time
from loguru import logger
from config.env import PathConfig


log_time = time.strftime('%Y%m%d', time.localtime())
# sys_log_file_path = os.path.join(PathConfig.ABS_ROOT_PATH, 'logs', 'sys_log', f'sys_request_log_{log_time}.log')
api_log_file_path = os.path.join(
    PathConfig.ABS_ROOT_PATH,
    'logs',
    'api_log',
    f'api_request_log_{log_time}.log',
)
exception_log_file_path = os.path.join(
    PathConfig.ABS_ROOT_PATH,
    'logs',
    'exception_log',
    f'exception_log_{log_time}.log',
)
# logger.add(sys_log_file_path, filter=lambda x: '[sys]' in x['message'],
#            rotation="50MB", encoding="utf-8", enqueue=True, compression="zip")
logger.add(
    api_log_file_path,
    filter=lambda x: '[api]' in x['message'],
    rotation='50MB',
    encoding='utf-8',
    enqueue=True,
    compression='zip',
)
logger.add(
    exception_log_file_path,
    filter=lambda x: '[exception]' in x['message'],
    rotation='50MB',
    encoding='utf-8',
    enqueue=True,
    compression='zip',
)
