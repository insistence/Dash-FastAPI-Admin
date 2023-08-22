from dash import dcc, html
import feffery_antd_components as fac
import json

import callbacks.monitor_c.job_c
from api.job import get_job_list_api
from api.dict import query_dict_data_list_api


def render(button_perms):

    option = []
    option_table = []
    info = query_dict_data_list_api(dict_type='sys_job_group')
    if info.get('code') == 200:
        data = info.get('data')
        option = [dict(label=item.get('dict_label'), value=item.get('dict_value')) for item in data]
        option_table = [
            dict(label=item.get('dict_label'), value=item.get('dict_value'), css_class=item.get('css_class')) for item
            in data]
    option_dict = {item.get('value'): item for item in option_table}

    job_params = dict(page_num=1, page_size=10)
    table_info = get_job_list_api(job_params)
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
                item['status'] = dict(checked=True)
            else:
                item['status'] = dict(checked=False)
            if str(item.get('job_group')) in option_dict.keys():
                item['job_group'] = dict(
                    tag=option_dict.get(str(item.get('job_group'))).get('label'),
                    color=json.loads(option_dict.get(str(item.get('job_group'))).get('css_class')).get('color')
                )
            item['key'] = str(item['job_id'])
            item['operation'] = [
                {
                    'title': '修改',
                    'icon': 'antd-edit'
                } if 'monitor:job:edit' in button_perms else None,
                {
                    'title': '删除',
                    'icon': 'antd-delete'
                } if 'monitor:job:remove' in button_perms else None,
                {
                    'title': '执行一次',
                    'icon': 'antd-rocket'
                } if 'monitor:job:changeStatus' in button_perms else None,
                {
                    'title': '任务详细',
                    'icon': 'antd-eye'
                } if 'monitor:job:query' in button_perms else None,
                {
                    'title': '调度日志',
                    'icon': 'antd-history'
                } if 'monitor:job:query' in button_perms else None
            ]

    return [
        dcc.Store(id='job-button-perms-container', data=button_perms),
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='job-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='job-export-container'),
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
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='job-job_name-input',
                                                                    placeholder='请输入任务名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    }
                                                                ),
                                                                label='任务名称'
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdSelect(
                                                                    id='job-job_group-select',
                                                                    placeholder='请选择任务组名',
                                                                    options=option,
                                                                    style={
                                                                        'width': 210
                                                                    }
                                                                ),
                                                                label='任务组名'
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdSelect(
                                                                    id='job-status-select',
                                                                    placeholder='请选择任务状态',
                                                                    options=[
                                                                        {
                                                                            'label': '正常',
                                                                            'value': '0'
                                                                        },
                                                                        {
                                                                            'label': '暂停',
                                                                            'value': '1'
                                                                        }
                                                                    ],
                                                                    style={
                                                                        'width': 200
                                                                    }
                                                                ),
                                                                label='任务状态'
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='job-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    )
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='job-reset',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-sync'
                                                                    )
                                                                )
                                                            )
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        }
                                                    ),
                                                ],
                                                layout='inline',
                                            )
                                        ],
                                        id='job-search-form-container',
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
                                            html.Div(
                                                [
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-plus'
                                                            ),
                                                            '新增',
                                                        ],
                                                        id='job-add',
                                                        style={
                                                            'color': '#1890ff',
                                                            'background': '#e8f4ff',
                                                            'border-color': '#a3d3ff'
                                                        }
                                                    ),
                                                ],
                                                hidden='monitor:job:add' not in button_perms
                                            ),
                                            html.Div(
                                                [
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-edit'
                                                            ),
                                                            '修改',
                                                        ],
                                                        id='job-edit',
                                                        disabled=True,
                                                        style={
                                                            'color': '#71e2a3',
                                                            'background': '#e7faf0',
                                                            'border-color': '#d0f5e0'
                                                        }
                                                    ),
                                                ],
                                                hidden='monitor:job:edit' not in button_perms
                                            ),
                                            html.Div(
                                                [
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-minus'
                                                            ),
                                                            '删除',
                                                        ],
                                                        id='job-delete',
                                                        disabled=True,
                                                        style={
                                                            'color': '#ff9292',
                                                            'background': '#ffeded',
                                                            'border-color': '#ffdbdb'
                                                        }
                                                    ),
                                                ],
                                                hidden='monitor:job:remove' not in button_perms
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
                                                        id='job-export',
                                                        style={
                                                            'color': '#ffba00',
                                                            'background': '#fff8e6',
                                                            'border-color': '#ffe399'
                                                        }
                                                    ),
                                                ],
                                                hidden='monitor:job:export' not in button_perms
                                            ),
                                            html.Div(
                                                [
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-history'
                                                            ),
                                                            '调度日志',
                                                        ],
                                                        id='job-log',
                                                        style={
                                                            'color': '#909399',
                                                            'background': '#f4f4f5',
                                                            'border-color': '#d3d4d6'
                                                        }
                                                    ),
                                                ],
                                                hidden='monitor:job:query' not in button_perms
                                            ),
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
                                                        id='job-hidden',
                                                        shape='circle'
                                                    ),
                                                    id='job-hidden-tooltip',
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
                                                        id='job-refresh',
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
                                            id='job-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'job_id',
                                                    'title': '任务编号',
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
                                                    'dataIndex': 'job_group',
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
                                                    'dataIndex': 'cron_expression',
                                                    'title': 'cron执行表达式',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status',
                                                    'title': '状态',
                                                    'renderOptions': {
                                                        'renderType': 'switch'
                                                    },
                                                },
                                                {
                                                    'title': '操作',
                                                    'dataIndex': 'operation',
                                                    'renderOptions': {
                                                        'renderType': 'dropdown',
                                                        'dropdownProps': {
                                                            'title': '更多'
                                                        }
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

        # 新增和编辑定时任务表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='job-job_name',
                                            placeholder='请输入任务名称',
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        id='job-job_name-form-item',
                                        required=True,
                                        label='任务名称',
                                        labelCol={
                                            'span': 6
                                        },
                                        wrapperCol={
                                            'span': 18
                                        }
                                    ),
                                    span=12
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdSelect(
                                            id='job-job_group',
                                            placeholder='请选择任务分组',
                                            options=option,
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        id='job-job_group-form-item',
                                        label='任务分组',
                                        labelCol={
                                            'span': 6
                                        },
                                        wrapperCol={
                                            'span': 18
                                        }
                                    ),
                                    span=12
                                )
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='job-invoke_target',
                                            placeholder='请输入调用目标字符串',
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        id='job-invoke_target-form-item',
                                        required=True,
                                        label='调用方法',
                                        labelCol={
                                            'span': 3
                                        },
                                        wrapperCol={
                                            'span': 21
                                        }
                                    ),
                                    span=24
                                ),
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='job-cron_expression',
                                            placeholder='请输入cron执行表达式',
                                            addonAfter=html.Div(
                                                [
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdText('生成表达式'),
                                                            fac.AntdIcon(icon='antd-field-time')
                                                        ]
                                                    )
                                                ],
                                                id='generate-expression'
                                            ),
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        id='job-cron_expression-form-item',
                                        required=True,
                                        label='cron表达式',
                                        labelCol={
                                            'span': 3
                                        },
                                        wrapperCol={
                                            'span': 21
                                        }
                                    ),
                                    span=24
                                ),
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdRadioGroup(
                                            id='job-misfire_policy',
                                            options=[
                                                {
                                                    'label': '立即执行',
                                                    'value': '1'
                                                },
                                                {
                                                    'label': '执行一次',
                                                    'value': '2'
                                                },
                                                {
                                                    'label': '放弃执行',
                                                    'value': '3'
                                                }
                                            ],
                                            defaultValue='1',
                                            optionType='button',
                                            buttonStyle='solid'
                                        ),
                                        id='job-misfire_policy-form-item',
                                        label='执行策略',
                                        labelCol={
                                            'span': 3
                                        },
                                        wrapperCol={
                                            'span': 21
                                        }
                                    ),
                                    span=24
                                ),
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdRadioGroup(
                                            id='job-concurrent',
                                            options=[
                                                {
                                                    'label': '允许',
                                                    'value': '0'
                                                },
                                                {
                                                    'label': '禁止',
                                                    'value': '1'
                                                }
                                            ],
                                            defaultValue='1',
                                            optionType='button',
                                            buttonStyle='solid'
                                        ),
                                        id='job-concurrent-form-item',
                                        label='是否并发',
                                        labelCol={
                                            'span': 6
                                        },
                                        wrapperCol={
                                            'span': 18
                                        }
                                    ),
                                    span=12
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdRadioGroup(
                                            id='job-status',
                                            options=[
                                                {
                                                    'label': '正常',
                                                    'value': '0'
                                                },
                                                {
                                                    'label': '暂停',
                                                    'value': '1'
                                                },
                                            ],
                                            defaultValue='0',
                                        ),
                                        id='job-status-form-item',
                                        label='状态',
                                        labelCol={
                                            'span': 6
                                        },
                                        wrapperCol={
                                            'span': 18
                                        }
                                    ),
                                    span=12
                                ),
                            ],
                            gutter=5
                        )
                    ],
                    style={
                        'marginRight': '30px'
                    }
                )
            ],
            id='job-modal',
            mask=False,
            width=850,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除定时任务二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='job-delete-text'),
            id='job-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),
    ]
