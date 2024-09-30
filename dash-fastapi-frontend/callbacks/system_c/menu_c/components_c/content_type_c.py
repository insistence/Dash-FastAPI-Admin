from dash import no_update
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from api.system.menu import MenuApi
from server import app
from utils.common_util import ValidateUtil
from utils.feedback_util import MessageManager


@app.callback(
    output=dict(
        form_validate=[
            Output(
                'menu-parent_id-form-item',
                'validateStatus',
                allow_duplicate=True,
            ),
            Output(
                'menu-menu_name-form-item',
                'validateStatus',
                allow_duplicate=True,
            ),
            Output(
                'menu-order_num-form-item',
                'validateStatus',
                allow_duplicate=True,
            ),
            Output('content-menu-path-form-item', 'validateStatus'),
            Output('menu-parent_id-form-item', 'help', allow_duplicate=True),
            Output('menu-menu_name-form-item', 'help', allow_duplicate=True),
            Output('menu-order_num-form-item', 'help', allow_duplicate=True),
            Output('content-menu-path-form-item', 'help'),
        ],
        modal_visible=Output('menu-modal', 'visible', allow_duplicate=True),
        operations=Output(
            'menu-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(confirm_trigger=Input('menu-modal-M-trigger', 'data')),
    state=dict(
        modal_type=State('menu-modal_type-store', 'data'),
        edit_row_info=State('menu-edit-id-store', 'data'),
        parent_id=State('menu-parent_id', 'value'),
        menu_type=State('menu-menu_type', 'value'),
        icon=State('menu-icon', 'value'),
        menu_name=State('menu-menu_name', 'value'),
        order_num=State('menu-order_num', 'value'),
        is_frame=State('content-menu-is_frame', 'value'),
        path=State('content-menu-path', 'value'),
        visible=State('content-menu-visible', 'value'),
        status=State('content-menu-status', 'value'),
    ),
    running=[[Output('menu-modal', 'confirmLoading'), True, False]],
    prevent_initial_call=True,
)
def menu_confirm_content(
    confirm_trigger,
    modal_type,
    edit_row_info,
    parent_id,
    menu_type,
    icon,
    menu_name,
    order_num,
    is_frame,
    path,
    visible,
    status,
):
    """
    菜单类型为目录时新增或编辑弹窗确认回调，实现新增或编辑操作
    """
    if confirm_trigger:
        if all(
            ValidateUtil.not_empty(item)
            for item in [parent_id, menu_name, order_num, path]
        ):
            params_add = dict(
                parent_id=parent_id,
                menu_type=menu_type,
                icon=icon,
                menu_name=menu_name,
                order_num=order_num,
                is_frame=is_frame,
                path=path,
                visible=visible,
                status=status,
            )
            params_edit = dict(
                menu_id=edit_row_info.get('menu_id') if edit_row_info else None,
                parent_id=parent_id,
                menu_type=menu_type,
                icon=icon,
                menu_name=menu_name,
                order_num=order_num,
                is_frame=is_frame,
                path=path,
                visible=visible,
                status=status,
            )
            modal_type = modal_type.get('type')
            if modal_type == 'add':
                MenuApi.add_menu(params_add)
            if modal_type == 'edit':
                MenuApi.update_menu(params_edit)
            if modal_type == 'add':
                MessageManager.success(content='新增成功')

                return dict(
                    form_validate=[None] * 8,
                    modal_visible=False,
                    operations={'type': 'add'},
                )
            if modal_type == 'edit':
                MessageManager.success(content='编辑成功')

                return dict(
                    form_validate=[None] * 8,
                    modal_visible=False,
                    operations={'type': 'edit'},
                )

            return dict(
                form_validate=[None] * 8,
                modal_visible=no_update,
                operations=no_update,
            )

        return dict(
            form_validate=[
                None if ValidateUtil.not_empty(parent_id) else 'error',
                None if ValidateUtil.not_empty(menu_name) else 'error',
                None if ValidateUtil.not_empty(order_num) else 'error',
                None if ValidateUtil.not_empty(path) else 'error',
                None
                if ValidateUtil.not_empty(parent_id)
                else '请选择上级菜单！',
                None
                if ValidateUtil.not_empty(menu_name)
                else '请输入菜单名称！',
                None
                if ValidateUtil.not_empty(order_num)
                else '请输入显示排序！',
                None if ValidateUtil.not_empty(path) else '请输入路由地址！',
            ],
            modal_visible=no_update,
            operations=no_update,
        )

    raise PreventUpdate


@app.callback(
    [
        Output('content-menu-is_frame', 'value'),
        Output('content-menu-path', 'value'),
        Output('content-menu-visible', 'value'),
        Output('content-menu-status', 'value'),
    ],
    Input('menu-edit-id-store', 'data'),
)
def set_edit_info(edit_info):
    """
    菜单类型为目录时回显菜单数据回调
    """
    if edit_info:
        return [
            edit_info.get('is_frame'),
            edit_info.get('path'),
            edit_info.get('visible'),
            edit_info.get('status'),
        ]

    raise PreventUpdate
