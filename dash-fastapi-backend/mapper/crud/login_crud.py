from sqlalchemy.orm import Session
from entity.user_entity import SysUser
from utils.time_format_tool import object_format_datetime


def login_by_account(db: Session, user_name: str):
    """
    根据用户名查询用户信息
    :param db: orm对象
    :param user_name: 用户名
    :return: 用户对象
    """
    user = db.query(SysUser).\
        filter_by(user_name=user_name).\
        distinct().\
        first()

    return object_format_datetime(user)
