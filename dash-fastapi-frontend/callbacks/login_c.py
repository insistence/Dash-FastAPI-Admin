from dash import dcc, get_asset_url, no_update
from dash.dependencies import Input, Output, State
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
        image_click=Output('login-captcha-image-container', 'n_clicks'),
        submit_loading=Output('login-submit', 'loading'),
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
        image_click=State('login-captcha-image-container', 'n_clicks'),
        captcha_hidden=State('captcha-row-container', 'hidden'),
    ),
    prevent_initial_call=True,
)
def login_auth(
    nClicks,
    username,
    password,
    input_captcha,
    session_id,
    image_click,
    captcha_hidden,
):
    if nClicks:
        if captcha_hidden:
            input_captcha = 'hidden'
        # 校验全部输入值是否不为空
        if all(
            validate_data_not_empty(item)
            for item in [username, password, input_captcha]
        ):
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
                image_click=no_update,
                submit_loading=False,
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
            image_click=no_update,
            submit_loading=False,
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
        image_click=image_click + 1,
        submit_loading=no_update,
        token=no_update,
        redirect_container=no_update,
    )


@app.callback(
    [
        Output('login-captcha-image', 'src'),
        Output('captcha_image-session_id-container', 'data'),
    ],
    Input('login-captcha-image-container', 'n_clicks'),
    prevent_initial_call=True,
)
def change_login_captcha_image(captcha_click):
    if captcha_click:
        captcha_image_info = LoginApi.get_code_img()
        captcha_image = f"data:image/gif;base64,{captcha_image_info.get('img')}"
        session_id = captcha_image_info.get('uuid')

        return [
            captcha_image,
            session_id,
        ]

    return [no_update] * 2


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
