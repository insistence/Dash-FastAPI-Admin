from module_admin.entity.vo.dept_vo import *
from module_admin.dao.dept_dao import *


class DeptService:
    """
    部门管理模块服务层
    """

    @classmethod
    def get_dept_tree_services(cls, result_db: Session, page_object: DeptModel):
        """
        获取部门树信息service
        :param result_db: orm对象
        :param page_object: 查询参数对象
        :return: 部门树信息对象
        """
        dept_list_result = DeptDao.get_dept_list_for_tree(result_db, page_object)
        dept_tree_result = cls.get_dept_tree(0, DeptTree(dept_tree=dept_list_result))

        return dept_tree_result

    @classmethod
    def get_dept_tree_for_edit_option_services(cls, result_db: Session, page_object: DeptModel):
        """
        获取部门编辑部门树信息service
        :param result_db: orm对象
        :param page_object: 查询参数对象
        :return: 部门树信息对象
        """
        dept_list_result = DeptDao.get_dept_info_for_edit_option(result_db, page_object)
        dept_tree_result = cls.get_dept_tree(0, DeptTree(dept_tree=dept_list_result))

        return dept_tree_result

    @classmethod
    def get_dept_list_services(cls, result_db: Session, page_object: DeptModel):
        """
        获取部门列表信息service
        :param result_db: orm对象
        :param page_object: 分页查询参数对象
        :return: 部门列表信息对象
        """
        dept_list_result = DeptDao.get_dept_list(result_db, page_object)

        return dept_list_result

    @classmethod
    def add_dept_services(cls, result_db: Session, page_object: DeptModel):
        """
        新增部门信息service
        :param result_db: orm对象
        :param page_object: 新增部门对象
        :return: 新增部门校验结果
        """
        parent_info = DeptDao.get_dept_by_id(result_db, page_object.parent_id)
        if parent_info:
            page_object.ancestors = f'{parent_info.ancestors},{page_object.parent_id}'
        else:
            page_object.ancestors = '0'
        dept = DeptDao.get_dept_detail_by_info(result_db, DeptModel(**dict(parent_id=page_object.parent_id, dept_name=page_object.dept_name)))
        if dept:
            result = dict(is_success=False, message='同一部门下不允许存在同名的部门')
        else:
            try:
                DeptDao.add_dept_dao(result_db, page_object)
                result_db.commit()
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))

        return CrudDeptResponse(**result)

    @classmethod
    def edit_dept_services(cls, result_db: Session, page_object: DeptModel):
        """
        编辑部门信息service
        :param result_db: orm对象
        :param page_object: 编辑部门对象
        :return: 编辑部门校验结果
        """
        parent_info = DeptDao.get_dept_by_id(result_db, page_object.parent_id)
        if parent_info:
            page_object.ancestors = f'{parent_info.ancestors},{page_object.parent_id}'
        else:
            page_object.ancestors = '0'
        edit_dept = page_object.dict(exclude_unset=True)
        dept_info = cls.detail_dept_services(result_db, edit_dept.get('dept_id'))
        if dept_info:
            if dept_info.parent_id != page_object.parent_id or dept_info.dept_name != page_object.dept_name:
                dept = DeptDao.get_dept_detail_by_info(result_db, DeptModel(
                    **dict(parent_id=page_object.parent_id, dept_name=page_object.dept_name)))
                if dept:
                    result = dict(is_success=False, message='同一部门下不允许存在同名的部门')
                    return CrudDeptResponse(**result)
            try:
                DeptDao.edit_dept_dao(result_db, edit_dept)
                cls.update_children_info(result_db, DeptModel(dept_id=page_object.dept_id,
                                                              ancestors=page_object.ancestors,
                                                              update_by=page_object.update_by,
                                                              update_time=page_object.update_time
                                                              )
                                         )
                result_db.commit()
                result = dict(is_success=True, message='更新成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='部门不存在')

        return CrudDeptResponse(**result)

    @classmethod
    def delete_dept_services(cls, result_db: Session, page_object: DeleteDeptModel):
        """
        删除部门信息service
        :param result_db: orm对象
        :param page_object: 删除部门对象
        :return: 删除部门校验结果
        """
        if page_object.dept_ids.split(','):
            dept_id_list = page_object.dept_ids.split(',')
            ancestors = DeptDao.get_dept_all_ancestors(result_db)
            try:
                for dept_id in dept_id_list:
                    for ancestor in ancestors:
                        if dept_id in ancestor[0]:
                            result = dict(is_success=False, message='该部门下有子部门，不允许删除')

                            return CrudDeptResponse(**result)

                    dept_id_dict = dict(dept_id=dept_id)
                    DeptDao.delete_dept_dao(result_db, DeptModel(**dept_id_dict))
                result_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='传入部门id为空')
        return CrudDeptResponse(**result)

    @classmethod
    def detail_dept_services(cls, result_db: Session, dept_id: int):
        """
        获取部门详细信息service
        :param result_db: orm对象
        :param dept_id: 部门id
        :return: 部门id对应的信息
        """
        dept = DeptDao.get_dept_detail_by_id(result_db, dept_id=dept_id)

        return dept

    @classmethod
    def get_dept_tree(cls, pid: int, permission_list: DeptTree):
        """
        工具方法：根据部门信息生成树形嵌套数据
        :param pid: 部门id
        :param permission_list: 部门列表信息
        :return: 部门树形嵌套数据
        """
        dept_list = []
        for permission in permission_list.dept_tree:
            if permission.parent_id == pid:
                children = cls.get_dept_tree(permission.dept_id, permission_list)
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

    @classmethod
    def update_children_info(cls, result_db, page_object):
        """
        工具方法：递归更新子部门信息
        :param result_db: orm对象
        :param page_object: 编辑部门对象
        :return:
        """
        children_info = DeptDao.get_children_dept(result_db, page_object.dept_id)
        if children_info:
            for child in children_info:
                child.ancestors = f'{page_object.ancestors},{page_object.dept_id}'
                DeptDao.edit_dept_dao(result_db,
                                      dict(dept_id=child.dept_id,
                                           ancestors=child.ancestors,
                                           update_by=page_object.update_by,
                                           update_time=page_object.update_time
                                           )
                                      )
                cls.update_children_info(result_db, DeptModel(dept_id=child.dept_id,
                                                              ancestors=child.ancestors,
                                                              update_by=page_object.update_by,
                                                              update_time=page_object.update_time
                                                              ))
