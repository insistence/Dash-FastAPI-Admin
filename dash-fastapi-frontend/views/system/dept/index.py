from dash import dcc
import feffery_antd_components as fac

import callbacks.system_c.dept_c
from api.dept import get_dept_list_api
from utils.tree_tool import get_dept_tree


def render():
    table_data_new = []
    default_expanded_row_keys = []
    table_info = get_dept_list_api({})
    if table_info['code'] == 200:
        table_data = table_info['data']['rows']
        for item in table_data:
            default_expanded_row_keys.append(str(item['dept_id']))
            if item['status'] == '0':
                item['status'] = dict(tag='正常', color='blue')
            else:
                item['status'] = dict(tag='停用', color='volcano')
            item['key'] = str(item['dept_id'])
            item['operation'] = [
                {
                    'content': '修改',
                    'type': 'link',
                    'icon': 'antd-edit'
                },
                {
                    'content': '新增',
                    'type': 'link',
                    'icon': 'antd-plus'
                },
                {
                    'content': '删除',
                    'type': 'link',
                    'icon': 'antd-delete'
                },
            ]
        table_data_new = get_dept_tree(0, table_data)

    return [
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdForm(
                                        [
                                            fac.AntdSpace(
                                                [
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='dept-dept_name-input',
                                                            placeholder='请输入部门名称',
                                                            autoComplete='off',
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='部门名称'
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='dept-status-select',
                                                            placeholder='部门状态',
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
                                                        label='部门状态'
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '搜索',
                                                            id='dept-search',
                                                            type='primary',
                                                            icon=fac.AntdIcon(
                                                                icon='antd-search'
                                                            )
                                                        )
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '重置',
                                                            id='dept-reset',
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
                                                id='dept-add',
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff'
                                                }
                                            ),
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-swap'
                                                    ),
                                                    '展开/折叠',
                                                ],
                                                id='dept-edit',
                                                disabled=True,
                                                style={
                                                    'color': '#909399',
                                                    'background': '#f4f4f5',
                                                    'border-color': '#d3d4d6'
                                                }
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
                                            id='dept-list-table',
                                            data=table_data_new,
                                            columns=[
                                                {
                                                    'dataIndex': 'dept_id',
                                                    'title': '部门编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                    'hidden': True
                                                },
                                                {
                                                    'dataIndex': 'dept_name',
                                                    'title': '部门名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'order_num',
                                                    'title': '排序',
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
                                            bordered=True,
                                            pagination={
                                                'hideOnSinglePage': True
                                            },
                                            defaultExpandedRowKeys=default_expanded_row_keys,
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

        # 新增部门表单modal
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
            fac.AntdText('是否确认删除？', id='delete-text'),
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
