from dash import dcc, html
import feffery_antd_components as fac

from api.menu import get_menu_list_api
from utils.tree_tool import list_to_tree
from views.system.menu.components.icon_category import render_icon
import callbacks.system_c.menu_c.menu_c


def render(*args, **kwargs):
    button_perms = kwargs.get('button_perms')
    table_data_new = []
    table_info = get_menu_list_api({})
    if table_info['code'] == 200:
        table_data = table_info['data']['rows']
        for item in table_data:
            item['key'] = str(item['menu_id'])
            item['icon'] = [
                {
                    'type': 'link',
                    'icon': item['icon'],
                    'disabled': True,
                    'style': {
                        'color': 'rgba(0, 0, 0, 0.8)'
                    }
                },
            ]
            if item['status'] == '1':
                item['operation'] = [
                    {
                        'content': '修改',
                        'type': 'link',
                        'icon': 'antd-edit'
                    } if 'system:menu:edit' in button_perms else {},
                    {
                        'content': '删除',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'system:menu:remove' in button_perms else {},
                ]
            else:
                item['operation'] = [
                    {
                        'content': '修改',
                        'type': 'link',
                        'icon': 'antd-edit'
                    } if 'system:menu:edit' in button_perms else {},
                    {
                        'content': '新增',
                        'type': 'link',
                        'icon': 'antd-plus'
                    } if 'system:menu:add' in button_perms else {},
                    {
                        'content': '删除',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'system:menu:remove' in button_perms else {},
                ]
            if item['status'] == '0':
                item['status'] = dict(tag='正常', color='blue')
            else:
                item['status'] = dict(tag='停用', color='volcano')
        table_data_new = list_to_tree(table_data, 'menu_id', 'parent_id')

    return [
        dcc.Store(id='menu-button-perms-container', data=button_perms),
        # 菜单管理模块操作类型存储容器
        dcc.Store(id='menu-operations-store'),
        dcc.Store(id='menu-operations-store-bk'),
        # modal菜单类型存储容器
        dcc.Store(id='menu-modal-menu-type-store'),
        # 不同菜单类型的触发器
        dcc.Store(id='menu-modal-M-trigger'),
        dcc.Store(id='menu-modal-C-trigger'),
        dcc.Store(id='menu-modal-F-trigger'),
        # 菜单管理模块修改操作行key存储容器
        dcc.Store(id='menu-edit-id-store'),
        # 菜单管理模块删除操作行key存储容器
        dcc.Store(id='menu-delete-ids-store'),
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
                                                                    id='menu-menu_name-input',
                                                                    placeholder='请输入菜单名称',
                                                                    autoComplete='off',
                                                                    allowClear=True,
                                                                    style={
                                                                        'width': 240
                                                                    }
                                                                ),
                                                                label='菜单名称'
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdSelect(
                                                                    id='menu-status-select',
                                                                    placeholder='菜单状态',
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
                                                                label='菜单状态'
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '搜索',
                                                                    id='menu-search',
                                                                    type='primary',
                                                                    icon=fac.AntdIcon(
                                                                        icon='antd-search'
                                                                    )
                                                                )
                                                            ),
                                                            fac.AntdFormItem(
                                                                fac.AntdButton(
                                                                    '重置',
                                                                    id='menu-reset',
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
                                        id='menu-search-form-container',
                                        hidden=False
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
                                                id={
                                                    'type': 'menu-operation-button',
                                                    'index': 'add'
                                                },
                                                style={
                                                    'color': '#1890ff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#a3d3ff'
                                                }
                                            ) if 'system:menu:add' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-swap'
                                                    ),
                                                    '展开/折叠',
                                                ],
                                                id='menu-fold',
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
                                                        id='menu-hidden',
                                                        shape='circle'
                                                    ),
                                                    id='menu-hidden-tooltip',
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
                                                        id='menu-refresh',
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
                                            id='menu-list-table',
                                            data=table_data_new,
                                            columns=[
                                                {
                                                    'dataIndex': 'menu_id',
                                                    'title': '菜单编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                    'hidden': True
                                                },
                                                {
                                                    'dataIndex': 'menu_name',
                                                    'title': '菜单名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'icon',
                                                    'title': '图标',
                                                    'width': 80,
                                                    'renderOptions': {
                                                        'renderType': 'button'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'order_num',
                                                    'title': '排序',
                                                    'width': 80,
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'perms',
                                                    'title': '权限标识',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'component',
                                                    'title': '组件路径',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status',
                                                    'title': '状态',
                                                    'width': 90,
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'create_time',
                                                    'title': '创建时间',
                                                    'width': 150,
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
                                            style={
                                                'width': '100%',
                                                'padding-right': '10px',
                                                'padding-bottom': '20px'
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

        # 新增和编辑菜单表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdTreeSelect(
                                        id='menu-parent_id',
                                        placeholder='请选择上级菜单',
                                        treeData=[],
                                        defaultValue='0',
                                        treeNodeFilterProp='title',
                                        style={
                                            'width': 495
                                        }
                                    ),
                                    label='上级菜单',
                                    required=True,
                                    id='menu-parent_id-form-item',
                                    labelCol={
                                        'span': 4,
                                    },
                                    wrapperCol={
                                        'span': 20
                                    }
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdRadioGroup(
                                        id='menu-menu_type',
                                        options=[
                                            {
                                                'label': '目录',
                                                'value': 'M'
                                            },
                                            {
                                                'label': '菜单',
                                                'value': 'C'
                                            },
                                            {
                                                'label': '按钮',
                                                'value': 'F'
                                            },
                                        ],
                                        defaultValue='M',
                                        style={
                                            'width': 495
                                        }
                                    ),
                                    label='菜单类型',
                                    required=True,
                                    id='menu-menu_type-form-item',
                                    labelCol={
                                        'span': 4,
                                    },
                                    wrapperCol={
                                        'span': 20
                                    }
                                )
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdPopover(
                                        fac.AntdInput(
                                            id='menu-icon',
                                            placeholder='点击此处选择图标',
                                            readOnly=True,
                                            style={
                                                'width': 495
                                            }
                                        ),
                                        content=render_icon(),
                                        trigger='click',
                                        placement='bottom'
                                    ),
                                    label='菜单图标',
                                    id='menu-icon-form-item',
                                    labelCol={
                                        'span': 4,
                                    },
                                    wrapperCol={
                                        'span': 20
                                    }
                                ),
                            ],
                            size="middle"
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdFormItem(
                                    fac.AntdInput(
                                        id='menu-menu_name',
                                        placeholder='请输入菜单名称',
                                        allowClear=True,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='菜单名称',
                                    required=True,
                                    id='menu-menu_name-form-item',
                                    labelCol={
                                        'span': 8,
                                    },
                                    wrapperCol={
                                        'span': 16
                                    }
                                ),
                                fac.AntdFormItem(
                                    fac.AntdInputNumber(
                                        id='menu-order_num',
                                        min=0,
                                        style={
                                            'width': 200
                                        }
                                    ),
                                    label='显示排序',
                                    required=True,
                                    id='menu-order_num-form-item',
                                    labelCol={
                                        'span': 8,
                                    },
                                    wrapperCol={
                                        'span': 16
                                    }
                                ),
                            ],
                            size="middle"
                        ),
                        html.Div(id='content-by-menu-type'),
                    ]
                )
            ],
            id='menu-modal',
            mask=False,
            width=680,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除菜单二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='menu-delete-text'),
            id='menu-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),
    ]
