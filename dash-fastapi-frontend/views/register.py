import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html
from callbacks import register_c  # noqa: F401


def render():
    return html.Div(
        [
            fac.AntdCard(
                [
                    dcc.Store(id='register-success-container'),
                    dcc.Store(id='register-captcha_image-session_id-container'),
                    fuc.FefferyKeyPress(
                        id='register-keyboard-enter-submit',
                        keys='enter',
                    ),
                    fac.AntdForm(
                        fac.AntdFlex(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        placeholder='请输入用户名',
                                        id='register-username',
                                        size='large',
                                        prefix=fac.AntdIcon(icon='antd-user'),
                                    ),
                                    id='register-username-form-item',
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        placeholder='请输入密码',
                                        id='register-password',
                                        mode='password',
                                        passwordUseMd5=True,
                                        size='large',
                                        prefix=fac.AntdIcon(icon='antd-lock'),
                                    ),
                                    id='register-password-form-item',
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        placeholder='请再次输入密码',
                                        id='register-confirm_password',
                                        mode='password',
                                        passwordUseMd5=True,
                                        size='large',
                                        prefix=fac.AntdIcon(icon='antd-lock'),
                                    ),
                                    id='register-confirm_password-form-item',
                                ),
                                html.Div(
                                    fac.AntdFormItem(
                                        fac.AntdFlex(
                                            [
                                                fac.AntdInput(
                                                    placeholder='请输入验证码',
                                                    id='register-captcha',
                                                    size='large',
                                                    prefix=fac.AntdIcon(
                                                        icon='antd-check-circle'
                                                    ),
                                                ),
                                                html.Div(
                                                    [
                                                        fac.AntdImage(
                                                            id='register-captcha-image',
                                                            src='',
                                                            height=39.6,
                                                            width=100,
                                                            preview=False,
                                                            style={
                                                                'border': '1px solid #d9d9d9',
                                                                'borderRadius': '8px',
                                                            },
                                                        )
                                                    ],
                                                    id='register-captcha-image-container',
                                                ),
                                            ],
                                            align='center',
                                            gap='small',
                                        ),
                                        id='register-captcha-form-item',
                                    ),
                                    id='register-captcha-row-container',
                                ),
                                fac.AntdFormItem(
                                    fac.AntdButton(
                                        '注册',
                                        id='register-submit',
                                        type='primary',
                                        block=True,
                                        size='large',
                                    ),
                                    style={'marginTop': '20px'},
                                ),
                            ],
                            vertical=True,
                        ),
                        layout='vertical',
                        style={'width': '100%'},
                    ),
                ],
                id='register-form-container',
                title='用户注册',
                hoverable=True,
                extraLink={
                    'content': '返回登录',
                    'href': '/login',
                    'target': '_self',
                    'style': {'fontSize': '16px'},
                },
                headStyle={
                    'fontWeight': 'bold',
                    'textAlign': 'center',
                    'fontSize': '30px',
                },
                style={
                    'position': 'fixed',
                    'top': '16%',
                    'left': '50%',
                    'width': '480px',
                    'minWidth': '420px',
                    'maxWidth': '75vw',
                    'padding': '0px 30px',
                    'transform': 'translateX(-50%)',
                },
            ),
        ],
        id='register-page',
    )
