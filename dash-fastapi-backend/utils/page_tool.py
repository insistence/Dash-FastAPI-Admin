from pydantic import BaseModel


class PageModel(BaseModel):
    """
    分页模型
    """
    page_num: int
    page_size: int
    total: int
    has_next: bool


def get_page_info(offset: int, page_num: int, page_size: int, count: int):
    """
    根据分页参数获取分页信息
    :param offset: 起始数据位置
    :param page_num: 当前页码
    :param page_size: 当前页面数据量
    :param count: 数据总数
    :return: 分页信息对象
    """
    has_next = False
    res_page_num = 1
    if (offset + page_size) < count:
        has_next = True
    else:
        if page_num > 1:
            res_page_num = page_num - 1

    result = dict(page_num=res_page_num, page_size=page_size, total=count, has_next=has_next)

    return PageModel(**result)
