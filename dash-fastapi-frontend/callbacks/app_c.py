import dash
from dash import dcc
import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from flask import session, request
from server import app, logger


# api拦截器——根据api返回编码确定是否强制退出
@app.callback(
    [Output('token-invalid-modal', 'visible'),
     Output('global-notification-container', 'children', allow_duplicate=True)],
    Input('api-check-token', 'data'),
    prevent_initial_call=True
)
def check_api_response(data):

    if session.get('code') == 401:
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
