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
     Input('dept-operations-store', 'data'),
     Input('dept-fold', 'nClicks')],
    [State('dept-dept_name-input', 'value'),
     State('dept-status-select', 'value'),
     State('dept-list-table', 'defaultExpandedRowKeys')],
    prevent_initial_call=True
)
def get_dept_table_data(search_click, operations, fold_click, dept_name, status_select, in_default_expanded_row_keys):

    query_params = dict(
        dept_name=dept_name,
        status=status_select
    )
    if search_click or operations or fold_click:
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
    [Output('dept-add-modal', 'visible', allow_duplicate=True),
     Output('dept-add-parent_id', 'treeData'),
     Output('dept-add-parent_id', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('dept-add', 'nClicks')],
    [Input('dept-add', 'nClicks'),
     Input('dept-list-table', 'nClicksButton')],
    [State('dept-list-table', 'clickedContent'),
     State('dept-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_user_modal(add_click, button_click, clicked_content, recently_button_clicked_row):
    if add_click or (button_click and clicked_content == '新增'):
        dept_params = dict(dept_name='')
        tree_info = get_dept_tree_api(dept_params)
        if tree_info['code'] == 200:
            tree_data = tree_info['data']

            return [
                True,
                tree_data,
                int(recently_button_clicked_row['key']) if recently_button_clicked_row else dash.no_update,
                {'timestamp': time.time()},
                None
            ]

        return [dash.no_update] * 3 + [{'timestamp': time.time()}, None]

    return [dash.no_update] * 4 + [None]


@app.callback(
    [Output('dept-add-parent_id-form-item', 'validateStatus'),
     Output('dept-add-dept_name-form-item', 'validateStatus'),
     Output('dept-add-order_num-form-item', 'validateStatus'),
     Output('dept-add-parent_id-form-item', 'help'),
     Output('dept-add-dept_name-form-item', 'help'),
     Output('dept-add-order_num-form-item', 'help'),
     Output('dept-add-modal', 'visible', allow_duplicate=True),
     Output('dept-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dept-add-modal', 'okCounts'),
    [State('dept-add-parent_id', 'value'),
     State('dept-add-dept_name', 'value'),
     State('dept-add-order_num', 'value'),
     State('dept-add-leader', 'value'),
     State('dept-add-phone', 'value'),
     State('dept-add-email', 'value'),
     State('dept-add-status', 'value')],
    prevent_initial_call=True
)
def dept_add_confirm(add_confirm, parent_id, dept_name, order_num, leader, phone, email, status):
    if add_confirm:

        if all([parent_id, dept_name, order_num]):
            params = dict(parent_id=parent_id, dept_name=dept_name, order_num=order_num,
                          leader=leader, phone=phone, email=email, status=status)
            add_button_result = add_dept_api(params)

            if add_button_result['code'] == 200:
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
                fuc.FefferyFancyMessage('新增失败', type='error')
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
            fuc.FefferyFancyMessage('新增失败', type='error')
        ]

    return [dash.no_update] * 10


@app.callback(
    [Output('dept-edit-modal', 'visible', allow_duplicate=True),
     Output('dept-edit-parent_id', 'treeData'),
     Output('dept-edit-parent_id', 'value'),
     Output('dept-edit-dept_name', 'value'),
     Output('dept-edit-order_num', 'value'),
     Output('dept-edit-leader', 'value'),
     Output('dept-edit-phone', 'value'),
     Output('dept-edit-email', 'value'),
     Output('dept-edit-status', 'value'),
     Output('dept-edit-id-store', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('dept-list-table', 'nClicksButton')],
    [State('dept-list-table', 'clickedContent'),
     State('dept-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def dept_edit_modal(button_click, clicked_content, recently_button_clicked_row):
    if button_click:

        if clicked_content == '修改':
            dept_id = int(recently_button_clicked_row['key'])
        else:
            return dash.no_update

        dept_params = dict(dept_id=dept_id)
        tree_info = get_dept_tree_for_edit_option_api(dept_params)
        edit_button_info = get_dept_detail_api(dept_id)
        if edit_button_info['code'] == 200 and tree_info['code'] == 200:
            edit_button_result = edit_button_info['data']
            tree_data = tree_info['data']

            return [
                True,
                tree_data,
                edit_button_result['parent_id'],
                edit_button_result['dept_name'],
                edit_button_result['order_num'],
                edit_button_result['leader'],
                edit_button_result['phone'],
                edit_button_result['email'],
                edit_button_result['status'],
                {'dept_id': dept_id},
                {'timestamp': time.time()}
            ]

        return [dash.no_update] * 10 + [{'timestamp': time.time()}]

    return [dash.no_update] * 11


@app.callback(
    [Output('dept-edit-parent_id-form-item', 'validateStatus'),
     Output('dept-edit-dept_name-form-item', 'validateStatus'),
     Output('dept-edit-order_num-form-item', 'validateStatus'),
     Output('dept-edit-parent_id-form-item', 'help'),
     Output('dept-edit-dept_name-form-item', 'help'),
     Output('dept-edit-order_num-form-item', 'help'),
     Output('dept-edit-modal', 'visible', allow_duplicate=True),
     Output('dept-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dept-edit-modal', 'okCounts'),
    [State('dept-edit-parent_id', 'value'),
     State('dept-edit-dept_name', 'value'),
     State('dept-edit-order_num', 'value'),
     State('dept-edit-leader', 'value'),
     State('dept-edit-phone', 'value'),
     State('dept-edit-email', 'value'),
     State('dept-edit-status', 'value'),
     State('dept-edit-id-store', 'data')],
    prevent_initial_call=True
)
def dept_edit_confirm(edit_confirm, parent_id, dept_name, order_num, leader, phone, email, status, dept_id):
    if edit_confirm:

        if all([parent_id, dept_name, order_num]):
            params = dict(dept_id=dept_id['dept_id'], parent_id=parent_id, dept_name=dept_name,
                          order_num=order_num, leader=leader, phone=phone, email=email,
                          status=status)
            edit_button_result = edit_dept_api(params)

            if edit_button_result['code'] == 200:
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
                fuc.FefferyFancyMessage('编辑失败', type='error')
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
            fuc.FefferyFancyMessage('编辑失败', type='error')
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
