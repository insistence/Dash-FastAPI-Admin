import feffery_antd_components as fac
from dash import dcc, get_asset_url, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from flask import session
from api.login import LoginApi
from server import app
from utils.common import validate_data_not_empty
from utils.feedback_util import MessageManager


@app.callback(
    output=dict(
        username_form_status=Output(
            'login-username-form-item', 'validateStatus'
        ),
        password_form_status=Output(
            'login-password-form-item', 'validateStatus'
        ),
        captcha_form_status=Output('login-captcha-form-item', 'validateStatus'),
        username_form_help=Output('login-username-form-item', 'help'),
        password_form_help=Output('login-password-form-item', 'help'),
        captcha_form_help=Output('login-captcha-form-item', 'help'),
        token=Output('token-container', 'data'),
        redirect_container=Output(
            'redirect-container', 'children', allow_duplicate=True
        ),
    ),
    inputs=dict(nClicks=Input('login-submit', 'nClicks')),
    state=dict(
        username=State('login-username', 'value'),
        password=State('login-password', 'value'),
        input_captcha=State('login-captcha', 'value'),
        session_id=State('captcha_image-session_id-container', 'data'),
        captcha_hidden=State('captcha-row-container', 'hidden'),
    ),
    running=[
        [Output('login-submit', 'loading'), True, False],
        [Output('login-captcha-image-container', 'n_clicks'), 0, 1],
    ],
    prevent_initial_call=True,
)
def login_auth(
    nClicks,
    username,
    password,
    input_captcha,
    session_id,
    captcha_hidden,
):
    if nClicks:
        validate_list = [username, password, input_captcha]
        if captcha_hidden:
            validate_list = [username, password]
        # 校验全部输入值是否不为空
        if all(validate_data_not_empty(item) for item in validate_list):
            user_params = dict(
                username=username,
                password=password,
                code=input_captcha,
                uuid=session_id,
            )
            userinfo_result = LoginApi.login(user_params)
            token = userinfo_result['token']
            session['Authorization'] = token
            MessageManager.success(content='登录成功')
            return dict(
                username_form_status=None,
                password_form_status=None,
                captcha_form_status=None,
                username_form_help=None,
                password_form_help=None,
                captcha_form_help=None,
                token=token,
                redirect_container=dcc.Location(
                    pathname='/', id='login-redirect'
                ),
            )

        return dict(
            username_form_status=None
            if validate_data_not_empty(username)
            else 'error',
            password_form_status=None
            if validate_data_not_empty(password)
            else 'error',
            captcha_form_status=None
            if validate_data_not_empty(input_captcha)
            else 'error',
            username_form_help=None
            if validate_data_not_empty(username)
            else '请输入用户名！',
            password_form_help=None
            if validate_data_not_empty(password)
            else '请输入密码！',
            captcha_form_help=None
            if validate_data_not_empty(input_captcha)
            else '请输入验证码！',
            token=None,
            redirect_container=None,
        )

    return dict(
        username_form_status=no_update,
        password_form_status=no_update,
        captcha_form_status=no_update,
        username_form_help=no_update,
        password_form_help=no_update,
        captcha_form_help=no_update,
        token=no_update,
        redirect_container=no_update,
    )


@app.callback(
    [
        Output('captcha-row-container', 'hidden'),
        Output('register-user-link-container', 'children'),
        Output('forget-password-link-container', 'children'),
        Output('login-captcha-image', 'src'),
        Output('captcha_image-session_id-container', 'data'),
    ],
    Input('login-captcha-image-container', 'n_clicks'),
    State('redirect-container', 'children'),
    prevent_initial_call=True,
)
def change_login_captcha_image(captcha_click, redirect):
    if captcha_click and not redirect:
        captcha_image_info = LoginApi.get_code_img()
        captcha_enabled = captcha_image_info.get('captcha_enabled')
        forget_enabled = captcha_image_info.get('forget_enabled')
        register_enabled = captcha_image_info.get('register_enabled')
        captcha_image = f"data:image/gif;base64,{captcha_image_info.get('img')}"
        session_id = captcha_image_info.get('uuid')

        return [
            not captcha_enabled,
            fac.AntdButton(
                '用户注册',
                id='register-user-link',
                type='link',
                href='/register',
                target='_self',
                style={'padding': 0},
            )
            if register_enabled
            else [],
            fac.AntdButton(
                '忘记密码',
                id='forget-password-link',
                type='link',
                href='/forget',
                target='_self',
                style={'padding': 0},
            )
            if forget_enabled
            else [],
            captcha_image,
            session_id,
        ]

    raise PreventUpdate


@app.callback(
    Output('container', 'style'),
    Input('url-container', 'pathname'),
    State('container', 'style'),
)
def random_bg(pathname, old_style):
    return {
        **old_style,
        'backgroundImage': 'url({})'.format(
            get_asset_url('imgs/login-background.jpg')
        ),
        'backgroundRepeat': 'no-repeat',
        'backgroundSize': 'cover',
    }
