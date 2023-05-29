from sqlalchemy import and_
from sqlalchemy.orm import Session
from entity.role_entity import SysRole
from utils.time_format_tool import list_format_datetime
from utils.page_tool import get_page_info


def get_role_by_id(db: Session, role_id: int):
    role_info = db.query(SysRole) \
        .filter(SysRole.role_id == role_id,
                SysRole.status == 0,
                SysRole.del_flag == 0) \
        .first()

    return role_info
