import feffery_antd_components as fac
from callbacks.system_c.menu_c.components_c import button_type_c  # noqa: F401


def render():
    return [
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdInput(
                            id='button-menu-perms',
                            placeholder='请输入权限字符',
                            allowClear=True,
                            style={'width': '100%'},
                        ),
                        label='权限字符',
                        tooltip='控制器中定义的权限字符，如：system:user:list',
                        id='button-menu-perms-form-item',
                        labelCol={'span': 4},
                        wrapperCol={'span': 20},
                    ),
                    span=24,
                )
            ],
            gutter=10,
        )
    ]
