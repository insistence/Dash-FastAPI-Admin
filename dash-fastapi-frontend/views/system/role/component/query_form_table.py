import feffery_antd_components as fac
from dash import html
from utils.permission_util import PermissionManager


def render(allocate_index, is_operation):
    table_column = [
        {
            'dataIndex': 'user_id',
            'title': '用户id',
            'hidden': True,
        },
        {
            'dataIndex': 'user_name',
            'title': '用户名称',
            'renderOptions': {'renderType': 'ellipsis'},
        },
        {
            'dataIndex': 'nick_name',
            'title': '用户昵称',
            'renderOptions': {'renderType': 'ellipsis'},
        },
        {
            'dataIndex': 'email',
            'title': '邮箱',
            'renderOptions': {'renderType': 'ellipsis'},
        },
        {
            'dataIndex': 'phonenumber',
            'title': '手机',
            'renderOptions': {'renderType': 'ellipsis'},
        },
        {
            'dataIndex': 'status',
            'title': '状态',
            'renderOptions': {'renderType': 'tags'},
        },
        {
            'dataIndex': 'create_time',
            'title': '创建时间',
            'renderOptions': {'renderType': 'ellipsis'},
        },
    ]

    if is_operation:
        table_column.append(
            {
                'title': '操作',
                'dataIndex': 'operation',
                'fixed': 'right',
                'width': 150,
                'renderOptions': {'renderType': 'button'},
            }
        )

    return fac.AntdRow(
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
                                                        id={
                                                            'type': 'allocate_user-user_name-input',
                                                            'index': allocate_index,
                                                        },
                                                        placeholder='请输入用户名称',
                                                        autoComplete='off',
                                                        allowClear=True,
                                                        style={'width': 240},
                                                    ),
                                                    label='用户名称',
                                                    style={
                                                        'paddingBottom': '10px'
                                                    },
                                                ),
                                                fac.AntdFormItem(
                                                    fac.AntdInput(
                                                        id={
                                                            'type': 'allocate_user-phonenumber-input',
                                                            'index': allocate_index,
                                                        },
                                                        placeholder='请输入手机号码',
                                                        autoComplete='off',
                                                        allowClear=True,
                                                        style={'width': 240},
                                                    ),
                                                    label='手机号码',
                                                    style={
                                                        'paddingBottom': '10px'
                                                    },
                                                ),
                                                fac.AntdFormItem(
                                                    fac.AntdButton(
                                                        '搜索',
                                                        id={
                                                            'type': 'allocate_user-search',
                                                            'index': allocate_index,
                                                        },
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
                                                        id={
                                                            'type': 'allocate_user-reset',
                                                            'index': allocate_index,
                                                        },
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
                                    id={
                                        'type': 'allocate_user-search-form-container',
                                        'index': allocate_index,
                                    },
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
                                                fac.AntdIcon(icon='antd-plus'),
                                                '添加用户',
                                            ],
                                            id='allocate_user-add',
                                            style={
                                                'color': '#1890ff',
                                                'background': '#e8f4ff',
                                                'border-color': '#a3d3ff',
                                            },
                                        )
                                        if PermissionManager.check_perms(
                                            'system:role:add'
                                        )
                                        else [],
                                        fac.AntdButton(
                                            [
                                                fac.AntdIcon(
                                                    icon='antd-close-circle'
                                                ),
                                                '批量取消授权',
                                            ],
                                            id={
                                                'type': 'allocate_user-operation-button',
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
                                            'system:role:remove'
                                        )
                                        else [],
                                    ],
                                    style={'paddingBottom': '10px'},
                                ),
                                span=16,
                            )
                            if is_operation
                            else [],
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
                                                    id={
                                                        'type': 'allocate_user-hidden',
                                                        'index': allocate_index,
                                                    },
                                                    shape='circle',
                                                ),
                                                id={
                                                    'type': 'allocate_user-hidden-tooltip',
                                                    'index': allocate_index,
                                                },
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
                                                    id={
                                                        'type': 'allocate_user-refresh',
                                                        'index': allocate_index,
                                                    },
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
                                span=8 if is_operation else 24,
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
                                        id={
                                            'type': 'allocate_user-list-table',
                                            'index': allocate_index,
                                        },
                                        data=[],
                                        columns=table_column,
                                        rowSelectionType='checkbox',
                                        rowSelectionWidth=50,
                                        bordered=True,
                                        maxWidth=1000,
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
    )
