from dash import html, dcc


def render_store_container():

    return html.Div(
        [
            # 应用主题颜色存储容器
            dcc.Store(id='system-app-primary-color-container', data='#1890ff'),
            dcc.Store(id='custom-app-primary-color-container', storage_type='session'),
            # 接口校验返回存储容器
            dcc.Store(id='api-check-token'),
            # 接口校验返回存储容器
            dcc.Store(id='api-check-result-container'),
            # token存储容器
            dcc.Store(id='token-container', storage_type='session'),
            # 菜单信息存储容器
            dcc.Store(id='menu-info-store-container'),
            dcc.Store(id='menu-list-store-container'),
            # 菜单current_key存储容器
            dcc.Store(id='current-key-container'),
        ]
    )
