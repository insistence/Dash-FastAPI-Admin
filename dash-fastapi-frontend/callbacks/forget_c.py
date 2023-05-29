import dash
from dash import dcc
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from flask import session, request

from server import app, logger
from api.user import change_password_api
from api.message import send_message_api


@app.callback(
    [Output('forget-username-form-item', 'validateStatus'),
     Output('forget-password-form-item', 'validateStatus'),
     Output('forget-password-again-form-item', 'validateStatus'),
     Output('forget-captcha-form-item', 'validateStatus'),
     Output('forget-username-form-item', 'help'),
     Output('forget-password-form-item', 'help'),
     Output('forget-password-again-form-item', 'help'),
     Output('forget-captcha-form-item', 'help'),
     Output('forget-submit', 'children'),
     Output('forget-submit', 'loading'),
     Output('forget-redirect-container', 'children'),
     Output('forget-message-container', 'children')],
    Input('forget-submit', 'nClicks'),
    [State('forget-username', 'value'),
     State('forget-password', 'value'),
     State('forget-password-again', 'value'),
     State('forget-input-captcha', 'value')],
    prevent_initial_call=True
)
def login_auth(nClicks, username, password, password_again, input_captcha):
    # 校验全部输入值是否不为空
    if all([nClicks, username, password, password_again, input_captcha]):

        if username:

            if password:

                if password_again:

                    if input_captcha:

                        if password == password_again:
                            try:
                                change_result = change_password_api(username, password, input_captcha)
                                if change_result['code'] == 200:

                                    return [
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        '保存中',
                                        True,
                                        dcc.Location(
                                            pathname='/login',
                                            id='forget-redirect'
                                        ),
                                        None
                                    ]

                                elif change_result['message'] == '用户不存在':

                                    return [
                                        'error',
                                        None,
                                        None,
                                        None,
                                        '用户不存在',
                                        None,
                                        None,
                                        None,
                                        '保存',
                                        False,
                                        None,
                                        None
                                    ]

                                elif change_result['message'] == '验证码错误':

                                    return [
                                        None,
                                        None,
                                        None,
                                        'error',
                                        None,
                                        None,
                                        None,
                                        '验证码错误！',
                                        '保存',
                                        False,
                                        None,
                                        None
                                    ]

                                elif change_result['message'] == '验证码校验失败':

                                    return [
                                        None,
                                        None,
                                        None,
                                        'error',
                                        None,
                                        None,
                                        None,
                                        '验证码校验失败！',
                                        '保存',
                                        False,
                                        None,
                                        None
                                    ]

                                else:

                                    return [
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        None,
                                        '保存',
                                        False,
                                        None,
                                        fuc.FefferyFancyMessage(change_result['message'], type='error')
                                    ]
                            except Exception as e:

                                return [
                                    None,
                                    None,
                                    None,
                                    None,
                                    None,
                                    None,
                                    None,
                                    None,
                                    '保存',
                                    False,
                                    None,
                                    fuc.FefferyFancyMessage('接口异常', type='error')
                                ]

                        else:
                            return [
                                None,
                                'error',
                                'error',
                                None,
                                None,
                                '两次密码不一致',
                                '两次密码不一致',
                                None,
                                '保存',
                                False,
                                None,
                                None
                            ]

                    else:
                        return [
                            None,
                            None,
                            None,
                            'error',
                            None,
                            None,
                            None,
                            '请输入验证码!',
                            '保存',
                            False,
                            None,
                            None
                        ]

                else:
                    return [
                        None,
                        None,
                        'error',
                        None,
                        None,
                        None,
                        '请再次输入新密码!',
                        None,
                        '保存',
                        False,
                        None,
                        None
                    ]

            else:
                return [
                    None,
                    'error',
                    None,
                    None,
                    None,
                    '请输入新密码!',
                    None,
                    None,
                    '保存',
                    False,
                    None,
                    None
                ]

        else:
            return [
                'error',
                None,
                None,
                None,
                '请输入用户名!',
                None,
                None,
                None,
                '保存',
                False,
                None,
                None
            ]

    return [
        None if username else 'error',
        None if password else 'error',
        None if password_again else 'error',
        None if input_captcha else 'error',
        None if username else '请输入用户名！',
        None if password else '请输入新密码！',
        None if password_again else '请再次输入新密码！',
        None if input_captcha else '请输入短信验证码！',
        '保存',
        False,
        None,
        None
    ]


@app.callback(
    [Output('message-code-count-down', 'delay'),
     Output('get-message-code', 'disabled'),
     Output('forget-sms-container', 'children')],
    [Input('get-message-code', 'nClicks'),
     Input('message-code-count-down', 'countdown')],
    State('forget-username', 'value'),
    prevent_initial_call=True
)
def message_countdown(nClicks, countdown, username):

    if dash.ctx.triggered_id == 'get-message-code':

        try:
            if username:
                send_result = send_message_api(username)
                if send_result['code'] == 200:

                    return [
                        120,
                        True,
                        fuc.FefferyFancyMessage(send_result['message'], type='success')
                    ]
                else:

                    return [
                        dash.no_update,
                        False,
                        fuc.FefferyFancyMessage(send_result['message'], type='error')
                    ]

            else:
                return [
                    dash.no_update,
                    False,
                    fuc.FefferyFancyMessage('请输入用户名', type='error')
                ]

        except Exception as e:

            return [
                dash.no_update,
                False,
                fuc.FefferyFancyMessage('短信接口异常', type='error')
            ]

    if dash.ctx.triggered_id == 'message-code-count-down':
        if countdown:
            return [
                dash.no_update, True, dash.no_update
            ]

        return dash.no_update, False, dash.no_update


@app.callback(
    Output('get-message-code', 'children'),
    Input('message-code-count-down', 'countdown'),
    prevent_initial_call=True
)
def update_button_content(countdown):
    if countdown:
        return f"获取中{countdown}s"

    return "获取验证码"
