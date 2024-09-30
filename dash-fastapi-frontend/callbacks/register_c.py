import time
from dash import dcc, get_asset_url, no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from api.login import LoginApi
from api.register import RegisterApi
from server import app
from utils.common_util import ValidateUtil
from utils.feedback_util import MessageManager


@app.callback(
    output=dict(
        username_form_status=Output(
            'register-username-form-item', 'validateStatus'
        ),
        password_form_status=Output(
            'register-password-form-item', 'validateStatus'
        ),
        confirm_password_form_status=Output(
            'register-confirm_password-form-item', 'validateStatus'
        ),
        captcha_form_status=Output(
            'register-captcha-form-item', 'validateStatus'
        ),
        username_form_help=Output('register-username-form-item', 'help'),
        password_form_help=Output('register-password-form-item', 'help'),
        confirm_password_form_help=Output(
            'register-confirm_password-form-item', 'help'
        ),
        captcha_form_help=Output('register-captcha-form-item', 'help'),
        redirect_container=Output(
            'redirect-container', 'children', allow_duplicate=True
        ),
        register_success=Output('register-success-container', 'data'),
    ),
    inputs=dict(
        button_click=Input('register-submit', 'nClicks'),
        keyboard_enter_press=Input(
            'register-keyboard-enter-submit', 'pressedCounts'
        ),
    ),
    state=dict(
        username=State('register-username', 'value'),
        password=State('register-password', 'value'),
        confirm_password=State('register-confirm_password', 'value'),
        input_captcha=State('register-captcha', 'value'),
        session_id=State('register-captcha_image-session_id-container', 'data'),
        captcha_hidden=State('register-captcha-row-container', 'hidden'),
    ),
    running=[
        [Output('register-submit', 'loading'), True, False],
        [Output('register-submit', 'children'), '注册中', '注册'],
        [Output('register-captcha-image-container', 'n_clicks'), 0, 1],
    ],
    prevent_initial_call=True,
)
def register(
    button_click,
    keyboard_enter_press,
    username,
    password,
    confirm_password,
    input_captcha,
    session_id,
    captcha_hidden,
):
    if button_click or keyboard_enter_press:
        validate_list = [username, password, confirm_password, input_captcha]
        if captcha_hidden:
            validate_list = [username, password, confirm_password]
        # 校验全部输入值是否不为空
        if all(ValidateUtil.not_empty(item) for item in validate_list):
            if password == confirm_password:
                register_params = dict(
                    username=username,
                    password=password,
                    confirm_password=confirm_password,
                    code=input_captcha,
                    uuid=session_id,
                )
                RegisterApi.register(register_params)
                MessageManager.success(content='注册成功')
                return dict(
                    username_form_status=None,
                    password_form_status=None,
                    confirm_password_form_status=None,
                    captcha_form_status=None,
                    username_form_help=None,
                    password_form_help=None,
                    confirm_password_form_help=None,
                    captcha_form_help=None,
                    redirect_container=dcc.Location(
                        pathname='/', id='register-redirect'
                    ),
                    register_success={'timestamp': time.time()},
                )
            else:
                MessageManager.warning(content='两次输入的密码不一致！')
                return dict(
                    username_form_status=None,
                    password_form_status='error',
                    confirm_password_form_status='error',
                    captcha_form_status=None,
                    username_form_help=None,
                    password_form_help='两次输入的密码不一致！',
                    confirm_password_form_help='两次输入的密码不一致！',
                    captcha_form_help=None,
                    redirect_container=None,
                    register_success=None,
                )

        return dict(
            username_form_status=None
            if ValidateUtil.not_empty(username)
            else 'error',
            password_form_status=None
            if ValidateUtil.not_empty(password)
            else 'error',
            confirm_password_form_status=None
            if ValidateUtil.not_empty(confirm_password)
            else 'error',
            captcha_form_status=None
            if ValidateUtil.not_empty(input_captcha)
            else 'error',
            username_form_help=None
            if ValidateUtil.not_empty(username)
            else '请输入用户名！',
            password_form_help=None
            if ValidateUtil.not_empty(password)
            else '请输入密码！',
            confirm_password_form_help=None
            if ValidateUtil.not_empty(confirm_password)
            else '请再次输入密码！',
            captcha_form_help=None
            if ValidateUtil.not_empty(input_captcha)
            else '请输入验证码！',
            redirect_container=None,
            register_success=None,
        )

    return dict(
        username_form_status=no_update,
        password_form_status=no_update,
        confirm_password_form_status=no_update,
        captcha_form_status=no_update,
        username_form_help=no_update,
        password_form_help=no_update,
        confirm_password_form_help=no_update,
        captcha_form_help=no_update,
        redirect_container=no_update,
        register_success=None,
    )


@app.callback(
    [
        Output('register-captcha-row-container', 'hidden'),
        Output('register-captcha-image', 'src'),
        Output('register-captcha_image-session_id-container', 'data'),
    ],
    Input('register-captcha-image-container', 'n_clicks'),
    State('register-success-container', 'data'),
    prevent_initial_call=True,
)
def change_register_captcha_image(captcha_click, login_success):
    if captcha_click and not login_success:
        captcha_image_info = LoginApi.get_code_img()
        captcha_enabled = captcha_image_info.get('captcha_enabled')
        captcha_image = f"data:image/gif;base64,{captcha_image_info.get('img')}"
        session_id = captcha_image_info.get('uuid')

        return [
            not captcha_enabled,
            captcha_image,
            session_id,
        ]

    raise PreventUpdate


@app.callback(
    Output('register-page', 'style'),
    Input('url-container', 'pathname'),
)
def random_register_bg(pathname):
    return {
        'height': '100vh',
        'overflow': 'auto',
        'WebkitBackgroundSize': '100% 100%',
        'backgroundSize': '100% 100',
        'backgroundImage': 'url({})'.format(
            get_asset_url('imgs/background.png')
        ),
    }
