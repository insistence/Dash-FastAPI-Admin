import dash
from dash import dcc
import feffery_utils_components as fuc
from flask import session
import time
from dash.dependencies import Input, Output, State

from server import app
from api.login import logout_api


# 页首右侧个人中心选项卡回调
@app.callback(
    [Output('dcc-url', 'pathname', allow_duplicate=True),
     Output('logout-modal', 'visible'),
     Output('layout-setting-drawer', 'visible')],
    Input('index-header-dropdown', 'nClicks'),
    State('index-header-dropdown', 'clickedKey'),
    prevent_initial_call=True
)
def index_dropdown_click(nClicks, clickedKey):
    if clickedKey == '退出登录':
        return [
            dash.no_update,
            True,
            False
        ]

    elif clickedKey == '个人资料':
        return [
            '/user/profile',
            False,
            False
        ]

    elif clickedKey == '布局设置':
        return [
            dash.no_update,
            False,
            True
        ]

    return [dash.no_update] * 3


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


# 布局设置回调
@app.callback(
    Output('hex-color-picker', 'color', allow_duplicate=True),
    Input('layout-setting-drawer', 'visible'),
    State('custom-app-primary-color-container', 'data'),
    prevent_initial_call=True
)
def init_hex_color_picker(visible, custom_color):
    if visible:
        if custom_color:
            return custom_color
    return dash.no_update


@app.callback(
    [Output('selected-color-input', 'value'),
     Output('selected-color-input', 'style')],
    Input('hex-color-picker', 'color'),
    State('selected-color-input', 'style'),
    prevent_initial_call=True
)
def show_selected_color(pick_color, old_style):

    return [
        pick_color,
        {
            **old_style,
            'background': pick_color
        }
    ]


@app.callback(
    [Output('custom-app-primary-color-container', 'data'),
     Output('hex-color-picker', 'color', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    [Input('save-setting', 'nClicks'),
     Input('reset-setting', 'nClicks')],
    [State('selected-color-input', 'value'),
     State('system-app-primary-color-container', 'data')],
    prevent_initial_call=True
)
def save_rest_layout_setting(save_click, reset_click, picked_color, system_color):
    if save_click or reset_click:
        trigger_id = dash.ctx.triggered_id
        if trigger_id == 'save-setting':

            return [
                picked_color,
                dash.no_update,
                fuc.FefferyFancyMessage('保存成功', type='success')
            ]

        elif trigger_id == 'reset-setting':

            return [
                None,
                system_color,
                fuc.FefferyFancyMessage('重置成功', type='success')
            ]

    return [
        dash.no_update,
        dash.no_update,
        dash.no_update
    ]

