import dash
from dash import dcc
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from flask import session
import time

from server import app
from api.login import login_api, get_captcha_image_api


@app.callback(
    output=dict(
        username_form_status=Output('login-username-form-item', 'validateStatus'),
        password_form_status=Output('login-password-form-item', 'validateStatus'),
        captcha_form_status=Output('login-captcha-form-item', 'validateStatus'),
        username_form_help=Output('login-username-form-item', 'help'),
        password_form_help=Output('login-password-form-item', 'help'),
        captcha_form_help=Output('login-captcha-form-item', 'help'),
        image_click=Output('login-captcha-image-container', 'n_clicks'),
        submit_loading=Output('login-submit', 'loading'),
        token=Output('token-container', 'data'),
        redirect_container=Output('redirect-container', 'children', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        nClicks=Input('login-submit', 'nClicks')
    ),
    state=dict(
        username=State('login-username', 'value'),
        password=State('login-password', 'value'),
        input_captcha=State('login-captcha', 'value'),
        session_id=State('captcha_image-session_id-container', 'data'),
        image_click=State('login-captcha-image-container', 'n_clicks'),
        captcha_hidden=State('captcha-row-container', 'hidden')
    ),
    prevent_initial_call=True
)
def login_auth(nClicks, username, password, input_captcha, session_id, image_click, captcha_hidden):
    if nClicks:
        if captcha_hidden:
            input_captcha = 'hidden'
        # 校验全部输入值是否不为空
        if all([username, password, input_captcha]):

            try:
                user_params = dict(username=username, password=password, captcha=input_captcha, session_id=session_id)
                userinfo_result = login_api(user_params)
                if userinfo_result['code'] == 200:
                    token = userinfo_result['data']['access_token']
                    session['Authorization'] = token
                    return dict(
                        username_form_status=None,
                        password_form_status=None,
                        captcha_form_status=None,
                        username_form_help=None,
                        password_form_help=None,
                        captcha_form_help=None,
                        image_click=dash.no_update,
                        submit_loading=False,
                        token=token,
                        redirect_container=dcc.Location(pathname='/', id='login-redirect'),
                        global_message_container=fuc.FefferyFancyMessage('登录成功', type='success')
                    )

                else:

                    return dict(
                        username_form_status=None,
                        password_form_status=None,
                        captcha_form_status=None,
                        username_form_help=None,
                        password_form_help=None,
                        captcha_form_help=None,
                        image_click=image_click + 1,
                        submit_loading=False,
                        token=None,
                        redirect_container=None,
                        global_message_container=fuc.FefferyFancyMessage(userinfo_result.get('message'), type='error')
                    )
            except Exception as e:
                print(e)
                return dict(
                    username_form_status=None,
                    password_form_status=None,
                    captcha_form_status=None,
                    username_form_help=None,
                    password_form_help=None,
                    captcha_form_help=None,
                    image_click=image_click + 1,
                    submit_loading=False,
                    token=None,
                    redirect_container=None,
                    global_message_container=fuc.FefferyFancyMessage('接口异常', type='error')
                )

        return dict(
            username_form_status=None if username else 'error',
            password_form_status=None if password else 'error',
            captcha_form_status=None if input_captcha else 'error',
            username_form_help=None if username else '请输入用户名！',
            password_form_help=None if password else '请输入密码！',
            captcha_form_help=None if input_captcha else '请输入验证码！',
            image_click=dash.no_update,
            submit_loading=False,
            token=None,
            redirect_container=None,
            global_message_container=None
        )

    return dict(
        username_form_status=dash.no_update,
        password_form_status=dash.no_update,
        captcha_form_status=dash.no_update,
        username_form_help=dash.no_update,
        password_form_help=dash.no_update,
        captcha_form_help=dash.no_update,
        image_click=image_click + 1,
        submit_loading=dash.no_update,
        token=dash.no_update,
        redirect_container=dash.no_update,
        global_message_container=dash.no_update
    )


@app.callback(
    [Output('login-captcha-image', 'src'),
     Output('captcha_image-session_id-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('login-captcha-image-container', 'n_clicks'),
    prevent_initial_call=True
)
def change_login_captcha_image(captcha_click):
    if captcha_click:
        try:
            captcha_image_info = get_captcha_image_api()
            if captcha_image_info.get('code') == 200:
                captcha_image = captcha_image_info.get('data').get('image')
                session_id = captcha_image_info.get('data').get('session_id')

                return [
                    captcha_image,
                    session_id,
                    dash.no_update,
                    dash.no_update
                ]
            else:
                return [
                    dash.no_update,
                    dash.no_update,
                    {'timestamp': time.time()},
                    dash.no_update
                ]
        except Exception as e:

            return [dash.no_update, dash.no_update, {'timestamp': time.time()}, fuc.FefferyFancyMessage('接口异常', type='error')]

    return [dash.no_update] * 4


@app.callback(
    Output('container', 'style'),
    Input('url-container', 'pathname'),
    State('container', 'style')
)
def random_bg(pathname, old_style):
    return {
        **old_style,
        'backgroundImage': 'url({})'.format(dash.get_asset_url('imgs/login-background.jpg')),
        'backgroundRepeat': 'no-repeat',
        'backgroundSize': 'cover'
    }
