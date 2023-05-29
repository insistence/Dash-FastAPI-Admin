import dash
from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc

import callbacks.login_c


def render_content():
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            fac.AntdText('HELLO', style={'color': 'rgba(255,255,255,0.8)'})
                        ],
                        style={
                            'fontSize': '60px',
                            'fontWeight': '500'
                        }
                    ),
                    html.Div(
                        [
                            fac.AntdText('WELCOME', style={'color': 'rgba(255,255,255,0.8)'}),
                        ],
                        style={
                            'fontSize': '60px',
                            'fontWeight': '500'
                        }
                    ),
                    html.Div(
                        [
                            fac.AntdText('欢迎使用通用后台管理系统', style={'color': 'rgba(255,255,255,0.8)'}),
                        ],
                        style={
                            'fontSize': '18px',
                            'fontWeight': '600',
                            'marginTop': '20px'
                        }
                    ),
                ],
                style={
                    'position': 'fixed',
                    'top': '20%',
                    'left': '26%',
                    'width': '430px',
                    'padding': '0px 30px',
                    'transform': 'translateX(-50%)'
                }
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
                                    prefix=fac.AntdIcon(
                                        icon='antd-user'
                                    ),
                                ),
                                id='login-username-form-item'
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    placeholder='请输入密码',
                                    id='login-password',
                                    mode='password',
                                    passwordUseMd5=True,
                                    size='large',
                                    prefix=fac.AntdIcon(
                                        icon='antd-lock'
                                    ),
                                ),
                                id='login-password-form-item'
                            ),
                            fac.AntdSpace(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            placeholder='请输入验证码',
                                            id='input-demo',
                                            size='large',
                                            prefix=fac.AntdIcon(
                                                icon='antd-check-circle'
                                            ),
                                            style={
                                                'width': '210px'
                                            }
                                        ),
                                        id='login-captcha-form-item'
                                    ),
                                    fac.AntdFormItem(
                                        fuc.FefferyCaptcha(
                                            id='login-captcha',
                                            charNum=4,
                                            height=30,
                                            bgColor='white',
                                            style={
                                                'marginBottom': 0,
                                                'paddingBottom': 0
                                            }
                                        )
                                    )
                                ],
                                align='end',
                                size=10
                            ),
                            fac.AntdSpace(
                                [
                                    html.Div(id='test'),
                                    fac.AntdButton(
                                        '忘记密码',
                                        id='forget-password-link',
                                        type='link',
                                        href='/forget',
                                        target='_self'
                                    )
                                ],
                                align='center',
                                size=240
                            ),
                            fac.AntdFormItem(
                                fac.AntdButton(
                                    '登录',
                                    id='login-submit',
                                    type='primary',
                                    block=True,
                                    size='large',
                                ),
                                style={
                                    'marginTop': '20px'
                                }
                            )
                        ],
                        layout='vertical',
                        style={
                            'width': '100%'
                        }
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
                    'transform': 'translateX(-50%)'
                }
            ),
            fac.AntdFooter(
                html.Div(
                    fac.AntdText(
                        '版权所有©2023 Dash-FastAPI',
                        style={
                            'margin': '0'
                        }
                    ),
                    style={
                        'display': 'flex',
                        'height': '100%',
                        'justifyContent': 'center',
                        'alignItems': 'center'
                    }
                ),
                style={
                    'backgroundColor': 'rgb(255 255 255 / 0%)',
                    'height': '40px',
                    'position': 'fixed',
                    'bottom': 0,
                    'left': '50%',
                    'width': '500px',
                    'padding': '20px 50px',
                    'transform': 'translateX(-50%)'
                }
            ),
        ],
        id='container',
        style={
            'height': '100vh',
        }
    )
