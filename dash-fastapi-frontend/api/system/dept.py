from utils.request import api_request


class DeptApi:
    """
    部门管理模块相关接口
    """

    @classmethod
    def list_dept(cls, query: dict):
        """
        查询部门列表接口

        :param query: 查询部门参数
        :return:
        """
        return api_request(
            url='/system/dept/list',
            method='get',
            params=query,
        )

    @classmethod
    def list_dept_exclude_child(cls, dept_id: str):
        """
        查询部门列表（排除节点）接口

        :param query: 部门id
        :return:
        """
        return api_request(
            url=f'/system/dept/listexclude/{dept_id}',
            method='get',
        )

    @classmethod
    def get_dept(cls, dept_id: str):
        """
        查询部门详情接口

        :param dept_id: 部门id
        :return:
        """
        return api_request(
            url=f'/system/dept/{dept_id}',
            method='get',
        )

    @classmethod
    def add_dept(cls, json: dict):
        """
        新增部门接口

        :param json: 新增部门参数
        :return:
        """
        return api_request(
            url='/system/dept',
            method='post',
            json=json,
        )

    @classmethod
    def update_dept(cls, json: dict):
        """
        修改部门接口

        :param json: 修改部门参数
        :return:
        """
        return api_request(
            url='/system/dept',
            method='put',
            json=json,
        )

    @classmethod
    def del_dept(cls, dept_id: str):
        """
        删除部门接口

        :param dept_id: 部门id
        :return:
        """
        return api_request(
            url=f'/system/dept/{dept_id}',
            method='delete',
        )
