from dash import dcc, html
import feffery_antd_components as fac

import callbacks.system_c.dict_c.dict_c
from . import dict_data
from api.dict import get_dict_type_list_api


def render(button_perms):

    dict_type_params = dict(page_num=1, page_size=10)
    table_info = get_dict_type_list_api(dict_type_params)
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
            if item['status'] == '0':
                item['status'] = dict(tag='正常', color='blue')
            else:
                item['status'] = dict(tag='停用', color='volcano')
            item['key'] = str(item['dict_id'])
            item['dict_type'] = {
                'content': item['dict_type'],
                'type': 'link',
            }
            item['operation'] = [
                {
                    'content': '修改',
                    'type': 'link',
                    'icon': 'antd-edit'
                } if 'system:dict:edit' in button_perms else {},
                {
                    'content': '删除',
                    'type': 'link',
                    'icon': 'antd-delete'
                } if 'system:dict:remove' in button_perms else {},
            ]

    return [
        dcc.Store(id='dict_type-button-perms-container', data=button_perms),
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='dict_type-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='dict_type-export-container'),
        # 字典管理模块操作类型存储容器
        dcc.Store(id='dict_type-operations-store'),
        dcc.Store(id='dict_type-operations-store-bk'),
        dcc.Store(id='dict_data-operations-store'),
        dcc.Store(id='dict_data-operations-store-bk'),
        # 字典管理模块修改操作行key存储容器
        dcc.Store(id='dict_type-edit-id-store'),
        dcc.Store(id='dict_data-edit-id-store'),
        # 字典管理模块删除操作行key存储容器
        dcc.Store(id='dict_type-delete-ids-store'),
        dcc.Store(id='dict_data-delete-ids-store'),
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
                                                            id='dict_type-dict_name-input',
                                                            placeholder='请输入字典名称',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='字典名称',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='dict_type-dict_type-input',
                                                            placeholder='请输入字典类型',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='字典类型',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='dict_type-status-select',
                                                            placeholder='字典状态',
                                                            options=[
                                                                {
                                                                    'label': '正常',
                                                                    'value': '0'
                                                                },
                                                                {
                                                                    'label': '停用',
                                                                    'value': '1'
                                                                }
                                                            ],
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='状态',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdDateRangePicker(
                                                            id='dict_type-create_time-range',
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='创建时间',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '搜索',
                                                            id='dict_type-search',
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
                                                            id='dict_type-reset',
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
                                        id='dict_type-search-form-container',
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
                                                    'type': 'dict_type-operation-button',
                                                    'index': 'add'
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff'
                                                }
                                            ) if 'system:dict:add' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-edit'
                                                    ),
                                                    '修改',
                                                ],
                                                id={
                                                    'type': 'dict_type-operation-button',
                                                    'index': 'edit'
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#71e2a3',
                                                    'background': '#e7faf0',
                                                    'border-color': '#d0f5e0'
                                                }
                                            ) if 'system:dict:edit' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-minus'
                                                    ),
                                                    '删除',
                                                ],
                                                id={
                                                    'type': 'dict_type-operation-button',
                                                    'index': 'delete'
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb'
                                                }
                                            ) if 'system:dict:remove' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='dict_type-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'border-color': '#ffe399'
                                                }
                                            ) if 'system:dict:export' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-sync'
                                                    ),
                                                    '刷新缓存',
                                                ],
                                                id='dict_type-refresh-cache',
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb'
                                                }
                                            ) if 'system:dict:edit' in button_perms else [],
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
                                                        id='dict_type-hidden',
                                                        shape='circle'
                                                    ),
                                                    id='dict_type-hidden-tooltip',
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
                                                        id='dict_type-refresh',
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
                                            id='dict_type-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'dict_id',
                                                    'title': '字典编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'dict_name',
                                                    'title': '字典名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'dict_type',
                                                    'title': '字典类型',
                                                    'renderOptions': {
                                                        'renderType': 'button'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status',
                                                    'title': '状态',
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

        # 新增和编辑字典类型表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id={
                                                'type': 'dict_type-form-value',
                                                'index': 'dict_name'
                                            },
                                            placeholder='请输入字典名称',
                                            allowClear=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='字典名称',
                                        required=True,
                                        id={
                                            'type': 'dict_type-form-label',
                                            'index': 'dict_name',
                                            'required': True
                                        }
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
                                            id={
                                                'type': 'dict_type-form-value',
                                                'index': 'dict_type'
                                            },
                                            placeholder='请输入字典类型',
                                            allowClear=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='字典类型',
                                        required=True,
                                        id={
                                            'type': 'dict_type-form-label',
                                            'index': 'dict_type',
                                            'required': True
                                        }
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
                                            id={
                                                'type': 'dict_type-form-value',
                                                'index': 'status'
                                            },
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
                                                'width': 350
                                            }
                                        ),
                                        label='状态',
                                        id={
                                            'type': 'dict_type-form-label',
                                            'index': 'status',
                                            'required': False
                                        }
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
                                            id={
                                                'type': 'dict_type-form-value',
                                                'index': 'remark'
                                            },
                                            placeholder='请输入内容',
                                            allowClear=True,
                                            mode='text-area',
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='备注',
                                        id={
                                            'type': 'dict_type-form-label',
                                            'index': 'remark',
                                            'required': False
                                        }
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
            id='dict_type-modal',
            mask=False,
            width=580,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除字典类型二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='dict_type-delete-text'),
            id='dict_type-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),

        # 字典数据modal
        fac.AntdModal(
            dict_data.render(button_perms),
            id='dict_type_to_dict_data-modal',
            mask=False,
            maskClosable=False,
            width=1000,
            renderFooter=False,
            okClickClose=False
        )
    ]
