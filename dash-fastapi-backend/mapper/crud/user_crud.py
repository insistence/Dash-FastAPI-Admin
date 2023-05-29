from sqlalchemy import and_
from sqlalchemy.orm import Session
from entity.user_entity import SysUser, SysUserRole, SysUserPost
from entity.role_entity import SysRole, SysRoleMenu
from entity.dept_entity import SysDept
from entity.post_entity import SysPost
from entity.menu_entity import SysMenu
from mapper.schema.user_schema import UserModel, UserRoleModel, UserPostModel, CurrentUserInfo, UserPageObject, \
    UserPageObjectResponse, CrudUserResponse
from utils.time_format_tool import list_format_datetime
from utils.page_tool import get_page_info


def get_user_by_name(db: Session, user_name: str):
    """
    根据用户名获取用户信息
    :param db: orm对象
    :param user_name: 用户名
    :return: 当前用户名的用户信息对象
    """
    query_user_info = db.query(SysUser) \
        .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_name == user_name) \
        .distinct().first()

    return query_user_info


def get_user_by_id(db: Session, user_id: int):
    """
    根据user_id获取用户信息
    :param db: orm对象
    :param user_id: 用户id
    :return: 当前user_id的用户信息对象
    """
    query_user_basic_info = db.query(SysUser) \
        .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
        .distinct().all()
    query_user_dept_info = db.query(SysDept).select_from(SysUser) \
        .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
        .outerjoin(SysDept, and_(SysUser.dept_id == SysDept.dept_id, SysDept.status == 0, SysDept.del_flag == 0)) \
        .distinct().all()
    query_user_role_info = db.query(SysRole).select_from(SysUser) \
        .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
        .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
        .outerjoin(SysRole, and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
        .distinct().all()
    query_user_post_info = db.query(SysPost).select_from(SysUser) \
        .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
        .outerjoin(SysUserPost, SysUser.user_id == SysUserPost.user_id) \
        .outerjoin(SysPost, and_(SysUserPost.post_id == SysPost.post_id, SysPost.status == 0)) \
        .distinct().all()
    query_user_menu_info = db.query(SysMenu).select_from(SysUser) \
        .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
        .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
        .outerjoin(SysRole, and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
        .outerjoin(SysRoleMenu, SysRole.role_id == SysRoleMenu.role_id) \
        .outerjoin(SysMenu, and_(SysRoleMenu.menu_id == SysMenu.menu_id, SysMenu.status == 0)) \
        .distinct().all()
    results = dict(
        user_basic_info=list_format_datetime(query_user_basic_info),
        user_dept_info=list_format_datetime(query_user_dept_info),
        user_role_info=list_format_datetime(query_user_role_info),
        user_post_info=list_format_datetime(query_user_post_info),
        user_menu_info=list_format_datetime(query_user_menu_info)
    )

    return CurrentUserInfo(**results)


def get_user_list(db: Session, page_object: UserPageObject):
    """
    根据查询参数获取用户列表信息
    :param db: orm对象
    :param page_object: 分页查询参数对象
    :return: 用户列表信息对象
    """
    offset = (page_object.page_num - 1) * page_object.page_size
    user_list = db.query(SysUser) \
        .filter(SysUser.del_flag == 0,
                SysUser.dept_id == page_object.dept_id if page_object.dept_id else True,
                SysUser.user_name.like(f'%{page_object.user_name}%') if page_object.user_name else True,
                SysUser.nick_name.like(f'%{page_object.nick_name}%') if page_object.nick_name else True,
                SysUser.email.like(f'%{page_object.email}%') if page_object.email else True,
                SysUser.phonenumber.like(f'%{page_object.phonenumber}%') if page_object.phonenumber else True,
                SysUser.sex == page_object.sex if page_object.sex else True
                ) \
        .offset(offset) \
        .limit(page_object.page_size) \
        .distinct().all()
    count = db.query(SysUser) \
        .filter(SysUser.del_flag == 0,
                SysUser.dept_id == page_object.dept_id if page_object.dept_id else True,
                SysUser.user_name.like(f'%{page_object.user_name}%') if page_object.user_name else True,
                SysUser.nick_name.like(f'%{page_object.nick_name}%') if page_object.nick_name else True,
                SysUser.email.like(f'%{page_object.email}%') if page_object.email else True,
                SysUser.phonenumber.like(f'%{page_object.phonenumber}%') if page_object.phonenumber else True,
                SysUser.sex == page_object.sex if page_object.sex else True
                ) \
        .distinct().count()

    page_info = get_page_info(offset, page_object.page_num, page_object.page_size, count)
    result = dict(
        rows=list_format_datetime(user_list),
        page_num=page_info.page_num,
        page_size=page_info.page_size,
        total=page_info.total,
        has_next=page_info.has_next
    )

    return UserPageObjectResponse(**result)


def add_user_crud(db: Session, user: UserModel):
    """
    新增用户数据库操作
    :param db: orm对象
    :param user: 用户对象
    :return: 新增校验结果
    """
    is_user = db.query(SysUser).filter(SysUser.user_name == user.user_name, SysUser.del_flag == 0).all()
    if is_user:
        result = dict(is_success=False, message='用户名已存在')
    else:
        db_user = SysUser(**user.dict())
        db.add(db_user)
        db.commit()  # 提交保存到数据库中
        db.refresh(db_user)  # 刷新
        result = dict(is_success=True, message='新增成功')

    return CrudUserResponse(**result)


def edit_user_crud(db: Session, user: UserModel):
    """
    编辑用户数据库操作
    :param db: orm对象
    :param user: 用户对象
    :return: 编辑校验结果
    """
    is_user_id = db.query(SysUser).filter(SysUser.user_id == user.user_id, SysUser.del_flag == 0).all()
    is_user_name = db.query(SysUser).filter(SysUser.user_name == user.user_name, SysUser.del_flag == 0).all()
    if not is_user_id:
        result = dict(is_success=False, message='用户不存在')
    elif is_user_name:
        result = dict(is_success=False, message='用户名已存在，不允许修改')
    else:
        # 筛选出属性值为不为None和''的
        filtered_dict = {k: v for k, v in user.dict().items() if v is not None and v != ''}
        db.query(SysUser)\
            .filter(SysUser.user_id == user.user_id)\
            .update(filtered_dict)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudUserResponse(**result)


def delete_user_crud(db: Session, user: UserModel):
    """
    删除用户数据库操作
    :param db: orm对象
    :param user: 用户对象
    :return:
    """
    db.query(SysUser) \
        .filter(SysUser.user_id == user.user_id) \
        .delete()
    db.commit()  # 提交保存到数据库中


def add_user_role_crud(db: Session, user_role: UserRoleModel):
    """
    新增用户角色关联信息数据库操作
    :param db: orm对象
    :param user_role: 用户角色关联对象
    :return:
    """
    db_user_role = SysUserRole(**user_role.dict())
    db.add(db_user_role)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_user_role)  # 刷新


def delete_user_role_crud(db: Session, user_role: UserRoleModel):
    """
    删除用户角色关联信息数据库操作
    :param db: orm对象
    :param user_role: 用户角色关联对象
    :return:
    """
    db.query(SysUserRole) \
        .filter(SysUserRole.user_id == user_role.user_id) \
        .delete()
    db.commit()  # 提交保存到数据库中


def add_user_post_crud(db: Session, user_post: UserPostModel):
    """
    新增用户岗位关联信息数据库操作
    :param db: orm对象
    :param user_post: 用户岗位关联对象
    :return:
    """
    db_user_post = SysUserPost(**user_post.dict())
    db.add(db_user_post)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_user_post)  # 刷新


def delete_user_post_crud(db: Session, user_post: UserPostModel):
    """
    删除用户岗位关联信息数据库操作
    :param db: orm对象
    :param user_post: 用户岗位关联对象
    :return:
    """
    db.query(SysUserPost) \
        .filter(SysUserPost.user_id == user_post.user_id) \
        .delete()
    db.commit()  # 提交保存到数据库中


def get_user_dept_info(db: Session, dept_id: int):
    dept_basic_info = db.query(SysDept) \
        .filter(SysDept.dept_id == dept_id,
                SysDept.status == 0,
                SysDept.del_flag == 0) \
        .first()
    return dept_basic_info
