from dash import html
import feffery_antd_components as fac


def render():
    return [
        fac.AntdSpace(
            [
                fac.AntdFormItem(
                    fac.AntdRadioGroup(
                        id='menu-menu-is_frame',
                        options=[
                            {
                                'label': '是',
                                'value': '0'
                            },
                            {
                                'label': '否',
                                'value': '1'
                            },
                        ],
                        defaultValue='1',
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
                                title='选择是外链则路由地址需要以`http(s)://`开头'
                            ),
                            fac.AntdText('是否外链')
                        ]
                    ),
                    id='menu-menu-is_frame-form-item',
                    labelCol={
                        'span': 8,
                    },
                    wrapperCol={
                        'span': 16
                    }
                ),
                fac.AntdFormItem(
                    fac.AntdInput(
                        id='menu-menu-path',
                        placeholder='请输入路由地址',
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
                                title='访问的路由地址，如：`user`，如外网地址需内链访问则以`http(s)://`开头'
                            ),
                            fac.AntdText('路由地址')
                        ]
                    ),
                    required=True,
                    id='menu-menu-path-form-item',
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
        fac.AntdSpace(
            [
                fac.AntdFormItem(
                    fac.AntdInput(
                        id='menu-menu-component',
                        placeholder='请输入组件路径',
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
                                title='访问的组件路径，如：`system.user.index`，默认在`views`目录下'
                            ),
                            fac.AntdText('组件路径')
                        ]
                    ),
                    id='menu-menu-component-form-item',
                    labelCol={
                        'span': 8,
                    },
                    wrapperCol={
                        'span': 16
                    }
                ),
                fac.AntdFormItem(
                    fac.AntdInput(
                        id='menu-menu-perms',
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
                    id='menu-menu-perms-form-item',
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
        fac.AntdSpace(
            [
                fac.AntdFormItem(
                    fac.AntdInput(
                        id='menu-menu-query',
                        placeholder='请输入路由参数',
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
                                title='访问路由的默认传递参数，如：`{"id": 1, "name": "ry"}`'
                            ),
                            fac.AntdText('路由参数')
                        ]
                    ),
                    id='menu-menu-query-form-item',
                    labelCol={
                        'span': 8,
                    },
                    wrapperCol={
                        'span': 16
                    }
                ),
                fac.AntdFormItem(
                    fac.AntdRadioGroup(
                        id='menu-menu-is_cache',
                        options=[
                            {
                                'label': '缓存',
                                'value': '0'
                            },
                            {
                                'label': '不缓存',
                                'value': '1'
                            },
                        ],
                        defaultValue='0',
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
                                title='选择是则会被`keep-alive`缓存，需要匹配组件的`name`和地址保持一致'
                            ),
                            fac.AntdText('是否缓存')
                        ]
                    ),
                    id='menu-menu-is_cache-form-item',
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
        fac.AntdSpace(
            [
                fac.AntdFormItem(
                    fac.AntdRadioGroup(
                        id='menu-menu-visible',
                        options=[
                            {
                                'label': '显示',
                                'value': '0'
                            },
                            {
                                'label': '隐藏',
                                'value': '1'
                            },
                        ],
                        defaultValue='0',
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
                                title='选择隐藏则路由将不会出现在侧边栏，但仍然可以访问'
                            ),
                            fac.AntdText('显示状态')
                        ]
                    ),
                    id='menu-menu-visible-form-item',
                    labelCol={
                        'span': 8,
                    },
                    wrapperCol={
                        'span': 16
                    }
                ),
                fac.AntdFormItem(
                    fac.AntdRadioGroup(
                        id='menu-menu-status',
                        options=[
                            {
                                'label': '正常',
                                'value': '0'
                            },
                            {
                                'label': '停用',
                                'value': '1'
                            },
                        ],
                        defaultValue='0',
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
                                title='选择停用则路由将不会出现在侧边栏，也不能被访问'
                            ),
                            fac.AntdText('菜单状态')
                        ]
                    ),
                    id='menu-menu-status-form-item',
                    labelCol={
                        'span': 8,
                    },
                    wrapperCol={
                        'span': 16
                    }
                ),
            ],
            size="middle"
        )
    ]
