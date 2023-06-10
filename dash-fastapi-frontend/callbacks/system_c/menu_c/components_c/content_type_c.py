import dash
import time
import uuid
from dash import html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc
from jsonpath_ng import parse
from flask import session, json
from collections import OrderedDict

from server import app
from utils.tree_tool import list_to_tree
from views.system.menu.components import *
from api.menu import add_menu_api, edit_menu_api


@app.callback(
    [Output('menu-parent_id-form-item', 'validateStatus', allow_duplicate=True),
     Output('menu-menu_name-form-item', 'validateStatus', allow_duplicate=True),
     Output('menu-order_num-form-item', 'validateStatus', allow_duplicate=True),
     Output('content-menu-path-form-item', 'validateStatus'),
     Output('menu-parent_id-form-item', 'help', allow_duplicate=True),
     Output('menu-menu_name-form-item', 'help', allow_duplicate=True),
     Output('menu-order_num-form-item', 'help', allow_duplicate=True),
     Output('content-menu-path-form-item', 'help'),
     Output('menu-modal', 'visible', allow_duplicate=True),
     Output('menu-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('menu-modal-M-trigger', 'data'),
    [State('menu-operations-store-bk', 'data'),
     State('menu-parent_id', 'value'),
     State('menu-menu_type', 'value'),
     State('menu-icon', 'value'),
     State('menu-menu_name', 'value'),
     State('menu-order_num', 'value'),
     State('content-menu-is_frame', 'value'),
     State('content-menu-path', 'value'),
     State('content-menu-visible', 'value'),
     State('content-menu-status', 'value')],
    prevent_initial_call=True
)
def menu_confirm(confirm_trigger, operation_type, parent_id, menu_type, icon, menu_name, order_num, is_frame, path, visible, status):
    if confirm_trigger:
        if all([parent_id, menu_name, order_num, path]):
            params = dict(parent_id=parent_id, menu_type=menu_type, icon=icon, menu_name=menu_name, order_num=order_num,
                        is_frame=is_frame, path=path, visible=visible, status=status)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_menu_api(params)
            if operation_type == 'edit':
                api_res = edit_menu_api(params)
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
