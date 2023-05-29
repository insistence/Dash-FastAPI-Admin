import datetime


def object_format_datetime(obj):
    """
    :param obj: 输入一个对象
    :return:对目标对象所有datetime类型的属性格式化
    """
    for attr in dir(obj):
        value = getattr(obj, attr)
        if isinstance(value, datetime.datetime):
            setattr(obj, attr, value.strftime('%Y-%m-%d %H:%M:%S'))
    return obj


def list_format_datetime(lst):
    """
    :param lst: 输入一个嵌套对象的列表
    :return: 对目标列表中所有对象的datetime类型的属性格式化
    """
    for obj in lst:
        for attr in dir(obj):
            value = getattr(obj, attr)
            if isinstance(value, datetime.datetime):
                setattr(obj, attr, value.strftime('%Y-%m-%d %H:%M:%S'))
    return lst
