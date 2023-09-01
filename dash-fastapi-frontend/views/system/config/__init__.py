from dash import dcc, html
import feffery_antd_components as fac

import callbacks.system_c.config_c
from api.config import get_config_list_api


def render(button_perms):

    config_params = dict(page_num=1, page_size=10)
    table_info = get_config_list_api(config_params)
    table_data = []
    page_num = 1
    page_size = 10
    total = 0
    if table_info['code'] == 200:
        table_data = table_info['data']['rows']
        page_num = table_info['data']['page_num']
        page_size = table_info['data']['page_size']
        total = table_info['data']['total']
        for item in table_data:
            if item['config_type'] == 'Y':
                item['config_type'] = dict(tag='是', color='blue')
            else:
                item['config_type'] = dict(tag='否', color='volcano')
            item['key'] = str(item['config_id'])
            item['operation'] = [
                {
                    'content': '修改',
                    'type': 'link',
                    'icon': 'antd-edit'
                } if 'system:config:edit' in button_perms else {},
                {
                    'content': '删除',
                    'type': 'link',
                    'icon': 'antd-delete'
                } if 'system:config:remove' in button_perms else {},
            ]

    return [
        dcc.Store(id='config-button-perms-container', data=button_perms),
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='config-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='config-export-container'),
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    html.Div(
                                        [
                                            fac.AntdForm(
                                                [
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='config-config_name-input',
                                                            placeholder='请输入参数名称',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 235
                                                            }
                                                        ),
                                                        label='参数名称',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='config-config_key-input',
                                                            placeholder='请输入参数键名',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 235
                                                            }
                                                        ),
                                                        label='参数键名',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='config-config_type-select',
                                                            placeholder='系统内置',
                                                            options=[
                                                                {
                                                                    'label': '是',
                                                                    'value': 'Y'
                                                                },
                                                                {
                                                                    'label': '否',
                                                                    'value': 'N'
                                                                }
                                                            ],
                                                            style={
                                                                'width': 235
                                                            }
                                                        ),
                                                        label='系统内置',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdDateRangePicker(
                                                            id='config-create_time-range',
                                                            style={
                                                                'width': 235
                                                            }
                                                        ),
                                                        label='创建时间',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '搜索',
                                                            id='config-search',
                                                            type='primary',
                                                            icon=fac.AntdIcon(
                                                                icon='antd-search'
                                                            )
                                                        ),
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '重置',
                                                            id='config-reset',
                                                            icon=fac.AntdIcon(
                                                                icon='antd-sync'
                                                            )
                                                        ),
                                                        style={'paddingBottom': '10px'},
                                                    )
                                                ],
                                                layout='inline',
                                            )
                                        ],
                                        id='config-search-form-container',
                                        hidden=False
                                    ),
                                )
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpace(
                                        [
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-plus'
                                                    ),
                                                    '新增',
                                                ],
                                                id={
                                                    'type': 'config-operation-button',
                                                    'index': 'add'
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff'
                                                }
                                            ) if 'system:config:add' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-edit'
                                                    ),
                                                    '修改',
                                                ],
                                                id={
                                                    'type': 'config-operation-button',
                                                    'index': 'edit'
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#71e2a3',
                                                    'background': '#e7faf0',
                                                    'border-color': '#d0f5e0'
                                                }
                                            ) if 'system:config:edit' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-minus'
                                                    ),
                                                    '删除',
                                                ],
                                                id={
                                                    'type': 'config-operation-button',
                                                    'index': 'delete'
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb'
                                                }
                                            ) if 'system:config:remove' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='config-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'border-color': '#ffe399'
                                                }
                                            ) if 'system:config:export' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-sync'
                                                    ),
                                                    '刷新缓存',
                                                ],
                                                id='config-refresh-cache',
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb',
                                                    'marginRight': '10px'
                                                }
                                            ) if 'system:config:edit' in button_perms else [],
                                        ],
                                        style={
                                            'paddingBottom': '10px'
                                        }
                                    ),
                                    span=16
                                ),
                                fac.AntdCol(
                                    fac.AntdSpace(
                                        [
                                            html.Div(
                                                fac.AntdTooltip(
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-search'
                                                            ),
                                                        ],
                                                        id='config-hidden',
                                                        shape='circle'
                                                    ),
                                                    id='config-hidden-tooltip',
                                                    title='隐藏搜索'
                                                )
                                            ),
                                            html.Div(
                                                fac.AntdTooltip(
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-sync'
                                                            ),
                                                        ],
                                                        id='config-refresh',
                                                        shape='circle'
                                                    ),
                                                    title='刷新'
                                                )
                                            ),
                                        ],
                                        style={
                                            'float': 'right',
                                            'paddingBottom': '10px'
                                        }
                                    ),
                                    span=8,
                                    style={
                                        'paddingRight': '10px'
                                    }
                                )
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpin(
                                        fac.AntdTable(
                                            id='config-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'config_id',
                                                    'title': '参数编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'config_name',
                                                    'title': '参数名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'config_key',
                                                    'title': '参数键名',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'config_value',
                                                    'title': '参数键值',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'config_type',
                                                    'title': '系统内置',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'remark',
                                                    'title': '备注',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'create_time',
                                                    'title': '创建时间',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'title': '操作',
                                                    'dataIndex': 'operation',
                                                    'renderOptions': {
                                                        'renderType': 'button'
                                                    },
                                                }
                                            ],
                                            rowSelectionType='checkbox',
                                            rowSelectionWidth=50,
                                            bordered=True,
                                            pagination={
                                                'pageSize': page_size,
                                                'current': page_num,
                                                'showSizeChanger': True,
                                                'pageSizeOptions': [10, 30, 50, 100],
                                                'showQuickJumper': True,
                                                'total': total
                                            },
                                            mode='server-side',
                                            style={
                                                'width': '100%',
                                                'padding-right': '10px'
                                            }
                                        ),
                                        text='数据加载中'
                                    ),
                                )
                            ]
                        ),
                    ],
                    span=24
                )
            ],
            gutter=5
        ),

        # 新增和编辑参数配置表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='config-config_name',
                                            placeholder='请输入参数名称',
                                            allowClear=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='参数名称',
                                        required=True,
                                        id='config-config_name-form-item'
                                    ),
                                    span=24
                                ),
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='config-config_key',
                                            placeholder='请输入参数键名',
                                            allowClear=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='参数键名',
                                        required=True,
                                        id='config-config_key-form-item'
                                    ),
                                    span=24
                                ),
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='config-config_value',
                                            placeholder='请输入参数键值',
                                            allowClear=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='参数键值',
                                        required=True,
                                        id='config-config_value-form-item'
                                    ),
                                    span=24
                                ),
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdRadioGroup(
                                            id='config-config_type',
                                            options=[
                                                {
                                                    'label': '是',
                                                    'value': 'Y'
                                                },
                                                {
                                                    'label': '否',
                                                    'value': 'N'
                                                },
                                            ],
                                            defaultValue='0',
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='系统内置',
                                        id='config-config_type-form-item'
                                    ),
                                    span=24
                                ),
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='config-remark',
                                            placeholder='请输入内容',
                                            allowClear=True,
                                            mode='text-area',
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='备注',
                                        id='config-remark-form-item'
                                    ),
                                    span=24
                                ),
                            ]
                        ),
                    ],
                    labelCol={
                        'span': 6
                    },
                    wrapperCol={
                        'span': 18
                    }
                )
            ],
            id='config-modal',
            mask=False,
            width=580,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除参数配置二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='config-delete-text'),
            id='config-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        )
    ]
