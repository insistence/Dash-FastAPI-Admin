import feffery_antd_components as fac
from callbacks.system_c.user_c.profile_c import reset_pwd_c  # noqa: F401


def render():
    return fac.AntdForm(
        [
            fac.AntdFormItem(
                fac.AntdInput(id='reset-old-password', mode='password'),
                id='reset-old-password-form-item',
                label='旧密码',
                required=True,
            ),
            fac.AntdFormItem(
                fac.AntdInput(id='reset-new-password', mode='password'),
                id='reset-new-password-form-item',
                label='新密码',
                required=True,
            ),
            fac.AntdFormItem(
                fac.AntdInput(id='reset-confirm-password', mode='password'),
                id='reset-confirm-password-form-item',
                label='确认密码',
                required=True,
            ),
            fac.AntdFormItem(
                fac.AntdSpace(
                    [
                        fac.AntdButton(
                            '保存', id='reset-password-submit', type='primary'
                        ),
                        fac.AntdButton(
                            '关闭',
                            id='reset-password-close',
                            type='primary',
                            danger=True,
                        ),
                    ],
                ),
                wrapperCol={'offset': 4},
            ),
        ],
        labelCol={'span': 4},
        wrapperCol={'span': 20},
        style={
            'margin': '0 auto'  # 以快捷实现居中布局效果
        },
    )
