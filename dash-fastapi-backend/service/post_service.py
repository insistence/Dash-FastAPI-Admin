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


def get_post_list_services(result_db: Session, page_object: PostPageObject):
    """
    获取岗位列表信息service
    :param result_db: orm对象
    :param page_object: 分页查询参数对象
    :return: 岗位列表信息对象
    """
    post_list_result = get_post_list(result_db, page_object)

    return post_list_result


def add_post_services(result_db: Session, page_object: PostModel):
    """
    新增岗位信息service
    :param result_db: orm对象
    :param page_object: 新增岗位对象
    :return: 新增岗位校验结果
    """
    add_post_result = add_post_crud(result_db, page_object)

    return add_post_result


def edit_post_services(result_db: Session, page_object: PostModel):
    """
    编辑岗位信息service
    :param result_db: orm对象
    :param page_object: 编辑岗位对象
    :return: 编辑岗位校验结果
    """
    edit_post_result = edit_post_crud(result_db, page_object)

    return edit_post_result


def delete_post_services(result_db: Session, page_object: DeletePostModel):
    """
    删除岗位信息service
    :param result_db: orm对象
    :param page_object: 删除岗位对象
    :return: 删除岗位校验结果
    """
    if page_object.post_ids.split(','):
        post_id_list = page_object.post_ids.split(',')
        for post_id in post_id_list:
            post_id_dict = dict(post_id=post_id)
            delete_post_crud(result_db, PostModel(**post_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入用户id为空')
    return CrudPostResponse(**result)


def detail_post_services(result_db: Session, post_id: int):
    """
    获取岗位详细信息service
    :param result_db: orm对象
    :param post_id: 岗位id
    :return: 岗位id对应的信息
    """
    post = get_post_detail_by_id(result_db, post_id=post_id)

    return post
