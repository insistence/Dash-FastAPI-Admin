from utils.request import api_request


class RoleApi:
    """
    角色管理模块相关接口
    """

    @classmethod
    def list_role(cls, query: dict):
        """
        查询角色列表接口

        :param query: 查询角色参数
        :return:
        """
        return api_request(
            url='/system/role/list',
            method='get',
            params=query,
        )

    @classmethod
    def get_role(cls, role_id: str):
        """
        查询角色详情接口

        :param role_id: 角色id
        :return:
        """
        return api_request(
            url=f'/system/role/{role_id}',
            method='get',
        )

    @classmethod
    def add_role(cls, json: dict):
        """
        新增角色接口

        :param json: 新增角色参数
        :return:
        """
        return api_request(
            url='/system/role',
            method='post',
            json=json,
        )

    @classmethod
    def update_role(cls, json: dict):
        """
        修改角色接口

        :param json: 修改角色参数
        :return:
        """
        return api_request(
            url='/system/role',
            method='put',
            json=json,
        )

    @classmethod
    def data_scope(cls, json: dict):
        """
        角色数据权限接口

        :param json: 角色数据权限参数
        :return:
        """
        return api_request(
            url='/system/role/dataScope',
            method='put',
            json=json,
        )

    @classmethod
    def change_user_status(cls, role_id: str, status: str):
        """
        角色状态修改接口

        :param role_id: 角色id
        :param status: 角色状态
        :return:
        """
        return api_request(
            url='/system/role/changeStatus',
            method='put',
            json=dict(role_id=role_id, status=status),
        )

    @classmethod
    def del_role(cls, role_id: str):
        """
        删除角色接口

        :param role_id: 角色id
        :return:
        """
        return api_request(
            url=f'/system/role/{role_id}',
            method='delete',
        )

    @classmethod
    def export_role(cls, data: dict):
        """
        导出角色接口

        :param data: 导出角色参数
        :return:
        """
        return api_request(
            url='/system/role/export',
            method='post',
            data=data,
            stream=True,
        )

    @classmethod
    def allocated_user_list(cls, query: dict):
        """
        查询角色已授权用户列表接口

        :param query: 查询角色已授权用户列表参数
        :return:
        """
        return api_request(
            url='/system/role/authUser/allocatedList',
            method='get',
            params=query,
        )

    @classmethod
    def unallocated_user_list(cls, query: dict):
        """
        查询角色未授权用户列表接口

        :param query: 查询角色未授权用户列表参数
        :return:
        """
        return api_request(
            url='/system/role/authUser/unallocatedList',
            method='get',
            params=query,
        )

    @classmethod
    def auth_user_cancel(cls, json: dict):
        """
        取消用户授权角色接口

        :param json: 用户授权角色参数
        :return:
        """
        return api_request(
            url='/system/role/authUser/cancel',
            method='put',
            json=json,
        )

    @classmethod
    def auth_user_cancel_all(cls, json: dict):
        """
        批量取消用户授权角色接口

        :param json: 用户授权角色参数
        :return:
        """
        return api_request(
            url='/system/role/authUser/cancelAll',
            method='put',
            json=json,
        )

    @classmethod
    def auth_user_select_all(cls, json: dict):
        """
        授权用户选择接口

        :param json: 用户选择角色参数
        :return:
        """
        return api_request(
            url='/system/role/authUser/selectAll',
            method='put',
            json=json,
        )

    @classmethod
    def dept_tree_select(cls, role_id: str):
        """
        根据角色id查询部门树结构接口

        :param role_id: 角色id
        :return:
        """
        return api_request(
            url=f'/system/role/deptTree/{role_id}',
            method='get',
        )
