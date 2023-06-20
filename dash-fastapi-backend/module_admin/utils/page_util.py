from pydantic import BaseModel


class PageModel(BaseModel):
    """
    分页模型
    """
    offset: int
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
    if offset >= count:
        res_offset_1 = (page_num - 2) * page_size
        if res_offset_1 < 0:
            res_offset = 0
            res_page_num = 1
        else:
            res_offset = res_offset_1
            res_page_num = page_num - 1
    else:
        res_offset = offset
        if (res_offset + page_size) < count:
            has_next = True
        res_page_num = page_num

    result = dict(offset=res_offset, page_num=res_page_num, page_size=page_size, total=count, has_next=has_next)

    return PageModel(**result)
