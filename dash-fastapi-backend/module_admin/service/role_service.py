from module_admin.entity.vo.role_vo import *
from module_admin.dao.role_dao import *
from utils.common_util import export_list2excel


class RoleService:
    """
    角色管理模块服务层
    """

    @classmethod
    def get_role_select_option_services(cls, result_db: Session):
        """
        获取角色列表不分页信息service
        :param result_db: orm对象
        :return: 角色列表不分页信息对象
        """
        role_list_result = get_role_select_option_dao(result_db)

        return role_list_result

    @classmethod
    def get_role_list_services(cls, result_db: Session, query_object: RoleQueryModel):
        """
        获取角色列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :return: 角色列表信息对象
        """
        role_list_result = get_role_list(result_db, query_object)

        return role_list_result

    @classmethod
    def add_role_services(cls, result_db: Session, page_object: AddRoleModel):
        """
        新增角色信息service
        :param result_db: orm对象
        :param page_object: 新增角色对象
        :return: 新增角色校验结果
        """
        add_role = RoleModel(**page_object.dict())
        add_role_result = add_role_dao(result_db, add_role)
        if add_role_result.is_success:
            role_id = get_role_by_name(result_db, page_object.role_name).role_id
            if page_object.menu_id:
                menu_id_list = page_object.menu_id.split(',')
                for menu in menu_id_list:
                    menu_dict = dict(role_id=role_id, menu_id=menu)
                    add_role_menu_dao(result_db, RoleMenuModel(**menu_dict))

        return add_role_result

    @classmethod
    def edit_role_services(cls, result_db: Session, page_object: AddRoleModel):
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
        edit_role_result = edit_role_dao(result_db, edit_role)
        if edit_role_result.is_success and page_object.type != 'status':
            role_id_dict = dict(role_id=page_object.role_id)
            delete_role_menu_dao(result_db, RoleMenuModel(**role_id_dict))
            if page_object.menu_id:
                menu_id_list = page_object.menu_id.split(',')
                for menu in menu_id_list:
                    menu_dict = dict(role_id=page_object.role_id, menu_id=menu)
                    add_role_menu_dao(result_db, RoleMenuModel(**menu_dict))

        return edit_role_result

    @classmethod
    def delete_role_services(cls, result_db: Session, page_object: DeleteRoleModel):
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
                delete_role_menu_dao(result_db, RoleMenuModel(**role_id_dict))
                delete_role_dao(result_db, RoleModel(**role_id_dict))
            result = dict(is_success=True, message='删除成功')
        else:
            result = dict(is_success=False, message='传入角色id为空')
        return CrudRoleResponse(**result)

    @classmethod
    def detail_role_services(cls, result_db: Session, role_id: int):
        """
        获取角色详细信息service
        :param result_db: orm对象
        :param role_id: 角色id
        :return: 角色id对应的信息
        """
        role = get_role_detail_by_id(result_db, role_id=role_id)

        return role

    @staticmethod
    def export_role_list_services(role_list: List):
        """
        导出角色列表信息service
        :param role_list: 角色信息列表
        :return: 角色列表信息对象
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            "role_id": "角色编号",
            "role_name": "角色名称",
            "role_key": "权限字符",
            "role_sort": "显示顺序",
            "status": "状态",
            "create_by": "创建者",
            "create_time": "创建时间",
            "update_by": "更新者",
            "update_time": "更新时间",
            "remark": "备注",
        }

        data = [RoleModel(**vars(row)).dict() for row in role_list]

        for item in data:
            if item.get('status') == '0':
                item['status'] = '正常'
            else:
                item['status'] = '停用'
        new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data]
        binary_data = export_list2excel(new_data)

        return binary_data
