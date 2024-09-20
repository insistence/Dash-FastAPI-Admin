import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html
from callbacks import login_c  # noqa: F401


def render_content():
    return html.Div(
        [
            dcc.Store(id='captcha_image-session_id-container'),
            html.Div(
                [
                    html.Div(
                        [
                            fac.AntdText(
                                'HELLO',
                                style={
                                    'color': 'rgba(255,255,255,0.8)',
                                    'fontSize': '60px',
                                    'fontWeight': '500',
                                },
                            )
                        ],
                    ),
                    html.Div(
                        [
                            fac.AntdText(
                                'WELCOME',
                                style={
                                    'color': 'rgba(255,255,255,0.8)',
                                    'fontSize': '60px',
                                    'fontWeight': '500',
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            fac.AntdText(
                                '欢迎使用通用后台管理系统',
                                style={
                                    'color': 'rgba(255,255,255,0.8)',
                                    'fontSize': '20px',
                                    'fontWeight': '600',
                                    'marginTop': '25px',
                                },
                            ),
                        ],
                    ),
                ],
                style={
                    'position': 'fixed',
                    'top': '20%',
                    'left': '26%',
                    'width': '430px',
                    'padding': '0px 30px',
                    'transform': 'translateX(-50%)',
                },
            ),
            fac.AntdCard(
                [
                    fac.AntdForm(
                        [
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    placeholder='请输入用户名',
                                    id='login-username',
                                    size='large',
                                    prefix=fac.AntdIcon(icon='antd-user'),
                                ),
                                id='login-username-form-item',
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    placeholder='请输入密码',
                                    id='login-password',
                                    mode='password',
                                    passwordUseMd5=True,
                                    size='large',
                                    prefix=fac.AntdIcon(icon='antd-lock'),
                                ),
                                id='login-password-form-item',
                            ),
                            html.Div(
                                [
                                    fac.AntdSpace(
                                        [
                                            fac.AntdFormItem(
                                                fac.AntdInput(
                                                    placeholder='请输入验证码',
                                                    id='login-captcha',
                                                    size='large',
                                                    prefix=fac.AntdIcon(
                                                        icon='antd-check-circle'
                                                    ),
                                                    style={'width': '210px'},
                                                ),
                                                id='login-captcha-form-item',
                                            ),
                                            fac.AntdFormItem(
                                                html.Div(
                                                    [
                                                        fac.AntdImage(
                                                            id='login-captcha-image',
                                                            src='',
                                                            height=37,
                                                            width=100,
                                                            preview=False,
                                                        )
                                                    ],
                                                    id='login-captcha-image-container',
                                                    style={
                                                        'border': '1px solid #ccc'
                                                    },
                                                )
                                            ),
                                        ],
                                        align='end',
                                        size=10,
                                    ),
                                ],
                                id='captcha-row-container',
                            ),
                            fuc.FefferyKeyPress(
                                id='keyboard-enter-submit', keys='enter'
                            ),
                            fac.AntdFormItem(
                                fac.AntdButton(
                                    '登录',
                                    id='login-submit',
                                    type='primary',
                                    loadingChildren='登录中',
                                    autoSpin=True,
                                    block=True,
                                    size='large',
                                ),
                                style={'marginTop': '20px'},
                            ),
                            fac.AntdFormItem(
                                html.Div(
                                    [
                                        html.Div(
                                            id='register-user-link-container'
                                        ),
                                        html.Div(
                                            id='forget-password-link-container'
                                        ),
                                    ],
                                    style={
                                        'display': 'flex',
                                        'justifyContent': 'space-between',
                                    },
                                )
                            ),
                        ],
                        layout='vertical',
                        style={'width': '100%'},
                    ),
                ],
                id='login-form-container',
                title='登录',
                hoverable=True,
                style={
                    'position': 'fixed',
                    'top': '16%',
                    'left': '70%',
                    'width': '430px',
                    'padding': '0px 30px',
                    'transform': 'translateX(-50%)',
                },
            ),
            fac.AntdFooter(
                html.Div(
                    fac.AntdText(
                        '版权所有©2023 Dash-FastAPI-Admin',
                        style={'margin': '0'},
                    ),
                    style={
                        'display': 'flex',
                        'height': '100%',
                        'justifyContent': 'center',
                        'alignItems': 'center',
                    },
                ),
                style={
                    'backgroundColor': 'rgb(255 255 255 / 0%)',
                    'height': '40px',
                    'position': 'fixed',
                    'bottom': 0,
                    'left': '50%',
                    'width': '500px',
                    'padding': 0,
                    'transform': 'translateX(-50%)',
                },
            ),
        ],
        id='container',
        style={
            'height': '100vh',
        },
    )
