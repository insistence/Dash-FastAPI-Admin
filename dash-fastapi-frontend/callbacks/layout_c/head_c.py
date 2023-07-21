import dash
from dash import dcc
from flask import session
import time
from dash.dependencies import Input, Output, State

from server import app
from api.login import logout_api


# 页首右侧个人中心选项卡回调
@app.callback(
    [Output('dcc-url', 'pathname', allow_duplicate=True),
     Output('logout-modal', 'visible')],
    Input('index-header-dropdown', 'nClicks'),
    State('index-header-dropdown', 'clickedKey'),
    prevent_initial_call=True
)
def index_dropdown_click(nClicks, clickedKey):
    if clickedKey == '退出登录':
        return [
            dash.no_update,
            True
        ]

    elif clickedKey == '个人资料':
        return [
            '/user/profile',
            False
        ]

    return [dash.no_update] * 2


# 退出登录回调
@app.callback(
    Output('redirect-container', 'children', allow_duplicate=True),
    Input('logout-modal', 'okCounts'),
    prevent_initial_call=True
)
def logout_confirm(okCounts):
    if okCounts:
        result = logout_api()
        if result['code'] == 200:
            session.clear()

            return [
                dcc.Location(
                    pathname='/login',
                    id='index-redirect'
                ),
            ]

    return dash.no_update


# 全局页面重载回调
@app.callback(
    Output('trigger-reload-output', 'reload'),
    Input('index-reload', 'nClicks'),
    prevent_initial_call=True
)
def reload_page(nClicks):
    return True
