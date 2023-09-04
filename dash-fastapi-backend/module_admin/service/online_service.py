from fastapi import Request
from jose import jwt
from config.env import JwtConfig
from module_admin.entity.vo.online_vo import *


class OnlineService:
    """
    在线用户管理模块服务层
    """

    @classmethod
    async def get_online_list_services(cls, request: Request, query_object: OnlinePageObject):
        """
        获取在线用户表信息service
        :param request: Request对象
        :param query_object: 查询参数对象
        :return: 在线用户列表信息
        """
        access_token_keys = await request.app.state.redis.keys('access_token*')
        if not access_token_keys:
            access_token_keys = []
        access_token_values_list = [await request.app.state.redis.get(key) for key in access_token_keys]
        online_info_list = []
        for item in access_token_values_list:
            payload = jwt.decode(item, JwtConfig.SECRET_KEY, algorithms=[JwtConfig.ALGORITHM])
            online_dict = dict(
                session_id=payload.get('session_id'),
                user_name=payload.get('user_name'),
                dept_name=payload.get('dept_name'),
                ipaddr=payload.get('login_info').get('ipaddr'),
                login_location=payload.get('login_info').get('login_location'),
                browser=payload.get('login_info').get('browser'),
                os=payload.get('login_info').get('os'),
                login_time=payload.get('login_info').get('login_time')
            )
            if query_object.user_name and not query_object.ipaddr:
                if query_object.user_name == payload.get('user_name'):
                    online_info_list = [online_dict]
                    break
            elif not query_object.user_name and query_object.ipaddr:
                if query_object.ipaddr == payload.get('ipaddr'):
                    online_info_list = [online_dict]
                    break
            elif query_object.user_name and query_object.ipaddr:
                if query_object.user_name == payload.get('user_name') and query_object.ipaddr == payload.get('ipaddr'):
                    online_info_list = [online_dict]
                    break
            else:
                online_info_list.append(online_dict)

        return online_info_list

    @classmethod
    async def delete_online_services(cls, request: Request, page_object: DeleteOnlineModel):
        """
        强退在线用户信息service
        :param request: Request对象
        :param page_object: 强退在线用户对象
        :return: 强退在线用户校验结果
        """
        if page_object.session_ids.split(','):
            session_id_list = page_object.session_ids.split(',')
            for session_id in session_id_list:
                await request.app.state.redis.delete(f'access_token:{session_id}')
            result = dict(is_success=True, message='强退成功')
        else:
            result = dict(is_success=False, message='传入session_id为空')
        return CrudOnlineResponse(**result)
