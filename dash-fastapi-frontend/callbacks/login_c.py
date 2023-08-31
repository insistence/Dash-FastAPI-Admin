import dash
from dash import dcc
import feffery_utils_components as fuc
from dash.dependencies import Input, Output, State
from flask import session
import time

from server import app, logger
from api.login import login_api, get_captcha_image_api


@app.callback(
    [Output('login-username-form-item', 'validateStatus'),
     Output('login-password-form-item', 'validateStatus'),
     Output('login-captcha-form-item', 'validateStatus'),
     Output('login-username-form-item', 'help'),
     Output('login-password-form-item', 'help'),
     Output('login-captcha-form-item', 'help'),
     Output('login-captcha-image-container', 'n_clicks'),
     Output('login-submit', 'loading'),
     Output('redirect-container', 'children', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('login-submit', 'nClicks'),
    [State('login-username', 'value'),
     State('login-password', 'value'),
     State('login-captcha', 'value'),
     State('captcha_image-session_id-container', 'data'),
     State('login-captcha-image-container', 'n_clicks'),],
    prevent_initial_call=True
)
def login_auth(nClicks, username, password, input_captcha, session_id, image_click):
    if nClicks:
        # 校验全部输入值是否不为空
        if all([username, password, input_captcha]):

            try:
                user_params = dict(username=username, password=password, captcha=input_captcha, session_id=session_id)
                userinfo_result = login_api(user_params)
                if userinfo_result['code'] == 200:
                    token = userinfo_result['data']['access_token']
                    session['Authorization'] = token

                    return [
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        dash.no_update,
                        True,
                        dcc.Location(
                            pathname='/',
                            id='login-redirect'
                        ),
                        fuc.FefferyFancyMessage('登录成功', type='success'),
                    ]

                elif userinfo_result['message'] == '用户不存在':

                    return [
                        'error',
                        None,
                        None,
                        '用户不存在',
                        None,
                        None,
                        image_click + 1,
                        False,
                        None,
                        None
                    ]

                elif userinfo_result['message'] == '密码错误':

                    return [
                        None,
                        'error',
                        None,
                        None,
                        '密码错误',
                        None,
                        image_click + 1,
                        False,
                        None,
                        None
                    ]

                elif userinfo_result['message'] == '验证码已失效':

                    return [
                        None,
                        None,
                        'error',
                        None,
                        None,
                        '验证码已失效',
                        image_click + 1,
                        False,
                        None,
                        None
                    ]

                elif userinfo_result['message'] == '验证码错误':

                    return [
                        None,
                        None,
                        'error',
                        None,
                        None,
                        '验证码错误',
                        image_click + 1,
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
                        image_click + 1,
                        False,
                        None,
                        fuc.FefferyFancyMessage(userinfo_result['message'], type='error'),
                    ]
            except Exception as e:
                print(e)
                return [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    image_click + 1,
                    False,
                    None,
                    fuc.FefferyFancyMessage('接口异常', type='error'),
                ]

        return [
            None if username else 'error',
            None if password else 'error',
            None if input_captcha else 'error',
            None if username else '请输入用户名！',
            None if password else '请输入密码！',
            None if input_captcha else '请输入验证码！',
            dash.no_update,
            False,
            None,
            None
        ]

    return [dash.no_update] * 6 + [image_click + 1] + [dash.no_update] * 3


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
