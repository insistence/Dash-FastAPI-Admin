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
            # 菜单current_key存储容器
            dcc.Store(id='current-key-container'),
            # 用户管理模块操作类型存储容器
            dcc.Store(id='user-operations-store'),
            # 用户管理模块修改操作行key存储容器
            dcc.Store(id='user-edit-id-store'),
            # 用户管理模块删除操作行key存储容器
            dcc.Store(id='user-delete-ids-store'),
            # 部门管理模块操作类型存储容器
            dcc.Store(id='dept-operations-store'),
            # 部门管理模块修改操作行key存储容器
            dcc.Store(id='dept-edit-id-store'),
            # 部门管理模块删除操作行key存储容器
            dcc.Store(id='dept-delete-ids-store'),
            # 岗位管理模块操作类型存储容器
            dcc.Store(id='post-operations-store'),
            # 岗位管理模块修改操作行key存储容器
            dcc.Store(id='post-edit-id-store'),
            # 岗位管理模块删除操作行key存储容器
            dcc.Store(id='post-delete-ids-store'),
        ]
    )
