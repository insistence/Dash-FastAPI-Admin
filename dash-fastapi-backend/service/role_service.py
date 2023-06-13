from mapper.schema.role_schema import *
from mapper.crud.role_crud import *


def get_role_select_option_services(result_db: Session):
    """
    获取角色列表不分页信息service
    :param result_db: orm对象
    :return: 角色列表不分页信息对象
    """
    role_list_result = get_role_select_option_crud(result_db)

    return role_list_result


def get_role_list_services(result_db: Session, page_object: RolePageObject):
    """
    获取角色列表信息service
    :param result_db: orm对象
    :param page_object: 分页查询参数对象
    :return: 角色列表信息对象
    """
    role_list_result = get_role_list(result_db, page_object)

    return role_list_result


def add_role_services(result_db: Session, page_object: AddRoleModel):
    """
    新增角色信息service
    :param result_db: orm对象
    :param page_object: 新增角色对象
    :return: 新增角色校验结果
    """
    add_role = RoleModel(**page_object.dict())
    add_role_result = add_role_crud(result_db, add_role)
    if add_role_result.is_success:
        role_id = get_role_by_name(result_db, page_object.role_name).role_id
        if page_object.menu_id:
            menu_id_list = page_object.menu_id.split(',')
            for menu in menu_id_list:
                menu_dict = dict(role_id=role_id, menu_id=menu)
                add_role_menu_crud(result_db, RoleMenuModel(**menu_dict))

    return add_role_result


def edit_role_services(result_db: Session, page_object: AddRoleModel):
    """
    编辑角色信息service
    :param result_db: orm对象
    :param page_object: 编辑角色对象
    :return: 编辑角色校验结果
    """
    edit_role = page_object.dict(exclude_unset=True)
    if page_object.type != 'status':
        del edit_role['menu_id']
    if page_object.type == 'status':
        del edit_role['type']
    edit_role_result = edit_role_crud(result_db, edit_role)
    if edit_role_result.is_success and page_object.type != 'status':
        role_id_dict = dict(role_id=page_object.role_id)
        delete_role_menu_crud(result_db, RoleMenuModel(**role_id_dict))
        if page_object.menu_id:
            menu_id_list = page_object.menu_id.split(',')
            for menu in menu_id_list:
                menu_dict = dict(role_id=page_object.role_id, menu_id=menu)
                add_role_menu_crud(result_db, RoleMenuModel(**menu_dict))

    return edit_role_result


def delete_role_services(result_db: Session, page_object: DeleteRoleModel):
    """
    删除角色信息service
    :param result_db: orm对象
    :param page_object: 删除角色对象
    :return: 删除角色校验结果
    """
    if page_object.role_ids.split(','):
        role_id_list = page_object.role_ids.split(',')
        for role_id in role_id_list:
            role_id_dict = dict(role_id=role_id, update_by=page_object.update_by, update_time=page_object.update_time)
            delete_role_menu_crud(result_db, RoleMenuModel(**role_id_dict))
            delete_role_crud(result_db, RoleModel(**role_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入角色id为空')
    return CrudRoleResponse(**result)


def detail_role_services(result_db: Session, role_id: int):
    """
    获取角色详细信息service
    :param result_db: orm对象
    :param role_id: 角色id
    :return: 角色id对应的信息
    """
    role = get_role_detail_by_id(result_db, role_id=role_id)

    return role
