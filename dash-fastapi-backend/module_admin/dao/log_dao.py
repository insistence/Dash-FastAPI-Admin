from sqlalchemy.orm import Session
from module_admin.entity.do.log_do import SysOperLog, SysLogininfor
from module_admin.entity.vo.log_vo import OperLogModel, LogininforModel, OperLogPageObject, OperLogPageObjectResponse, \
    LoginLogPageObject, LoginLogPageObjectResponse, CrudLogResponse
from utils.time_format_util import list_format_datetime
from utils.page_util import get_page_info
from datetime import datetime, time


def get_operation_log_detail_by_id(db: Session, oper_id: int):
    operation_log_info = db.query(SysOperLog) \
        .filter(SysOperLog.oper_id == oper_id) \
        .first()

    return operation_log_info


def get_operation_log_list(db: Session, page_object: OperLogPageObject):
    """
    根据查询参数获取操作日志列表信息
    :param db: orm对象
    :param page_object: 分页查询参数对象
    :return: 操作日志列表信息对象
    """
    count = db.query(SysOperLog) \
        .filter(SysOperLog.title.like(f'%{page_object.title}%') if page_object.title else True,
                SysOperLog.oper_name.like(f'%{page_object.oper_name}%') if page_object.oper_name else True,
                SysOperLog.business_type == page_object.business_type if page_object.business_type else True,
                SysOperLog.status == page_object.status if page_object.status else True,
                SysOperLog.oper_time.between(
                    datetime.combine(datetime.strptime(page_object.oper_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(page_object.oper_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                            if page_object.oper_time_start and page_object.oper_time_end else True
                )\
        .distinct().count()
    offset_com = (page_object.page_num - 1) * page_object.page_size
    page_info = get_page_info(offset_com, page_object.page_num, page_object.page_size, count)
    operation_log_list = db.query(SysOperLog) \
        .filter(SysOperLog.title.like(f'%{page_object.title}%') if page_object.title else True,
                SysOperLog.oper_name.like(f'%{page_object.oper_name}%') if page_object.oper_name else True,
                SysOperLog.business_type == page_object.business_type if page_object.business_type else True,
                SysOperLog.status == page_object.status if page_object.status else True,
                SysOperLog.oper_time.between(
                    datetime.combine(datetime.strptime(page_object.oper_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(page_object.oper_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                            if page_object.oper_time_start and page_object.oper_time_end else True
                )\
        .offset(page_info.offset) \
        .limit(page_object.page_size) \
        .distinct().all()

    result = dict(
        rows=list_format_datetime(operation_log_list),
        page_num=page_info.page_num,
        page_size=page_info.page_size,
        total=page_info.total,
        has_next=page_info.has_next
    )

    return OperLogPageObjectResponse(**result)


def add_operation_log_dao(db: Session, operation_log: OperLogModel):
    """
    新增操作日志数据库操作
    :param db: orm对象
    :param operation_log: 操作日志对象
    :return: 新增校验结果
    """
    db_operation_log = SysOperLog(**operation_log.dict())
    db.add(db_operation_log)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_operation_log)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudLogResponse(**result)


def delete_operation_log_dao(db: Session, operation_log: OperLogModel):
    """
    删除操作日志数据库操作
    :param db: orm对象
    :param operation_log: 操作日志对象
    :return:
    """
    db.query(SysOperLog) \
        .filter(SysOperLog.oper_id == operation_log.oper_id) \
        .delete()
    db.commit()  # 提交保存到数据库中


def get_login_log_list(db: Session, page_object: LoginLogPageObject):
    """
    根据查询参数获取登录日志列表信息
    :param db: orm对象
    :param page_object: 分页查询参数对象
    :return: 登录日志列表信息对象
    """
    count = db.query(SysLogininfor) \
        .filter(SysLogininfor.ipaddr.like(f'%{page_object.ipaddr}%') if page_object.ipaddr else True,
                SysLogininfor.user_name.like(f'%{page_object.user_name}%') if page_object.user_name else True,
                SysLogininfor.status == page_object.status if page_object.status else True,
                SysLogininfor.login_time.between(
                    datetime.combine(datetime.strptime(page_object.login_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(page_object.login_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                            if page_object.login_time_start and page_object.login_time_end else True
                )\
        .distinct().count()
    offset_com = (page_object.page_num - 1) * page_object.page_size
    page_info = get_page_info(offset_com, page_object.page_num, page_object.page_size, count)
    login_log_list = db.query(SysLogininfor) \
        .filter(SysLogininfor.ipaddr.like(f'%{page_object.ipaddr}%') if page_object.ipaddr else True,
                SysLogininfor.user_name.like(f'%{page_object.user_name}%') if page_object.user_name else True,
                SysLogininfor.status == page_object.status if page_object.status else True,
                SysLogininfor.login_time.between(
                    datetime.combine(datetime.strptime(page_object.login_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(page_object.login_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                            if page_object.login_time_start and page_object.login_time_end else True
                )\
        .offset(page_info.offset) \
        .limit(page_object.page_size) \
        .distinct().all()

    result = dict(
        rows=list_format_datetime(login_log_list),
        page_num=page_info.page_num,
        page_size=page_info.page_size,
        total=page_info.total,
        has_next=page_info.has_next
    )

    return LoginLogPageObjectResponse(**result)


def add_login_log_dao(db: Session, login_log: LogininforModel):
    """
    新增登录日志数据库操作
    :param db: orm对象
    :param login_log: 登录日志对象
    :return: 新增校验结果
    """
    db_login_log = SysLogininfor(**login_log.dict())
    db.add(db_login_log)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_login_log)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudLogResponse(**result)


def delete_login_log_dao(db: Session, login_log: LogininforModel):
    """
    删除登录日志数据库操作
    :param db: orm对象
    :param login_log: 登录日志对象
    :return:
    """
    db.query(SysLogininfor) \
        .filter(SysLogininfor.info_id == login_log.info_id) \
        .delete()
    db.commit()  # 提交保存到数据库中
