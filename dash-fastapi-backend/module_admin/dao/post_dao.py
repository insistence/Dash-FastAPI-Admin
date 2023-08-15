from sqlalchemy.orm import Session
from module_admin.entity.do.post_do import SysPost
from module_admin.entity.vo.post_vo import PostModel, CrudPostResponse
from utils.time_format_util import list_format_datetime


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


def get_post_select_option_dao(db: Session):
    post_info = db.query(SysPost) \
        .filter(SysPost.status == 0) \
        .all()

    return post_info


def get_post_list(db: Session, query_object: PostModel):
    """
    根据查询参数获取岗位列表信息
    :param db: orm对象
    :param query_object: 查询参数对象
    :return: 岗位列表信息对象
    """
    post_list = db.query(SysPost) \
        .filter(SysPost.post_code.like(f'%{query_object.post_code}%') if query_object.post_code else True,
                SysPost.post_name.like(f'%{query_object.post_name}%') if query_object.post_name else True,
                SysPost.status == query_object.status if query_object.status else True
                ) \
        .order_by(SysPost.post_sort) \
        .distinct().all()

    return list_format_datetime(post_list)


def add_post_dao(db: Session, post: PostModel):
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


def edit_post_dao(db: Session, post: dict):
    """
    编辑岗位数据库操作
    :param db: orm对象
    :param post: 需要更新的岗位字典
    :return: 编辑校验结果
    """
    is_post_id = db.query(SysPost).filter(SysPost.post_id == post.get('post_id')).all()
    if not is_post_id:
        result = dict(is_success=False, message='岗位不存在')
    else:
        db.query(SysPost) \
            .filter(SysPost.post_id == post.get('post_id')) \
            .update(post)
        db.commit()  # 提交保存到数据库中
        result = dict(is_success=True, message='更新成功')

    return CrudPostResponse(**result)


def delete_post_dao(db: Session, post: PostModel):
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
