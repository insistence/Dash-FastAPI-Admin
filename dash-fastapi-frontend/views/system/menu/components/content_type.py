from dash import html
import feffery_antd_components as fac

import callbacks.system_c.menu_c.components_c.content_type_c


def render():
    return [
        fac.AntdSpace(
            [
                fac.AntdFormItem(
                    fac.AntdRadioGroup(
                        id='content-menu-is_frame',
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
                    id='content-menu-is_frame-form-item',
                    labelCol={
                        'span': 8,
                    },
                    wrapperCol={
                        'span': 16
                    }
                ),
                fac.AntdFormItem(
                    fac.AntdInput(
                        id='content-menu-path',
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
                    id='content-menu-path-form-item',
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
                        id='content-menu-visible',
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
                    id='content-menu-visible-form-item',
                    labelCol={
                        'span': 8,
                    },
                    wrapperCol={
                        'span': 16
                    }
                ),
                fac.AntdFormItem(
                    fac.AntdRadioGroup(
                        id='content-menu-status',
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
                    id='content-menu-status-form-item',
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
