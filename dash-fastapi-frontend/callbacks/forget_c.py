import dash
from dash import dcc
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from server import app
from api.user import forget_user_pwd_api
from api.message import send_message_api


@app.callback(
    output=dict(
        username_form_status=Output('forget-username-form-item', 'validateStatus'),
        password_form_status=Output('forget-password-form-item', 'validateStatus'),
        password_again_form_status=Output('forget-password-again-form-item', 'validateStatus'),
        captcha_form_status=Output('forget-captcha-form-item', 'validateStatus'),
        username_form_help=Output('forget-username-form-item', 'help'),
        password_form_help=Output('forget-password-form-item', 'help'),
        password_again_form_help=Output('forget-password-again-form-item', 'help'),
        captcha_form_help=Output('forget-captcha-form-item', 'help'),
        submit_loading=Output('forget-submit', 'loading'),
        redirect_container=Output('redirect-container', 'children', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        nClicks=Input('forget-submit', 'nClicks')
    ),
    state=dict(
        username=State('forget-username', 'value'),
        password=State('forget-password', 'value'),
        password_again=State('forget-password-again', 'value'),
        input_captcha=State('forget-input-captcha', 'value'),
        session_id=State('sms_code-session_id-container', 'data')
    ),
    prevent_initial_call=True
)
def forget_auth(nClicks, username, password, password_again, input_captcha, session_id):
    if nClicks:
    # 校验全部输入值是否不为空
        if all([username, password, password_again, input_captcha]):

            if password == password_again:
                try:
                    forget_params = dict(user_name=username, password=password, sms_code=input_captcha, session_id=session_id)
                    change_result = forget_user_pwd_api(forget_params)
                    if change_result.get('code') == 200:

                        return dict(
                            username_form_status=None,
                            password_form_status=None,
                            password_again_form_status=None,
                            captcha_form_status=None,
                            username_form_help=None,
                            password_form_help=None,
                            password_again_form_help=None,
                            captcha_form_help=None,
                            submit_loading=False,
                            redirect_container=dcc.Location(pathname='/login', id='forget-redirect'),
                            global_message_container=fuc.FefferyFancyMessage(change_result.get('message'), type='success')
                        )

                    else:

                        return dict(
                            username_form_status=None,
                            password_form_status=None,
                            password_again_form_status=None,
                            captcha_form_status=None,
                            username_form_help=None,
                            password_form_help=None,
                            password_again_form_help=None,
                            captcha_form_help=None,
                            submit_loading=False,
                            redirect_container=None,
                            global_message_container=fuc.FefferyFancyMessage(change_result.get('message'), type='error')
                        )
                except Exception as e:

                    return dict(
                        username_form_status=None,
                        password_form_status=None,
                        password_again_form_status=None,
                        captcha_form_status=None,
                        username_form_help=None,
                        password_form_help=None,
                        password_again_form_help=None,
                        captcha_form_help=None,
                        submit_loading=False,
                        redirect_container=None,
                        global_message_container=fuc.FefferyFancyMessage(str(e), type='error')
                    )

            else:
                return dict(
                    username_form_status=None,
                    password_form_status='error',
                    password_again_form_status='error',
                    captcha_form_status=None,
                    username_form_help=None,
                    password_form_help='两次密码不一致',
                    password_again_form_help='两次密码不一致',
                    captcha_form_help=None,
                    submit_loading=False,
                    redirect_container=None,
                    global_message_container=None
                )

        return dict(
            username_form_status=None if username else 'error',
            password_form_status=None if password else 'error',
            password_again_form_status=None if password_again else 'error',
            captcha_form_status=None if input_captcha else 'error',
            username_form_help=None if username else '请输入用户名！',
            password_form_help=None if password else '请输入新密码！',
            password_again_form_help=None if password_again else '请再次输入新密码！',
            captcha_form_help=None if input_captcha else '请输入短信验证码！',
            submit_loading=False,
            redirect_container=None,
            global_message_container=None
        )

    raise PreventUpdate


@app.callback(
    [Output('message-code-count-down', 'delay'),
     Output('get-message-code', 'disabled', allow_duplicate=True),
     Output('sms_code-session_id-container', 'data'),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('get-message-code', 'nClicks'),
    [State('forget-username', 'value'),
     State('sms_code-session_id-container', 'data')],
    prevent_initial_call=True
)
def message_countdown(nClicks, username, session_id):
    if nClicks:

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

    return [dash.no_update] * 4


app.clientside_callback(
    '''
    (countdown) => {
        if (countdown) {
            return true;
        }
        return false;
    }
    ''',
    Output('get-message-code', 'disabled', allow_duplicate=True),
    Input('message-code-count-down', 'countdown'),
    prevent_initial_call=True
)


app.clientside_callback(
    '''
    (countdown) => {
         if (countdown) {
            return `获取中${countdown}s`
         }
         return '获取验证码'
    }
    ''',
    Output('get-message-code', 'children'),
    Input('message-code-count-down', 'countdown'),
    prevent_initial_call=True
)
