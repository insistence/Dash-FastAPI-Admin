from dash import dcc, html
import feffery_antd_components as fac

from .component import query_form_table
import callbacks.system_c.user_c.allocate_role_c


def render(button_perms):

    return [
        dcc.Store(id='allocate_role-button-perms-container', data=button_perms),
        dcc.Store(id='allocate_role-user_id-container'),
        # 分配角色模块操作类型存储容器
        dcc.Store(id={
            'type': 'allocate_role-operations-container',
            'index': 'allocated'
        }),
        dcc.Store(id={
            'type': 'allocate_role-operations-container',
            'index': 'unallocated'
        }),
        # 分配角色模块删除操作行key存储容器
        dcc.Store(id='allocate_role-delete-ids-store'),
        query_form_table.render(button_perms=button_perms, allocate_index='allocated', is_operation=True),

        # 添加用户表单modal
        fac.AntdModal(
            [
                query_form_table.render(button_perms=button_perms, allocate_index='unallocated', is_operation=False),
            ],
            id='allocate_role-modal',
            title='选择角色',
            mask=False,
            maskClosable=False,
            width=900,
            renderFooter=True,
            okClickClose=False
        ),

        # 取消授权二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认取消授权？', id='allocate_role-delete-text'),
            id='allocate_role-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True
        ),
    ]
