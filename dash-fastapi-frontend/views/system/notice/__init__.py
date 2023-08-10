from dash import dcc, html
import feffery_antd_components as fac
import feffery_utils_components as fuc

import callbacks.system_c.notice_c
from api.notice import get_notice_list_api


def render(button_perms):

    notice_params = dict(page_num=1, page_size=10)
    table_info = get_notice_list_api(notice_params)
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
                item['status'] = dict(tag='正常', color='blue')
            else:
                item['status'] = dict(tag='关闭', color='volcano')
            if item['notice_type'] == '1':
                item['notice_type'] = dict(tag='通知', color='gold')
            else:
                item['notice_type'] = dict(tag='公告', color='green')
            item['key'] = str(item['notice_id'])
            item['operation'] = [
                {
                    'content': '修改',
                    'type': 'link',
                    'icon': 'antd-edit'
                } if 'system:notice:edit' in button_perms else {},
                {
                    'content': '删除',
                    'type': 'link',
                    'icon': 'antd-delete'
                } if 'system:notice:remove' in button_perms else {},
            ]

    return [
        dcc.Store(id='notice-button-perms-container', data=button_perms),
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
                                                            }
                                                        ),
                                                        label='公告标题',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='notice-update_by-input',
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
                                                            id='notice-notice_type-select',
                                                            placeholder='公告类型',
                                                            options=[
                                                                {
                                                                    'label': '通知',
                                                                    'value': '1'
                                                                },
                                                                {
                                                                    'label': '公告',
                                                                    'value': '2'
                                                                }
                                                            ],
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='类型',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdDateRangePicker(
                                                            id='notice-create_time-range',
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
                                                            id='notice-search',
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
                                                            id='notice-reset',
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
                                        hidden='system:notice:query' not in button_perms
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
                                                        id='notice-add',
                                                        style={
                                                            'color': '#1890ff',
                                                            'background': '#e8f4ff',
                                                            'border-color': '#a3d3ff'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:notice:add' not in button_perms
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
                                                        id='notice-edit',
                                                        disabled=True,
                                                        style={
                                                            'color': '#71e2a3',
                                                            'background': '#e7faf0',
                                                            'border-color': '#d0f5e0'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:notice:edit' not in button_perms
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
                                                        id='notice-delete',
                                                        disabled=True,
                                                        style={
                                                            'color': '#ff9292',
                                                            'background': '#ffeded',
                                                            'border-color': '#ffdbdb'
                                                        }
                                                    ),
                                                ],
                                                hidden='system:notice:remove' not in button_perms
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

        # 新增和编辑通知公告modal
        # 初始化渲染富文本编辑器
        fuc.FefferyExecuteJs(
            id='notice-init-editor'
        ),
        # 回写内容到富文本编辑器
        fuc.FefferyExecuteJs(
            id='notice-written-editor'
        ),
        dcc.Store(id='notice-written-editor-store'),
        # 监听富文本编辑器内容并取回
        fuc.FefferySessionStorage(
            id='notice-content'
        ),

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
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        id='notice-notice_title-form-item',
                                        required=True,
                                        label='公告标题',
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
                                            id='notice-notice_type',
                                            options=[
                                                {
                                                    'label': '通知',
                                                    'value': '1'
                                                },
                                                {
                                                    'label': '公告',
                                                    'value': '2'
                                                },
                                            ],
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        id='notice-notice_type-form-item',
                                        required=True,
                                        label='公告类型',
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
                                        fac.AntdRadioGroup(
                                            id='notice-status',
                                            options=[
                                                {
                                                    'label': '正常',
                                                    'value': '0'
                                                },
                                                {
                                                    'label': '关闭',
                                                    'value': '1'
                                                }
                                            ],
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        id='notice-status-form-item',
                                        label='状态',
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
                                        html.Div(
                                            [
                                                html.Div(
                                                    id='notice-notice_content-toolbar-container',
                                                    style={
                                                        'borderBottom': '1px solid #ccc'
                                                    }
                                                ),
                                                html.Div(
                                                    id='notice-notice_content-editor-container',
                                                    style={
                                                        'height': 300,
                                                        'width': '100%'
                                                    }
                                                )
                                            ],
                                            id='notice-notice_content-editor-wrapper',
                                            style={
                                                'zIndex': 9999,
                                                'border': '1px solid #ccc',
                                                'marginBottom': 15
                                            }
                                        ),
                                        id='notice-notice_content-form-item',
                                        label='内容',
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
                        )
                    ],
                    style={
                        'marginRight': '30px'
                    }
                )
            ],
            id='notice-modal',
            mask=False,
            width=900,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除通知公告二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='notice-delete-text'),
            id='notice-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),
    ]
