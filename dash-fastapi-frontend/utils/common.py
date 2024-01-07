def validate_data_not_empty(input_data):
    """
    工具方法：根据输入数据校验数据是否不为None和''
    :param input_data: 输入数据
    :return: 校验结果
    """
    return input_data is not None and input_data != ''
