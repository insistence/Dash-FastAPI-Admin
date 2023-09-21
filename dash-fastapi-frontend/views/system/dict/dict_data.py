from dash import dcc, html
import feffery_antd_components as fac

import callbacks.system_c.dict_c.dict_data_c


def render(button_perms):

    return [
        dcc.Store(id='dict_data-button-perms-container', data=button_perms),
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='dict_data-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='dict_data-export-container'),
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
                                                        fac.AntdSelect(
                                                            id='dict_data-dict_type-select',
                                                            placeholder='字典名称',
                                                            options=[],
                                                            allowClear=False,
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='字典名称',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='dict_data-dict_label-input',
                                                            placeholder='请输入字典标签',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='字典标签',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='dict_data-status-select',
                                                            placeholder='数据状态',
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
                                                        fac.AntdButton(
                                                            '搜索',
                                                            id='dict_data-search',
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
                                                            id='dict_data-reset',
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
                                        id='dict_data-search-form-container',
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
                                                    'type': 'dict_data-operation-button',
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
                                                    'type': 'dict_data-operation-button',
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
                                                    'type': 'dict_data-operation-button',
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
                                                id='dict_data-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'border-color': '#ffe399'
                                                }
                                            ) if 'system:dict:export' in button_perms else [],
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
                                                        id='dict_data-hidden',
                                                        shape='circle'
                                                    ),
                                                    id='dict_data-hidden-tooltip',
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
                                                        id='dict_data-refresh',
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
                                            id='dict_data-list-table',
                                            data=[],
                                            columns=[
                                                {
                                                    'dataIndex': 'dict_code',
                                                    'title': '字典编码',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'dict_label',
                                                    'title': '字典标签',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'dict_value',
                                                    'title': '字典键值',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'dict_sort',
                                                    'title': '字典排序',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
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
                                                    'fixed': 'right',
                                                    'width': 150,
                                                    'renderOptions': {
                                                        'renderType': 'button'
                                                    },
                                                }
                                            ],
                                            rowSelectionType='checkbox',
                                            rowSelectionWidth=50,
                                            bordered=True,
                                            maxWidth=1000,
                                            pagination={
                                                'pageSize': 10,
                                                'current': 1,
                                                'showSizeChanger': True,
                                                'pageSizeOptions': [10, 30, 50, 100],
                                                'showQuickJumper': True,
                                                'total': 0
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

        # 新增和编辑字典数据表单modal
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
                                                'type': 'dict_data-form-value',
                                                'index': 'dict_type'
                                            },
                                            placeholder='请输入字典类型',
                                            disabled=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='字典类型',
                                        id={
                                            'type': 'dict_data-form-label',
                                            'index': 'dict_type',
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
                                                'type': 'dict_data-form-value',
                                                'index': 'dict_label'
                                            },
                                            placeholder='请输入数据标签',
                                            allowClear=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='数据标签',
                                        required=True,
                                        id={
                                            'type': 'dict_data-form-label',
                                            'index': 'dict_label',
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
                                                'type': 'dict_data-form-value',
                                                'index': 'dict_value'
                                            },
                                            placeholder='请输入数据键值',
                                            allowClear=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='数据键值',
                                        required=True,
                                        id={
                                            'type': 'dict_data-form-label',
                                            'index': 'dict_value',
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
                                                'type': 'dict_data-form-value',
                                                'index': 'css_class'
                                            },
                                            placeholder='请输入样式属性',
                                            allowClear=True,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='样式属性',
                                        id={
                                            'type': 'dict_data-form-label',
                                            'index': 'css_class',
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
                                        fac.AntdInputNumber(
                                            id={
                                                'type': 'dict_data-form-value',
                                                'index': 'dict_sort'
                                            },
                                            defaultValue=0,
                                            min=0,
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='显示排序',
                                        required=True,
                                        id={
                                            'type': 'dict_data-form-label',
                                            'index': 'dict_sort',
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
                                        fac.AntdSelect(
                                            id={
                                                'type': 'dict_data-form-value',
                                                'index': 'list_class'
                                            },
                                            placeholder='回显样式',
                                            options=[
                                                {
                                                    'label': '默认',
                                                    'value': 'default'
                                                },
                                                {
                                                    'label': '主要',
                                                    'value': 'primary'
                                                },
                                                {
                                                    'label': '成功',
                                                    'value': 'success'
                                                },
                                                {
                                                    'label': '信息',
                                                    'value': 'info'
                                                },
                                                {
                                                    'label': '警告',
                                                    'value': 'warning'
                                                },
                                                {
                                                    'label': '危险',
                                                    'value': 'danger'
                                                }
                                            ],
                                            style={
                                                'width': 350
                                            }
                                        ),
                                        label='回显样式',
                                        id={
                                            'type': 'dict_data-form-label',
                                            'index': 'list_class',
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
                                        fac.AntdRadioGroup(
                                            id={
                                                'type': 'dict_data-form-value',
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
                                            'type': 'dict_data-form-label',
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
                                                'type': 'dict_data-form-value',
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
                                            'type': 'dict_data-form-label',
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
            id='dict_data-modal',
            mask=False,
            maskClosable=False,
            width=580,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除字典数据二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='dict_data-delete-text'),
            id='dict_data-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True
        ),
    ]
