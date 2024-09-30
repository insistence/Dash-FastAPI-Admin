from typing import Any, Literal
from api.system.dict.data import DictDataApi
from utils.cache_util import TTLCacheManager


class DictManager:
    """
    字典管理器
    """

    @classmethod
    def get_dict_options(cls, dict_type: str):
        """
        获取字典数据

        :param dict_type: 字典类型
        :return: 字典数据
        """
        cache_dict_value = TTLCacheManager.get(target_key=dict_type)
        if cache_dict_value:
            select_options, dict_options = cache_dict_value
        else:
            dict_data = DictDataApi.get_dicts(dict_type=dict_type).get('data')
            select_options = [
                dict(
                    label=item.get('dict_label'),
                    value=item.get('dict_value'),
                )
                for item in dict_data
            ]
            dict_options = [
                dict(
                    label=item.get('dict_label'),
                    value=item.get('dict_value'),
                    css_class=item.get('css_class'),
                    list_class=item.get('list_class'),
                )
                for item in dict_data
            ]
            TTLCacheManager.set(
                target_key=dict_type,
                target_value=[select_options, dict_options],
            )

        return [select_options, dict_options]

    @classmethod
    def get_dict_label(cls, dict_type: str, dict_value: Any):
        """
        根据字典类型和字典值获取字典标签

        :param dict_type: 字典类型
        :param dict_value: 字典值
        :return: 字典标签
        """
        options = cls.get_dict_options(dict_type=dict_type)[1]
        if dict_value is None:
            return ''

        for option in options:
            if option.get('value') == str(dict_value):
                return option.get('label')
        return str(dict_value)

    @classmethod
    def get_tag_color(
        cls,
        tag_type: Literal[
            'default', 'primary', 'success', 'info', 'warning', 'danger'
        ] = 'default',
    ):
        """
        根据标签类型获取标签颜色

        :param tag_type: 标签类型
        :return: 标签颜色
        """
        if tag_type == 'primary':
            return 'blue'
        elif tag_type == 'success':
            return 'green'
        elif tag_type == 'info':
            return 'cyan'
        elif tag_type == 'warning':
            return 'gold'
        elif tag_type == 'danger':
            return 'red'
        return None

    @classmethod
    def get_dict_tag(cls, dict_type: dict, dict_value: Any):
        """
        根据字典类型和字典值获取字典标签tag

        :param dict_type: 字典类型
        :param dict_value: 字典值
        :return: 字典标签tag
        """
        options = cls.get_dict_options(dict_type=dict_type)[1]
        for option in options:
            if option.get('value') == str(dict_value):
                return dict(
                    tag=option.get('label'),
                    color=cls.get_tag_color(option.get('list_class')),
                )
