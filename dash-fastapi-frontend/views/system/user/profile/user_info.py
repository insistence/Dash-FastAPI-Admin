import feffery_antd_components as fac

import callbacks.system_c.user_c.profile_c.user_info_c


def render():
    return fac.AntdForm(
        [
            fac.AntdFormItem(
                fac.AntdInput(
                    id='reset-user-nick_name',
                    placeholder='请输入用户昵称'
                ),
                id='reset-user-nick_name-form-item',
                label='用户昵称',
                required=True
            ),
            fac.AntdFormItem(
                fac.AntdInput(
                    id='reset-user-phonenumber',
                    placeholder='请输入手机号码'
                ),
                id='reset-user-phonenumber-form-item',
                label='手机号码',
                required=True
            ),
            fac.AntdFormItem(
                fac.AntdInput(
                    id='reset-user-email',
                    placeholder='请输入邮箱'
                ),
                id='reset-user-email-form-item',
                label='邮箱',
                required=True
            ),
            fac.AntdFormItem(
                fac.AntdRadioGroup(
                    id='reset-user-sex',
                    options=[
                        {
                            'label': '男',
                            'value': '0'
                        },
                        {
                            'label': '女',
                            'value': '1'
                        }
                    ],
                    defaultValue='1'
                ),
                id='reset-user-sex-form-item',
                label='性别'
            ),
            fac.AntdFormItem(
                fac.AntdSpace(
                    [
                        fac.AntdButton(
                            '保存',
                            id='reset-submit',
                            type='primary'
                        ),
                        fac.AntdButton(
                            '关闭',
                            id='reset-close',
                            type='primary',
                            danger=True
                        ),
                    ],
                ),
                wrapperCol={
                    'offset': 4
                }
            )
        ],
        labelCol={
            'span': 4
        },
        wrapperCol={
            'span': 20
        },
        style={
            'margin': '0 auto'  # 以快捷实现居中布局效果
        }
    )
