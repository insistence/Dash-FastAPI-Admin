from module_admin.entity.vo.user_vo import *
from module_admin.dao.user_dao import *
from module_admin.service.login_service import verify_password
from utils.common_util import export_list2excel


class UserService:
    """
    用户管理模块服务层
    """

    @classmethod
    def get_user_list_services(cls, result_db: Session, query_object: UserQueryModel):
        """
        获取用户列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :return: 用户列表信息对象
        """
        user_list_result = UserDao.get_user_list(result_db, query_object)

        return user_list_result

    @classmethod
    def add_user_services(cls, result_db: Session, page_object: AddUserModel):
        """
        新增用户信息service
        :param result_db: orm对象
        :param page_object: 新增用户对象
        :return: 新增用户校验结果
        """
        add_user = UserModel(**page_object.dict())
        user = UserDao.get_user_by_info(result_db, UserModel(**dict(user_name=page_object.user_name)))
        if user:
            result = dict(is_success=False, message='用户名已存在')
        else:
            try:
                add_result = UserDao.add_user_dao(result_db, add_user)
                user_id = add_result.user_id
                if page_object.role_id:
                    role_id_list = page_object.role_id.split(',')
                    for role in role_id_list:
                        role_dict = dict(user_id=user_id, role_id=role)
                        UserDao.add_user_role_dao(result_db, UserRoleModel(**role_dict))
                if page_object.post_id:
                    post_id_list = page_object.post_id.split(',')
                    for post in post_id_list:
                        post_dict = dict(user_id=user_id, post_id=post)
                        UserDao.add_user_post_dao(result_db, UserPostModel(**post_dict))
                result_db.commit()
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))

        return CrudUserResponse(**result)

    @classmethod
    def edit_user_services(cls, result_db: Session, page_object: AddUserModel):
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
        user_info = cls.detail_user_services(result_db, edit_user.get('user_id'))
        if user_info:
            if page_object.type != 'status' and page_object.type != 'avatar' and user_info.user.user_name != page_object.user_name:
                user = UserDao.get_user_by_info(result_db, UserModel(**dict(user_name=page_object.user_name)))
                if user:
                    result = dict(is_success=False, message='用户名已存在')
                    return CrudUserResponse(**result)
            try:
                UserDao.edit_user_dao(result_db, edit_user)
                if page_object.type != 'status' and page_object.type != 'avatar':
                    user_id_dict = dict(user_id=page_object.user_id)
                    UserDao.delete_user_role_dao(result_db, UserRoleModel(**user_id_dict))
                    UserDao.delete_user_post_dao(result_db, UserPostModel(**user_id_dict))
                    if page_object.role_id:
                        role_id_list = page_object.role_id.split(',')
                        for role in role_id_list:
                            role_dict = dict(user_id=page_object.user_id, role_id=role)
                            UserDao.add_user_role_dao(result_db, UserRoleModel(**role_dict))
                    if page_object.post_id:
                        post_id_list = page_object.post_id.split(',')
                        for post in post_id_list:
                            post_dict = dict(user_id=page_object.user_id, post_id=post)
                            UserDao.add_user_post_dao(result_db, UserPostModel(**post_dict))
                result_db.commit()
                result = dict(is_success=True, message='更新成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='用户不存在')

        return CrudUserResponse(**result)

    @classmethod
    def delete_user_services(cls, result_db: Session, page_object: DeleteUserModel):
        """
        删除用户信息service
        :param result_db: orm对象
        :param page_object: 删除用户对象
        :return: 删除用户校验结果
        """
        if page_object.user_ids.split(','):
            user_id_list = page_object.user_ids.split(',')
            try:
                for user_id in user_id_list:
                    user_id_dict = dict(user_id=user_id, update_by=page_object.update_by, update_time=page_object.update_time)
                    UserDao.delete_user_role_dao(result_db, UserRoleModel(**user_id_dict))
                    UserDao.delete_user_post_dao(result_db, UserPostModel(**user_id_dict))
                    UserDao.delete_user_dao(result_db, UserModel(**user_id_dict))
                result_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='传入用户id为空')
        return CrudUserResponse(**result)

    @classmethod
    def detail_user_services(cls, result_db: Session, user_id: int):
        """
        获取用户详细信息service
        :param result_db: orm对象
        :param user_id: 用户id
        :return: 用户id对应的信息
        """
        user = UserDao.get_user_detail_by_id(result_db, user_id=user_id)

        return UserDetailModel(
            user=user.user_basic_info[0],
            dept=user.user_dept_info[0],
            role=user.user_role_info,
            post=user.user_post_info
        )

    @classmethod
    def reset_user_services(cls, result_db: Session, page_object: ResetUserModel):
        """
        重置用户密码service
        :param result_db: orm对象
        :param page_object: 重置用户对象
        :return: 重置用户校验结果
        """
        user = UserDao.get_user_detail_by_id(result_db, user_id=page_object.user_id).user_basic_info[0]
        if page_object.old_password:
            if not verify_password(page_object.old_password, user.password):
                result = CrudUserResponse(**dict(is_success=False, message='旧密码不正确'))
            else:
                reset_user = page_object.dict(exclude_unset=True)
                del reset_user['old_password']
                result = UserDao.edit_user_dao(result_db, reset_user)
        else:
            reset_user = page_object.dict(exclude_unset=True)
            result = UserDao.edit_user_dao(result_db, reset_user)

        return result

    @staticmethod
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
