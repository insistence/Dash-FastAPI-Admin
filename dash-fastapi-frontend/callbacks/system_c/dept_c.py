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
from utils.tree_tool import get_dept_tree
from api.dept import get_dept_tree_api, get_dept_list_api, add_dept_api, edit_dept_api, delete_dept_api, \
    get_dept_detail_api, get_dept_tree_for_edit_option_api


@app.callback(
    [Output('dept-list-table', 'data', allow_duplicate=True),
     Output('dept-list-table', 'key'),
     Output('dept-list-table', 'defaultExpandedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('dept-fold', 'nClicks')],
    [Input('dept-search', 'nClicks'),
     Input('dept-refresh', 'nClicks'),
     Input('dept-operations-store', 'data'),
     Input('dept-fold', 'nClicks')],
    [State('dept-dept_name-input', 'value'),
     State('dept-status-select', 'value'),
     State('dept-list-table', 'defaultExpandedRowKeys'),
     State('dept-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_dept_table_data(search_click, refresh_click, operations, fold_click, dept_name, status_select, in_default_expanded_row_keys, button_perms):

    query_params = dict(
        dept_name=dept_name,
        status=status_select
    )
    if search_click or refresh_click or operations or fold_click:
        table_info = get_dept_list_api(query_params)
        default_expanded_row_keys = []
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
                    item['operation'] = [
                        {
                            'content': '修改',
                            'type': 'link',
                            'icon': 'antd-edit'
                        } if 'system:dept:edit' in button_perms else {},
                        {
                            'content': '新增',
                            'type': 'link',
                            'icon': 'antd-plus'
                        } if 'system:dept:add' in button_perms else {},
                    ]
                else:
                    item['operation'] = [
                        {
                            'content': '修改',
                            'type': 'link',
                            'icon': 'antd-edit'
                        } if 'system:dept:edit' in button_perms else {},
                        {
                            'content': '新增',
                            'type': 'link',
                            'icon': 'antd-plus'
                        } if 'system:dept:add' in button_perms else {},
                        {
                            'content': '删除',
                            'type': 'link',
                            'icon': 'antd-delete'
                        } if 'system:dept:remove' in button_perms else {},
                    ]
            table_data_new = get_dept_tree(0, table_data)

            if fold_click:
                if in_default_expanded_row_keys:
                    return [table_data_new, str(uuid.uuid4()), [], {'timestamp': time.time()}, None]

            return [table_data_new, str(uuid.uuid4()), default_expanded_row_keys, {'timestamp': time.time()}, None]

        return [dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}, None]

    return [dash.no_update] * 4 + [None]


@app.callback(
    [Output('dept-dept_name-input', 'value'),
     Output('dept-status-select', 'value'),
     Output('dept-operations-store', 'data')],
    Input('dept-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_dept_query_params(reset_click):
    if reset_click:
        return [None, None, {'type': 'reset'}]

    return [dash.no_update] * 3


@app.callback(
    [Output('dept-search-form-container', 'hidden'),
     Output('dept-hidden-tooltip', 'title')],
    Input('dept-hidden', 'nClicks'),
    State('dept-search-form-container', 'hidden'),
    prevent_initial_call=True
)
def hidden_dept_search_form(hidden_click, hidden_status):
    if hidden_click:

        return [not hidden_status, '隐藏搜索' if hidden_status else '显示搜索']
    return [dash.no_update] * 2


@app.callback(
    [Output('dept-modal', 'visible', allow_duplicate=True),
     Output('dept-modal', 'title'),
     Output('dept-parent_id-div', 'hidden'),
     Output('dept-parent_id', 'treeData'),
     Output('dept-parent_id', 'value'),
     Output('dept-dept_name', 'value'),
     Output('dept-order_num', 'value'),
     Output('dept-leader', 'value'),
     Output('dept-phone', 'value'),
     Output('dept-email', 'value'),
     Output('dept-status', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('dept-add', 'nClicks'),
     Output('dept-edit-id-store', 'data'),
     Output('dept-operations-store-bk', 'data')],
    [Input('dept-add', 'nClicks'),
     Input('dept-list-table', 'nClicksButton')],
    [State('dept-list-table', 'clickedContent'),
     State('dept-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_dept_modal(add_click, button_click, clicked_content, recently_button_clicked_row):
    if add_click or (button_click and clicked_content != '删除'):
        dept_params = dict(dept_name='')
        if clicked_content == '修改':
            tree_info = get_dept_tree_for_edit_option_api(dept_params)
        else:
            tree_info = get_dept_tree_api(dept_params)
        if tree_info['code'] == 200:
            tree_data = tree_info['data']

            if add_click:
                return [
                    True,
                    '新增部门',
                    False,
                    tree_data,
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    '0',
                    {'timestamp': time.time()},
                    None,
                    None,
                    {'type': 'add'}
                ]
            elif button_click and clicked_content == '新增':
                return [
                    True,
                    '新增部门',
                    False,
                    tree_data,
                    str(recently_button_clicked_row['key']),
                    None,
                    None,
                    None,
                    None,
                    None,
                    '0',
                    {'timestamp': time.time()},
                    None,
                    None,
                    {'type': 'add'}
                ]
            elif button_click and clicked_content == '修改':
                dept_id = int(recently_button_clicked_row['key'])
                dept_info_res = get_dept_detail_api(dept_id=dept_id)
                if dept_info_res['code'] == 200:
                    dept_info = dept_info_res['data']
                    if dept_info.get('parent_id') == 0:
                        return [
                            True,
                            '编辑部门',
                            True,
                            tree_data,
                            str(dept_info.get('parent_id')),
                            dept_info.get('dept_name'),
                            dept_info.get('order_num'),
                            dept_info.get('leader'),
                            dept_info.get('phone'),
                            dept_info.get('email'),
                            dept_info.get('status'),
                            {'timestamp': time.time()},
                            None,
                            dept_info,
                            {'type': 'edit'}
                        ]
                    else:
                        return [
                            True,
                            '编辑部门',
                            False,
                            tree_data,
                            str(dept_info.get('parent_id')),
                            dept_info.get('dept_name'),
                            dept_info.get('order_num'),
                            dept_info.get('leader'),
                            dept_info.get('phone'),
                            dept_info.get('email'),
                            dept_info.get('status'),
                            {'timestamp': time.time()},
                            None,
                            dept_info,
                            {'type': 'edit'}
                        ]

        return [dash.no_update] * 10 + [{'timestamp': time.time()}, None, None, None]

    return [dash.no_update] * 11 + [None, None, None]


@app.callback(
    [Output('dept-parent_id-form-item', 'validateStatus'),
     Output('dept-dept_name-form-item', 'validateStatus'),
     Output('dept-order_num-form-item', 'validateStatus'),
     Output('dept-parent_id-form-item', 'help'),
     Output('dept-dept_name-form-item', 'help'),
     Output('dept-order_num-form-item', 'help'),
     Output('dept-modal', 'visible'),
     Output('dept-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dept-modal', 'okCounts'),
    [State('dept-operations-store-bk', 'data'),
     State('dept-edit-id-store', 'data'),
     State('dept-parent_id', 'value'),
     State('dept-dept_name', 'value'),
     State('dept-order_num', 'value'),
     State('dept-leader', 'value'),
     State('dept-phone', 'value'),
     State('dept-email', 'value'),
     State('dept-status', 'value')],
    prevent_initial_call=True
)
def dept_confirm(confirm_trigger, operation_type, cur_dept_info, parent_id, dept_name, order_num, leader, phone, email, status):
    if confirm_trigger:
        if all([parent_id, dept_name, order_num]):
            params_add = dict(parent_id=parent_id, dept_name=dept_name, order_num=order_num, leader=leader, phone=phone, 
                              email=email, status=status)
            params_edit = dict(dept_id=cur_dept_info.get('dept_id') if cur_dept_info else None, parent_id=parent_id, dept_name=dept_name,
                          order_num=order_num, leader=leader, phone=phone, email=email, status=status)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_dept_api(params_add)
            if operation_type == 'edit':
                api_res = edit_dept_api(params_edit)
            if api_res.get('code') == 200:
                if operation_type == 'add':
                    return [
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
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('处理失败', type='error')
            ]
        
        return [
            None if parent_id else 'error',
            None if dept_name else 'error',
            None if order_num else 'error',
            None if parent_id else '请选择上级部门！',
            None if dept_name else '请输入部门名称！',
            None if order_num else '请输入显示排序！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]         

    return [dash.no_update] * 10


@app.callback(
    [Output('dept-delete-text', 'children'),
     Output('dept-delete-confirm-modal', 'visible'),
     Output('dept-delete-ids-store', 'data')],
    [Input('dept-list-table', 'nClicksButton')],
    [State('dept-list-table', 'clickedContent'),
     State('dept-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def dept_delete_modal(button_click, clicked_content, recently_button_clicked_row):
    if button_click:

        if clicked_content == '删除':
            dept_ids = recently_button_clicked_row['key']
        else:
            return dash.no_update

        return [
            f'是否确认删除部门编号为{dept_ids}的部门？',
            True,
            {'dept_ids': dept_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('dept-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dept-delete-confirm-modal', 'okCounts'),
    State('dept-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def dept_delete_confirm(delete_confirm, dept_ids_data):
    if delete_confirm:

        params = dept_ids_data
        delete_button_info = delete_dept_api(params)
        if delete_button_info['code'] == 200:
            return [
                {'type': 'delete'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('删除成功', type='success')
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('删除失败', type='error')
        ]

    return [dash.no_update] * 3
