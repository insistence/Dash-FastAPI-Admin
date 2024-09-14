import feffery_antd_components as fac
import feffery_utils_components as fuc
import uuid
from dash import dcc, html
from flask import session
from api.system.notice import NoticeApi
from callbacks.system_c import notice_c  # noqa: F401
from components.ApiRadioGroup import ApiRadioGroup
from components.ApiSelect import ApiSelect
from config.global_config import ApiBaseUrlConfig
from utils.dict_util import DictManager
from utils.permission_util import PermissionManager


def render(*args, **kwargs):
    notice_params = dict(page_num=1, page_size=10)
    table_info = NoticeApi.list_notice(notice_params)
    table_data = table_info['rows']
    page_num = table_info['page_num']
    page_size = table_info['page_size']
    total = table_info['total']
    for item in table_data:
        item['status'] = DictManager.get_dict_tag(
            dict_type='sys_notice_status', dict_value=item.get('status')
        )
        item['notice_type'] = DictManager.get_dict_tag(
            dict_type='sys_notice_type', dict_value=item.get('notice_type')
        )
        item['key'] = str(item['notice_id'])
        item['operation'] = [
            {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
            if PermissionManager.check_perms('system:notice:edit')
            else {},
            {'content': '删除', 'type': 'link', 'icon': 'antd-delete'}
            if PermissionManager.check_perms('system:notice:remove')
            else {},
        ]

    return [
        # 通知公告管理模块操作类型存储容器
        dcc.Store(id='notice-operations-store'),
        dcc.Store(id='notice-operations-store-bk'),
        # 通知公告管理模块修改操作行key存储容器
        dcc.Store(id='notice-edit-id-store'),
        # 通知公告管理模块删除操作行key存储容器
        dcc.Store(id='notice-delete-ids-store'),
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
                                                            id='notice-notice_title-input',
                                                            placeholder='请输入公告标题',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            },
                                                        ),
                                                        label='公告标题',
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='notice-update_by-input',
                                                            placeholder='请输入操作人员',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            },
                                                        ),
                                                        label='操作人员',
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        ApiSelect(
                                                            dict_type='sys_notice_type',
                                                            id='notice-notice_type-select',
                                                            placeholder='公告类型',
                                                            style={
                                                                'width': 240
                                                            },
                                                        ),
                                                        label='类型',
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdDateRangePicker(
                                                            id='notice-create_time-range',
                                                            style={
                                                                'width': 240
                                                            },
                                                        ),
                                                        label='创建时间',
                                                        style={
                                                            'paddingBottom': '10px'
                                                        },
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '搜索',
                                                            id='notice-search',
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
                                                            id='notice-reset',
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
                                        id='notice-search-form-container',
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
                                                    'type': 'notice-operation-button',
                                                    'index': 'add',
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff',
                                                },
                                            )
                                            if PermissionManager.check_perms(
                                                'system:notice:add'
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
                                                    'type': 'notice-operation-button',
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
                                                'system:notice:edit'
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
                                                    'type': 'notice-operation-button',
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
                                                'system:notice:remove'
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
                                                        id='notice-hidden',
                                                        shape='circle',
                                                    ),
                                                    id='notice-hidden-tooltip',
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
                                                        id='notice-refresh',
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
                                            id='notice-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'notice_id',
                                                    'title': '序号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'notice_title',
                                                    'title': '公告标题',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'notice_type',
                                                    'title': '公告类型',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
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
                                                    'dataIndex': 'create_by',
                                                    'title': '创建者',
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
        # 新增和编辑通知公告modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='notice-notice_title',
                                            style={'width': '100%'},
                                        ),
                                        id='notice-notice_title-form-item',
                                        required=True,
                                        label='公告标题',
                                        labelCol={'span': 6},
                                        wrapperCol={'span': 18},
                                    ),
                                    span=12,
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        ApiSelect(
                                            dict_type='sys_notice_type',
                                            id='notice-notice_type',
                                            style={'width': '100%'},
                                        ),
                                        id='notice-notice_type-form-item',
                                        required=True,
                                        label='公告类型',
                                        labelCol={'span': 6},
                                        wrapperCol={'span': 18},
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
                                        ApiRadioGroup(
                                            dict_type='sys_notice_status',
                                            id='notice-status',
                                            style={'width': '100%'},
                                        ),
                                        id='notice-status-form-item',
                                        label='状态',
                                        labelCol={'span': 3},
                                        wrapperCol={'span': 21},
                                    ),
                                    span=24,
                                ),
                            ],
                            gutter=5,
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fuc.FefferyRichTextEditor(
                                            id='notice-content',
                                            editorConfig={
                                                'placeholder': '请输入...'
                                            },
                                            uploadImage={
                                                'server': f'{ApiBaseUrlConfig.BaseUrl}/common/uploadForEditor',
                                                'fieldName': 'file',
                                                'maxFileSize': 10 * 1024 * 1024,
                                                'maxNumberOfFiles': 10,
                                                'meta': {
                                                    'baseUrl': ApiBaseUrlConfig.BaseUrl,
                                                    'uploadId': str(
                                                        uuid.uuid4()
                                                    ),
                                                    'taskPath': 'notice',
                                                },
                                                'metaWithUrl': True,
                                                'headers': {
                                                    'Authorization': 'Bearer '
                                                    + session.get(
                                                        'Authorization'
                                                    )
                                                },
                                                'withCredentials': True,
                                                'timeout': 5 * 1000,
                                                'base64LimitSize': 500 * 1024,
                                            },
                                            uploadVideo={
                                                'server': f'{ApiBaseUrlConfig.BaseUrl}/common/uploadForEditor',
                                                'fieldName': 'file',
                                                'maxFileSize': 100
                                                * 1024
                                                * 1024,
                                                'maxNumberOfFiles': 3,
                                                'meta': {
                                                    'baseUrl': ApiBaseUrlConfig.BaseUrl,
                                                    'uploadId': str(
                                                        uuid.uuid4()
                                                    ),
                                                    'taskPath': 'notice',
                                                },
                                                'metaWithUrl': True,
                                                'headers': {
                                                    'Authorization': 'Bearer '
                                                    + session.get(
                                                        'Authorization'
                                                    )
                                                },
                                                'withCredentials': True,
                                                'timeout': 15 * 1000,
                                            },
                                            editorStyle={
                                                'height': 300,
                                                'width': '100%',
                                            },
                                            style={'marginBottom': 15},
                                        ),
                                        id='notice-notice_content-form-item',
                                        label='内容',
                                        labelCol={'span': 3},
                                        wrapperCol={'span': 21},
                                    ),
                                    span=24,
                                ),
                            ],
                            gutter=5,
                        ),
                    ],
                    style={'marginRight': '30px'},
                )
            ],
            id='notice-modal',
            mask=False,
            width=900,
            renderFooter=True,
            okClickClose=False,
        ),
        # 删除通知公告二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='notice-delete-text'),
            id='notice-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True,
        ),
    ]
