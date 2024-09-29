import feffery_antd_components as fac
from dash import dcc, html
from callbacks.monitor_c.job_c import job_log_c  # noqa: F401
from components.ApiSelect import ApiSelect
from utils.permission_util import PermissionManager


def render():
    return [
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='job_log-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='job_log-export-container'),
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
                                                            id='job_log-job_name-input',
                                                            placeholder='请输入任务名称',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            },
                                                        ),
                                                        label='任务名称',
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        ApiSelect(
                                                            dict_type='sys_job_group',
                                                            id='job_log-job_group-select',
                                                            placeholder='请选择任务组名',
                                                            style={
                                                                'width': 240
                                                            },
                                                        ),
                                                        label='任务组名',
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='job_log-status-select',
                                                            placeholder='请选择执行状态',
                                                            options=[
                                                                {
                                                                    'label': '成功',
                                                                    'value': '0',
                                                                },
                                                                {
                                                                    'label': '失败',
                                                                    'value': '1',
                                                                },
                                                            ],
                                                            style={
                                                                'width': 240
                                                            },
                                                        ),
                                                        label='执行状态',
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdDateRangePicker(
                                                            id='job_log-create_time-range',
                                                            style={
                                                                'width': 240
                                                            },
                                                        ),
                                                        label='执行时间',
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '搜索',
                                                            id='job_log-search',
                                                            type='primary',
                                                            icon=fac.AntdIcon(
                                                                icon='antd-search'
                                                            ),
                                                        ),
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '重置',
                                                            id='job_log-reset',
                                                            icon=fac.AntdIcon(
                                                                icon='antd-sync'
                                                            ),
                                                        ),
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                ],
                                                layout='inline',
                                            )
                                        ],
                                        id='job_log-search-form-container',
                                        hidden=False,
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
                                                        icon='antd-delete'
                                                    ),
                                                    '删除',
                                                ],
                                                id={
                                                    'type': 'job_log-operation-button',
                                                    'index': 'delete',
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'monitor:job:remove'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-clear'
                                                    ),
                                                    '清空',
                                                ],
                                                id={
                                                    'type': 'job_log-operation-button',
                                                    'index': 'clear',
                                                },
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'monitor:job:remove'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='job_log-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'border-color': '#ffe399',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'monitor:job:export'
                                            )
                                            else [],
                                        ],
                                        style={'paddingBottom': '10px'},
                                    ),
                                    span=16,
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
                                                        id='job_log-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='job_log-hidden-tooltip',
                                                    title='隐藏搜索',
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
                                                        id='job_log-refresh',
                                                        shape='circle',
                                                    ),
                                                    title='刷新',
                                                )
                                            ),
                                        ],
                                        style={
                                            'float': 'right',
                                            'paddingBottom': '10px',
                                        },
                                    ),
                                    span=8,
                                    style={'paddingRight': '10px'},
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpin(
                                        fac.AntdTable(
                                            id='job_log-list-table',
                                            data=[],
                                            columns=[
                                                {
                                                    'dataIndex': 'job_log_id',
                                                    'title': '日志编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'job_name',
                                                    'title': '任务名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'job_group_tag',
                                                    'title': '任务组名',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'invoke_target',
                                                    'title': '调用目标字符串',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'job_message',
                                                    'title': '日志信息',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status_tag',
                                                    'title': '执行状态',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'create_time',
                                                    'title': '执行时间',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'title': '操作',
                                                    'dataIndex': 'operation',
                                                    'width': 120,
                                                    'renderOptions': {
                                                        'renderType': 'button'
                                                    },
                                                },
                                            ],
                                            rowSelectionType='checkbox',
                                            rowSelectionWidth=50,
                                            bordered=True,
                                            pagination={
                                                'pageSize': 10,
                                                'current': 1,
                                                'showSizeChanger': True,
                                                'pageSizeOptions': [
                                                    10,
                                                    30,
                                                    50,
                                                    100,
                                                ],
                                                'showQuickJumper': True,
                                                'total': 0,
                                            },
                                            mode='server-side',
                                            style={
                                                'width': '100%',
                                                'padding-right': '10px',
                                            },
                                        ),
                                        text='数据加载中',
                                    ),
                                )
                            ]
                        ),
                    ],
                    span=24,
                )
            ],
            gutter=5,
        ),
        # 任务调度日志明细modal，表单项id使用字典类型，index与后端数据库字段一一对应
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'job_name',
                                            }
                                        ),
                                        label='任务名称',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'job_name',
                                        },
                                        labelCol={'span': 8},
                                        wrapperCol={'span': 16},
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'job_group',
                                            }
                                        ),
                                        label='任务分组',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'job_group',
                                        },
                                        labelCol={'span': 8},
                                        wrapperCol={'span': 16},
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'job_executor',
                                            }
                                        ),
                                        label='任务执行器',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'job_executor',
                                        },
                                        labelCol={'span': 8},
                                        wrapperCol={'span': 16},
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'invoke_target',
                                            }
                                        ),
                                        label='调用目标字符串',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'invoke_target',
                                        },
                                        labelCol={'span': 8},
                                        wrapperCol={'span': 16},
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'job_args',
                                            }
                                        ),
                                        label='位置参数',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'job_args',
                                        },
                                        labelCol={'span': 8},
                                        wrapperCol={'span': 16},
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'job_kwargs',
                                            }
                                        ),
                                        label='关键字参数',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'job_kwargs',
                                        },
                                        labelCol={'span': 8},
                                        wrapperCol={'span': 16},
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'job_trigger',
                                            }
                                        ),
                                        label='任务触发器',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'job_trigger',
                                        },
                                        labelCol={'span': 4},
                                        wrapperCol={'span': 20},
                                    ),
                                    span=24,
                                ),
                            ],
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'job_message',
                                            }
                                        ),
                                        label='日志信息',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'job_message',
                                        },
                                        labelCol={'span': 4},
                                        wrapperCol={'span': 20},
                                    ),
                                    span=24,
                                ),
                            ],
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'status',
                                            }
                                        ),
                                        label='执行状态',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'status',
                                        },
                                        labelCol={'span': 8},
                                        wrapperCol={'span': 16},
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'create_time',
                                            }
                                        ),
                                        label='执行时间',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'create_time',
                                        },
                                        labelCol={'span': 8},
                                        wrapperCol={'span': 16},
                                    ),
                                    span=12,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdText(
                                            id={
                                                'type': 'job_log-form-value',
                                                'index': 'exception_info',
                                            }
                                        ),
                                        label='异常信息',
                                        required=True,
                                        id={
                                            'type': 'job_log-form-label',
                                            'index': 'exception_info',
                                        },
                                        labelCol={'span': 4},
                                        wrapperCol={'span': 20},
                                    ),
                                    span=24,
                                ),
                            ],
                        ),
                    ],
                    labelCol={'span': 8},
                    wrapperCol={'span': 16},
                    style={'marginRight': '15px'},
                )
            ],
            id='job_log-modal',
            mask=False,
            width=850,
            renderFooter=False,
        ),
        # 删除任务调度日志二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='job_log-delete-text'),
            id='job_log-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
    ]
