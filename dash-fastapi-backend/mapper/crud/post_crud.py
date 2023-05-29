from sqlalchemy import and_
from sqlalchemy.orm import Session
from entity.post_entity import SysPost
from utils.time_format_tool import list_format_datetime
from utils.page_tool import get_page_info


def get_post_by_id(db: Session, post_id: int):
    post_info = db.query(SysPost) \
        .filter(SysPost.post_id == post_id,
                SysPost.status == 0) \
        .first()

    return post_info
