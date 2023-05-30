from mapper.schema.user_schema import *
from mapper.crud.user_crud import *


def get_user_list_services(result_db: Session, page_object: UserPageObject):
    """
    获取用户列表信息service
    :param result_db: orm对象
    :param page_object: 分页查询参数对象
    :return: 用户列表信息对象
    """
    user_list_result = get_user_list(result_db, page_object)

    return user_list_result


def add_user_services(result_db: Session, page_object: AddUserModel):
    """
    新增用户信息service
    :param result_db: orm对象
    :param page_object: 新增用户对象
    :return: 新增用户校验结果
    """
    add_user = UserModel(**page_object.dict())
    add_user_result = add_user_crud(result_db, add_user)
    if add_user_result.is_success:
        user_id = get_user_by_name(result_db, page_object.user_name).user_id
        if page_object.role_id:
            role_id_list = page_object.role_id.split(',')
            for role in role_id_list:
                role_dict = dict(user_id=user_id, role_id=role)
                add_user_role_crud(result_db, UserRoleModel(**role_dict))
        if page_object.post_id:
            post_id_list = page_object.post_id.split(',')
            for post in post_id_list:
                post_dict = dict(user_id=user_id, post_id=post)
                add_user_post_crud(result_db, UserPostModel(**post_dict))

    return add_user_result


def edit_user_services(result_db: Session, page_object: AddUserModel):
    """
    编辑用户信息service
    :param result_db: orm对象
    :param page_object: 编辑用户对象
    :return: 编辑用户校验结果
    """
    edit_user = UserModel(**page_object.dict())
    edit_user_result = edit_user_crud(result_db, edit_user)
    if edit_user_result.is_success:
        user_id_dict = dict(user_id=page_object.user_id)
        delete_user_role_crud(result_db, UserRoleModel(**user_id_dict))
        delete_user_post_crud(result_db, UserPostModel(**user_id_dict))
        if page_object.role_id:
            role_id_list = page_object.role_id.split(',')
            for role in role_id_list:
                role_dict = dict(user_id=page_object.user_id, role_id=role)
                add_user_role_crud(result_db, UserRoleModel(**role_dict))
        if page_object.post_id:
            post_id_list = page_object.post_id.split(',')
            for post in post_id_list:
                post_dict = dict(user_id=page_object.user_id, post_id=post)
                add_user_post_crud(result_db, UserPostModel(**post_dict))

    return edit_user_result


def delete_user_services(result_db: Session, page_object: DeleteUserModel):
    """
    删除用户信息service
    :param result_db: orm对象
    :param page_object: 删除用户对象
    :return: 删除用户校验结果
    """
    if page_object.user_ids.split(','):
        user_id_list = page_object.user_ids.split(',')
        for user_id in user_id_list:
            user_id_dict = dict(user_id=user_id, update_by=page_object.update_by, update_time=page_object.update_time)
            delete_user_role_crud(result_db, UserRoleModel(**user_id_dict))
            delete_user_post_crud(result_db, UserPostModel(**user_id_dict))
            delete_user_crud(result_db, UserModel(**user_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入用户id为空')
    return CrudUserResponse(**result)


def detail_user_services(result_db: Session, user_id: int):
    """
    获取用户列表信息service
    :param result_db: orm对象
    :param user_id: 用户id
    :return: 用户id对应的信息
    """
    user = get_user_detail_by_id(result_db, user_id=user_id)

    return UserDetailModel(
        user=user.user_basic_info[0],
        dept=user.user_dept_info[0],
        role=user.user_role_info,
        post=user.user_post_info
    )
