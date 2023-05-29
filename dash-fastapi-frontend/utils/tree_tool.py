def find_node_values(data, key):
    """
    递归查找所有包含目标键的字典，并返回该键对应的值组成的列表。
    :param data: 待查找的树形list
    :param key: 目标键
    :return: 包含目标键的字典中目标键对应的值组成的列表
    """
    result = []
    for item in data:
        if isinstance(item, dict):
            if key in item:
                result.append(item[key])
            # 递归查找子节点
            result.extend(find_node_values(item.values(), key))
        elif isinstance(item, list):
            # 递归查找子节点
            result.extend(find_node_values(item, key))
    return result


def find_key_by_href(data, href):
    """
        递归查找所有包含目标键的字典，并返回该键对应的值组成的列表。
        :param data: 待查找的树形list
        :param href: 目标pathname
        :return: 目标值对应的key
        """
    for item in data:
        if 'children' in item:
            result = find_key_by_href(item['children'], href)
            if result is not None:
                return result
        elif 'href' in item['props'] and item['props']['href'] == href:
            return item['props']['key']
    return None


def find_title_by_key(data, key):
    """
    递归查找所有包含目标键的字典，并返回该键对应的值组成的列表。
    :param data: 待查找的树形list
    :param key: 目标key
    :return: 目标值对应的title
    """
    for item in data:
        if 'children' in item:
            result = find_title_by_key(item['children'], key)
            if result is not None:
                return result
        elif 'key' in item['props'] and item['props']['key'] == key:
            return item['props']['title']
    return None


def find_href_by_key(data, key):
    """
    递归查找所有包含目标键的字典，并返回该键对应的值组成的列表。
    :param data: 待查找的树形list
    :param key: 目标key
    :return: 目标值对应的href
    """
    for item in data:
        if 'children' in item:
            result = find_href_by_key(item['children'], key)
            if result is not None:
                return result
        elif 'key' in item['props'] and item['props']['key'] == key:
            return item['props']['href']
    return None


def find_modules_by_key(data, key):
    """
    递归查找所有包含目标键的字典，并返回该键对应的值组成的列表。
    :param data: 待查找的树形list
    :param key: 目标key
    :return: 目标值对应的module
    """
    for item in data:
        if 'children' in item:
            result = find_modules_by_key(item['children'], key)
            if result is not None:
                return result
        elif 'key' in item['props'] and item['props']['key'] == key:
            return item['props']['modules']
    return None


def find_parents(tree, target_key):
    """
    递归查找所有包含目标键的字典，并返回该键对应的值组成的列表。
    :param tree: 待查找的树形list
    :param target_key: 目标target_key
    :return: 目标值对应的所有根节点的title
    """
    result = []

    def search_parents(node, key):
        if 'children' in node:
            for child in node['children']:
                temp_result = search_parents(child, key)
                if len(temp_result) > 0:
                    result.append({'title': node['props']['title']})
                    result.extend(temp_result)
                    return result

        if 'key' in node['props'] and node['props']['key'] == key:
            result.append({'title': node['props']['title']})
            return result

        return []

    for node in tree:
        result = search_parents(node, target_key)
        if len(result) > 0:
            break

    return result[::-1]
