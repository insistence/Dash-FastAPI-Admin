from sqlalchemy.orm import Session
from module_admin.entity.do.menu_do import SysMenu
from module_admin.entity.vo.menu_vo import MenuModel, MenuResponse, CrudMenuResponse
from utils.time_format_util import list_format_datetime


def get_menu_detail_by_id(db: Session, menu_id: int):
    menu_info = db.query(SysMenu) \
        .filter(SysMenu.menu_id == menu_id) \
        .first()

    return menu_info


def get_menu_info_for_edit_option(db: Session, menu_info: MenuModel):
    menu_result = db.query(SysMenu) \
        .filter(SysMenu.menu_id != menu_info.menu_id, SysMenu.parent_id != menu_info.menu_id,
                SysMenu.status == 0) \
        .all()

    return list_format_datetime(menu_result)


def get_menu_list_for_tree(db: Session, menu_info: MenuModel):
    menu_query_all = db.query(SysMenu) \
        .filter(SysMenu.status == 0,
                SysMenu.menu_name.like(f'%{menu_info.menu_name}%') if menu_info.menu_name else True) \
        .order_by(SysMenu.order_num) \
        .distinct().all()

    return list_format_datetime(menu_query_all)


def get_menu_list(db: Session, page_object: MenuModel):
    """
    根据查询参数获取菜单列表信息
    :param db: orm对象
    :param page_object: 不分页查询参数对象
    :return: 菜单列表信息对象
    """
    if page_object.menu_name or page_object.status:
        menu_query_all = db.query(SysMenu) \
            .filter(SysMenu.status == page_object.status if page_object.status else True,
                    SysMenu.menu_name.like(f'%{page_object.menu_name}%') if page_object.menu_name else True) \
            .order_by(SysMenu.order_num)\
            .distinct().all()
    else:
        menu_query_all = db.query(SysMenu) \
            .order_by(SysMenu.order_num) \
            .distinct().all()

    result = dict(
        rows=list_format_datetime(menu_query_all),
    )

    return MenuResponse(**result)


def add_menu_dao(db: Session, menu: MenuModel):
    """
    新增菜单数据库操作
    :param db: orm对象
    :param menu: 菜单对象
    :return: 新增校验结果
    """
    db_menu = SysMenu(**menu.dict())
    db.add(db_menu)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_menu)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudMenuResponse(**result)


def edit_menu_dao(db: Session, menu: dict):
    """
    编辑菜单数据库操作
    :param db: orm对象
    :param menu: 需要更新的菜单字典
    :return: 编辑校验结果
    """
    is_menu_id = db.query(SysMenu).filter(SysMenu.menu_id == menu.get('menu_id')).all()
    if not is_menu_id:
        result = dict(is_success=False, message='菜单不存在')
    else:
        db.query(SysMenu) \
            .filter(SysMenu.menu_id == menu.get('menu_id')) \
            .update(menu)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudMenuResponse(**result)


def delete_menu_dao(db: Session, menu: MenuModel):
    """
    删除菜单数据库操作
    :param db: orm对象
    :param menu: 菜单对象
    :return:
    """
    db.query(SysMenu) \
        .filter(SysMenu.menu_id == menu.menu_id) \
        .delete()
    db.commit()  # 提交保存到数据库中
