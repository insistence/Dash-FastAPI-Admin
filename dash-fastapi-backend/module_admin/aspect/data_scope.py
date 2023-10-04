from fastapi import Depends
from module_admin.entity.vo.user_vo import CurrentUserInfoServiceResponse
from module_admin.service.login_service import get_current_user
from typing import Optional


class GetDataScope:
    """
    获取当前用户数据权限对应的查询sql语句
    """
    def __init__(self, query_alias: Optional[str] = '', db_alias: Optional[str] = 'db'):
        self.query_alias = query_alias
        self.db_alias = db_alias

    def __call__(self, current_user: CurrentUserInfoServiceResponse = Depends(get_current_user)):
        user_id = current_user.user.user_id
        dept_id = current_user.user.dept_id
        role_datascope_list = [dict(role_id=item.role_id, data_scope=int(item.data_scope)) for item in current_user.role]
        max_data_scope_dict = min(role_datascope_list, key=lambda x: x['data_scope'])
        max_role_id = max_data_scope_dict['role_id']
        max_data_scope = max_data_scope_dict['data_scope']
        if self.query_alias == '' or max_data_scope == 1 or user_id == 1:
            param_sql = '1 == 1'
        elif max_data_scope == 2:
            param_sql = f'{self.query_alias}.dept_id.in_({self.db_alias}.query(SysRoleDept.dept_id).filter(SysRoleDept.role_id == {max_role_id}))'
        elif max_data_scope == 3:
            param_sql = f'{self.query_alias}.dept_id == {dept_id}'
        elif max_data_scope == 4:
            param_sql = f'{self.query_alias}.dept_id.in_({self.db_alias}.query(SysDept.dept_id).filter(or_(SysDept.dept_id == {dept_id}, func.find_in_set({dept_id}, SysDept.ancestors))))'
        elif max_data_scope == 5:
            param_sql = f'{self.query_alias}.user_id == {user_id}'
        else:
            param_sql = '1 == 0'

        return param_sql
