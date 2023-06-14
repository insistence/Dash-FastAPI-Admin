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
            if item['parent_id'] == 0:
                item['operation'] = []
            else:
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
                                                            allowClear=True,
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
                                                id='dept-fold',
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

        # 新增和编辑部门表单modal
        fac.AntdModal(
            [
                fac.AntdForm(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdTreeSelect(
                                            id='dept-parent_id',
                                            placeholder='请选择上级部门',
                                            treeData=[],
                                            treeNodeFilterProp='title',
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        label='上级部门',
                                        required=True,
                                        id='dept-parent_id-form-item',
                                        labelCol={
                                            'span': 4
                                        },
                                        wrapperCol={
                                            'span': 20
                                        }
                                    ),
                                    span=24
                                ),
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='dept-dept_name',
                                            placeholder='请输入部门名称',
                                            allowClear=True,
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        label='部门名称',
                                        required=True,
                                        id='dept-dept_name-form-item'
                                    ),
                                    span=12
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInputNumber(
                                            id='dept-order_num',
                                            min=0,
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        label='显示顺序',
                                        required=True,
                                        id='dept-order_num-form-item'
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
                                            id='dept-leader',
                                            placeholder='请输入负责人',
                                            allowClear=True,
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        label='负责人',
                                        id='dept-leader-form-item'
                                    ),
                                    span=12
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='dept-phone',
                                            placeholder='请输入联系电话',
                                            allowClear=True,
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        label='联系电话',
                                        id='dept-phone-form-item'
                                    ),
                                    span=12
                                ),
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='dept-email',
                                            placeholder='请输入邮箱',
                                            allowClear=True,
                                            style={
                                                'width': '100%'
                                            }
                                        ),
                                        label='邮箱',
                                        id='dept-email-form-item'
                                    ),
                                    span=12
                                ),
                                fac.AntdCol(
                                    fac.AntdFormItem(
                                        fac.AntdRadioGroup(
                                            id='dept-status',
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
                                                'width': '100%'
                                            }
                                        ),
                                        label='部门状态',
                                        id='dept-status-form-item'
                                    ),
                                    span=12
                                ),
                            ],
                            gutter=5
                        ),
                    ],
                    labelCol={
                        'span': 8
                    },
                    wrapperCol={
                        'span': 16
                    },
                    style={
                        'marginRight': '15px'
                    }
                )
            ],
            id='dept-modal',
            mask=False,
            width=650,
            renderFooter=True,
            okClickClose=False
        ),

        # 删除部门二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='dept-delete-text'),
            id='dept-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),
    ]
