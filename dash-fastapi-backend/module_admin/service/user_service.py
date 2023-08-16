from module_admin.entity.vo.user_vo import *
from module_admin.dao.user_dao import *
from module_admin.service.login_service import verify_password
from utils.common_util import export_list2excel


def get_user_list_services(result_db: Session, query_object: UserQueryModel):
    """
    获取用户列表信息service
    :param result_db: orm对象
    :param query_object: 查询参数对象
    :return: 用户列表信息对象
    """
    user_list_result = get_user_list(result_db, query_object)

    return user_list_result


def add_user_services(result_db: Session, page_object: AddUserModel):
    """
    新增用户信息service
    :param result_db: orm对象
    :param page_object: 新增用户对象
    :return: 新增用户校验结果
    """
    add_user = UserModel(**page_object.dict())
    add_user_result = add_user_dao(result_db, add_user)
    if add_user_result.is_success:
        user_id = get_user_by_name(result_db, page_object.user_name).user_id
        if page_object.role_id:
            role_id_list = page_object.role_id.split(',')
            for role in role_id_list:
                role_dict = dict(user_id=user_id, role_id=role)
                add_user_role_dao(result_db, UserRoleModel(**role_dict))
        if page_object.post_id:
            post_id_list = page_object.post_id.split(',')
            for post in post_id_list:
                post_dict = dict(user_id=user_id, post_id=post)
                add_user_post_dao(result_db, UserPostModel(**post_dict))

    return add_user_result


def edit_user_services(result_db: Session, page_object: AddUserModel):
    """
    编辑用户信息service
    :param result_db: orm对象
    :param page_object: 编辑用户对象
    :return: 编辑用户校验结果
    """
    edit_user = page_object.dict(exclude_unset=True)
    if page_object.type != 'status' and page_object.type != 'avatar':
        del edit_user['role_id']
        del edit_user['post_id']
    if page_object.type == 'status' or page_object.type == 'avatar':
        del edit_user['type']
    edit_user_result = edit_user_dao(result_db, edit_user)
    if edit_user_result.is_success and page_object.type != 'status' and page_object.type != 'avatar':
        user_id_dict = dict(user_id=page_object.user_id)
        delete_user_role_dao(result_db, UserRoleModel(**user_id_dict))
        delete_user_post_dao(result_db, UserPostModel(**user_id_dict))
        if page_object.role_id:
            role_id_list = page_object.role_id.split(',')
            for role in role_id_list:
                role_dict = dict(user_id=page_object.user_id, role_id=role)
                add_user_role_dao(result_db, UserRoleModel(**role_dict))
        if page_object.post_id:
            post_id_list = page_object.post_id.split(',')
            for post in post_id_list:
                post_dict = dict(user_id=page_object.user_id, post_id=post)
                add_user_post_dao(result_db, UserPostModel(**post_dict))

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
            delete_user_role_dao(result_db, UserRoleModel(**user_id_dict))
            delete_user_post_dao(result_db, UserPostModel(**user_id_dict))
            delete_user_dao(result_db, UserModel(**user_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入用户id为空')
    return CrudUserResponse(**result)


def detail_user_services(result_db: Session, user_id: int):
    """
    获取用户详细信息service
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


def reset_user_services(result_db: Session, page_object: ResetUserModel):
    """
    重置用户密码service
    :param result_db: orm对象
    :param page_object: 重置用户对象
    :return: 重置用户校验结果
    """
    user = get_user_detail_by_id(result_db, user_id=page_object.user_id).user_basic_info[0]
    if page_object.old_password:
        if not verify_password(page_object.old_password, user.password):
            result = CrudUserResponse(**dict(is_success=False, message='旧密码不正确'))
        else:
            reset_user = page_object.dict(exclude_unset=True)
            del reset_user['old_password']
            result = edit_user_dao(result_db, reset_user)
    else:
        reset_user = page_object.dict(exclude_unset=True)
        result = edit_user_dao(result_db, reset_user)

    return result


def export_user_list_services(user_list: List):
    """
    导出用户信息service
    :param user_list: 用户信息列表
    :return: 用户信息对应excel的二进制数据
    """
    # 创建一个映射字典，将英文键映射到中文键
    mapping_dict = {
        "user_id": "用户编号",
        "user_name": "用户名称",
        "nick_name": "用户昵称",
        "dept_name": "部门",
        "email": "邮箱地址",
        "phonenumber": "手机号码",
        "sex": "性别",
        "status": "状态",
        "create_by": "创建者",
        "create_time": "创建时间",
        "update_by": "更新者",
        "update_time": "更新时间",
        "remark": "备注",
    }

    data = user_list

    for item in data:
        if item.get('status') == '0':
            item['status'] = '正常'
        else:
            item['status'] = '停用'
        if item.get('sex') == '0':
            item['sex'] = '男'
        elif item.get('sex') == '1':
            item['sex'] = '女'
        else:
            item['sex'] = '未知'
    new_data = [{mapping_dict.get(key): value for key, value in item.items() if mapping_dict.get(key)} for item in data]
    binary_data = export_list2excel(new_data)

    return binary_data
