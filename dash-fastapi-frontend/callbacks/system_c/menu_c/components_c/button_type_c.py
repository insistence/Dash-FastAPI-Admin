import dash
import time
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from utils.common import validate_data_not_empty
from api.system.menu import MenuApi


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
            Output('menu-parent_id-form-item', 'help', allow_duplicate=True),
            Output('menu-menu_name-form-item', 'help', allow_duplicate=True),
            Output('menu-order_num-form-item', 'help', allow_duplicate=True),
        ],
        modal_visible=Output('menu-modal', 'visible', allow_duplicate=True),
        operations=Output(
            'menu-operations-store', 'data', allow_duplicate=True
        ),
        api_check_token_trigger=Output(
            'api-check-token', 'data', allow_duplicate=True
        ),
        global_message_container=Output(
            'global-message-container', 'children', allow_duplicate=True
        ),
    ),
    inputs=dict(
        confirm_trigger=Input('menu-modal-F-trigger', 'data'),
    ),
    state=dict(
        modal_type=State('menu-operations-store-bk', 'data'),
        edit_row_info=State('menu-edit-id-store', 'data'),
        parent_id=State('menu-parent_id', 'value'),
        menu_type=State('menu-menu_type', 'value'),
        icon=State('menu-icon', 'value'),
        menu_name=State('menu-menu_name', 'value'),
        order_num=State('menu-order_num', 'value'),
        perms=State('button-menu-perms', 'value'),
    ),
    prevent_initial_call=True,
)
def menu_confirm_button(
    confirm_trigger,
    modal_type,
    edit_row_info,
    parent_id,
    menu_type,
    icon,
    menu_name,
    order_num,
    perms,
):
    """
    菜单类型为按钮时新增或编辑弹窗确认回调，实现新增或编辑操作
    """
    if confirm_trigger:
        if all(
            validate_data_not_empty(item)
            for item in [parent_id, menu_name, order_num]
        ):
            params_add = dict(
                parent_id=parent_id,
                menu_type=menu_type,
                icon=icon,
                menu_name=menu_name,
                order_num=order_num,
                perms=perms,
            )
            params_edit = dict(
                menu_id=edit_row_info.get('menu_id') if edit_row_info else None,
                parent_id=parent_id,
                menu_type=menu_type,
                icon=icon,
                menu_name=menu_name,
                order_num=order_num,
                perms=perms,
            )
            api_res = {}
            modal_type = modal_type.get('type')
            if modal_type == 'add':
                api_res = MenuApi.add_menu(params_add)
            if modal_type == 'edit':
                api_res = MenuApi.update_menu(params_edit)
            if api_res.get('code') == 200:
                if modal_type == 'add':
                    return dict(
                        form_validate=[None] * 6,
                        modal_visible=False,
                        operations={'type': 'add'},
                        api_check_token_trigger={'timestamp': time.time()},
                        global_message_container=fuc.FefferyFancyMessage(
                            '新增成功', type='success'
                        ),
                    )
                if modal_type == 'edit':
                    return dict(
                        form_validate=[None] * 6,
                        modal_visible=False,
                        operations={'type': 'edit'},
                        api_check_token_trigger={'timestamp': time.time()},
                        global_message_container=fuc.FefferyFancyMessage(
                            '编辑成功', type='success'
                        ),
                    )

            return dict(
                form_validate=[None] * 6,
                modal_visible=dash.no_update,
                operations=dash.no_update,
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage(
                    '处理失败', type='error'
                ),
            )

        return dict(
            form_validate=[
                None if validate_data_not_empty(parent_id) else 'error',
                None if validate_data_not_empty(menu_name) else 'error',
                None if validate_data_not_empty(order_num) else 'error',
                None
                if validate_data_not_empty(parent_id)
                else '请选择上级菜单！',
                None
                if validate_data_not_empty(menu_name)
                else '请输入菜单名称！',
                None
                if validate_data_not_empty(order_num)
                else '请输入显示排序！',
            ],
            modal_visible=dash.no_update,
            operations=dash.no_update,
            api_check_token_trigger=dash.no_update,
            global_message_container=fuc.FefferyFancyMessage(
                '处理失败', type='error'
            ),
        )

    raise PreventUpdate


@app.callback(
    Output('button-menu-perms', 'value'), Input('menu-edit-id-store', 'data')
)
def set_edit_info(edit_info):
    """
    菜单类型为按钮时回显菜单数据回调
    """
    if edit_info:
        return edit_info.get('perms')

    raise PreventUpdate
