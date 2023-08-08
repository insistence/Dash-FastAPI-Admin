from dash import dcc, html
import feffery_antd_components as fac

import callbacks.system_c.role_c
from api.role import get_role_list_api


def render(button_perms):

    role_params = dict(page_num=1, page_size=10)
    table_info = get_role_list_api(role_params)
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
            item['key'] = str(item['role_id'])
            if item['role_id'] == 1:
                item['operation'] = []
            else:
                item['operation'] = [
                    {
                        'content': '修改',
                        'type': 'link',
                        'icon': 'antd-edit'
                    } if 'system:role:edit' in button_perms else {},
                    {
                        'content': '删除',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'system:role:remove' in button_perms else {},
                ]

    return [
        dcc.Store(id='role-button-perms-container', data=button_perms),
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
                                                            id='role-role_name-input',
                                                            placeholder='请输入角色名称',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 220
                                                            }
                                                        ),
                                                        label='角色名称',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='role-role_key-input',
                                                            placeholder='请输入权限字符',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 220
                                                            }
                                                        ),
                                                        label='权限字符',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='role-status-select',
                                                            placeholder='角色状态',
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
                                                                'width': 220
                                                            }
                                                        ),
                                                        label='状态',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdDateRangePicker(
                                                            id='role-create_time-range',
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
                                                            id='role-search',
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
                                                            id='role-reset',
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
                                        hidden='system:role:query' not in button_perms
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
                                                        id='role-add',
                                                        style={
                                                            'color': '#1890ff',
                                                            'background': '#e8f4ff',
                                                            'border-color': '#a3d3ff'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:role:add' not in button_perms
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
                                                        id='role-edit',
                                                        disabled=True,
                                                        style={
                                                            'color': '#71e2a3',
                                                            'background': '#e7faf0',
                                                            'border-color': '#d0f5e0'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:role:edit' not in button_perms
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
                                                        id='role-delete',
                                                        disabled=True,
                                                        style={
                                                            'color': '#ff9292',
                                                            'background': '#ffeded',
                                                            'border-color': '#ffdbdb'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:role:remove' not in button_perms
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
                                                        id='role-export',
                                                        style={
                                                            'color': '#ffba00',
                                                            'background': '#fff8e6',
                                                            'border-color': '#ffe399'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:role:export' not in button_perms
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
                                            id='role-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'role_id',
                                                    'title': '角色编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'role_name',
                                                    'title': '角色名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'role_key',
                                                    'title': '权限字符',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'role_sort',
                                                    'title': '显示顺序',
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

        # 新增和编辑角色表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='role-role_name',
                                placeholder='请输入角色名称',
                                allowClear=True,
                                style={
                                    'width': 350
                                }
                            ),
                            label='角色名称',
                            required=True,
                            id='role-role_name-form-item',
                            labelCol={
                                'span': 6
                            },
                            wrapperCol={
                                'span': 18
                            }
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='role-role_key',
                                placeholder='请输入权限字符',
                                allowClear=True,
                                style={
                                    'width': 350
                                }
                            ),
                            label=html.Div(
                                [
                                    fac.AntdTooltip(
                                        fac.AntdIcon(
                                            icon='antd-question-circle'
                                        ),
                                        title='控制器中定义的权限字符，如：common'
                                    ),
                                    fac.AntdText('权限字符')
                                ]
                            ),
                            required=True,
                            id='role-role_Key-form-item',
                            labelCol={
                                'span': 6
                            },
                            wrapperCol={
                                'span': 18
                            }
                        ),
                        fac.AntdFormItem(
                            fac.AntdInputNumber(
                                id='role-role_sort',
                                placeholder='请输入角色顺序',
                                defaultValue=0,
                                min=0,
                                style={
                                    'width': 350
                                }
                            ),
                            label='角色顺序',
                            required=True,
                            id='role-role_sort-form-item',
                            labelCol={
                                'span': 6
                            },
                            wrapperCol={
                                'span': 18
                            }
                        ),
                        fac.AntdFormItem(
                            fac.AntdRadioGroup(
                                id='role-status',
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
                                style={
                                    'width': 350
                                }
                            ),
                            label='状态',
                            id='role-status-form-item',
                            labelCol={
                                'span': 6
                            },
                            wrapperCol={
                                'span': 18
                            }
                        ),
                        fac.AntdFormItem(
                            [
                                fac.AntdRow(
                                    [
                                        fac.AntdCol(
                                            fac.AntdCheckbox(
                                                id='role-menu-perms-radio-fold-unfold',
                                                label='展开/折叠'
                                            ),
                                            span=7,
                                        ),
                                        fac.AntdCol(
                                            fac.AntdCheckbox(
                                                id='role-menu-perms-radio-all-none',
                                                label='全选/全不选'
                                            ),
                                            span=8,
                                        ),
                                        fac.AntdCol(
                                            fac.AntdCheckbox(
                                                id='role-menu-perms-radio-parent-children',
                                                label='父子联动',
                                                checked=True
                                            ),
                                            span=6,
                                        ),
                                    ],
                                    style={
                                        'paddingTop': '6px'
                                    }
                                ),
                                fac.AntdRow(
                                    fac.AntdCol(
                                        html.Div(
                                            [
                                                fac.AntdTree(
                                                    id='role-menu-perms',
                                                    treeData=[],
                                                    multiple=True,
                                                    checkable=True,
                                                    showLine=False,
                                                    selectable=False
                                                )
                                            ],
                                            style={
                                                'border': 'solid 1px rgba(0, 0, 0, 0.2)',
                                                'border-radius': '5px',
                                                'width': 350
                                            }
                                        )
                                    ),
                                    style={
                                        'paddingTop': '6px'
                                    }
                                ),
                            ],
                            label='菜单权限',
                            id='role-menu-perms-form-item',
                            labelCol={
                                'span': 6
                            },
                            wrapperCol={
                                'span': 18
                            }
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='role-remark',
                                placeholder='请输入内容',
                                allowClear=True,
                                mode='text-area',
                                style={
                                    'width': 350
                                }
                            ),
                            label='备注',
                            id='role-remark-form-item',
                            labelCol={
                                'span': 6
                            },
                            wrapperCol={
                                'span': 18
                            }
                        ),
                    ]
                )
            ],
            id='role-modal',
            mask=False,
            width=600,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除角色二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='role-delete-text'),
            id='role-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),
    ]
