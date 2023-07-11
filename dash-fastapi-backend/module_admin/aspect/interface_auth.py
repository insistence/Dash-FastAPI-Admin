from fastapi import Depends
from module_admin.entity.vo.user_vo import *
from module_admin.service.login_service import get_current_user
from module_admin.utils.response_util import AuthException


class CheckUserInterfaceAuth:
    """
    校验当前用户是否具有相应的接口权限
    """
    def __init__(self, perm_str: str = 'common'):
        self.perm_str = perm_str

    def __call__(self, current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
        user_auth_list = [item.perms for item in current_user.menu]
        user_auth_list.append('common')
        if self.perm_str in user_auth_list:
            return True
        raise AuthException(data="", message="该用户无此接口权限")
