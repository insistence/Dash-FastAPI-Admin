from sqlalchemy import and_
from sqlalchemy.orm import Session
from entity.post_entity import SysPost
from mapper.schema.post_schema import PostModel, PostPageObject, PostPageObjectResponse, CrudPostResponse
from utils.time_format_tool import list_format_datetime
from utils.page_tool import get_page_info


def get_post_by_id(db: Session, post_id: int):
    post_info = db.query(SysPost) \
        .filter(SysPost.post_id == post_id,
                SysPost.status == 0) \
        .first()

    return post_info


def get_post_detail_by_id(db: Session, post_id: int):
    post_info = db.query(SysPost) \
        .filter(SysPost.post_id == post_id) \
        .first()

    return post_info


def get_post_select_option_crud(db: Session):
    post_info = db.query(SysPost) \
        .filter(SysPost.status == 0) \
        .all()

    return post_info


def get_post_list(db: Session, page_object: PostPageObject):
    """
    根据查询参数获取岗位列表信息
    :param db: orm对象
    :param page_object: 分页查询参数对象
    :return: 岗位列表信息对象
    """
    count = db.query(SysPost) \
        .filter(SysPost.post_code.like(f'%{page_object.post_code}%') if page_object.post_code else True,
                SysPost.post_name.like(f'%{page_object.post_name}%') if page_object.post_name else True,
                SysPost.status == page_object.status if page_object.status else True
                )\
        .order_by(SysPost.post_sort)\
        .distinct().count()
    offset_com = (page_object.page_num - 1) * page_object.page_size
    page_info = get_page_info(offset_com, page_object.page_num, page_object.page_size, count)
    post_list = db.query(SysPost) \
        .filter(SysPost.post_code.like(f'%{page_object.post_code}%') if page_object.post_code else True,
                SysPost.post_name.like(f'%{page_object.post_name}%') if page_object.post_name else True,
                SysPost.status == page_object.status if page_object.status else True
                ) \
        .order_by(SysPost.post_sort) \
        .offset(page_info.offset) \
        .limit(page_object.page_size) \
        .distinct().all()

    result = dict(
        rows=list_format_datetime(post_list),
        page_num=page_info.page_num,
        page_size=page_info.page_size,
        total=page_info.total,
        has_next=page_info.has_next
    )

    return PostPageObjectResponse(**result)


def add_post_crud(db: Session, post: PostModel):
    """
    新增岗位数据库操作
    :param db: orm对象
    :param post: 岗位对象
    :return: 新增校验结果
    """
    db_post = SysPost(**post.dict())
    db.add(db_post)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_post)  # 刷新
    result = dict(is_success=True, message='新增成功')

    return CrudPostResponse(**result)


def edit_post_crud(db: Session, post: PostModel):
    """
    编辑岗位数据库操作
    :param db: orm对象
    :param post: 岗位对象
    :return: 编辑校验结果
    """
    is_post_id = db.query(SysPost).filter(SysPost.post_id == post.post_id).all()
    if not is_post_id:
        result = dict(is_success=False, message='岗位不存在')
    else:
        # 筛选出属性值为不为None和''的
        filtered_dict = {k: v for k, v in post.dict().items() if v is not None and v != ''}
        db.query(SysPost) \
            .filter(SysPost.post_id == post.post_id) \
            .update(filtered_dict)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudPostResponse(**result)


def delete_post_crud(db: Session, post: PostModel):
    """
    删除岗位数据库操作
    :param db: orm对象
    :param post: 岗位对象
    :return:
    """
    db.query(SysPost) \
        .filter(SysPost.post_id == post.post_id) \
        .delete()
    db.commit()  # 提交保存到数据库中
