import feffery_antd_components as fac
from dash import dcc
from callbacks.system_c.user_c import allocate_role_c  # noqa: F401


def render(button_perms):
    return [
        dcc.Store(id='allocate_role-user_id-container'),
        fac.AntdTitle(
            '基本信息',
            level=4,
            style={
                'fontSize': '15px',
                'color': '#6379bb',
                'borderBottom': '1px solid #ddd',
                'margin': '8px 10px 25px 10px',
                'paddingBottom': '5px',
            },
        ),
        fac.AntdForm(
            fac.AntdRow(
                [
                    fac.AntdCol(
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='allocate_role-nick_name-input',
                                placeholder='请输入用户昵称',
                                autoComplete='off',
                                disabled=True,
                                # style={'width': 240},
                            ),
                            label='用户昵称',
                            style={'paddingBottom': '10px'},
                        ),
                        span=8,
                        offset=2,
                    ),
                    fac.AntdCol(
                        fac.AntdFormItem(
                            fac.AntdInput(
                                id='allocate_role-user_name-input',
                                placeholder='请输入登录账号',
                                autoComplete='off',
                                disabled=True,
                                # style={'width': 240},
                            ),
                            label='登录账号',
                            style={'paddingBottom': '10px'},
                        ),
                        span=8,
                        offset=2,
                    ),
                ]
            ),
        ),
        fac.AntdTitle(
            '角色信息',
            level=4,
            style={
                'fontSize': '15px',
                'color': '#6379bb',
                'borderBottom': '1px solid #ddd',
                'margin': '8px 10px 25px 10px',
                'paddingBottom': '5px',
            },
        ),
        fac.AntdSpin(
            fac.AntdTable(
                id='allocate_role-list-table',
                data=[],
                columns=[
                    {
                        'dataIndex': 'role_id',
                        'title': '角色id',
                        'hidden': True,
                    },
                    {
                        'dataIndex': 'role_name',
                        'title': '角色名称',
                        'renderOptions': {'renderType': 'ellipsis'},
                    },
                    {
                        'dataIndex': 'role_key',
                        'title': '权限字符',
                        'renderOptions': {'renderType': 'ellipsis'},
                    },
                    {
                        'dataIndex': 'create_time',
                        'title': '创建时间',
                        'renderOptions': {'renderType': 'ellipsis'},
                    },
                ],
                rowSelectionType='checkbox',
                rowSelectionWidth=50,
                bordered=True,
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
                style={
                    'width': '100%',
                    'padding-right': '10px',
                },
            ),
            text='数据加载中',
        ),
        fac.AntdCenter(
            fac.AntdSpace(
                [
                    fac.AntdButton(
                        '提交', id='allocate_role-submit-button', type='primary'
                    ),
                    fac.AntdButton(
                        '返回',
                        id='allocate_role-back-button',
                    ),
                ]
            )
        ),
    ]
    # return [
    #     dcc.Store(id='allocate_role-button-perms-container', data=button_perms),
    #     dcc.Store(id='allocate_role-user_id-container'),
    #     # 分配角色模块操作类型存储容器
    #     dcc.Store(
    #         id={
    #             'type': 'allocate_role-operations-container',
    #             'index': 'allocated',
    #         }
    #     ),
    #     dcc.Store(
    #         id={
    #             'type': 'allocate_role-operations-container',
    #             'index': 'unallocated',
    #         }
    #     ),
    #     # 分配角色模块删除操作行key存储容器
    #     dcc.Store(id='allocate_role-delete-ids-store'),
    #     query_form_table.render(
    #         button_perms=button_perms,
    #         allocate_index='allocated',
    #         is_operation=True,
    #     ),
    #     # 添加用户表单modal
    #     fac.AntdModal(
    #         [
    #             query_form_table.render(
    #                 button_perms=button_perms,
    #                 allocate_index='unallocated',
    #                 is_operation=False,
    #             ),
    #         ],
    #         id='allocate_role-modal',
    #         title='选择角色',
    #         mask=False,
    #         maskClosable=False,
    #         width=900,
    #         renderFooter=True,
    #         okClickClose=False,
    #     ),
    #     # 取消授权二次确认modal
    #     fac.AntdModal(
    #         fac.AntdText('是否确认取消授权？', id='allocate_role-delete-text'),
    #         id='allocate_role-delete-confirm-modal',
    #         visible=False,
    #         title='提示',
    #         renderFooter=True,
    #     ),
    # ]
