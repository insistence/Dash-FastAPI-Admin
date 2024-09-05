import feffery_antd_components as fac
from dash import dcc, html
from api.system.post import PostApi
from callbacks.system_c import post_c  # noqa: F401
from utils.permission_util import PermissionManager


def render(*args, **kwargs):
    button_perms = kwargs.get('button_perms')

    post_params = dict(page_num=1, page_size=10)
    table_info = PostApi.list_post(post_params)
    table_data = table_info['rows']
    page_num = table_info['page_num']
    page_size = table_info['page_size']
    total = table_info['total']
    for item in table_data:
        if item['status'] == '0':
            item['status'] = dict(tag='正常', color='blue')
        else:
            item['status'] = dict(tag='停用', color='volcano')
        item['key'] = str(item['post_id'])
        item['operation'] = [
            {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
            if PermissionManager.check_perms('system:post:edit')
            else {},
            {'content': '删除', 'type': 'link', 'icon': 'antd-delete'}
            if PermissionManager.check_perms('system:post:remove')
            else {},
        ]

    return [
        dcc.Store(id='post-button-perms-container', data=button_perms),
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='post-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='post-export-container'),
        # 岗位管理模块操作类型存储容器
        dcc.Store(id='post-operations-store'),
        dcc.Store(id='post-operations-store-bk'),
        # 岗位管理模块修改操作行key存储容器
        dcc.Store(id='post-edit-id-store'),
        # 岗位管理模块删除操作行key存储容器
        dcc.Store(id='post-delete-ids-store'),
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
                                                                    id='post-post_code-input',
                                                                    placeholder='请输入岗位编码',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                ),
                                                                label='岗位编码',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdInput(
                                                                    id='post-post_name-input',
                                                                    placeholder='请输入岗位名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 210
                                                                    },
                                                                ),
                                                                label='岗位名称',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdSelect(
                                                                    id='post-status-select',
                                                                    placeholder='岗位状态',
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
                                                                        'width': 200
                                                                    },
                                                                ),
                                                                label='岗位状态',
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='post-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    ),
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='post-reset',
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
                                        id='post-search-form-container',
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
                                                id={
                                                    'type': 'post-operation-button',
                                                    'index': 'add',
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'system:post:add'
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
                                                    'type': 'post-operation-button',
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
                                                'system:post:edit'
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
                                                    'type': 'post-operation-button',
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
                                                'system:post:remove'
                                            )
                                            else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='post-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'border-color': '#ffe399',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'system:post:export'
                                            )
                                            else [],
                                        ],
                                        style={
                                            'paddingBottom': '10px',
                                        },
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
                                                        id='post-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='post-hidden-tooltip',
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
                                                        id='post-refresh',
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
                                            id='post-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'post_id',
                                                    'title': '岗位编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'post_code',
                                                    'title': '岗位编码',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'post_name',
                                                    'title': '岗位名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'post_sort',
                                                    'title': '岗位排序',
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
        # 新增和编辑岗位表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id={
                                    'type': 'post-form-value',
                                    'index': 'post_name',
                                },
                                placeholder='请输入岗位名称',
                                allowClear=True,
                                style={'width': 350},
                            ),
                            label='岗位名称',
                            required=True,
                            id={
                                'type': 'post-form-label',
                                'index': 'post_name',
                                'required': True,
                            },
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id={
                                    'type': 'post-form-value',
                                    'index': 'post_code',
                                },
                                placeholder='请输入岗位编码',
                                allowClear=True,
                                style={'width': 350},
                            ),
                            label='岗位编码',
                            required=True,
                            id={
                                'type': 'post-form-label',
                                'index': 'post_code',
                                'required': True,
                            },
                        ),
                        fac.AntdFormItem(
                            fac.AntdInputNumber(
                                id={
                                    'type': 'post-form-value',
                                    'index': 'post_sort',
                                },
                                defaultValue=0,
                                min=0,
                                style={'width': 350},
                            ),
                            label='岗位顺序',
                            required=True,
                            id={
                                'type': 'post-form-label',
                                'index': 'post_sort',
                                'required': True,
                            },
                        ),
                        fac.AntdFormItem(
                            fac.AntdRadioGroup(
                                id={
                                    'type': 'post-form-value',
                                    'index': 'status',
                                },
                                options=[
                                    {'label': '正常', 'value': '0'},
                                    {'label': '停用', 'value': '1'},
                                ],
                                defaultValue='0',
                                style={'width': 350},
                            ),
                            label='岗位状态',
                            id={
                                'type': 'post-form-label',
                                'index': 'status',
                                'required': False,
                            },
                        ),
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id={
                                    'type': 'post-form-value',
                                    'index': 'remark',
                                },
                                placeholder='请输入内容',
                                allowClear=True,
                                mode='text-area',
                                style={'width': 350},
                            ),
                            label='备注',
                            id={
                                'type': 'post-form-label',
                                'index': 'remark',
                                'required': False,
                            },
                        ),
                    ],
                    labelCol={'span': 6},
                    wrapperCol={'span': 18},
                )
            ],
            id='post-modal',
            mask=False,
            width=580,
            renderFooter=True,
            okClickClose=False,
        ),
        # 删除岗位二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='post-delete-text'),
            id='post-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
    ]
