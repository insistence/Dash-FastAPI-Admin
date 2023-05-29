from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc

import callbacks.forget_c


def render_forget_content():
    return html.Div(
        [
            fac.AntdCard(
                [
                    fac.AntdForm(
                        [
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    placeholder='请输入用户名',
                                    id='forget-username',
                                    size='large',
                                    prefix=fac.AntdIcon(
                                        icon='antd-user'
                                    ),
                                ),
                                id='forget-username-form-item'
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    placeholder='请输入新密码',
                                    id='forget-password',
                                    mode='password',
                                    passwordUseMd5=True,
                                    size='large',
                                    prefix=fac.AntdIcon(
                                        icon='antd-lock'
                                    ),
                                ),
                                id='forget-password-form-item'
                            ),
                            fac.AntdFormItem(
                                fac.AntdInput(
                                    placeholder='请再次输入新密码',
                                    id='forget-password-again',
                                    mode='password',
                                    passwordUseMd5=True,
                                    size='large',
                                    prefix=fac.AntdIcon(
                                        icon='antd-lock'
                                    ),
                                ),
                                id='forget-password-again-form-item'
                            ),
                            fac.AntdSpace(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            placeholder='请输入短信验证码',
                                            id='forget-input-captcha',
                                            size='large',
                                            prefix=fac.AntdIcon(
                                                icon='antd-check-circle'
                                            ),
                                            style={
                                                'width': '270px'
                                            }
                                        ),
                                        id='forget-captcha-form-item'
                                    ),
                                    fac.AntdFormItem(
                                        fac.AntdButton(
                                            '获取验证码',
                                            id='get-message-code',
                                            type='primary',
                                            size='large'
                                        )
                                    ),
                                ],
                                align='end',
                                size=10
                            ),
                            fac.AntdFormItem(
                                fac.AntdButton(
                                    '保存',
                                    id='forget-submit',
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

                    # 重定向容器
                    html.Div(id='forget-redirect-container'),
                    fuc.FefferyCountDown(id='message-code-count-down')
                ],
                id='forget-form-container',
                title='重置密码',
                hoverable=True,
                extraLink={
                    'content': '返回登录',
                    'href': '/login',
                    'target': '_self',
                    'style': {
                        'font-size': '16px'
                    }
                },
                headStyle={
                    'font-weight': 'bold',
                    'text-align': 'center',
                    'font-size': '30px'
                },
                style={
                    'position': 'fixed',
                    'top': '16%',
                    'left': '50%',
                    'width': '500px',
                    'padding': '0px 30px',
                    'transform': 'translateX(-50%)'
                }
            ),
            # 消息提示
            html.Div(id='forget-message-container'),
            html.Div(id='forget-sms-container'),
        ]
    )

