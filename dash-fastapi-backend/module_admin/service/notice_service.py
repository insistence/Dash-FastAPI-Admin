from module_admin.entity.vo.notice_vo import *
from module_admin.dao.notice_dao import *


def get_notice_list_services(result_db: Session, query_object: NoticePageObject):
    """
    获取通知公告列表信息service
    :param result_db: orm对象
    :param query_object: 查询参数对象
    :return: 通知公告列表信息对象
    """
    notice_list_result = get_notice_list(result_db, query_object)

    return notice_list_result


def add_notice_services(result_db: Session, page_object: NoticeModel):
    """
    新增通知公告信息service
    :param result_db: orm对象
    :param page_object: 新增通知公告对象
    :return: 新增通知公告校验结果
    """
    add_notice_result = add_notice_dao(result_db, page_object)

    return add_notice_result


def edit_notice_services(result_db: Session, page_object: NoticeModel):
    """
    编辑通知公告信息service
    :param result_db: orm对象
    :param page_object: 编辑通知公告对象
    :return: 编辑通知公告校验结果
    """
    edit_notice = page_object.dict(exclude_unset=True)
    edit_notice_result = edit_notice_dao(result_db, edit_notice)

    return edit_notice_result


def delete_notice_services(result_db: Session, page_object: DeleteNoticeModel):
    """
    删除通知公告信息service
    :param result_db: orm对象
    :param page_object: 删除通知公告对象
    :return: 删除通知公告校验结果
    """
    if page_object.notice_ids.split(','):
        notice_id_list = page_object.notice_ids.split(',')
        for notice_id in notice_id_list:
            notice_id_dict = dict(notice_id=notice_id)
            delete_notice_dao(result_db, NoticeModel(**notice_id_dict))
        result = dict(is_success=True, message='删除成功')
    else:
        result = dict(is_success=False, message='传入岗位id为空')
    return CrudNoticeResponse(**result)


def detail_notice_services(result_db: Session, notice_id: int):
    """
    获取通知公告详细信息service
    :param result_db: orm对象
    :param notice_id: 通知公告id
    :return: 通知公告id对应的信息
    """
    notice = get_notice_detail_by_id(result_db, notice_id=notice_id)

    return notice
