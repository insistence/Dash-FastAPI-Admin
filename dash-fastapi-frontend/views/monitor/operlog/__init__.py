from dash import dcc, html
import feffery_antd_components as fac

import callbacks.monitor_c.operlog_c
from api.log import get_operation_log_list_api


def render(button_perms):

    operation_log_params = dict(page_num=1, page_size=10)
    table_info = get_operation_log_list_api(operation_log_params)
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
            if item['status'] == 0:
                item['status'] = dict(tag='成功', color='blue')
            else:
                item['status'] = dict(tag='失败', color='volcano')
            if item['business_type'] == 0:
                item['business_type'] = dict(tag='其他', color='purple')
            elif item['business_type'] == 1:
                item['business_type'] = dict(tag='新增', color='green')
            elif item['business_type'] == 2:
                item['business_type'] = dict(tag='修改', color='orange')
            elif item['business_type'] == 3:
                item['business_type'] = dict(tag='删除', color='red')
            elif item['business_type'] == 4:
                item['business_type'] = dict(tag='授权', color='lime')
            elif item['business_type'] == 5:
                item['business_type'] = dict(tag='导出', color='geekblue')
            elif item['business_type'] == 6:
                item['business_type'] = dict(tag='导入', color='blue')
            elif item['business_type'] == 7:
                item['business_type'] = dict(tag='强退', color='magenta')
            elif item['business_type'] == 8:
                item['business_type'] = dict(tag='生成代码', color='cyan')
            elif item['business_type'] == 9:
                item['business_type'] = dict(tag='清空数据', color='volcano')
            item['key'] = str(item['oper_id'])
            item['cost_time'] = f"{item['cost_time']}毫秒"
            item['operation'] = [
                {
                    'content': '详情',
                    'type': 'link',
                    'icon': 'antd-eye'
                } if 'monitor:operlog:query' in button_perms else {},
            ]

    return [
        dcc.Store(id='operation_log-button-perms-container', data=button_perms),
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='operation_log-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='operation_log-export-container'),
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
                                                            id='operation_log-title-input',
                                                            placeholder='请输入系统模块',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='系统模块',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='operation_log-oper_name-input',
                                                            placeholder='请输入操作人员',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='操作人员',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='operation_log-business_type-select',
                                                            placeholder='操作类型',
                                                            options=[
                                                                {
                                                                    'label': '新增',
                                                                    'value': 1
                                                                },
                                                                {
                                                                    'label': '修改',
                                                                    'value': 2
                                                                },
                                                                {
                                                                    'label': '删除',
                                                                    'value': 3
                                                                },
                                                                {
                                                                    'label': '授权',
                                                                    'value': 4
                                                                },
                                                                {
                                                                    'label': '导出',
                                                                    'value': 5
                                                                },
                                                                {
                                                                    'label': '导入',
                                                                    'value': 6
                                                                },
                                                                {
                                                                    'label': '强退',
                                                                    'value': 7
                                                                },
                                                                {
                                                                    'label': '生成代码',
                                                                    'value': 8
                                                                },
                                                                {
                                                                    'label': '清空数据',
                                                                    'value': 9
                                                                },
                                                                {
                                                                    'label': '其他',
                                                                    'value': 0
                                                                },
                                                            ],
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='类型',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='operation_log-status-select',
                                                            placeholder='操作状态',
                                                            options=[
                                                                {
                                                                    'label': '成功',
                                                                    'value': 0
                                                                },
                                                                {
                                                                    'label': '失败',
                                                                    'value': 1
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
                                                            id='operation_log-oper_time-range',
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='操作时间',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '搜索',
                                                            id='operation_log-search',
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
                                                            id='operation_log-reset',
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
                                        hidden='monitor:operlog:query' not in button_perms
                                    ),
                                )
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpace(
                                        [
                                            html.Div(
                                                [
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-delete'
                                                            ),
                                                            '删除',
                                                        ],
                                                        id='operation_log-delete',
                                                        disabled=True,
                                                        style={
                                                            'color': '#ff9292',
                                                            'background': '#ffeded',
                                                            'border-color': '#ffdbdb'
                                                        }
                                                    ),
                                                ],
                                                hidden='monitor:operlog:remove' not in button_perms
                                            ),
                                            html.Div(
                                                [
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-clear'
                                                            ),
                                                            '清空',
                                                        ],
                                                        id='operation_log-clear',
                                                        style={
                                                            'color': '#ff9292',
                                                            'background': '#ffeded',
                                                            'border-color': '#ffdbdb'
                                                        }
                                                    ),
                                                ],
                                                hidden='monitor:operlog:remove' not in button_perms
                                            ),
                                            html.Div(
                                                [
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-arrow-down'
                                                            ),
                                                            '导出',
                                                        ],
                                                        id='operation_log-export',
                                                        style={
                                                            'color': '#ffba00',
                                                            'background': '#fff8e6',
                                                            'border-color': '#ffe399'
                                                        }
                                                    ),
                                                ],
                                                hidden='monitor:operlog:export' not in button_perms
                                            ),
                                        ],
                                        style={
                                            'paddingBottom': '10px'
                                        }
                                    ),
                                )
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpin(
                                        fac.AntdTable(
                                            id='operation_log-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'oper_id',
                                                    'title': '日志编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'title',
                                                    'title': '系统模块',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'business_type',
                                                    'title': '操作类型',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'oper_name',
                                                    'title': '操作人员',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'oper_ip',
                                                    'title': '操作地址',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'oper_location',
                                                    'title': '操作地点',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status',
                                                    'title': '操作状态',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'oper_time',
                                                    'title': '操作日期',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'cost_time',
                                                    'title': '消耗时间',
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

        # 操作日志明细modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-title-text'),
                                        label='操作模块',
                                        required=True,
                                        id='operation_log-title-form-item',
                                        labelCol={
                                            'span': 8
                                        },
                                        wrapperCol={
                                            'span': 16
                                        }
                                    ),
                                    span=12
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-oper_url-text'),
                                        label='请求地址',
                                        required=True,
                                        id='operation_log-oper_url-form-item',
                                        labelCol={
                                            'span': 8
                                        },
                                        wrapperCol={
                                            'span': 16
                                        }
                                    ),
                                    span=12
                                ),
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-login_info-text'),
                                        label='登录信息',
                                        required=True,
                                        id='operation_log-login_info-form-item',
                                        labelCol={
                                            'span': 8
                                        },
                                        wrapperCol={
                                            'span': 16
                                        }
                                    ),
                                    span=12
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-request_method-text'),
                                        label='请求方式',
                                        required=True,
                                        id='operation_log-request_method-form-item',
                                        labelCol={
                                            'span': 8
                                        },
                                        wrapperCol={
                                            'span': 16
                                        }
                                    ),
                                    span=12
                                ),
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-method-text'),
                                        label='操作方法',
                                        required=True,
                                        id='operation_log-method-form-item',
                                        labelCol={
                                            'span': 4
                                        },
                                        wrapperCol={
                                            'span': 20
                                        }
                                    ),
                                    span=24
                                ),
                            ],
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-oper_param-text'),
                                        label='请求参数',
                                        required=True,
                                        id='operation_log-oper_param-form-item',
                                        labelCol={
                                            'span': 4
                                        },
                                        wrapperCol={
                                            'span': 20
                                        }
                                    ),
                                    span=24
                                ),
                            ],
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-json_result-text'),
                                        label='返回参数',
                                        required=True,
                                        id='operation_log-json_result-form-item',
                                        labelCol={
                                            'span': 4
                                        },
                                        wrapperCol={
                                            'span': 20
                                        }
                                    ),
                                    span=24
                                ),
                            ],
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-status-text'),
                                        label='操作状态',
                                        required=True,
                                        id='operation_log-status-form-item',
                                        labelCol={
                                            'span': 12
                                        },
                                        wrapperCol={
                                            'span': 12
                                        }
                                    ),
                                    span=8
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-cost_time-text'),
                                        label='消耗时间',
                                        required=True,
                                        id='operation_log-cost_time-form-item',
                                        labelCol={
                                            'span': 12
                                        },
                                        wrapperCol={
                                            'span': 12
                                        }
                                    ),
                                    span=6
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(id='operation_log-oper_time-text'),
                                        label='操作时间',
                                        required=True,
                                        id='operation_log-oper_time-form-item',
                                        labelCol={
                                            'span': 8
                                        },
                                        wrapperCol={
                                            'span': 16
                                        }
                                    ),
                                    span=10
                                ),
                            ],
                            gutter=5
                        ),
                    ],
                    labelCol={
                        'span': 8
                    },
                    wrapperCol={
                        'span': 16
                    },
                    style={
                        'marginRight': '15px'
                    }
                )
            ],
            id='operation_log-modal',
            mask=False,
            width=850,
            renderFooter=False,
        ),

        # 删除操作日志二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='operation_log-delete-text'),
            id='operation_log-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),
    ]
