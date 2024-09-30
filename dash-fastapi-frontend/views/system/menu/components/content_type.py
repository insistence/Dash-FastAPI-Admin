import feffery_antd_components as fac
from callbacks.system_c.menu_c.components_c import content_type_c  # noqa: F401
from config.constant import (
    MenuConstant,
    SysNormalDisableConstant,
    SysShowHideConstant,
)
from components.ApiRadioGroup import ApiRadioGroup


def render():
    return [
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdRadioGroup(
                            id='content-menu-is_frame',
                            options=[
                                {
                                    'label': '是',
                                    'value': MenuConstant.YES_FRAME,
                                },
                                {'label': '否', 'value': MenuConstant.NO_FRAME},
                            ],
                            defaultValue=MenuConstant.NO_FRAME,
                            style={'width': '100%'},
                        ),
                        label='是否外链',
                        tooltip='选择是外链则路由地址需要以`http(s)://`开头',
                        id='content-menu-is_frame-form-item',
                    ),
                    span=12,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdInput(
                            id='content-menu-path',
                            placeholder='请输入路由地址',
                            allowClear=True,
                            style={'width': '100%'},
                        ),
                        label='路由地址',
                        tooltip='访问的路由地址，如：`user`，如外网地址需内链访问则以`http(s)://`开头',
                        required=True,
                        id='content-menu-path-form-item',
                    ),
                    span=12,
                ),
            ],
            gutter=10,
        ),
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdFormItem(
                        ApiRadioGroup(
                            dict_type='sys_show_hide',
                            id='content-menu-visible',
                            defaultValue=SysShowHideConstant.SHOW,
                            style={'width': '100%'},
                        ),
                        label='显示状态',
                        tooltip='选择隐藏则路由将不会出现在侧边栏，但仍然可以访问',
                        id='content-menu-visible-form-item',
                    ),
                    span=12,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        ApiRadioGroup(
                            dict_type='sys_normal_disable',
                            id='content-menu-status',
                            defaultValue=SysNormalDisableConstant.NORMAL,
                            style={'width': '100%'},
                        ),
                        label='菜单状态',
                        tooltip='选择停用则路由将不会出现在侧边栏，也不能被访问',
                        id='content-menu-status-form-item',
                    ),
                    span=12,
                ),
            ],
            gutter=10,
        ),
    ]
