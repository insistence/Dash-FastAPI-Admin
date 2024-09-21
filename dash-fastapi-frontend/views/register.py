import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import dcc, html
from callbacks import register_c  # noqa: F401


def render_register_content():
    return html.Div(
        [
            fac.AntdCard(
                [
                    dcc.Store(id='register-success-container'),
                    dcc.Store(id='register-captcha_image-session_id-container'),
                    fac.AntdForm(
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
                                [
                                    fac.AntdSpace(
                                        [
                                            fac.AntdFormItem(
                                                fac.AntdInput(
                                                    placeholder='请输入验证码',
                                                    id='register-captcha',
                                                    size='large',
                                                    prefix=fac.AntdIcon(
                                                        icon='antd-check-circle'
                                                    ),
                                                    style={'width': '280px'},
                                                ),
                                                id='register-captcha-form-item',
                                            ),
                                            fac.AntdFormItem(
                                                html.Div(
                                                    [
                                                        fac.AntdImage(
                                                            id='register-captcha-image',
                                                            src='',
                                                            height=37,
                                                            width=100,
                                                            preview=False,
                                                        )
                                                    ],
                                                    id='register-captcha-image-container',
                                                    style={
                                                        'border': '1px solid #ccc'
                                                    },
                                                ),
                                            ),
                                        ],
                                        align='end',
                                        size=10,
                                    ),
                                ],
                                id='register-captcha-row-container',
                            ),
                            fuc.FefferyKeyPress(
                                id='register-keyboard-enter-submit',
                                keys='enter',
                            ),
                            fac.AntdFormItem(
                                fac.AntdButton(
                                    '注册',
                                    id='register-submit',
                                    type='primary',
                                    loadingChildren='注册中',
                                    autoSpin=True,
                                    block=True,
                                    size='large',
                                ),
                                style={'marginBottom': '10px'},
                            ),
                        ],
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
                    'style': {'font-size': '16px'},
                },
                headStyle={
                    'font-weight': 'bold',
                    'text-align': 'center',
                    'font-size': '30px',
                },
                style={
                    'position': 'fixed',
                    'top': '16%',
                    'left': '50%',
                    'width': '500px',
                    'padding': '0px 30px',
                    'transform': 'translateX(-50%)',
                },
            ),
        ]
    )
