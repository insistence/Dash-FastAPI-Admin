from mapper.schema.dept_schema import *
from mapper.crud.dept_crud import *


def get_dept_tree_services(result_db: Session, page_object: DeptPageObject):
    """
    获取部门树信息service
    :param result_db: orm对象
    :param page_object: 分页查询参数对象
    :return: 部门树信息对象
    """
    dept_list_result = get_dept_list_for_tree(result_db, page_object)
    dept_tree_result = get_dept_tree(0, DeptTree(dept_tree=dept_list_result))

    return dept_tree_result


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
                dept_list_data['value'] = permission.dept_id
                dept_list_data['children'] = children
            else:
                dept_list_data['title'] = permission.dept_name
                dept_list_data['key'] = str(permission.dept_id)
                dept_list_data['value'] = permission.dept_id
            dept_list.append(dept_list_data)

    return dept_list
