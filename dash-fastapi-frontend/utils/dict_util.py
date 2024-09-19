from cachebox import cached, TTLCache
from flask import session
from typing import Any, Literal
from api.system.dict.data import DictDataApi


def _DictManager__custom_key_maker(*args, **kwargs):
    key = args[1].get('dict_type')
    if session.get('Authorization'):
        key = f'{session.get("Authorization")}:{args[1].get("dict_type")}'
    return key


class DictManager:
    @classmethod
    @cached(TTLCache(0, ttl=600), key_maker=_DictManager__custom_key_maker)
    def get_dict_options(cls, dict_type: str):
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

        return [select_options, dict_options]

    @classmethod
    def get_dict_label(cls, dict_type: str, dict_value: Any):
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
        options = cls.get_dict_options(dict_type=dict_type)[1]
        for option in options:
            if option.get('value') == str(dict_value):
                return dict(
                    tag=option.get('label'),
                    color=cls.get_tag_color(option.get('list_class')),
                )
