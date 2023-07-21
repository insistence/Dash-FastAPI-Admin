from dash import dcc, html
import feffery_antd_components as fac

from . import profile
from api.user import get_user_list_api
from api.dept import get_dept_tree_api

import callbacks.system_c.user_c.user_c


def render(button_perms):
    dept_params = dict(dept_name='')
    user_params = dict(page_num=1, page_size=10)
    tree_info = get_dept_tree_api(dept_params)
    table_info = get_user_list_api(user_params)
    tree_data = []
    table_data = []
    page_num = 1
    page_size = 10
    total = 0
    if tree_info['code'] == 200:
        tree_data = tree_info['data']
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
            item['key'] = str(item['user_id'])
            item['operation'] = [
                {
                    'title': '修改',
                    'icon': 'antd-edit'
                } if 'system:user:edit' in button_perms else None,
                {
                    'title': '删除',
                    'icon': 'antd-delete'
                } if 'system:user:remove' in button_perms else None,
                {
                    'title': '重置密码',
                    'icon': 'antd-key'
                } if 'system:user:resetPwd' in button_perms else None
            ]

    return [
        dcc.Store(id='user-button-perms-container', data=button_perms),
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdInput(
                            id='dept-input-search',
                            placeholder='请输入部门名称',
                            autoComplete='off',
                            allowClear=True,
                            prefix=fac.AntdIcon(
                                icon='antd-search'
                            ),
                            style={
                                'width': '85%'
                            }
                        ),
                        fac.AntdTree(
                            id='dept-tree',
                            treeData=tree_data,
                            defaultExpandAll=True,
                            showLine=False,
                            style={
                                'margin-top': '10px'
                            }
                        )
                    ],
                    span=4
                ),
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
                                                                    id='user-user_name-input',
                                                                    placeholder='请输入用户名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    }
                                                                ),
                                                                label='用户名称'
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='user-phone_number-input',
                                                                    placeholder='请输入手机号码',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    }
                                                                ),
                                                                label='手机号码'
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdSelect(
                                                                    id='user-status-select',
                                                                    placeholder='用户状态',
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
                                                                label='用户状态'
                                                            ),
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        }
                                                    ),
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdFormItem(
                                                                fac.AntdDateRangePicker(
                                                                    id='user-create_time-range',
                                                                    style={
                                                                        'width': 240
                                                                    }
                                                                ),
                                                                label='创建时间'
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='user-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    )
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='user-reset',
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
                                        hidden='system:user:query' not in button_perms
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
                                                        id='user-add',
                                                        style={
                                                            'color': '#1890ff',
                                                            'background': '#e8f4ff',
                                                            'border-color': '#a3d3ff'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:user:add' not in button_perms
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
                                                        id='user-edit',
                                                        disabled=True,
                                                        style={
                                                            'color': '#71e2a3',
                                                            'background': '#e7faf0',
                                                            'border-color': '#d0f5e0'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:user:edit' not in button_perms
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
                                                        id='user-delete',
                                                        disabled=True,
                                                        style={
                                                            'color': '#ff9292',
                                                            'background': '#ffeded',
                                                            'border-color': '#ffdbdb'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:user:remove' not in button_perms
                                            ),
                                            html.Div(
                                                [
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-arrow-up'
                                                            ),
                                                            '导入',
                                                        ],
                                                        id='user-import',
                                                        style={
                                                            'color': '#909399',
                                                            'background': '#f4f4f5',
                                                            'border-color': '#d3d4d6'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:user:export' not in button_perms
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
                                                        id='user-export',
                                                        style={
                                                            'color': '#ffba00',
                                                            'background': '#fff8e6',
                                                            'border-color': '#ffe399'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:user:import' not in button_perms
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
                                            id='user-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'user_id',
                                                    'title': '用户编号',
                                                    'width': 100,
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'user_name',
                                                    'title': '用户名称',
                                                    'width': 120,
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'nick_name',
                                                    'title': '用户昵称',
                                                    'width': 120,
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'dept_name',
                                                    'title': '部门',
                                                    'width': 130,
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'phonenumber',
                                                    'title': '手机号码',
                                                    'width': 130,
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status',
                                                    'title': '状态',
                                                    'width': 110,
                                                    'renderOptions': {
                                                        'renderType': 'switch'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'create_time',
                                                    'title': '创建时间',
                                                    'width': 160,
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
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
                    span=20
                )
            ],
            gutter=5
        ),

        # 新增用户表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-add-nick_name',
                                        placeholder='请输入用户昵称',
                                        allowClear=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='用户昵称',
                                    required=True,
                                    id='user-add-nick_name-form-item'
                                ),
                                fac.AntdFormItem(
                                    fac.AntdTreeSelect(
                                        id='user-add-dept_id',
                                        placeholder='请选择归属部门',
                                        treeData=[],
                                        treeNodeFilterProp='title',
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='归属部门',
                                    id='user-add-dept_id-form-item',
                                    labelCol={
                                        'offset': 1
                                    },
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-add-phone_number',
                                        placeholder='请输入手机号码',
                                        allowClear=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='手机号码',
                                    id='user-add-phone_number-form-item',
                                    labelCol={
                                        'offset': 1
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-add-email',
                                        placeholder='请输入邮箱',
                                        allowClear=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='邮箱',
                                    id='user-add-email-form-item',
                                    labelCol={
                                        'offset': 5
                                    },
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-add-user_name',
                                        placeholder='请输入用户名称',
                                        allowClear=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='用户名称',
                                    required=True,
                                    id='user-add-user_name-form-item'
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-add-password',
                                        placeholder='请输入密码',
                                        mode='password',
                                        passwordUseMd5=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='用户密码',
                                    required=True,
                                    id='user-add-password-form-item'
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id='user-add-sex',
                                        placeholder='请选择性别',
                                        options=[
                                            {
                                                'label': '男',
                                                'value': '0'
                                            },
                                            {
                                                'label': '女',
                                                'value': '1'
                                            },
                                            {
                                                'label': '未知',
                                                'value': '2'
                                            },
                                        ],
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='用户性别',
                                    id='user-add-sex-form-item',
                                    labelCol={
                                        'offset': 1
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdRadioGroup(
                                        id='user-add-status',
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
                                    label='用户状态',
                                    id='user-add-status-form-item',
                                    labelCol={
                                        'offset': 2
                                    },
                                )
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id='user-add-post',
                                        placeholder='请选择岗位',
                                        options=[],
                                        mode='multiple',
                                        optionFilterProp='label',
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='岗位',
                                    id='user-add-post-form-item',
                                    labelCol={
                                        'offset': 4
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id='user-add-role',
                                        placeholder='请选择角色',
                                        options=[],
                                        mode='multiple',
                                        optionFilterProp='label',
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='岗位',
                                    id='user-add-role-form-item',
                                    labelCol={
                                        'offset': 8
                                    },
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-add-remark',
                                        placeholder='请输入内容',
                                        allowClear=True,
                                        mode='text-area',
                                        style={
                                            'width': 490
                                        }
                                    ),
                                    label='备注',
                                    id='user-add-remark-form-item',
                                    labelCol={
                                        'offset': 2
                                    },
                                ),
                            ]
                        )
                    ]
                )
            ],
            id='user-add-modal',
            title='新增用户',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=False
        ),

        # 编辑用户表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-edit-nick_name',
                                        placeholder='请输入用户昵称',
                                        allowClear=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='用户昵称',
                                    required=True,
                                    id='user-edit-nick_name-form-item'
                                ),
                                fac.AntdFormItem(
                                    fac.AntdTreeSelect(
                                        id='user-edit-dept_id',
                                        placeholder='请选择归属部门',
                                        treeData=[],
                                        treeNodeFilterProp='title',
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='归属部门',
                                    id='user-edit-dept_id-form-item'
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-edit-phone_number',
                                        placeholder='请输入手机号码',
                                        allowClear=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='手机号码',
                                    id='user-edit-phone_number-form-item',
                                    labelCol={
                                        'offset': 1
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-edit-email',
                                        placeholder='请输入邮箱',
                                        allowClear=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='邮箱',
                                    id='user-edit-email-form-item',
                                    labelCol={
                                        'offset': 4
                                    },
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id='user-edit-sex',
                                        placeholder='请选择性别',
                                        options=[
                                            {
                                                'label': '男',
                                                'value': '0'
                                            },
                                            {
                                                'label': '女',
                                                'value': '1'
                                            },
                                            {
                                                'label': '未知',
                                                'value': '2'
                                            },
                                        ],
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='用户性别',
                                    id='user-edit-sex-form-item',
                                    labelCol={
                                        'offset': 1
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdRadioGroup(
                                        id='user-edit-status',
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
                                            'width': 200
                                        }
                                    ),
                                    label='用户状态',
                                    id='user-edit-status-form-item',
                                    labelCol={
                                        'offset': 1
                                    },
                                )
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id='user-edit-post',
                                        placeholder='请选择岗位',
                                        options=[],
                                        mode='multiple',
                                        optionFilterProp='label',
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='岗位',
                                    id='user-edit-post-form-item',
                                    labelCol={
                                        'offset': 4
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id='user-edit-role',
                                        placeholder='请选择角色',
                                        options=[],
                                        mode='multiple',
                                        optionFilterProp='label',
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='岗位',
                                    id='user-edit-role-form-item',
                                    labelCol={
                                        'offset': 7
                                    },
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='user-edit-remark',
                                        placeholder='请输入内容',
                                        allowClear=True,
                                        mode='text-area',
                                        style={
                                            'width': 485
                                        }
                                    ),
                                    label='备注',
                                    id='user-edit-remark-form-item',
                                    labelCol={
                                        'offset': 2
                                    },
                                ),
                            ]
                        )
                    ]
                )
            ],
            id='user-edit-modal',
            title='编辑用户',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除用户二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='user-delete-text'),
            id='user-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),

        # 重置密码modal
        fac.AntdModal(
            fac.AntdForm(
                [
                    fac.AntdFormItem(
                        fac.AntdInput(
                            id='reset-password-input',
                            mode='password'
                        ),
                    ),
                ],
                layout='vertical'
            ),
            id='user-reset-password-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),
    ]
