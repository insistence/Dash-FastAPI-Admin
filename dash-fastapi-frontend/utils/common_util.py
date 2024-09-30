from typing import Dict, List, Union


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
