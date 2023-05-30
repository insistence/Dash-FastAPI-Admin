from sqlalchemy import and_
from sqlalchemy.orm import Session
from entity.dept_entity import SysDept
from mapper.schema.dept_schema import DeptPageObject
from utils.time_format_tool import list_format_datetime
from utils.page_tool import get_page_info


def get_dept_by_id(db: Session, dept_id: int):
    dept_info = db.query(SysDept) \
        .filter(SysDept.dept_id == dept_id,
                SysDept.status == 0,
                SysDept.del_flag == 0) \
        .first()

    return dept_info


def get_dept_list_for_tree(db: Session, dept_info: DeptPageObject):
    if dept_info.dept_name:
        dept_query_all = db.query(SysDept) \
            .filter(SysDept.status == 0,
                    SysDept.del_flag == 0,
                    SysDept.dept_name.like(f'%{dept_info.dept_name}%') if dept_info.dept_name else True) \
            .all()

        dept = []
        if dept_query_all:
            for dept_query in dept_query_all:
                ancestor_info = dept_query.ancestors.split(',')
                ancestor_info.append(dept_query.dept_id)
                for ancestor in ancestor_info:
                    dept_item = get_dept_by_id(db, int(ancestor))
                    if dept_item:
                        dept.append(dept_item)
        # 去重
        dept_result = list(set(dept))
    else:
        dept_result = db.query(SysDept) \
            .filter(SysDept.status == 0, SysDept.del_flag == 0) \
            .all()

    return list_format_datetime(dept_result)
