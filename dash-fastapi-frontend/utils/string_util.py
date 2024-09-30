class StringUtil:
    """
    字符串工具类
    """

    @classmethod
    def insert_before_substring(
        cls, original_str: str, start_substr: str, new_str: str
    ):
        """
        在字符串中指定字符串位置插入新字符串

        :param original_str: 原始字符串
        :param start_substr: 指定的字符串
        :param new_str: 插入的新字符串
        :return: 处理完成的新字符串
        """
        start_index = original_str.find(start_substr)
        if start_index != -1:
            before_start = original_str[:start_index]
            after_start = original_str[start_index:]
            new_str_with_insertion = before_start + new_str + after_start
            return new_str_with_insertion
        else:
            return original_str
