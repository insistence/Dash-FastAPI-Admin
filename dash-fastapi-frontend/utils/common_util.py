from copy import deepcopy
from typing import Dict, List, Union


class FilterUtil:
    """
    过滤工具类
    """

    @classmethod
    def fliter_params(cls, params_name: Union[str, List[str]], fliter_dict: Dict):
        """
        过滤字典数据中指定名称的参数

        :param params_name: 需要过滤的参数名称
        :param fliter_dict: 需要过滤的字典数据
        :return: 过滤后的字典数据
        """
        copy_dict = deepcopy(fliter_dict)
        if isinstance(params_name, str) and params_name in copy_dict:
            copy_dict.pop(params_name)
        elif isinstance(params_name, list):
            for name in params_name:
                if name in copy_dict:
                    copy_dict.pop(name)

        return copy_dict


class ValidateUtil:
    """
    校验工具类
    """

    @classmethod
    def is_empty(cls, input_data: Union[Dict, List, str]):
        """
        工具方法：根据输入数据校验数据是否为空

        :param input_data: 输入数据
        :return: 校验结果
        """
        return (
            input_data is None
            or input_data == {}
            or input_data == []
            or input_data == ''
        )

    @classmethod
    def not_empty(cls, input_data: Union[Dict, List, str]):
        """
        工具方法：根据输入数据校验数据是否不为空

        :param input_data: 输入数据
        :return: 校验结果
        """
        return not cls.is_empty(input_data)
