from fastapi import APIRouter, Request
from fastapi import Depends, Header
from config.get_db import get_db
from module_admin.service.login_service import get_current_user
from module_admin.service.notice_service import *
from module_admin.entity.vo.notice_vo import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import get_page_obj
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


noticeController = APIRouter(dependencies=[Depends(get_current_user)])


@noticeController.post("/notice/get", response_model=NoticePageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:list'))])
async def get_system_notice_list(request: Request, notice_page_query: NoticePageObject, query_db: Session = Depends(get_db)):
    try:
        notice_query = NoticeQueryModel(**notice_page_query.dict())
        # 获取全量数据
        notice_query_result = get_notice_list_services(query_db, notice_query)
        # 分页操作
        notice_page_query_result = get_page_obj(notice_query_result, notice_page_query.page_num, notice_page_query.page_size)
        logger.info('获取成功')
        return response_200(data=notice_page_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@noticeController.post("/notice/add", response_model=CrudNoticeResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:add'))])
@log_decorator(title='通知公告管理', business_type=1)
async def add_system_notice(request: Request, add_notice: NoticeModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        add_notice.create_by = current_user.user.user_name
        add_notice.update_by = current_user.user.user_name
        add_notice_result = add_notice_services(query_db, add_notice)
        logger.info(add_notice_result.message)
        if add_notice_result.is_success:
            return response_200(data=add_notice_result, message=add_notice_result.message)
        else:
            return response_400(data="", message=add_notice_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@noticeController.patch("/notice/edit", response_model=CrudNoticeResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:edit'))])
@log_decorator(title='通知公告管理', business_type=2)
async def edit_system_notice(request: Request, edit_notice: NoticeModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        edit_notice.update_by = current_user.user.user_name
        edit_notice.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_notice_result = edit_notice_services(query_db, edit_notice)
        if edit_notice_result.is_success:
            logger.info(edit_notice_result.message)
            return response_200(data=edit_notice_result, message=edit_notice_result.message)
        else:
            logger.warning(edit_notice_result.message)
            return response_400(data="", message=edit_notice_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@noticeController.post("/notice/delete", response_model=CrudNoticeResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:remove'))])
@log_decorator(title='通知公告管理', business_type=3)
async def delete_system_notice(request: Request, delete_notice: DeleteNoticeModel, query_db: Session = Depends(get_db)):
    try:
        delete_notice_result = delete_notice_services(query_db, delete_notice)
        if delete_notice_result.is_success:
            logger.info(delete_notice_result.message)
            return response_200(data=delete_notice_result, message=delete_notice_result.message)
        else:
            logger.warning(delete_notice_result.message)
            return response_400(data="", message=delete_notice_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@noticeController.get("/notice/{notice_id}", response_model=NoticeModel, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:query'))])
async def query_detail_system_post(request: Request, notice_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_notice_result = detail_notice_services(query_db, notice_id)
        logger.info(f'获取notice_id为{notice_id}的信息成功')
        return response_200(data=detail_notice_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
