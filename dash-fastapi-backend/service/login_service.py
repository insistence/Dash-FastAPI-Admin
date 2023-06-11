from mapper.schema.user_schema import *
from mapper.crud.login_crud import *
from mapper.crud.user_crud import *
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.env import JwtConfig
from utils.response_tool import *
from utils.log_tool import *
from datetime import datetime, timedelta
from fastapi import Request
from fastapi import Depends, Header
from config.get_db import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(request: Request = Request, token: str = Header(...), result_db: Session = Depends(get_db)):
    """
    根据token获取当前用户信息
    :param request: Request对象
    :param token: 用户token
    :param result_db: orm对象
    :return: 当前用户信息对象
    :raise: 令牌异常AuthException
    """
    if token[:6] != 'Bearer':
        logger.warning("用户token不合法")
        raise AuthException(data="", message="用户token不合法")
    try:
        payload = jwt.decode(token[6:], JwtConfig.SECRET_KEY, algorithms=[JwtConfig.ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            logger.warning("用户token不合法")
            raise AuthException(data="", message="用户token不合法")
        token_data = TokenData(user_id=int(user_id))
    except JWTError:
        logger.warning("用户token已失效，请重新登录")
        raise AuthException(data="", message="用户token已失效，请重新登录")
    user = get_user_by_id(result_db, user_id=token_data.user_id)
    if user is None:
        logger.warning("用户token不合法")
        raise AuthException(data="", message="用户token不合法")
    redis_token = await request.app.state.redis.get(f'{user.user_basic_info[0].user_id}_access_token')
    redis_session = await request.app.state.redis.get(f'{user.user_basic_info[0].user_id}_session_id')
    if token[6:] == redis_token:
        await request.app.state.redis.set(f'{user.user_basic_info[0].user_id}_access_token', redis_token,
                                          ex=timedelta(minutes=30))
        await request.app.state.redis.set(f'{user.user_basic_info[0].user_id}_session_id', redis_session,
                                          ex=timedelta(minutes=30))
        # user_dept_info = deal_user_dept_info(result_db, DeptInfo(dept_id=user.user_dept_info[0].dept_id,
        #                                                          dept_name=user.user_dept_info[0].dept_name,
        #                                                          ancestors=user.user_dept_info[0].ancestors))
        # user_role_info = deal_user_role_info(RoleInfo(role_info=user.user_role_info))
        user_menu_info = deal_user_menu_info(0, MenuList(menu_info=user.user_menu_info))

        return CurrentUserInfoServiceResponse(
            user=user.user_basic_info[0],
            dept=user.user_dept_info[0],
            role=user.user_role_info,
            post=user.user_post_info,
            menu=user_menu_info
        )
    else:
        logger.warning("用户token已失效，请重新登录")
        raise AuthException(data="", message="用户token已失效，请重新登录")


async def logout_services(request: Request, current_user: CurrentUserInfoServiceResponse):
    """
    退出登录services
    :param request: Request对象
    :param current_user: 用户用户
    :return: 退出登录结果
    """
    await request.app.state.redis.delete(f'{current_user.user.user_id}_access_token')
    await request.app.state.redis.delete(f'{current_user.user.user_id}_session_id')

    return True


def verify_password(plain_password, hashed_password):
    """
    工具方法：校验当前输入的密码与数据库存储的密码是否一致
    :param plain_password: 当前输入的密码
    :param hashed_password: 数据库存储的密码
    :return: 校验结果
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(input_password):
    """
    工具方法：对当前输入的密码进行加密
    :param input_password: 输入的密码
    :return: 加密成功的密码
    """
    return pwd_context.hash(input_password)


def authenticate_user(query_db: Session, user_name: str, input_password: str):
    """
    根据用户名密码校验用户登录
    :param query_db: orm对象
    :param user_name: 用户名
    :param input_password: 用户密码
    :return: 校验结果
    """
    user = login_by_account(query_db, user_name)
    if not user:
        return '用户不存在'
    if not verify_password(input_password, user.password):
        return '密码错误'
    if user.status == '1':
        return '用户已停用'
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    根据登录信息创建当前用户token
    :param data: 登录信息
    :param expires_delta: token有效期
    :return: token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JwtConfig.SECRET_KEY, algorithm=JwtConfig.ALGORITHM)
    return encoded_jwt


def deal_user_dept_info(db: Session, dept_info: DeptInfo):
    tmp_dept_name = dept_info.dept_name
    dept_ancestors = dept_info.ancestors.split(',')
    tmp_dept_list = []
    for item in dept_ancestors:
        dept_obj = get_user_dept_info(db, int(item))
        if dept_obj:
            tmp_dept_list.append(dept_obj.dept_name)
    tmp_dept_list.append(tmp_dept_name)
    user_dept_info = '/'.join(tmp_dept_list)

    return user_dept_info


def deal_user_role_info(role_info: RoleInfo):
    tmp_user_role_info = []
    for item in role_info.role_info:
        tmp_user_role_info.append(item.role_name)
    user_role_info = '/'.join(tmp_user_role_info)

    return user_role_info


def deal_user_menu_info(pid: int, permission_list: MenuList):
    """
    工具方法：根据菜单信息生成树形嵌套数据
    :param pid: 菜单id
    :param permission_list: 菜单列表信息
    :return: 菜单树形嵌套数据
    """
    menu_list = []
    for permission in permission_list.menu_info:
        if permission.parent_id == pid:
            children = deal_user_menu_info(permission.menu_id, permission_list)
            antd_menu_list_data = {}
            if children and permission.menu_type == 'M':
                antd_menu_list_data['component'] = 'SubMenu'
                antd_menu_list_data['props'] = {
                    'key': str(permission.menu_id),
                    'title': permission.menu_name,
                    'icon': permission.icon
                }
                antd_menu_list_data['children'] = children
            elif children and permission.menu_type == 'C':
                antd_menu_list_data['component'] = 'Item'
                antd_menu_list_data['props'] = {
                    'key': str(permission.menu_id),
                    'title': permission.menu_name,
                    'icon': permission.icon,
                    'href': permission.path,
                    'modules': permission.component
                }
                antd_menu_list_data['button'] = children
            elif permission.menu_type == 'F':
                antd_menu_list_data['component'] = 'Button'
                antd_menu_list_data['props'] = {
                    'key': str(permission.menu_id),
                    'title': permission.menu_name,
                    'icon': permission.icon
                }
            else:
                antd_menu_list_data['component'] = 'Item'
                antd_menu_list_data['props'] = {
                    'key': str(permission.menu_id),
                    'title': permission.menu_name,
                    'icon': permission.icon,
                    'href': permission.path,
                }
            menu_list.append(antd_menu_list_data)

    return menu_list
