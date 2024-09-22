from config.enums import ApiMethod
from utils.request import api_request


class MenuApi:
    """
    菜单管理模块相关接口
    """

    @classmethod
    def list_menu(cls, query: dict):
        """
        查询菜单列表接口

        :param query: 查询菜单参数
        :return:
        """
        return api_request(
            url='/system/menu/list',
            method=ApiMethod.GET,
            params=query,
        )

    @classmethod
    def get_menu(cls, menu_id: int):
        """
        查询菜单详情接口

        :param menu_id: 菜单id
        :return:
        """
        return api_request(
            url=f'/system/menu/{menu_id}',
            method=ApiMethod.GET,
        )

    @classmethod
    def treeselect(cls):
        """
        查询菜单下拉树结构接口

        :return:
        """
        return api_request(
            url='/system/menu/treeselect',
            method=ApiMethod.GET,
        )

    @classmethod
    def role_menu_treeselect(cls, role_id: int):
        """
        根据角色id查询菜单下拉树结构接口

        :param role_id: 角色id
        :return:
        """
        return api_request(
            url=f'/system/menu/roleMenuTreeselect/{role_id}',
            method=ApiMethod.GET,
        )

    @classmethod
    def add_menu(cls, json: dict):
        """
        新增菜单接口

        :param json: 新增菜单参数
        :return:
        """
        return api_request(
            url='/system/menu',
            method=ApiMethod.POST,
            json=json,
        )

    @classmethod
    def update_menu(cls, json: dict):
        """
        修改菜单接口

        :param json: 修改菜单参数
        :return:
        """
        return api_request(
            url='/system/menu',
            method=ApiMethod.PUT,
            json=json,
        )

    @classmethod
    def del_menu(cls, menu_id: str):
        """
        删除菜单接口

        :param menu_id: 菜单id
        :return:
        """
        return api_request(
            url=f'/system/menu/{menu_id}',
            method=ApiMethod.DELETE,
        )
