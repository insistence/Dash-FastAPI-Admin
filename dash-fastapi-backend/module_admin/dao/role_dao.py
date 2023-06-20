from sqlalchemy import and_, desc
from sqlalchemy.orm import Session
from module_admin.entity.do.role_entity import SysRole, SysRoleMenu
from module_admin.entity.do.menu_entity import SysMenu
from module_admin.entity.vo.role_schema import RoleModel, RoleMenuModel, RolePageObject, RolePageObjectResponse, CrudRoleResponse, RoleDetailModel
from module_admin.utils.time_format_tool import list_format_datetime, object_format_datetime
from module_admin.utils.page_tool import get_page_info
from datetime import datetime, time


def get_role_by_name(db: Session, role_name: str):
    """
    根据角色名获取角色信息
    :param db: orm对象
    :param role_name: 角色名
    :return: 当前角色名的角色信息对象
    """
    query_role_info = db.query(SysRole) \
        .filter(SysRole.status == 0, SysRole.del_flag == 0, SysRole.role_name == role_name) \
        .order_by(desc(SysRole.create_time)).distinct().first()

    return query_role_info


def get_role_by_id(db: Session, role_id: int):
    role_info = db.query(SysRole) \
        .filter(SysRole.role_id == role_id,
                SysRole.status == 0,
                SysRole.del_flag == 0) \
        .first()

    return role_info


def get_role_detail_by_id(db: Session, role_id: int):
    """
    根据role_id获取角色详细信息
    :param db: orm对象
    :param role_id: 角色id
    :return: 当前role_id的角色信息对象
    """
    query_role_basic_info = db.query(SysRole) \
        .filter(SysRole.del_flag == 0, SysRole.role_id == role_id) \
        .distinct().first()
    query_role_menu_info = db.query(SysMenu).select_from(SysRole) \
        .filter(SysRole.del_flag == 0, SysRole.role_id == role_id) \
        .outerjoin(SysRoleMenu, SysRole.role_id == SysRoleMenu.role_id) \
        .outerjoin(SysMenu, and_(SysRoleMenu.menu_id == SysMenu.menu_id, SysMenu.status == 0)) \
        .distinct().all()
    results = dict(
        role=object_format_datetime(query_role_basic_info),
        menu=list_format_datetime(query_role_menu_info),
    )

    return RoleDetailModel(**results)


def get_role_select_option_crud(db: Session):
    role_info = db.query(SysRole) \
        .filter(SysRole.status == 0, SysRole.del_flag == 0) \
        .all()

    return role_info


def get_role_list(db: Session, page_object: RolePageObject):
    """
    根据查询参数获取角色列表信息
    :param db: orm对象
    :param page_object: 分页查询参数对象
    :return: 角色列表信息对象
    """
    count = db.query(SysRole) \
        .filter(SysRole.del_flag == 0,
                SysRole.role_name.like(f'%{page_object.role_name}%') if page_object.role_name else True,
                SysRole.role_key.like(f'%{page_object.role_key}%') if page_object.role_key else True,
                SysRole.status == page_object.status if page_object.status else True,
                SysRole.create_time.between(
                    datetime.combine(datetime.strptime(page_object.create_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(page_object.create_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                if page_object.create_time_start and page_object.create_time_end else True
                )\
        .order_by(SysRole.role_sort)\
        .distinct().count()
    offset_com = (page_object.page_num - 1) * page_object.page_size
    page_info = get_page_info(offset_com, page_object.page_num, page_object.page_size, count)
    role_list = db.query(SysRole) \
        .filter(SysRole.del_flag == 0,
                SysRole.role_name.like(f'%{page_object.role_name}%') if page_object.role_name else True,
                SysRole.role_key.like(f'%{page_object.role_key}%') if page_object.role_key else True,
                SysRole.status == page_object.status if page_object.status else True,
                SysRole.create_time.between(
                    datetime.combine(datetime.strptime(page_object.create_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(page_object.create_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                if page_object.create_time_start and page_object.create_time_end else True
                ) \
        .order_by(SysRole.role_sort) \
        .offset(page_info.offset) \
        .limit(page_object.page_size) \
        .distinct().all()

    result = dict(
        rows=list_format_datetime(role_list),
        page_num=page_info.page_num,
        page_size=page_info.page_size,
        total=page_info.total,
        has_next=page_info.has_next
    )

    return RolePageObjectResponse(**result)


def add_role_crud(db: Session, role: RoleModel):
    """
    新增角色数据库操作
    :param db: orm对象
    :param role: 角色对象
    :return: 新增校验结果
    """
    db_role = SysRole(**role.dict())
    db.add(db_role)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_role)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudRoleResponse(**result)


def edit_role_crud(db: Session, role: dict):
    """
    编辑角色数据库操作
    :param db: orm对象
    :param role: 需要更新的角色字典
    :return: 编辑校验结果
    """
    is_role_id = db.query(SysRole).filter(SysRole.role_id == role.get('role_id')).all()
    if not is_role_id:
        result = dict(is_success=False, message='角色不存在')
    else:
        db.query(SysRole) \
            .filter(SysRole.role_id == role.get('role_id')) \
            .update(role)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudRoleResponse(**result)


def delete_role_crud(db: Session, role: RoleModel):
    """
    删除角色数据库操作
    :param db: orm对象
    :param user: 角色对象
    :return:
    """
    db.query(SysRole) \
        .filter(SysRole.role_id == role.role_id) \
        .update({SysRole.del_flag: '2', SysRole.update_by: role.update_by, SysRole.update_time: role.update_time})
    db.commit()  # 提交保存到数据库中


def add_role_menu_crud(db: Session, role_menu: RoleMenuModel):
    """
    新增角色菜单关联信息数据库操作
    :param db: orm对象
    :param role_menu: 用户角色菜单关联对象
    :return:
    """
    db_role_menu = SysRoleMenu(**role_menu.dict())
    db.add(db_role_menu)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_role_menu)  # 刷新
    
    
def delete_role_menu_crud(db: Session, role_menu: RoleMenuModel):
    """
    删除角色菜单关联信息数据库操作
    :param db: orm对象
    :param role_menu: 角色菜单关联对象
    :return:
    """
    db.query(SysRoleMenu) \
        .filter(SysRoleMenu.role_id == role_menu.role_id) \
        .delete()
    db.commit()  # 提交保存到数据库中
