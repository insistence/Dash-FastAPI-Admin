from module_admin.entity.vo.user_vo import *
from module_admin.dao.user_dao import *
from utils.pwd_util import *
from utils.common_util import *


class UserService:
    """
    用户管理模块服务层
    """

    @classmethod
    def get_user_list_services(cls, result_db: Session, query_object: UserQueryModel, data_scope_sql: str):
        """
        获取用户列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :param data_scope_sql: 数据权限对应的查询sql语句
        :return: 用户列表信息对象
        """
        user_list_result = UserDao.get_user_list(result_db, query_object, data_scope_sql)

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
        reset_user = page_object.dict(exclude_unset=True)
        if page_object.old_password:
            user = UserDao.get_user_detail_by_id(result_db, user_id=page_object.user_id).user_basic_info[0]
            if not PwdUtil.verify_password(page_object.old_password, user.password):
                result = dict(is_success=False, message='旧密码不正确')
                return CrudUserResponse(**result)
            else:
                del reset_user['old_password']
        if page_object.sms_code and page_object.session_id:
            del reset_user['sms_code']
            del reset_user['session_id']
        try:
            UserDao.edit_user_dao(result_db, reset_user)
            result_db.commit()
            result = dict(is_success=True, message='重置成功')
        except Exception as e:
            result_db.rollback()
            result = dict(is_success=False, message=str(e))

        return CrudUserResponse(**result)

    @classmethod
    def batch_import_user_services(cls, result_db: Session, user_import: ImportUserModel, current_user: CurrentUserInfoServiceResponse):
        """
        批量导入用户service
        :param user_import: 用户导入参数对象
        :param result_db: orm对象
        :param current_user: 当前用户对象
        :return: 批量导入用户结果
        """
        header_dict = {
            "部门编号": "dept_id",
            "登录名称": "user_name",
            "用户名称": "nick_name",
            "用户邮箱": "email",
            "手机号码": "phonenumber",
            "用户性别": "sex",
            "帐号状态": "status"
        }
        filepath = get_filepath_from_url(user_import.url)
        df = pd.read_excel(filepath)
        df.rename(columns=header_dict, inplace=True)
        add_error_result = []
        count = 0
        try:
            for index, row in df.iterrows():
                count = count + 1
                if row['sex'] == '男':
                    row['sex'] = '0'
                if row['sex'] == '女':
                    row['sex'] = '1'
                if row['sex'] == '未知':
                    row['sex'] = '2'
                if row['status'] == '正常':
                    row['status'] = '0'
                if row['status'] == '停用':
                    row['status'] = '1'
                add_user = UserModel(
                    **dict(
                        dept_id=row['dept_id'],
                        user_name=row['user_name'],
                        password=PwdUtil.get_password_hash('123456'),
                        nick_name=row['nick_name'],
                        email=row['email'],
                        phonenumber=row['phonenumber'],
                        sex=row['sex'],
                        status=row['status'],
                        create_by=current_user.user.user_name,
                        update_by=current_user.user.user_name
                    )
                )
                user_info = UserDao.get_user_by_info(result_db, UserModel(**dict(user_name=row['user_name'])))
                if user_info:
                    if user_import.is_update:
                        edit_user = UserModel(
                            **dict(
                                user_id=user_info.user_id,
                                dept_id=row['dept_id'],
                                user_name=row['user_name'],
                                nick_name=row['nick_name'],
                                email=row['email'],
                                phonenumber=row['phonenumber'],
                                sex=row['sex'],
                                status=row['status'],
                                update_by=current_user.user.user_name
                            )
                        ).dict(exclude_unset=True)
                        UserDao.edit_user_dao(result_db, edit_user)
                    else:
                        add_error_result.append(f"{count}.用户账号{row['user_name']}已存在")
                else:
                    UserDao.add_user_dao(result_db, add_user)
            result_db.commit()
            result = dict(is_success=True, message='\n'.join(add_error_result))
        except Exception as e:
            result_db.rollback()
            result = dict(is_success=False, message=str(e))

        return CrudUserResponse(**result)

    @staticmethod
    def get_user_import_template_services():
        """
        获取用户导入模板service
        :return: 用户导入模板excel的二进制数据
        """
        header_list = ["部门编号", "登录名称", "用户名称", "用户邮箱", "手机号码", "用户性别", "帐号状态"]
        selector_header_list = ["用户性别", "帐号状态"]
        option_list = [{"用户性别": ["男", "女", "未知"]}, {"帐号状态": ["正常", "停用"]}]
        binary_data = get_excel_template(header_list=header_list, selector_header_list=selector_header_list, option_list=option_list)

        return binary_data

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

    @classmethod
    def get_user_role_allocated_list_services(cls, result_db: Session, page_object: UserRoleQueryModel):
        """
        根据用户id获取已分配角色列表或根据角色id获取已分配用户列表
        :param result_db: orm对象
        :param page_object: 用户关联角色对象
        :return: 已分配角色列表或已分配用户列表
        """
        allocated_list = []
        if page_object.user_id:
            allocated_list = UserDao.get_user_role_allocated_list_by_user_id(result_db, page_object)
        if page_object.role_id:
            allocated_list = UserDao.get_user_role_allocated_list_by_role_id(result_db, page_object)

        return allocated_list

    @classmethod
    def get_user_role_unallocated_list_services(cls, result_db: Session, page_object: UserRoleQueryModel):
        """
        根据用户id获取未分配角色列表或根据角色id获取未分配用户列表
        :param result_db: orm对象
        :param page_object: 用户关联角色对象
        :return: 未分配角色列表或未分配用户列表
        """
        unallocated_list = []
        if page_object.user_id:
            unallocated_list = UserDao.get_user_role_unallocated_list_by_user_id(result_db, page_object)
        if page_object.role_id:
            unallocated_list = UserDao.get_user_role_unallocated_list_by_role_id(result_db, page_object)

        return unallocated_list

    @classmethod
    def add_user_role_services(cls, result_db: Session, page_object: CrudUserRoleModel):
        """
        新增用户关联角色信息service
        :param result_db: orm对象
        :param page_object: 新增用户关联角色对象
        :return: 新增用户关联角色校验结果
        """
        if page_object.user_ids and page_object.role_ids:
            user_id_list = page_object.user_ids.split(',')
            role_id_list = page_object.role_ids.split(',')
            if len(user_id_list) == 1 and len(role_id_list) >= 1:
                try:
                    for role_id in role_id_list:
                        user_role_dict = dict(user_id=page_object.user_ids, role_id=role_id)
                        user_role = cls.detail_user_role_services(result_db, UserRoleModel(**user_role_dict))
                        if user_role:
                            continue
                        else:
                            UserDao.add_user_role_dao(result_db, UserRoleModel(**user_role_dict))
                    result_db.commit()
                    result = dict(is_success=True, message='新增成功')
                except Exception as e:
                    result_db.rollback()
                    result = dict(is_success=False, message=str(e))
            elif len(user_id_list) >= 1 and len(role_id_list) == 1:
                try:
                    for user_id in user_id_list:
                        user_role_dict = dict(user_id=user_id, role_id=page_object.role_ids)
                        user_role = cls.detail_user_role_services(result_db, UserRoleModel(**user_role_dict))
                        if user_role:
                            continue
                        else:
                            UserDao.add_user_role_dao(result_db, UserRoleModel(**user_role_dict))
                    result_db.commit()
                    result = dict(is_success=True, message='新增成功')
                except Exception as e:
                    result_db.rollback()
                    result = dict(is_success=False, message=str(e))
            else:
                result = dict(is_success=False, message='不满足新增条件')
        else:
            result = dict(is_success=False, message='传入用户角色关联信息为空')

        return CrudUserResponse(**result)

    @classmethod
    def delete_user_role_services(cls, result_db: Session, page_object: CrudUserRoleModel):
        """
        删除用户关联角色信息service
        :param result_db: orm对象
        :param page_object: 删除用户关联角色对象
        :return: 删除用户关联角色校验结果
        """
        if page_object.user_ids and page_object.role_ids:
            user_id_list = page_object.user_ids.split(',')
            role_id_list = page_object.role_ids.split(',')
            if len(user_id_list) == 1 and len(role_id_list) >= 1:
                try:
                    for role_id in role_id_list:
                        UserDao.delete_user_role_by_user_and_role_dao(result_db, UserRoleModel(**dict(user_id=page_object.user_ids, role_id=role_id)))
                    result_db.commit()
                    result = dict(is_success=True, message='删除成功')
                except Exception as e:
                    result_db.rollback()
                    result = dict(is_success=False, message=str(e))
            elif len(user_id_list) >= 1 and len(role_id_list) == 1:
                try:
                    for user_id in user_id_list:
                        UserDao.delete_user_role_by_user_and_role_dao(result_db, UserRoleModel(**dict(user_id=user_id, role_id=page_object.role_ids)))
                    result_db.commit()
                    result = dict(is_success=True, message='删除成功')
                except Exception as e:
                    result_db.rollback()
                    result = dict(is_success=False, message=str(e))
            else:
                result = dict(is_success=False, message='不满足删除条件')
        else:
            result = dict(is_success=False, message='传入用户角色关联信息为空')

        return CrudUserResponse(**result)

    @classmethod
    def detail_user_role_services(cls, result_db: Session, page_object: UserRoleModel):
        """
        获取用户关联角色详细信息service
        :param result_db: orm对象
        :param page_object: 用户关联角色对象
        :return: 用户关联角色详细信息
        """
        user_role = UserDao.get_user_role_detail(result_db, page_object)

        return user_role
