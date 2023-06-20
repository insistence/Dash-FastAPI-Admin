from module_admin.entity.vo.dept_schema import *
from module_admin.mapper.dept_crud import *


def get_dept_tree_services(result_db: Session, page_object: DeptModel):
    """
    获取部门树信息service
    :param result_db: orm对象
    :param page_object: 查询参数对象
    :return: 部门树信息对象
    """
    dept_list_result = get_dept_list_for_tree(result_db, page_object)
    dept_tree_result = get_dept_tree(0, DeptTree(dept_tree=dept_list_result))

    return dept_tree_result


def get_dept_tree_for_edit_option_services(result_db: Session, page_object: DeptModel):
    """
    获取部门编辑部门树信息service
    :param result_db: orm对象
    :param page_object: 查询参数对象
    :return: 部门树信息对象
    """
    dept_list_result = get_dept_info_for_edit_option(result_db, page_object)
    dept_tree_result = get_dept_tree(0, DeptTree(dept_tree=dept_list_result))

    return dept_tree_result


def get_dept_list_services(result_db: Session, page_object: DeptModel):
    """
    获取部门列表信息service
    :param result_db: orm对象
    :param page_object: 分页查询参数对象
    :return: 部门列表信息对象
    """
    dept_list_result = get_dept_list(result_db, page_object)

    return dept_list_result


def add_dept_services(result_db: Session, page_object: DeptModel):
    """
    新增部门信息service
    :param result_db: orm对象
    :param page_object: 新增部门对象
    :return: 新增部门校验结果
    """
    parent_info = get_dept_by_id(result_db, page_object.parent_id)
    if parent_info:
        page_object.ancestors = f'{parent_info.ancestors},{page_object.parent_id}'
    else:
        page_object.ancestors = '0'
    add_dept_result = add_dept_crud(result_db, page_object)

    return add_dept_result


def edit_dept_services(result_db: Session, page_object: DeptModel):
    """
    编辑部门信息service
    :param result_db: orm对象
    :param page_object: 编辑部门对象
    :return: 编辑部门校验结果
    """
    parent_info = get_dept_by_id(result_db, page_object.parent_id)
    if parent_info:
        page_object.ancestors = f'{parent_info.ancestors},{page_object.parent_id}'
    else:
        page_object.ancestors = '0'
    edit_dept = page_object.dict(exclude_unset=True)
    edit_dept_result = edit_dept_crud(result_db, edit_dept)
    update_children_info(result_db, DeptModel(dept_id=page_object.dept_id,
                                              ancestors=page_object.ancestors,
                                              update_by=page_object.update_by,
                                              update_time=page_object.update_time
                                              )
                         )

    return edit_dept_result


def delete_dept_services(result_db: Session, page_object: DeleteDeptModel):
    """
    删除部门信息service
    :param result_db: orm对象
    :param page_object: 删除部门对象
    :return: 删除部门校验结果
    """
    if page_object.dept_ids.split(','):
        dept_id_list = page_object.dept_ids.split(',')
        ancestors = get_dept_all_ancestors(result_db)
        for dept_id in dept_id_list:
            for ancestor in ancestors:
                if dept_id in ancestor[0]:
                    result = dict(is_success=False, message='该部门下有子部门，不允许删除')

                    return CrudDeptResponse(**result)

            dept_id_dict = dict(dept_id=dept_id)
            delete_dept_crud(result_db, DeptModel(**dept_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入用户id为空')
    return CrudDeptResponse(**result)


def detail_dept_services(result_db: Session, dept_id: int):
    """
    获取部门详细信息service
    :param result_db: orm对象
    :param dept_id: 部门id
    :return: 部门id对应的信息
    """
    post = get_dept_detail_by_id(result_db, dept_id=dept_id)

    return post


def get_dept_tree(pid: int, permission_list: DeptTree):
    """
    工具方法：根据部门信息生成树形嵌套数据
    :param pid: 部门id
    :param permission_list: 部门列表信息
    :return: 部门树形嵌套数据
    """
    dept_list = []
    for permission in permission_list.dept_tree:
        if permission.parent_id == pid:
            children = get_dept_tree(permission.dept_id, permission_list)
            dept_list_data = {}
            if children:
                dept_list_data['title'] = permission.dept_name
                dept_list_data['key'] = str(permission.dept_id)
                dept_list_data['value'] = str(permission.dept_id)
                dept_list_data['children'] = children
            else:
                dept_list_data['title'] = permission.dept_name
                dept_list_data['key'] = str(permission.dept_id)
                dept_list_data['value'] = str(permission.dept_id)
            dept_list.append(dept_list_data)

    return dept_list


def update_children_info(result_db, page_object):
    """
    工具方法：递归更新子部门信息
    :param result_db: orm对象
    :param page_object: 编辑部门对象
    :return:
    """
    children_info = get_children_dept(result_db, page_object.dept_id)
    if children_info:
        for child in children_info:
            child.ancestors = f'{page_object.ancestors},{page_object.dept_id}'
            edit_dept_crud(result_db,
                           dict(dept_id=child.dept_id,
                                ancestors=child.ancestors,
                                update_by=page_object.update_by,
                                update_time=page_object.update_time
                                )
                           )
            update_children_info(result_db, DeptModel(dept_id=child.dept_id,
                                                      ancestors=child.ancestors,
                                                      update_by=page_object.update_by,
                                                      update_time=page_object.update_time
                                                      ))
