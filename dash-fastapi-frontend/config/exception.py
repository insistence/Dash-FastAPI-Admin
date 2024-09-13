from dash import set_props
from utils.feedback_util import MessageManager, NotificationManager
from utils.log_util import logger


class AuthException(Exception):
    """
    自定义令牌异常AuthException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class RequestException(Exception):
    """
    自定义请求异常RequestException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class ServiceException(Exception):
    """
    自定义服务异常ServiceException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class ServiceWarning(Exception):
    """
    自定义服务警告ServiceWarning
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


def global_exception_handler(error):
    if isinstance(error, AuthException):
        set_props('token-invalid-modal', {'visible': True})
    elif isinstance(error, RequestException):
        NotificationManager.error(description=error.message, message='请求异常')
    elif isinstance(error, ServiceWarning):
        MessageManager.warning(content=error.message)
    elif isinstance(error, ServiceException):
        MessageManager.error(content=error.message)
    else:
        logger.exception(f'[exception]{error}')
        NotificationManager.error(description=str(error), message='服务异常')
