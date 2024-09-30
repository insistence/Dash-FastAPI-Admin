from dash import dcc, get_asset_url, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from api.forget import ForgetApi
from server import app
from utils.common_util import ValidateUtil
from utils.feedback_util import MessageManager


@app.callback(
    output=dict(
        username_form_status=Output(
            'forget-username-form-item', 'validateStatus'
        ),
        password_form_status=Output(
            'forget-password-form-item', 'validateStatus'
        ),
        password_again_form_status=Output(
            'forget-password-again-form-item', 'validateStatus'
        ),
        captcha_form_status=Output(
            'forget-captcha-form-item', 'validateStatus'
        ),
        username_form_help=Output('forget-username-form-item', 'help'),
        password_form_help=Output('forget-password-form-item', 'help'),
        password_again_form_help=Output(
            'forget-password-again-form-item', 'help'
        ),
        captcha_form_help=Output('forget-captcha-form-item', 'help'),
        redirect_container=Output(
            'redirect-container', 'children', allow_duplicate=True
        ),
    ),
    inputs=dict(nClicks=Input('forget-submit', 'nClicks')),
    state=dict(
        username=State('forget-username', 'value'),
        password=State('forget-password', 'value'),
        password_again=State('forget-password-again', 'value'),
        input_captcha=State('forget-input-captcha', 'value'),
        session_id=State('sms_code-session_id-container', 'data'),
    ),
    running=[
        [Output('forget-submit', 'loading'), True, False],
        [Output('forget-submit', 'children'), '保存中', '保存'],
    ],
    prevent_initial_call=True,
)
def forget_auth(
    nClicks, username, password, password_again, input_captcha, session_id
):
    if nClicks:
        # 校验全部输入值是否不为空
        if all(
            ValidateUtil.not_empty(item)
            for item in [username, password, password_again, input_captcha]
        ):
            if password == password_again:
                forget_params = dict(
                    user_name=username,
                    password=password,
                    sms_code=input_captcha,
                    session_id=session_id,
                )
                ForgetApi.forget_password(forget_params)
                MessageManager.success(content='重置成功')
                return dict(
                    username_form_status=None,
                    password_form_status=None,
                    password_again_form_status=None,
                    captcha_form_status=None,
                    username_form_help=None,
                    password_form_help=None,
                    password_again_form_help=None,
                    captcha_form_help=None,
                    redirect_container=dcc.Location(
                        pathname='/login', id='forget-redirect'
                    ),
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
                    redirect_container=None,
                )

        return dict(
            username_form_status=None
            if ValidateUtil.not_empty(username)
            else 'error',
            password_form_status=None
            if ValidateUtil.not_empty(password)
            else 'error',
            password_again_form_status=None
            if ValidateUtil.not_empty(password_again)
            else 'error',
            captcha_form_status=None
            if ValidateUtil.not_empty(input_captcha)
            else 'error',
            username_form_help=None
            if ValidateUtil.not_empty(username)
            else '请输入用户名！',
            password_form_help=None
            if ValidateUtil.not_empty(password)
            else '请输入新密码！',
            password_again_form_help=None
            if ValidateUtil.not_empty(password_again)
            else '请再次输入新密码！',
            captcha_form_help=None
            if ValidateUtil.not_empty(input_captcha)
            else '请输入短信验证码！',
            redirect_container=None,
        )

    raise PreventUpdate


@app.callback(
    [
        Output('message-code-count-down', 'delay'),
        Output('get-message-code', 'disabled', allow_duplicate=True),
        Output('sms_code-session_id-container', 'data'),
    ],
    Input('get-message-code', 'nClicks'),
    [
        State('forget-username', 'value'),
        State('sms_code-session_id-container', 'data'),
    ],
    prevent_initial_call=True,
)
def message_countdown(nClicks, username, session_id):
    if nClicks:
        if username:
            send_result = ForgetApi.send_message(
                dict(user_name=username, session_id=session_id)
            )
            MessageManager.success(content='获取成功')
            return [
                120,
                True,
                send_result.get('data').get('session_id'),
            ]

        else:
            MessageManager.error(content='请输入用户名')
            return [
                no_update,
                False,
                no_update,
            ]

    raise PreventUpdate


@app.callback(
    Output('forget-page', 'style'),
    Input('url-container', 'pathname'),
)
def random_forget_bg(pathname):
    return {
        'height': '100vh',
        'overflow': 'auto',
        'WebkitBackgroundSize': '100% 100%',
        'backgroundSize': '100% 100',
        'backgroundImage': 'url({})'.format(
            get_asset_url('imgs/background.png')
        ),
    }


app.clientside_callback(
    """
    (countdown) => {
        if (countdown) {
            return true;
        }
        return false;
    }
    """,
    Output('get-message-code', 'disabled', allow_duplicate=True),
    Input('message-code-count-down', 'countdown'),
    prevent_initial_call=True,
)


app.clientside_callback(
    """
    (countdown) => {
         if (countdown) {
            return `${countdown}秒后重新获取`
         }
         return '获取验证码'
    }
    """,
    Output('get-message-code', 'children'),
    Input('message-code-count-down', 'countdown'),
    prevent_initial_call=True,
)
