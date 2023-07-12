from fastapi import APIRouter, Request
from fastapi import Depends, Header
from config.get_db import get_db
from module_admin.service.login_service import get_current_user
from module_admin.service.post_service import *
from module_admin.entity.vo.post_vo import *
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.annotation.log_annotation import log_decorator


postController = APIRouter(dependencies=[Depends(get_current_user)])


@postController.post("/post/forSelectOption", response_model=PostSelectOptionResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('common'))])
async def get_system_post_select(request: Request, query_db: Session = Depends(get_db)):
    try:
        role_query_result = get_post_select_option_services(query_db)
        logger.info('获取成功')
        return response_200(data=role_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@postController.post("/post/get", response_model=PostPageObjectResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:post:list'))])
async def get_system_post_list(request: Request, post_query: PostPageObject, query_db: Session = Depends(get_db)):
    try:
        post_query_result = get_post_list_services(query_db, post_query)
        logger.info('获取成功')
        return response_200(data=post_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@postController.post("/post/add", response_model=CrudPostResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:post:add'))])
@log_decorator(title='岗位管理', business_type=1)
async def add_system_post(request: Request, add_post: PostModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        add_post.create_by = current_user.user.user_name
        add_post.update_by = current_user.user.user_name
        add_post_result = add_post_services(query_db, add_post)
        logger.info(add_post_result.message)
        if add_post_result.is_success:
            return response_200(data=add_post_result, message=add_post_result.message)
        else:
            return response_400(data="", message=add_post_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@postController.patch("/post/edit", response_model=CrudPostResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:post:edit'))])
@log_decorator(title='岗位管理', business_type=2)
async def edit_system_post(request: Request, edit_post: PostModel, token: Optional[str] = Header(...), query_db: Session = Depends(get_db)):
    try:
        current_user = await get_current_user(request, token, query_db)
        edit_post.update_by = current_user.user.user_name
        edit_post.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        edit_post_result = edit_post_services(query_db, edit_post)
        if edit_post_result.is_success:
            logger.info(edit_post_result.message)
            return response_200(data=edit_post_result, message=edit_post_result.message)
        else:
            logger.warning(edit_post_result.message)
            return response_400(data="", message=edit_post_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@postController.post("/post/delete", response_model=CrudPostResponse, dependencies=[Depends(CheckUserInterfaceAuth('system:post:remove'))])
@log_decorator(title='岗位管理', business_type=3)
async def delete_system_post(request: Request, delete_post: DeletePostModel, query_db: Session = Depends(get_db)):
    try:
        delete_post_result = delete_post_services(query_db, delete_post)
        if delete_post_result.is_success:
            logger.info(delete_post_result.message)
            return response_200(data=delete_post_result, message=delete_post_result.message)
        else:
            logger.warning(delete_post_result.message)
            return response_400(data="", message=delete_post_result.message)
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")


@postController.get("/post/{post_id}", response_model=PostModel, dependencies=[Depends(CheckUserInterfaceAuth('system:post:edit'))])
async def query_detail_system_post(request: Request, post_id: int, query_db: Session = Depends(get_db)):
    try:
        detail_post_result = detail_post_services(query_db, post_id)
        logger.info(f'获取post_id为{post_id}的信息成功')
        return response_200(data=detail_post_result, message='获取成功')
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
