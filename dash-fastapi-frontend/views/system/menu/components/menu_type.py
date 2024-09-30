import feffery_antd_components as fac
from callbacks.system_c.menu_c.components_c import menu_type_c  # noqa: F401
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
                            id='menu-menu-is_frame',
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
                        id='menu-menu-is_frame-form-item',
                    ),
                    span=12,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdInput(
                            id='menu-menu-path',
                            placeholder='请输入路由地址',
                            allowClear=True,
                            style={'width': '100%'},
                        ),
                        label='路由地址',
                        tooltip='访问的路由地址，如：`user`，如外网地址需内链访问则以`http(s)://`开头',
                        required=True,
                        id='menu-menu-path-form-item',
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
                        fac.AntdInput(
                            id='menu-menu-route_name',
                            placeholder='请输入路由名称',
                            allowClear=True,
                            style={'width': '100%'},
                        ),
                        label='路由名称',
                        tooltip='默认不填则和路由地址相同：如地址为：`user`，则名称为`User`（注意：因为router会删除名称相同路由，为避免名字的冲突，特殊情况下请自定义，保证唯一性）',
                        id='menu-menu-route_name-form-item',
                    ),
                    span=12,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdInput(
                            id='menu-menu-component',
                            placeholder='请输入组件路径',
                            allowClear=True,
                            style={'width': '100%'},
                        ),
                        label='组件路径',
                        tooltip='访问的组件路径，如：`system.user.index`，默认在`views`目录下',
                        id='menu-menu-component-form-item',
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
                        fac.AntdInput(
                            id='menu-menu-perms',
                            placeholder='请输入权限字符',
                            allowClear=True,
                            style={'width': '100%'},
                        ),
                        label='权限字符',
                        tooltip='控制器中定义的权限字符，如：system:user:list',
                        id='menu-menu-perms-form-item',
                    ),
                    span=12,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        fac.AntdInput(
                            id='menu-menu-query',
                            placeholder='请输入路由参数',
                            allowClear=True,
                            style={'width': '100%'},
                        ),
                        label='路由参数',
                        tooltip='访问路由的默认传递参数，如：`{"id": 1, "name": "ry"}`',
                        id='menu-menu-query-form-item',
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
                        fac.AntdRadioGroup(
                            id='menu-menu-is_cache',
                            options=[
                                {
                                    'label': '缓存',
                                    'value': MenuConstant.YES_CACHE,
                                },
                                {
                                    'label': '不缓存',
                                    'value': MenuConstant.NO_CACHE,
                                },
                            ],
                            defaultValue=MenuConstant.YES_CACHE,
                            style={'width': '100%'},
                        ),
                        label='是否缓存',
                        id='menu-menu-is_cache-form-item',
                    ),
                    span=12,
                ),
                fac.AntdCol(
                    fac.AntdFormItem(
                        ApiRadioGroup(
                            dict_type='sys_show_hide',
                            id='menu-menu-visible',
                            defaultValue=SysShowHideConstant.SHOW,
                            style={'width': '100%'},
                        ),
                        label='显示状态',
                        tooltip='选择隐藏则路由将不会出现在侧边栏，但仍然可以访问',
                        id='menu-menu-visible-form-item',
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
                            dict_type='sys_normal_disable',
                            id='menu-menu-status',
                            defaultValue=SysNormalDisableConstant.NORMAL,
                            style={'width': '100%'},
                        ),
                        label='菜单状态',
                        tooltip='选择停用则路由将不会出现在侧边栏，也不能被访问',
                        id='menu-menu-status-form-item',
                    ),
                    span=12,
                ),
            ],
            gutter=10,
        ),
    ]
