from mapper.schema.post_schema import *
from mapper.crud.post_crud import *


def get_post_select_option_services(result_db: Session):
    """
    获取岗位列表不分页信息service
    :param result_db: orm对象
    :return: 岗位列表不分页信息对象
    """
    post_list_result = get_post_select_option_crud(result_db)

    return post_list_result
