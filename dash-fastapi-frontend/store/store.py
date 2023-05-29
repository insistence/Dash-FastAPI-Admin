from dash import html, dcc


def render_store_container():
    return html.Div(
        [
            dcc.Store(id='api-check-token'),
            # 接口校验返回存储容器
            dcc.Store(id='api-check-result-container'),
            # token存储容器
            dcc.Store(id='token-container'),
            # 菜单current_key存储容器
            dcc.Store(id='current-key-container')
        ]
    )
