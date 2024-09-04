from dash import dcc, html
import feffery_antd_components as fac
import feffery_utils_components as fuc
from flask import session

from . import allocate_role
from views.components import ManuallyUpload
from api.system.user import UserApi
from utils.permission_util import PermissionManager
from config.global_config import ApiBaseUrlConfig

import callbacks.system_c.user_c.user_c  # noqa: F401


def render(*args, **kwargs):
    button_perms = kwargs.get('button_perms')
    user_params = dict(page_num=1, page_size=10)
    tree_info = UserApi.dept_tree_select()
    table_info = UserApi.list_user(user_params)
    tree_data = []
    table_data = []
    page_num = 1
    page_size = 10
    total = 0
    if tree_info['code'] == 200:
        tree_data = tree_info['data']
    if table_info['code'] == 200:
        table_data = table_info['rows']
        page_num = table_info['page_num']
        page_size = table_info['page_size']
        total = table_info['total']
        for item in table_data:
            if item['status'] == '0':
                item['status'] = dict(
                    checked=True, disabled=item['user_id'] == 1
                )
            else:
                item['status'] = dict(
                    checked=False, disabled=item['user_id'] == 1
                )
            item['key'] = str(item['user_id'])
            if item['user_id'] == 1:
                item['operation'] = []
            else:
                item['operation'] = [
                    {'title': '修改', 'icon': 'antd-edit'}
                    if PermissionManager.check_perms('system:user:edit')
                    else None,
                    {'title': '删除', 'icon': 'antd-delete'}
                    if PermissionManager.check_perms('system:user:remove')
                    else None,
                    {'title': '重置密码', 'icon': 'antd-key'}
                    if PermissionManager.check_perms('system:user:resetPwd')
                    else None,
                    {'title': '分配角色', 'icon': 'antd-check-circle'}
                    if PermissionManager.check_perms('system:user:edit')
                    else None,
                ]

    return [
        dcc.Store(id='user-button-perms-container', data=button_perms),
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='user-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='user-export-container'),
        # 用户管理模块操作类型存储容器
        dcc.Store(id='user-operations-store'),
        # 用户管理模块修改操作行key存储容器
        dcc.Store(id='user-edit-id-store'),
        # 用户管理模块删除操作行key存储容器
        dcc.Store(id='user-delete-ids-store'),
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdInput(
                            id='dept-input-search',
                            placeholder='请输入部门名称',
                            autoComplete='off',
                            allowClear=True,
                            prefix=fac.AntdIcon(icon='antd-search'),
                            style={'width': '85%'},
                        ),
                        fac.AntdTree(
                            id='dept-tree',
                            treeData=tree_data,
                            defaultExpandAll=True,
                            showLine=False,
                            style={'margin-top': '10px'},
                        ),
                    ],
                    span=4,
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
                                                                    },
                                                                ),
                                                                label='用户名称',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='user-phone_number-input',
                                                                    placeholder='请输入手机号码',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='手机号码',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdSelect(
                                                                    id='user-status-select',
                                                                    placeholder='用户状态',
                                                                    options=[
                                                                        {
                                                                            'label': '正常',
                                                                            'value': '0',
                                                                        },
                                                                        {
                                                                            'label': '停用',
                                                                            'value': '1',
                                                                        },
                                                                    ],
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='用户状态',
                                                            ),
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdSpace(
                                                        [
                                                            fac.AntdFormItem(
                                                                fac.AntdDateRangePicker(
                                                                    id='user-create_time-range',
                                                                    style={
                                                                        'width': 240
                                                                    },
                                                                ),
                                                                label='创建时间',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='user-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='user-reset',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-sync'
                                                                    ),
                                                                )
                                                            ),
                                                        ],
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                ],
                                                layout='inline',
                                            )
                                        ],
                                        id='user-search-form-container',
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
                                                        icon='antd-plus'
                                                    ),
                                                    '新增',
                                                ],
                                                id='user-add',
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'system:user:add'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-edit'
                                                    ),
                                                    '修改',
                                                ],
                                                id={
                                                    'type': 'user-operation-button',
                                                    'index': 'edit',
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#71e2a3',
                                                    'background': '#e7faf0',
                                                    'border-color': '#d0f5e0',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'system:user:edit'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-minus'
                                                    ),
                                                    '删除',
                                                ],
                                                id={
                                                    'type': 'user-operation-button',
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
                                                'system:user:remove'
                                            )
                                            else [],
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
                                                    'border-color': '#d3d4d6',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'system:user:import'
                                            )
                                            else [],
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
                                                    'border-color': '#ffe399',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'system:user:export'
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
                                                        id='user-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='user-hidden-tooltip',
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
                                                        id='user-refresh',
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
                                                        },
                                                    },
                                                },
                                            ],
                                            rowSelectionType='checkbox',
                                            rowSelectionWidth=50,
                                            bordered=True,
                                            pagination={
                                                'pageSize': page_size,
                                                'current': page_num,
                                                'showSizeChanger': True,
                                                'pageSizeOptions': [
                                                    10,
                                                    30,
                                                    50,
                                                    100,
                                                ],
                                                'showQuickJumper': True,
                                                'total': total,
                                            },
                                            mode='server-side',
                                            style={
                                                'width': '100%',
                                                'paddingRight': '10px',
                                            },
                                        ),
                                        text='数据加载中',
                                    ),
                                )
                            ]
                        ),
                    ],
                    span=20,
                ),
            ],
            gutter=5,
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
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'nick_name',
                                        },
                                        placeholder='请输入用户昵称',
                                        allowClear=True,
                                        style={'width': 200},
                                    ),
                                    label='用户昵称',
                                    required=True,
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'nick_name',
                                        'required': True,
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdTreeSelect(
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'dept_id',
                                        },
                                        placeholder='请选择归属部门',
                                        treeData=[],
                                        treeNodeFilterProp='title',
                                        style={'width': 200},
                                    ),
                                    label='归属部门',
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'dept_id',
                                        'required': False,
                                    },
                                    labelCol={'offset': 1},
                                ),
                            ],
                            size='middle',
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'phonenumber',
                                        },
                                        placeholder='请输入手机号码',
                                        allowClear=True,
                                        style={'width': 200},
                                    ),
                                    label='手机号码',
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'phonenumber',
                                        'required': False,
                                    },
                                    labelCol={'offset': 1},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'email',
                                        },
                                        placeholder='请输入邮箱',
                                        allowClear=True,
                                        style={'width': 200},
                                    ),
                                    label='邮箱',
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'email',
                                        'required': False,
                                    },
                                    labelCol={'offset': 5},
                                ),
                            ],
                            size='middle',
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'user_name',
                                        },
                                        placeholder='请输入用户名称',
                                        allowClear=True,
                                        style={'width': 200},
                                    ),
                                    label='用户名称',
                                    required=True,
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'user_name',
                                        'required': True,
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'password',
                                        },
                                        placeholder='请输入密码',
                                        mode='password',
                                        passwordUseMd5=True,
                                        style={'width': 200},
                                    ),
                                    label='用户密码',
                                    required=True,
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'password',
                                        'required': True,
                                    },
                                ),
                            ],
                            size='middle',
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'sex',
                                        },
                                        placeholder='请选择性别',
                                        options=[
                                            {'label': '男', 'value': '0'},
                                            {'label': '女', 'value': '1'},
                                            {'label': '未知', 'value': '2'},
                                        ],
                                        style={'width': 200},
                                    ),
                                    label='用户性别',
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'sex',
                                        'required': False,
                                    },
                                    labelCol={'offset': 1},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdRadioGroup(
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'status',
                                        },
                                        options=[
                                            {'label': '正常', 'value': '0'},
                                            {'label': '停用', 'value': '1'},
                                        ],
                                        defaultValue='0',
                                        style={'width': 200},
                                    ),
                                    label='用户状态',
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'status',
                                        'required': False,
                                    },
                                    labelCol={'offset': 2},
                                ),
                            ],
                            size='middle',
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
                                        style={'width': 200},
                                    ),
                                    label='岗位',
                                    id='user-add-post-form-item',
                                    labelCol={'offset': 4},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id='user-add-role',
                                        placeholder='请选择角色',
                                        options=[],
                                        mode='multiple',
                                        optionFilterProp='label',
                                        style={'width': 200},
                                    ),
                                    label='角色',
                                    id='user-add-role-form-item',
                                    labelCol={'offset': 8},
                                ),
                            ],
                            size='middle',
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id={
                                            'type': 'user_add-form-value',
                                            'index': 'remark',
                                        },
                                        placeholder='请输入内容',
                                        allowClear=True,
                                        mode='text-area',
                                        style={'width': 490},
                                    ),
                                    label='备注',
                                    id={
                                        'type': 'user_add-form-label',
                                        'index': 'remark',
                                        'required': False,
                                    },
                                    labelCol={'offset': 2},
                                ),
                            ]
                        ),
                    ]
                )
            ],
            id='user-add-modal',
            title='新增用户',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=False,
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
                                        id={
                                            'type': 'user_edit-form-value',
                                            'index': 'nick_name',
                                        },
                                        placeholder='请输入用户昵称',
                                        allowClear=True,
                                        style={'width': 200},
                                    ),
                                    label='用户昵称',
                                    required=True,
                                    id={
                                        'type': 'user_edit-form-label',
                                        'index': 'nick_name',
                                        'required': True,
                                    },
                                ),
                                fac.AntdFormItem(
                                    fac.AntdTreeSelect(
                                        id={
                                            'type': 'user_edit-form-value',
                                            'index': 'dept_id',
                                        },
                                        placeholder='请选择归属部门',
                                        treeData=[],
                                        treeNodeFilterProp='title',
                                        style={'width': 200},
                                    ),
                                    label='归属部门',
                                    id={
                                        'type': 'user_edit-form-label',
                                        'index': 'dept_id',
                                        'required': False,
                                    },
                                ),
                            ],
                            size='middle',
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id={
                                            'type': 'user_edit-form-value',
                                            'index': 'phonenumber',
                                        },
                                        placeholder='请输入手机号码',
                                        allowClear=True,
                                        style={'width': 200},
                                    ),
                                    label='手机号码',
                                    id={
                                        'type': 'user_edit-form-label',
                                        'index': 'phonenumber',
                                        'required': False,
                                    },
                                    labelCol={'offset': 1},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id={
                                            'type': 'user_edit-form-value',
                                            'index': 'email',
                                        },
                                        placeholder='请输入邮箱',
                                        allowClear=True,
                                        style={'width': 200},
                                    ),
                                    label='邮箱',
                                    id={
                                        'type': 'user_edit-form-label',
                                        'index': 'email',
                                        'required': False,
                                    },
                                    labelCol={'offset': 4},
                                ),
                            ],
                            size='middle',
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id={
                                            'type': 'user_edit-form-value',
                                            'index': 'sex',
                                        },
                                        placeholder='请选择性别',
                                        options=[
                                            {'label': '男', 'value': '0'},
                                            {'label': '女', 'value': '1'},
                                            {'label': '未知', 'value': '2'},
                                        ],
                                        style={'width': 200},
                                    ),
                                    label='用户性别',
                                    id={
                                        'type': 'user_edit-form-label',
                                        'index': 'sex',
                                        'required': False,
                                    },
                                    labelCol={'offset': 1},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdRadioGroup(
                                        id={
                                            'type': 'user_edit-form-value',
                                            'index': 'status',
                                        },
                                        options=[
                                            {'label': '正常', 'value': '0'},
                                            {'label': '停用', 'value': '1'},
                                        ],
                                        style={'width': 200},
                                    ),
                                    label='用户状态',
                                    id={
                                        'type': 'user_edit-form-label',
                                        'index': 'status',
                                        'required': False,
                                    },
                                    labelCol={'offset': 1},
                                ),
                            ],
                            size='middle',
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
                                        style={'width': 200},
                                    ),
                                    label='岗位',
                                    id='user-edit-post-form-item',
                                    labelCol={'offset': 4},
                                ),
                                fac.AntdFormItem(
                                    fac.AntdSelect(
                                        id='user-edit-role',
                                        placeholder='请选择角色',
                                        options=[],
                                        mode='multiple',
                                        optionFilterProp='label',
                                        style={'width': 200},
                                    ),
                                    label='角色',
                                    id='user-edit-role-form-item',
                                    labelCol={'offset': 7},
                                ),
                            ],
                            size='middle',
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id={
                                            'type': 'user_edit-form-value',
                                            'index': 'remark',
                                        },
                                        placeholder='请输入内容',
                                        allowClear=True,
                                        mode='text-area',
                                        style={'width': 485},
                                    ),
                                    label='备注',
                                    id={
                                        'type': 'user_edit-form-label',
                                        'index': 'remark',
                                        'required': False,
                                    },
                                    labelCol={'offset': 2},
                                ),
                            ]
                        ),
                    ]
                )
            ],
            id='user-edit-modal',
            title='编辑用户',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=False,
        ),
        # 删除用户二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='user-delete-text'),
            id='user-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
        # 用户导入modal
        fac.AntdModal(
            [
                html.Div(
                    [
                        ManuallyUpload().render(),
                        # fac.AntdDraggerUpload(
                        #     id='user-upload-choose',
                        #     apiUrl=f'{ApiBaseUrlConfig.BaseUrl}/common/upload',
                        #     downloadUrlFromBackend=True,
                        #     headers={
                        #         'Authorization': 'Bearer '
                        #         + session.get('Authorization')
                        #     },
                        #     fileTypes=['xls', 'xlsx'],
                        #     fileListMaxLength=1,
                        #     text='用户导入',
                        #     hint='点击或拖拽文件至此处进行上传',
                        # ),
                    ],
                    style={'marginTop': '10px'},
                ),
                html.Div(
                    [
                        fac.AntdCheckbox(
                            id='user-import-update-check', checked=False
                        ),
                        fac.AntdText(
                            '是否更新已经存在的用户数据',
                            style={'marginLeft': '5px'},
                        ),
                    ],
                    style={'textAlign': 'center', 'marginTop': '10px'},
                ),
                html.Div(
                    [
                        fac.AntdText('仅允许导入xls、xlsx格式文件。'),
                        fac.AntdButton(
                            '下载模板',
                            id='download-user-import-template',
                            type='link',
                        ),
                    ],
                    style={'textAlign': 'center', 'marginTop': '10px'},
                ),
            ],
            id='user-import-confirm-modal',
            visible=False,
            title='用户导入',
            width=600,
            renderFooter=True,
            centered=True,
            okText='导入',
            confirmAutoSpin=True,
            loadingOkText='导入中',
            okClickClose=False,
        ),
        fac.AntdModal(
            fac.AntdText(
                id='batch-result-content',
                className={'whiteSpace': 'break-spaces'},
            ),
            id='batch-result-modal',
            visible=False,
            title='用户导入结果',
            renderFooter=False,
            centered=True,
        ),
        # 重置密码modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='reset-password-input', mode='password'
                            ),
                            label='请输入新密码',
                        ),
                    ],
                    layout='vertical',
                ),
                dcc.Store(id='reset-password-row-key-store'),
            ],
            id='user-reset-password-confirm-modal',
            visible=False,
            title='重置密码',
            renderFooter=True,
            centered=True,
        ),
        # 分配角色modal
        fac.AntdModal(
            allocate_role.render(button_perms),
            id='user_to_allocated_role-modal',
            title='分配角色',
            mask=False,
            maskClosable=False,
            width=1000,
            renderFooter=False,
            okClickClose=False,
        ),
    ]
