import dash
import time
from dash.dependencies import Input, Output, State
import feffery_utils_components as fuc

from server import app
from api.menu import add_menu_api, edit_menu_api


@app.callback(
    [Output('menu-parent_id-form-item', 'validateStatus', allow_duplicate=True),
     Output('menu-menu_name-form-item', 'validateStatus', allow_duplicate=True),
     Output('menu-order_num-form-item', 'validateStatus', allow_duplicate=True),
     Output('menu-menu-path-form-item', 'validateStatus'),
     Output('menu-parent_id-form-item', 'help', allow_duplicate=True),
     Output('menu-menu_name-form-item', 'help', allow_duplicate=True),
     Output('menu-order_num-form-item', 'help', allow_duplicate=True),
     Output('menu-menu-path-form-item', 'help', allow_duplicate=True),
     Output('menu-modal', 'visible'),
     Output('menu-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('menu-modal-C-trigger', 'data'),
    [State('menu-operations-store-bk', 'data'),
     State('menu-edit-id-store', 'data'),
     State('menu-parent_id', 'value'),
     State('menu-menu_type', 'value'),
     State('menu-icon', 'value'),
     State('menu-menu_name', 'value'),
     State('menu-order_num', 'value'),
     State('menu-menu-is_frame', 'value'),
     State('menu-menu-path', 'value'),
     State('menu-menu-component', 'value'),
     State('menu-menu-perms', 'value'),
     State('menu-menu-query', 'value'),
     State('menu-menu-is_cache', 'value'),
     State('menu-menu-visible', 'value'),
     State('menu-menu-status', 'value')],
    prevent_initial_call=True
)
def menu_confirm_menu(confirm_trigger, operation_type, cur_menu_info, parent_id, menu_type, icon, menu_name, order_num, is_frame, path, 
                 component, perms, query, is_cache, visible, status):
    if confirm_trigger:
        if all([parent_id, menu_name, order_num, path]):
            params_add = dict(parent_id=parent_id, menu_type=menu_type, icon=icon, menu_name=menu_name, order_num=order_num, is_frame=is_frame, 
                              path=path, component=component, perms=perms, query=query, is_cache=is_cache, visible=visible, status=status)
            params_edit = dict(menu_id=cur_menu_info.get('menu_id') if cur_menu_info else None, parent_id=parent_id, menu_type=menu_type, icon=icon, 
                            menu_name=menu_name, order_num=order_num, is_frame=is_frame, path=path, component=component, 
                            perms=perms, query=query, is_cache=is_cache, visible=visible, status=status)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_menu_api(params_add)
            if operation_type == 'edit':
                api_res = edit_menu_api(params_edit)
            if api_res.get('code') == 200:
                if operation_type == 'add':
                    return [
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        False,
                        {'type': 'add'},
                        {'timestamp': time.time()},
                        fuc.FefferyFancyMessage('新增成功', type='success')
                    ]
                if operation_type == 'edit':
                    return [
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        False,
                        {'type': 'edit'},
                        {'timestamp': time.time()},
                        fuc.FefferyFancyMessage('编辑成功', type='success')
                    ]
            
            return [
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('处理失败', type='error')
            ]
        
        return [
            None if parent_id else 'error',
            None if menu_name else 'error',
            None if order_num else 'error',
            None if path else 'error',
            None if parent_id else '请选择上级菜单！',
            None if menu_name else '请输入菜单名称！',
            None if order_num else '请输入显示排序！',
            None if path else '请输入路由地址！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]         

    return [dash.no_update] * 12


@app.callback(
    [Output('menu-menu-is_frame', 'value'),
     Output('menu-menu-path', 'value'),
     Output('menu-menu-component', 'value'),
     Output('menu-menu-perms', 'value'),
     Output('menu-menu-query', 'value'),
     Output('menu-menu-is_cache', 'value'),
     Output('menu-menu-visible', 'value'),
     Output('menu-menu-status', 'value')],
    Input('menu-edit-id-store', 'data')
)
def set_edit_info(edit_info):
    if edit_info:
        return [
            edit_info.get('is_frame'),
            edit_info.get('path'),
            edit_info.get('component'),
            edit_info.get('perms'),
            edit_info.get('query'),
            edit_info.get('is_cache'),
            edit_info.get('visible'),
            edit_info.get('status')
        ]

    return [dash.no_update] * 8
