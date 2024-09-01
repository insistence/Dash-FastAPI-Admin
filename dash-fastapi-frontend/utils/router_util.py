import json
from copy import deepcopy
from typing import Dict, List


class CommonConstant:
    """
    常用常量

    WWW: www主域
    HTTP: http请求
    HTTPS: https请求
    """

    WWW = 'www.'
    HTTP = 'http://'
    HTTPS = 'https://'


class RouterUtil:
    """
    路由工具类
    """

    @classmethod
    def generate_menu_tree(cls, router_list: List, path: str = ''):
        """
        生成菜单树

        :param router_list: 路由列表
        :param path: 路由path
        :return: 菜单树
        """
        menu_list = []
        for router in router_list:
            copy_router = deepcopy(router)
            copy_router['path'] = (
                copy_router.get('path')
                if copy_router.get('path')
                and (
                    copy_router.get('path').startswith('/')
                    or cls.is_http(copy_router.get('path'))
                )
                else '/' + copy_router.get('path')
            )
            copy_router['props'] = {
                **copy_router.get('meta'),
                'key': copy_router.get('name'),
                'href': path + copy_router.get('path'),
            }
            if copy_router.get('component') in ['Layout', 'ParentView']:
                copy_router['component'] = 'SubMenu'
            elif copy_router.get('component') == 'InnerLink':
                if copy_router.get('path') == '/':
                    copy_router = copy_router['children']
                    copy_router['props']['href'] = '/' + copy_router.get('path')
                    cls.__genrate_item_menu(
                        copy_router, 'components.inner_link'
                    )
                else:
                    if copy_router.get('children'):
                        copy_router['component'] = 'SubMenu'
                    else:
                        cls.__genrate_item_menu(
                            copy_router, 'components.inner_link'
                        )
            else:
                cls.__genrate_item_menu(
                    copy_router, copy_router.get('component')
                )

            if copy_router.get('children'):
                copy_router['children'] = cls.generate_menu_tree(
                    copy_router.get('children'),
                    copy_router.get('props').get('href'),
                )
            else:
                query = (
                    '?'
                    + '&'.join(
                        [
                            '{}={}'.format(k, v)
                            for k, v in json.loads(
                                copy_router.get('query')
                            ).items()
                        ]
                    )
                    if copy_router.get('query')
                    else ''
                )
                copy_router['props']['href'] = (
                    copy_router.get('props').get('href') + query
                )
            copy_router.pop('name', None)
            copy_router.pop('meta', None)
            menu_list.append(copy_router)

        return menu_list

    @classmethod
    def get_visible_routers(cls, router_list: List):
        """
        获取可见路由

        :param router_list: 路由列表
        :return: 可见路由列表
        """
        new_router_list = []
        for router in router_list:
            copy_router = deepcopy(router)
            if copy_router.get('hidden'):
                continue
            if copy_router.get('children'):
                copy_router['children'] = cls.get_visible_routers(
                    copy_router.get('children')
                )
            new_router_list.append(copy_router)

        return new_router_list

    @classmethod
    def __genrate_item_menu(cls, router: Dict, modules: str):
        """
        生成Item类型菜单

        :param router: 路由信息
        :param modules: 组件路径

        :return: Item类型菜单
        """
        router['props']['modules'] = modules
        router['component'] = 'Item'

        return router

    @classmethod
    def is_http(cls, link: str):
        """
        判断是否为http(s)://开头

        :param link: 链接
        :return: 是否为http(s)://开头
        """
        return link.startswith(CommonConstant.HTTP) or link.startswith(
            CommonConstant.HTTPS
        )
