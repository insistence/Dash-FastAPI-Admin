import json
from copy import deepcopy
from typing import Dict, List
from config.constant import CommonConstant, MenuConstant


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
            if (
                copy_router.get('path') in ['', '/']
                and len(copy_router.get('children') or []) == 1
            ):
                copy_router = copy_router['children'][0]
            copy_router['path'] = (
                copy_router.get('path')
                if copy_router.get('path')
                and (
                    copy_router.get('path').startswith('/')
                    or cls.is_http(copy_router.get('path'))
                )
                else '/' + copy_router.get('path')
            )
            meta = copy_router.get('meta') if copy_router.get('meta') else {}
            copy_router['props'] = {
                **meta,
                'key': copy_router.get('name') + path + copy_router.get('path'),
                'href': path + copy_router.get('path'),
            }
            if copy_router.get('component') in [
                MenuConstant.LAYOUT,
                MenuConstant.PARENT_VIEW,
            ]:
                copy_router['component'] = MenuConstant.SUB_MENU
                if cls.is_http(copy_router.get('path')):
                    copy_router['props']['target'] = '_blank'
            elif copy_router.get('component') == MenuConstant.INNER_LINK:
                if copy_router.get('path') == '/':
                    copy_router = copy_router['children']
                    copy_router['props']['href'] = '/' + copy_router.get('path')
                    cls.__genrate_item_menu(copy_router, 'innerlink')
                else:
                    if copy_router.get('children'):
                        copy_router['component'] = MenuConstant.SUB_MENU
                    else:
                        cls.__genrate_item_menu(copy_router, 'innerlink')
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
    def generate_search_panel_data(
        cls, menu_list: List, section_path: List = []
    ):
        """
        生成搜索面板数据

        :param menu_list: 菜单列表
        :param section_path: 分组路径
        :return: 搜索面板数据
        """
        search_panel_data = []
        for item in menu_list:
            if item.get('children'):
                section_path.append(item.get('props').get('title'))
                search_panel_data.extend(
                    cls.generate_search_panel_data(
                        item.get('children'), section_path
                    )
                )
                section_path.pop()
            else:
                href = item.get('props').get('href')
                target = (
                    '_blank'
                    if cls.is_http(item.get('props').get('href'))
                    else '_self'
                )
                item_dict = dict(
                    id=item.get('props').get('key'),
                    title=item.get('props').get('title'),
                    section='/'.join(section_path),
                    handler=f'() => window.open("{href}", "{target}")',
                )
                search_panel_data.append(item_dict)

        return search_panel_data

    @classmethod
    def generate_validate_pathname_list(cls, menu_list: List):
        """
        生成合法路由列表

        :param menu_list: 菜单列表
        :return: 合法路由列表
        """
        validate_pathname_list = []
        for item in menu_list:
            if item.get('children'):
                validate_pathname_list.extend(
                    cls.generate_validate_pathname_list(item.get('children'))
                )
            else:
                href = item.get('props').get('href')
                validate_pathname_list.append(href)

        return validate_pathname_list

    @classmethod
    def __genrate_item_menu(cls, router: Dict, modules: str):
        """
        生成Item类型菜单

        :param router: 路由信息
        :param modules: 组件路径

        :return: Item类型菜单
        """
        router['props']['modules'] = modules
        router['component'] = MenuConstant.ITEM

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
