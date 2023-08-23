from sqlalchemy import and_
from sqlalchemy.orm import Session
from module_admin.entity.do.menu_do import SysMenu
from module_admin.entity.do.user_do import SysUser, SysUserRole
from module_admin.entity.do.role_do import SysRole, SysRoleMenu
from module_admin.entity.vo.menu_vo import MenuModel, MenuResponse, CrudMenuResponse
from utils.time_format_util import list_format_datetime


class MenuDao:
    """
    菜单管理模块数据库操作层
    """

    @classmethod
    def get_menu_detail_by_id(cls, db: Session, menu_id: int):
        """
        根据菜单id获取岗位详细信息
        :param db: orm对象
        :param menu_id: 菜单id
        :return: 菜单信息对象
        """
        menu_info = db.query(SysMenu) \
            .filter(SysMenu.menu_id == menu_id) \
            .first()

        return menu_info

    @classmethod
    def get_menu_detail_by_info(cls, db: Session, menu: MenuModel):
        """
        根据菜单参数获取菜单信息
        :param db: orm对象
        :param menu: 菜单参数对象
        :return: 菜单信息对象
        """
        menu_info = db.query(SysMenu) \
            .filter(SysMenu.parent_id == menu.parent_id if menu.parent_id else True,
                    SysMenu.menu_name == menu.menu_name if menu.menu_name else True,
                    SysMenu.menu_type == menu.menu_type if menu.menu_type else True) \
            .first()

        return menu_info

    @classmethod
    def get_menu_info_for_edit_option(cls, db: Session, menu_info: MenuModel, user_id: int, role: list):
        """
        根据角色信息获取菜单编辑对应的在用菜单列表信息
        :param db: orm对象
        :param menu_info: 菜单对象
        :param user_id: 用户id
        :param role: 用户角色列表信息
        :return: 菜单列表信息
        """
        menu_result = []
        for item in role:
            if item.role_id == 1:
                menu_result = db.query(SysMenu) \
                    .filter(SysMenu.menu_id != menu_info.menu_id, SysMenu.parent_id != menu_info.menu_id,
                            SysMenu.status == 0) \
                    .all()
            else:
                menu_result = db.query(SysMenu).select_from(SysUser) \
                    .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
                    .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
                    .outerjoin(SysRole,
                               and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
                    .outerjoin(SysRoleMenu, SysRole.role_id == SysRoleMenu.role_id) \
                    .outerjoin(SysMenu, and_(SysRoleMenu.menu_id == SysMenu.menu_id,
                                             SysMenu.menu_id != menu_info.menu_id, SysMenu.parent_id != menu_info.menu_id,
                                             SysMenu.status == 0)) \
                    .order_by(SysMenu.order_num) \
                    .distinct().all()

        return list_format_datetime(menu_result)

    @classmethod
    def get_menu_list_for_tree(cls, db: Session, menu_info: MenuModel, user_id: int, role: list):
        """
        根据角色信息获取所有在用菜单列表信息
        :param db: orm对象
        :param menu_info: 菜单对象
        :param user_id: 用户id
        :param role: 用户角色列表信息
        :return: 菜单列表信息
        """
        menu_query_all = []
        for item in role:
            if item.role_id == 1:
                menu_query_all = db.query(SysMenu) \
                    .filter(SysMenu.status == 0,
                            SysMenu.menu_name.like(f'%{menu_info.menu_name}%') if menu_info.menu_name else True) \
                    .order_by(SysMenu.order_num) \
                    .distinct().all()
                break
            else:
                menu_query_all = db.query(SysMenu).select_from(SysUser) \
                    .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
                    .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
                    .outerjoin(SysRole,
                               and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
                    .outerjoin(SysRoleMenu, SysRole.role_id == SysRoleMenu.role_id) \
                    .outerjoin(SysMenu, and_(SysRoleMenu.menu_id == SysMenu.menu_id,
                                             SysMenu.status == 0,
                                             SysMenu.menu_name.like(
                                                 f'%{menu_info.menu_name}%') if menu_info.menu_name else True)) \
                    .order_by(SysMenu.order_num) \
                    .distinct().all()

        return list_format_datetime(menu_query_all)

    @classmethod
    def get_menu_list(cls, db: Session, page_object: MenuModel, user_id: int, role: list):
        """
        根据查询参数获取菜单列表信息
        :param db: orm对象
        :param page_object: 不分页查询参数对象
        :param user_id: 用户id
        :param role: 用户角色列表
        :return: 菜单列表信息对象
        """
        menu_query_all = []
        for item in role:
            if item.role_id == 1:
                menu_query_all = db.query(SysMenu) \
                    .filter(SysMenu.status == page_object.status if page_object.status else True,
                            SysMenu.menu_name.like(
                                f'%{page_object.menu_name}%') if page_object.menu_name else True) \
                    .order_by(SysMenu.order_num) \
                    .distinct().all()
                break
            else:
                menu_query_all = db.query(SysMenu).select_from(SysUser) \
                    .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
                    .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
                    .outerjoin(SysRole,
                               and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
                    .outerjoin(SysRoleMenu, SysRole.role_id == SysRoleMenu.role_id) \
                    .outerjoin(SysMenu, and_(SysRoleMenu.menu_id == SysMenu.menu_id,
                                             SysMenu.status == page_object.status if page_object.status else True,
                                             SysMenu.menu_name.like(
                                                 f'%{page_object.menu_name}%') if page_object.menu_name else True)) \
                    .order_by(SysMenu.order_num) \
                    .distinct().all()

        result = dict(
            rows=list_format_datetime(menu_query_all),
        )

        return MenuResponse(**result)

    @classmethod
    def add_menu_dao(cls, db: Session, menu: MenuModel):
        """
        新增菜单数据库操作
        :param db: orm对象
        :param menu: 菜单对象
        :return:
        """
        db_menu = SysMenu(**menu.dict())
        db.add(db_menu)
        db.flush()

        return db_menu

    @classmethod
    def edit_menu_dao(cls, db: Session, menu: dict):
        """
        编辑菜单数据库操作
        :param db: orm对象
        :param menu: 需要更新的菜单字典
        :return:
        """
        db.query(SysMenu) \
            .filter(SysMenu.menu_id == menu.get('menu_id')) \
            .update(menu)

    @classmethod
    def delete_menu_dao(cls, db: Session, menu: MenuModel):
        """
        删除菜单数据库操作
        :param db: orm对象
        :param menu: 菜单对象
        :return:
        """
        db.query(SysMenu) \
            .filter(SysMenu.menu_id == menu.menu_id) \
            .delete()
