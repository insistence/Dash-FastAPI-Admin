from sqlalchemy import and_
from sqlalchemy.orm import Session
from entity.dept_entity import SysDept
from utils.time_format_tool import list_format_datetime
from utils.page_tool import get_page_info


def get_dept_by_id(db: Session, dept_id: int):
    dept_info = db.query(SysDept) \
        .filter(SysDept.dept_id == dept_id,
                SysDept.status == 0,
                SysDept.del_flag == 0) \
        .first()

    return dept_info

