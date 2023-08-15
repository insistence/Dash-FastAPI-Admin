from sqlalchemy.orm import Session
from module_admin.entity.do.notice_do import SysNotice
from module_admin.entity.vo.notice_vo import NoticeModel, NoticeQueryModel, CrudNoticeResponse
from utils.time_format_util import list_format_datetime, object_format_datetime
from datetime import datetime, time


def get_notice_detail_by_id(db: Session, notice_id: int):
    notice_info = db.query(SysNotice) \
        .filter(SysNotice.notice_id == notice_id) \
        .first()

    return object_format_datetime(notice_info)


def get_notice_list(db: Session, query_object: NoticeQueryModel):
    """
    根据查询参数获取通知公告列表信息
    :param db: orm对象
    :param query_object: 查询参数对象
    :return: 通知公告列表信息对象
    """
    notice_list = db.query(SysNotice) \
        .filter(SysNotice.notice_title.like(f'%{query_object.notice_title}%') if query_object.notice_title else True,
                SysNotice.update_by.like(f'%{query_object.update_by}%') if query_object.update_by else True,
                SysNotice.notice_type == query_object.notice_type if query_object.notice_type else True,
                SysNotice.create_time.between(
                    datetime.combine(datetime.strptime(query_object.create_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.create_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                                  if query_object.create_time_start and query_object.create_time_end else True
                ) \
        .distinct().all()

    return list_format_datetime(notice_list)


def add_notice_dao(db: Session, notice: NoticeModel):
    """
    新增通知公告数据库操作
    :param db: orm对象
    :param notice: 通知公告对象
    :return: 新增校验结果
    """
    db_notice = SysNotice(**notice.dict())
    db.add(db_notice)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_notice)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudNoticeResponse(**result)


def edit_notice_dao(db: Session, notice: dict):
    """
    编辑通知公告数据库操作
    :param db: orm对象
    :param notice: 需要更新的通知公告字典
    :return: 编辑校验结果
    """
    is_notice_id = db.query(SysNotice).filter(SysNotice.notice_id == notice.get('notice_id')).all()
    if not is_notice_id:
        result = dict(is_success=False, message='通知公告不存在')
    else:
        db.query(SysNotice) \
            .filter(SysNotice.notice_id == notice.get('notice_id')) \
            .update(notice)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudNoticeResponse(**result)


def delete_notice_dao(db: Session, notice: NoticeModel):
    """
    删除通知公告数据库操作
    :param db: orm对象
    :param notice: 通知公告对象
    :return:
    """
    db.query(SysNotice) \
        .filter(SysNotice.notice_id == notice.notice_id) \
        .delete()
    db.commit()  # 提交保存到数据库中
