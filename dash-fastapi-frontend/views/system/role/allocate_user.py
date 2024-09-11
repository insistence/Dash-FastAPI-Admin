import feffery_antd_components as fac
from dash import dcc
from callbacks.system_c.role_c import allocate_user_c  # noqa: F401
from .component import query_form_table


def render():
    return [
        dcc.Store(id='allocate_user-role_id-container'),
        # 分配用户模块操作类型存储容器
        dcc.Store(
            id={
                'type': 'allocate_user-operations-container',
                'index': 'allocated',
            }
        ),
        dcc.Store(
            id={
                'type': 'allocate_user-operations-container',
                'index': 'unallocated',
            }
        ),
        # 分配用户模块删除操作行key存储容器
        dcc.Store(id='allocate_user-delete-ids-store'),
        query_form_table.render(
            allocate_index='allocated',
            is_operation=True,
        ),
        # 添加用户表单modal
        fac.AntdModal(
            [
                query_form_table.render(
                    allocate_index='unallocated',
                    is_operation=False,
                ),
            ],
            id='allocate_user-modal',
            title='选择用户',
            mask=False,
            maskClosable=False,
            width=900,
            renderFooter=True,
            okClickClose=False,
        ),
        # 取消授权二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认取消授权？', id='allocate_user-delete-text'),
            id='allocate_user-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
        ),
    ]
