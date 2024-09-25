from dash import html, dcc


def render_store_container():
    return html.Div(
        [
            # 应用主题颜色存储容器
            dcc.Store(id='system-app-primary-color-container', data='#1890ff'),
            dcc.Store(
                id='custom-app-primary-color-container', storage_type='session'
            ),
            # 接口校验返回存储容器
            dcc.Store(id='api-check-result-container'),
            # token存储容器
            dcc.Store(id='token-container', storage_type='session'),
            # 当前路由存储容器
            dcc.Store(id='current-pathname-container'),
            # 路由列表存储容器
            dcc.Store(id='router-list-container'),
        ]
    )
