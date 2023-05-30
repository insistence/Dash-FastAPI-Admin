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
