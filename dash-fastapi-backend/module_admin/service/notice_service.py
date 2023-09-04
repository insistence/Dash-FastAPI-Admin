from module_admin.entity.vo.notice_vo import *
from module_admin.dao.notice_dao import *


class NoticeService:
    """
    通知公告管理模块服务层
    """

    @classmethod
    def get_notice_list_services(cls, result_db: Session, query_object: NoticeQueryModel):
        """
        获取通知公告列表信息service
        :param result_db: orm对象
        :param query_object: 查询参数对象
        :return: 通知公告列表信息对象
        """
        notice_list_result = NoticeDao.get_notice_list(result_db, query_object)

        return notice_list_result

    @classmethod
    def add_notice_services(cls, result_db: Session, page_object: NoticeModel):
        """
        新增通知公告信息service
        :param result_db: orm对象
        :param page_object: 新增通知公告对象
        :return: 新增通知公告校验结果
        """
        notice = NoticeDao.get_notice_detail_by_info(result_db, page_object)
        if notice:
            result = dict(is_success=False, message='通知公告已存在')
        else:
            try:
                NoticeDao.add_notice_dao(result_db, page_object)
                result_db.commit()
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))

        return CrudNoticeResponse(**result)

    @classmethod
    def edit_notice_services(cls, result_db: Session, page_object: NoticeModel):
        """
        编辑通知公告信息service
        :param result_db: orm对象
        :param page_object: 编辑通知公告对象
        :return: 编辑通知公告校验结果
        """
        edit_notice = page_object.dict(exclude_unset=True)
        notice_info = cls.detail_notice_services(result_db, edit_notice.get('notice_id'))
        if notice_info:
            if notice_info.notice_title != page_object.notice_title or notice_info.notice_type != page_object.notice_type or notice_info.notice_content != page_object.notice_content:
                notice = NoticeDao.get_notice_detail_by_info(result_db, page_object)
                if notice:
                    result = dict(is_success=False, message='通知公告已存在')
                    return CrudNoticeResponse(**result)
            try:
                NoticeDao.edit_notice_dao(result_db, edit_notice)
                result_db.commit()
                result = dict(is_success=True, message='更新成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='通知公告不存在')

        return CrudNoticeResponse(**result)

    @classmethod
    def delete_notice_services(cls, result_db: Session, page_object: DeleteNoticeModel):
        """
        删除通知公告信息service
        :param result_db: orm对象
        :param page_object: 删除通知公告对象
        :return: 删除通知公告校验结果
        """
        if page_object.notice_ids.split(','):
            notice_id_list = page_object.notice_ids.split(',')
            try:
                for notice_id in notice_id_list:
                    notice_id_dict = dict(notice_id=notice_id)
                    NoticeDao.delete_notice_dao(result_db, NoticeModel(**notice_id_dict))
                result_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                result_db.rollback()
                result = dict(is_success=False, message=str(e))
        else:
            result = dict(is_success=False, message='传入通知公告id为空')
        return CrudNoticeResponse(**result)

    @classmethod
    def detail_notice_services(cls, result_db: Session, notice_id: int):
        """
        获取通知公告详细信息service
        :param result_db: orm对象
        :param notice_id: 通知公告id
        :return: 通知公告id对应的信息
        """
        notice = NoticeDao.get_notice_detail_by_id(result_db, notice_id=notice_id)

        return notice
