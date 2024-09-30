class TreeUtil:
    """
    树形数据处理工具类
    """

    @classmethod
    def find_node_values(cls, data, key):
        """
        递归查找所有包含目标键的字典，并返回该键对应的值组成的列表

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
                result.extend(cls.find_node_values(item.values(), key))
            elif isinstance(item, list):
                # 递归查找子节点
                result.extend(cls.find_node_values(item, key))
        return result

    @classmethod
    def find_key_by_href(cls, data, href):
        """
        递归查找所有包含目标键的字典，并返回该键对应的值组成的列表

        :param data: 待查找的树形list
        :param href: 目标pathname
        :return: 目标值对应的key
        """
        for item in data:
            if 'children' in item:
                result = cls.find_key_by_href(item['children'], href)
                if result is not None:
                    return result
            elif 'href' in item['props'] and item['props']['href'] == href:
                return item['props']['key']
        return None

    @classmethod
    def find_title_by_key(cls, data, key):
        """
        递归查找所有包含目标键的字典，并返回该键对应的值组成的列表

        :param data: 待查找的树形list
        :param key: 目标key
        :return: 目标值对应的title
        """
        for item in data:
            if 'children' in item:
                result = cls.find_title_by_key(item['children'], key)
                if result is not None:
                    return result
            elif 'key' in item['props'] and item['props']['key'] == key:
                return item['props']['title']
        return None

    @classmethod
    def find_href_by_key(cls, data, key):
        """
        递归查找所有包含目标键的字典，并返回该键对应的值组成的列表

        :param data: 待查找的树形list
        :param key: 目标key
        :return: 目标值对应的href
        """
        for item in data:
            if 'children' in item:
                result = cls.find_href_by_key(item['children'], key)
                if result is not None:
                    return result
            elif 'key' in item['props'] and item['props']['key'] == key:
                return item['props'].get('href')
        return None

    @classmethod
    def find_modules_by_key(cls, data, key):
        """
        递归查找所有包含目标键的字典，并返回该键对应的值组成的列表

        :param data: 待查找的树形list
        :param key: 目标key
        :return: 目标值对应的module
        """
        for item in data:
            if 'children' in item:
                result = cls.find_modules_by_key(item['children'], key)
                if result is not None:
                    return result
            elif 'key' in item['props'] and item['props']['key'] == key:
                return item['props'].get('modules')
        return None

    @classmethod
    def find_parents(cls, tree, target_key):
        """
        递归查找所有包含目标键的字典，并返回该键对应的值组成的列表

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

    @classmethod
    def deal_user_menu_info(cls, pid: int, permission_list: list):
        """
        工具方法：根据菜单信息生成树形嵌套数据

        :param pid: 菜单id
        :param permission_list: 菜单列表信息
        :return: 菜单树形嵌套数据
        """
        menu_list = []
        for permission in permission_list:
            if permission['parent_id'] == pid:
                children = cls.deal_user_menu_info(
                    permission['menu_id'], permission_list
                )
                antd_menu_list_data = {}
                if children and permission['menu_type'] == 'M':
                    antd_menu_list_data['component'] = 'SubMenu'
                    antd_menu_list_data['props'] = {
                        'key': str(permission['menu_id']),
                        'title': permission['menu_name'],
                        'icon': permission['icon'],
                        'modules': permission['component'],
                    }
                    antd_menu_list_data['children'] = children
                elif permission['menu_type'] == 'C':
                    antd_menu_list_data['component'] = 'Item'
                    antd_menu_list_data['props'] = {
                        'key': str(permission['menu_id']),
                        'title': permission['menu_name'],
                        'icon': permission['icon'],
                        'href': permission['path'],
                        'modules': permission['component'],
                    }
                    antd_menu_list_data['button'] = children
                elif permission['menu_type'] == 'F':
                    antd_menu_list_data['component'] = 'Button'
                    antd_menu_list_data['props'] = {
                        'key': str(permission['menu_id']),
                        'title': permission['menu_name'],
                        'icon': permission['icon'],
                    }
                elif permission['is_frame'] == 0:
                    antd_menu_list_data['component'] = 'Item'
                    antd_menu_list_data['props'] = {
                        'key': str(permission['menu_id']),
                        'title': permission['menu_name'],
                        'icon': permission['icon'],
                        'href': permission['path'],
                        'target': '_blank',
                        'modules': 'link',
                    }
                else:
                    antd_menu_list_data['component'] = 'Item'
                    antd_menu_list_data['props'] = {
                        'key': str(permission['menu_id']),
                        'title': permission['menu_name'],
                        'icon': permission['icon'],
                        'href': permission['path'],
                        'modules': permission['component'],
                    }
                menu_list.append(antd_menu_list_data)

        return menu_list

    @classmethod
    def get_dept_tree(cls, pid: int, permission_list: list):
        """
        工具方法：根据部门信息生成树形嵌套数据

        :param pid: 部门id
        :param permission_list: 部门列表信息
        :return: 部门树形嵌套数据
        """
        dept_list = []
        for permission in permission_list:
            if permission['parent_id'] == pid:
                children = cls.get_dept_tree(
                    permission['dept_id'], permission_list
                )
                dept_list_data = {}
                if children:
                    dept_list_data['children'] = children
                dept_list_data['key'] = str(permission['dept_id'])
                dept_list_data['dept_id'] = permission['dept_id']
                dept_list_data['dept_name'] = permission['dept_name']
                dept_list_data['order_num'] = permission['order_num']
                dept_list_data['status'] = permission['status']
                dept_list_data['create_time'] = permission['create_time']
                dept_list_data['operation'] = permission['operation']
                dept_list.append(dept_list_data)

        return dept_list

    @classmethod
    def list_to_tree(
        cls, permission_list: list, sub_id_str: str, parent_id_str: str
    ) -> list:
        """
        工具方法：根据列表信息生成树形嵌套数据

        :param permission_list: 列表信息
        :param sub_id_str: 子id字符串
        :param parent_id_str: 父id字符串
        :return: 树形嵌套数据
        """
        # 转成id为key的字典
        mapping: dict = dict(
            zip([i[sub_id_str] for i in permission_list], permission_list)
        )

        # 树容器
        container: list = []

        for d in permission_list:
            # 如果找不到父级项，则是根节点
            parent: dict = mapping.get(d[parent_id_str])
            if parent is None:
                container.append(d)
            else:
                children: list = parent.get('children')
                if not children:
                    children = []
                children.append(d)
                parent.update({'children': children})

        return container

    @classmethod
    def list_to_tree_select(
        cls,
        permission_list: list,
        title_str: str,
        key_str: str,
        value_str: str,
        parent_id_str: str,
    ) -> list:
        """
        工具方法：根据列表信息生成树选择器嵌套数据

        :param permission_list: 列表信息
        :param title_str: title字符串
        :param key_str: key字符串
        :param value_str: value字符串
        :param parent_id_str: parent_id字符串
        :return: 树形嵌套数据
        """
        permission_list = [
            dict(
                title=item[title_str],
                key=str(item[key_str]),
                value=str(item[value_str]),
                parent_id=str(item[parent_id_str]),
            )
            for item in permission_list
        ]
        # 转成id为key的字典
        mapping: dict = dict(
            zip([i['key'] for i in permission_list], permission_list)
        )

        # 树容器
        container: list = []

        for d in permission_list:
            # 如果找不到父级项，则是根节点
            parent: dict = mapping.get(d['parent_id'])
            if parent is None:
                container.append(d)
            else:
                children: list = parent.get('children')
                if not children:
                    children = []
                children.append(d)
                parent.update({'children': children})

        return container

    @classmethod
    def get_search_panel_data(cls, menu_list: list):
        search_data = []
        for item in menu_list:
            if item.get('menu_type') == 'C' or item.get('is_frame') == 0:
                item_dict = dict(
                    id=str(item.get('menu_id')),
                    title=item.get('menu_name'),
                    handler='() => window.open("%s", "_self")'
                    % item.get('path'),
                )
                search_data.append(item_dict)

        return search_data

    @classmethod
    def find_tree_all_keys(cls, tree, keys_list):
        """
        递归函数，用于查找树形数据结构中所有键名为'name'的值，并将它们添加到列表中。

        :param tree: 树形数据结构，假设为嵌套字典或列表
        :param keys_list: 用于存储找到的'key'值的列表
        :return: 包含所有找到的'key'值的列表
        """
        if isinstance(tree, dict):
            for key, value in tree.items():
                if key == 'key':
                    keys_list.append(value)
                elif isinstance(value, (dict, list)):
                    cls.find_tree_all_keys(value, keys_list)
        elif isinstance(tree, list):
            for item in tree:
                cls.find_tree_all_keys(item, keys_list)

        return keys_list
