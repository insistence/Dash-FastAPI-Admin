from copy import deepcopy
from datetime import datetime
from dateutil.parser import parse
from typing import Dict, List, Union


class TimeFormatUtil:
    """
    时间格式化工具类
    """

    @classmethod
    def format_time(
        cls, time_info: Union[str, datetime], format: str = '%Y-%m-%d %H:%M:%S'
    ):
        """
        格式化时间字符串或datetime对象为指定格式

        :param time_info: 时间字符串或datetime对象
        :param format: 格式化格式，默认为'%Y-%m-%d %H:%M:%S'
        :return: 格式化后的时间字符串
        """
        if isinstance(time_info, datetime):
            format_date = time_info.strftime(format)
        else:
            try:
                date = parse(time_info)
                format_date = date.strftime(format)
            except Exception:
                format_date = time_info

        return format_date

    @classmethod
    def format_time_dict(
        cls, time_dict: Dict, format: str = '%Y-%m-%d %H:%M:%S'
    ):
        """
        格式化时间字典

        :param time_dict: 时间字典
        :param format: 格式化格式，默认为'%Y-%m-%d %H:%M:%S'
        :return: 格式化后的时间字典
        """
        copy_time_dict = deepcopy(time_dict)
        for k, v in copy_time_dict.items():
            if isinstance(v, (str, datetime)):
                copy_time_dict[k] = cls.format_time(v, format)
            elif isinstance(v, dict):
                copy_time_dict[k] = cls.format_time_dict(v, format)
            elif isinstance(v, list):
                copy_time_dict[k] = cls.format_time_list(v, format)
            else:
                copy_time_dict[k] = v

        return copy_time_dict

    @classmethod
    def format_time_list(
        cls, time_list: List, format: str = '%Y-%m-%d %H:%M:%S'
    ):
        """
        格式化时间列表

        :param time_list: 时间列表
        :param format: 格式化格式，默认为'%Y-%m-%d %H:%M:%S'
        :return: 格式化后的时间列表
        """
        format_time_list = []
        for item in time_list:
            if isinstance(item, (str, datetime)):
                format_item = cls.format_time(item, format)
            elif isinstance(item, dict):
                format_item = cls.format_time_dict(item, format)
            elif isinstance(item, list):
                format_item = cls.format_time_list(item, format)
            else:
                format_item = item

            format_time_list.append(format_item)

        return format_time_list
