from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from entity.dept_entity import SysDept
from mapper.schema.dept_schema import DeptModel, DeptResponse, CrudDeptResponse
from utils.time_format_tool import list_format_datetime
from utils.page_tool import get_page_info


def get_dept_by_id(db: Session, dept_id: int):
    dept_info = db.query(SysDept) \
        .filter(SysDept.dept_id == dept_id,
                SysDept.status == 0,
                SysDept.del_flag == 0) \
        .first()

    return dept_info


def get_dept_detail_by_id(db: Session, dept_id: int):
    dept_info = db.query(SysDept) \
        .filter(SysDept.dept_id == dept_id,
                SysDept.del_flag == 0) \
        .first()

    return dept_info


def get_dept_info_for_edit_option(db: Session, dept_info: DeptModel):
    dept_result = db.query(SysDept) \
        .filter(SysDept.dept_id != dept_info.dept_id, SysDept.parent_id != dept_info.dept_id,
                SysDept.del_flag == 0, SysDept.status == 0) \
        .all()

    return list_format_datetime(dept_result)


def get_children_dept(db: Session, dept_id: int):
    dept_result = db.query(SysDept) \
        .filter(SysDept.parent_id == dept_id,
                SysDept.del_flag == 0) \
        .all()

    return list_format_datetime(dept_result)


def get_dept_all_ancestors(db: Session):
    ancestors = db.query(SysDept.ancestors)\
        .filter(SysDept.del_flag == 0)\
        .all()

    return ancestors


def get_dept_list_for_tree(db: Session, dept_info: DeptModel):
    if dept_info.dept_name:
        dept_query_all = db.query(SysDept) \
            .filter(SysDept.status == 0,
                    SysDept.del_flag == 0,
                    SysDept.dept_name.like(f'%{dept_info.dept_name}%') if dept_info.dept_name else True) \
            .order_by(SysDept.order_num) \
            .distinct().all()

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
            .order_by(SysDept.order_num) \
            .distinct().all()

    return list_format_datetime(dept_result)


def get_dept_list(db: Session, page_object: DeptModel):
    """
    根据查询参数获取部门列表信息
    :param db: orm对象
    :param page_object: 不分页查询参数对象
    :return: 部门列表信息对象
    """
    if page_object.dept_name or page_object.status:
        dept_query_all = db.query(SysDept) \
            .filter(SysDept.del_flag == 0,
                    SysDept.status == page_object.status if page_object.status else True,
                    SysDept.dept_name.like(f'%{page_object.dept_name}%') if page_object.dept_name else True) \
            .order_by(SysDept.order_num)\
            .distinct().all()

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
            .filter(SysDept.del_flag == 0) \
            .order_by(SysDept.order_num) \
            .distinct().all()

    result = dict(
        rows=list_format_datetime(dept_result),
    )

    return DeptResponse(**result)


def add_dept_crud(db: Session, dept: DeptModel):
    """
    新增部门数据库操作
    :param db: orm对象
    :param dept: 部门对象
    :return: 新增校验结果
    """
    db_dept = SysDept(**dept.dict())
    db.add(db_dept)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_dept)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudDeptResponse(**result)


def edit_dept_crud(db: Session, dept: DeptModel):
    """
    编辑部门数据库操作
    :param db: orm对象
    :param dept: 部门对象
    :return: 编辑校验结果
    """
    print(dept.dept_id)
    is_dept_id = db.query(SysDept).filter(SysDept.dept_id == dept.dept_id).all()
    if not is_dept_id:
        result = dict(is_success=False, message='部门不存在')
    else:
        # 筛选出属性值为不为None和''的
        filtered_dict = {k: v for k, v in dept.dict().items() if v is not None and v != ''}
        db.query(SysDept) \
            .filter(SysDept.dept_id == dept.dept_id) \
            .update(filtered_dict)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudDeptResponse(**result)


def delete_dept_crud(db: Session, dept: DeptModel):
    """
    删除部门数据库操作
    :param db: orm对象
    :param dept: 部门对象
    :return:
    """
    db.query(SysDept) \
        .filter(SysDept.dept_id == dept.dept_id) \
        .update({SysDept.del_flag: '2', SysDept.update_by: dept.update_by, SysDept.update_time: dept.update_time})
    db.commit()  # 提交保存到数据库中
