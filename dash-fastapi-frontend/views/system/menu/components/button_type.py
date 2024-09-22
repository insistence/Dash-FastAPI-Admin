import feffery_antd_components as fac
from dash import html
from callbacks.system_c.menu_c.components_c import button_type_c  # noqa: F401


def render():
    return [
        fac.AntdSpace(
            [
                fac.AntdFormItem(
                    fac.AntdInput(
                        id='button-menu-perms',
                        placeholder='请输入权限字符',
                        allowClear=True,
                        style={
                            'width': 200
                        }
                    ),
                    label=html.Div(
                        [
                            fac.AntdTooltip(
                                fac.AntdIcon(
                                    icon='antd-question-circle'
                                ),
                                title='控制器中定义的权限字符，如：system:user:list'
                            ),
                            fac.AntdText('权限字符')
                        ]
                    ),
                    id='button-menu-perms-form-item',
                    labelCol={
                        'span': 8,
                    },
                    wrapperCol={
                        'span': 16
                    }
                ),
            ],
            size="middle"
        ),
    ]
