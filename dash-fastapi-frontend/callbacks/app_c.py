import dash
from dash import dcc
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from flask import session
from server import app
from api.config import query_config_list_api


# api拦截器——根据api返回编码确定是否强制退出
@app.callback(
    [Output('token-invalid-modal', 'visible'),
     Output('global-notification-container', 'children', allow_duplicate=True)],
    Input('api-check-token', 'data'),
    prevent_initial_call=True
)
def check_api_response(data):

    if session.get('code') == 401 and 'token' in session.get('message'):
        return [True, fuc.FefferyFancyNotification(session.get('message'), type='error', autoClose=2000)]

    elif session.get('code') == 200:
        return [dash.no_update, dash.no_update]

    else:
        return [dash.no_update, fuc.FefferyFancyNotification(session.get('message'), type='warning', autoClose=2000)]


# api拦截器——退出登录二次确认
@app.callback(
    Output('redirect-container', 'children', allow_duplicate=True),
    Input('token-invalid-modal', 'okCounts'),
    prevent_initial_call=True
)
def redirect_page(okCounts):

    if okCounts:
        session.clear()

        return [
            dcc.Location(
                pathname='/login',
                id='index-redirect'
            )
        ]

    return dash.no_update


# 应用初始化主题颜色
@app.callback(
    Output('system-app-primary-color-container', 'data'),
    Input('app-mount', 'id'),
    State('custom-app-primary-color-container', 'data')
)
def get_primary_color(_, custom_color):
    if not custom_color:
        primary_color_res = query_config_list_api(config_key='sys.index.skinName')
        if primary_color_res.get('code') == 200:
            primary_color = primary_color_res.get('data')

            return primary_color

    return dash.no_update


@app.callback(
    Output('app-config-provider', 'primaryColor'),
    [Input('system-app-primary-color-container', 'data'),
     Input('custom-app-primary-color-container', 'data')],
    prevent_initial_call=True
)
def render_app_primary_color(system_color, custom_color):
    if custom_color:
        return custom_color

    return system_color
