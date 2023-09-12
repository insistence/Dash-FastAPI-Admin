from pydantic import BaseModel
from typing import Union, Optional, List


class TokenData(BaseModel):
    """
    token解析结果
    """
    user_id: Union[int, None] = None


class UserModel(BaseModel):
    """
    用户表对应pydantic模型
    """
    user_id: Optional[int]
    dept_id: Optional[int]
    user_name: Optional[str]
    nick_name: Optional[str]
    user_type: Optional[str]
    email: Optional[str]
    phonenumber: Optional[str]
    sex: Optional[str]
    avatar: Optional[str]
    password: Optional[str]
    status: Optional[str]
    del_flag: Optional[str]
    login_ip: Optional[str]
    login_date: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True


class UserRoleModel(BaseModel):
    """
    用户和角色关联表对应pydantic模型
    """
    user_id: Optional[int]
    role_id: Optional[int]

    class Config:
        orm_mode = True


class UserPostModel(BaseModel):
    """
    用户与岗位关联表对应pydantic模型
    """
    user_id: Optional[int]
    post_id: Optional[int]

    class Config:
        orm_mode = True


class DeptModel(BaseModel):
    """
    部门表对应pydantic模型
    """
    dept_id: Optional[int]
    parent_id: Optional[int]
    ancestors: Optional[str]
    dept_name: Optional[str]
    order_num: Optional[int]
    leader: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    status: Optional[str]
    del_flag: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]

    class Config:
        orm_mode = True


class RoleModel(BaseModel):
    """
    角色表对应pydantic模型
    """
    role_id: Optional[int]
    role_name: Optional[str]
    role_key: Optional[str]
    role_sort: Optional[int]
    data_scope: Optional[str]
    menu_check_strictly: Optional[int]
    dept_check_strictly: Optional[int]
    status: Optional[str]
    del_flag: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True


class PostModel(BaseModel):
    """
    岗位信息表对应pydantic模型
    """
    post_id: Optional[int]
    post_code: Optional[str]
    post_name: Optional[str]
    post_sort: Optional[int]
    status: Optional[str]
    create_by: Optional[str]
    create_time: Optional[str]
    update_by: Optional[str]
    update_time: Optional[str]
    remark: Optional[str]

    class Config:
        orm_mode = True


class CurrentUserInfo(BaseModel):
    """
    数据库返回当前用户信息
    """
    user_basic_info: List[Union[UserModel, None]]
    user_dept_info: List[Union[DeptModel, None]]
    user_role_info: List[Union[RoleModel, None]]
    user_post_info: List[Union[PostModel, None]]
    user_menu_info: Union[List, None]


class UserDetailModel(BaseModel):
    """
    获取用户详情信息响应模型
    """
    user: Union[UserModel, None]
    dept: Union[DeptModel, None]
    role: List[Union[RoleModel, None]]
    post: List[Union[PostModel, None]]


class CurrentUserInfoServiceResponse(UserDetailModel):
    """
    获取当前用户信息响应模型
    """
    menu: Union[List, None]


class UserQueryModel(UserModel):
    """
    用户管理不分页查询模型
    """
    create_time_start: Optional[str]
    create_time_end: Optional[str]


class UserPageObject(UserQueryModel):
    """
    用户管理分页查询模型
    """
    page_num: int
    page_size: int


class UserInfoJoinDept(UserModel):
    """
    数据库查询用户列表返回模型
    """
    dept_name: Optional[str]


class UserPageObjectResponse(BaseModel):
    """
    用户管理列表分页查询返回模型
    """
    rows: List[Union[UserInfoJoinDept, None]] = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class AddUserModel(UserModel):
    """
    新增用户模型
    """
    role_id: Optional[str]
    post_id: Optional[str]
    type: Optional[str]


class ResetUserModel(UserModel):
    """
    重置用户密码模型
    """
    old_password: Optional[str]
    sms_code: Optional[str]
    session_id: Optional[str]


class DeleteUserModel(BaseModel):
    """
    删除用户模型
    """
    user_ids: str
    update_by: Optional[str]
    update_time: Optional[str]


class UserRoleQueryModel(UserRoleModel):
    """
    用户角色关联管理不分页查询模型
    """
    user_name: Optional[str]
    phonenumber: Optional[str]
    role_name: Optional[str]
    role_key: Optional[str]


class UserRolePageObject(UserRoleQueryModel):
    """
    用户角色关联管理分页查询模型
    """
    page_num: int
    page_size: int


class UserRolePageObjectResponse(BaseModel):
    """
    用户角色关联管理列表分页查询返回模型
    """
    rows: List = []
    page_num: int
    page_size: int
    total: int
    has_next: bool


class CrudUserRoleModel(BaseModel):
    """
    新增、删除用户关联角色及角色关联用户模型
    """
    user_ids: Optional[str]
    role_ids: Optional[str]


class ImportUserModel(BaseModel):
    """
    批量导入用户模型
    """
    url: str
    is_update: bool


class CrudUserResponse(BaseModel):
    """
    操作用户响应模型
    """
    is_success: bool
    message: str


class DeptInfo(BaseModel):
    """
    查询部门树
    """
    dept_id: int
    dept_name: str
    ancestors: str


class RoleInfo(BaseModel):
    """
    用户角色信息
    """
    role_info: Union[List, None]


class MenuList(BaseModel):
    """
    用户菜单信息
    """
    menu_info: Union[List, None]
