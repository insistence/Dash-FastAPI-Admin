from dash import html, dcc


def render_store_container():

    return html.Div(
        [
            # 接口校验返回存储容器
            dcc.Store(id='api-check-token'),
            # 接口校验返回存储容器
            dcc.Store(id='api-check-result-container'),
            # token存储容器
            dcc.Store(id='token-container'),
            # 菜单信息存储容器
            dcc.Store(id='menu-info-store-container'),
            dcc.Store(id='menu-list-store-container'),
            # 菜单current_key存储容器
            dcc.Store(id='current-key-container'),
            # 用户管理模块操作类型存储容器
            dcc.Store(id='user-operations-store'),
            # 用户管理模块修改操作行key存储容器
            dcc.Store(id='user-edit-id-store'),
            # 用户管理模块删除操作行key存储容器
            dcc.Store(id='user-delete-ids-store'),
            # 角色管理模块操作类型存储容器
            dcc.Store(id='role-operations-store'),
            dcc.Store(id='role-operations-store-bk'),
            # 角色管理模块修改操作行key存储容器
            dcc.Store(id='role-edit-id-store'),
            # 角色管理模块删除操作行key存储容器
            dcc.Store(id='role-delete-ids-store'),
            # 角色管理模块菜单权限存储容器
            dcc.Store(id='role-menu-store'),
            dcc.Store(id='current-role-menu-store'),
            # 菜单管理模块操作类型存储容器
            dcc.Store(id='menu-operations-store'),
            dcc.Store(id='menu-operations-store-bk'),
            # modal菜单类型存储容器
            dcc.Store(id='menu-modal-menu-type-store'),
            # 不同菜单类型的触发器
            dcc.Store(id='menu-modal-M-trigger'),
            dcc.Store(id='menu-modal-C-trigger'),
            dcc.Store(id='menu-modal-F-trigger'),
            # 菜单管理模块修改操作行key存储容器
            dcc.Store(id='menu-edit-id-store'),
            # 菜单管理模块删除操作行key存储容器
            dcc.Store(id='menu-delete-ids-store'),
            # 部门管理模块操作类型存储容器
            dcc.Store(id='dept-operations-store'),
            dcc.Store(id='dept-operations-store-bk'),
            # 部门管理模块修改操作行key存储容器
            dcc.Store(id='dept-edit-id-store'),
            # 部门管理模块删除操作行key存储容器
            dcc.Store(id='dept-delete-ids-store'),
            # 岗位管理模块操作类型存储容器
            dcc.Store(id='post-operations-store'),
            dcc.Store(id='post-operations-store-bk'),
            # 岗位管理模块修改操作行key存储容器
            dcc.Store(id='post-edit-id-store'),
            # 岗位管理模块删除操作行key存储容器
            dcc.Store(id='post-delete-ids-store'),
            # 字典管理模块操作类型存储容器
            dcc.Store(id='dict_type-operations-store'),
            dcc.Store(id='dict_type-operations-store-bk'),
            dcc.Store(id='dict_data-operations-store'),
            dcc.Store(id='dict_data-operations-store-bk'),
            # 字典管理模块修改操作行key存储容器
            dcc.Store(id='dict_type-edit-id-store'),
            dcc.Store(id='dict_data-edit-id-store'),
            # 字典管理模块删除操作行key存储容器
            dcc.Store(id='dict_type-delete-ids-store'),
            dcc.Store(id='dict_data-delete-ids-store'),
            # 操作日志管理模块操作类型存储容器
            dcc.Store(id='operation_log-operations-store'),
            # 操作日志管理模块删除操作行key存储容器
            dcc.Store(id='operation_log-delete-ids-store'),
            # 登录日志管理模块操作类型存储容器
            dcc.Store(id='login_log-operations-store'),
            # 操作日志管理模块删除操作行key存储容器
            dcc.Store(id='login_log-delete-ids-store'),
        ]
    )
