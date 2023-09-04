import dash
from dash import dcc
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State

from server import app
from api.user import forget_user_pwd_api
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
     Output('forget-submit', 'loading'),
     Output('redirect-container', 'children', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('forget-submit', 'nClicks'),
    [State('forget-username', 'value'),
     State('forget-password', 'value'),
     State('forget-password-again', 'value'),
     State('forget-input-captcha', 'value'),
     State('sms_code-session_id-container', 'data')],
    prevent_initial_call=True
)
def login_auth(nClicks, username, password, password_again, input_captcha, session_id):
    if nClicks:
    # 校验全部输入值是否不为空
        if all([username, password, password_again, input_captcha]):

            if password == password_again:
                try:
                    forget_params = dict(user_name=username, password=password, sms_code=input_captcha, session_id=session_id)
                    change_result = forget_user_pwd_api(forget_params)
                    if change_result.get('code') == 200:

                        return [
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            None,
                            True,
                            dcc.Location(
                                pathname='/login',
                                id='forget-redirect'
                            ),
                            fuc.FefferyFancyMessage(change_result.get('message'), type='success')
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
                            False,
                            None,
                            fuc.FefferyFancyMessage(change_result.get('message'), type='error')
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
                        False,
                        None,
                        fuc.FefferyFancyMessage(str(e), type='error')
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
            False,
            None,
            None
        ]

    return [dash.no_update] * 11


@app.callback(
    [Output('message-code-count-down', 'delay'),
     Output('get-message-code', 'disabled'),
     Output('sms_code-session_id-container', 'data'),
     Output('global-message-container', 'children', allow_duplicate=True)],
    [Input('get-message-code', 'nClicks'),
     Input('message-code-count-down', 'countdown')],
    [State('forget-username', 'value'),
     State('sms_code-session_id-container', 'data')],
    prevent_initial_call=True
)
def message_countdown(nClicks, countdown, username, session_id):
    if nClicks:

        if dash.ctx.triggered_id == 'get-message-code':

            try:
                if username:
                    send_result = send_message_api(dict(user_name=username, session_id=session_id))
                    if send_result.get('code') == 200:

                        return [
                            120,
                            True,
                            send_result.get('data').get('session_id'),
                            fuc.FefferyFancyMessage(send_result.get('message'), type='success')
                        ]
                    else:

                        return [
                            dash.no_update,
                            False,
                            dash.no_update,
                            fuc.FefferyFancyMessage(send_result.get('message'), type='error')
                        ]

                else:
                    return [
                        dash.no_update,
                        False,
                        dash.no_update,
                        fuc.FefferyFancyMessage('请输入用户名', type='error')
                    ]

            except Exception as e:

                return [
                    dash.no_update,
                    False,
                    dash.no_update,
                    fuc.FefferyFancyMessage(str(e), type='error')
                ]

        if dash.ctx.triggered_id == 'message-code-count-down':
            if countdown:
                return [
                    dash.no_update, True, dash.no_update, dash.no_update
                ]

            return dash.no_update, False, dash.no_update, dash.no_update

    return [dash.no_update] * 4


@app.callback(
    Output('get-message-code', 'children'),
    Input('message-code-count-down', 'countdown'),
    prevent_initial_call=True
)
def update_button_content(countdown):
    if countdown:
        return f"获取中{countdown}s"

    return "获取验证码"
