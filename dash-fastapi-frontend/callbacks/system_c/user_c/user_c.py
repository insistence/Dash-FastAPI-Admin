import dash
import time
import uuid
from dash import html, dcc
from dash.dependencies import Input, Output, State, ALL
import feffery_antd_components as fac
import feffery_utils_components as fuc
from jsonpath_ng import parse
from flask import session, json
from collections import OrderedDict

from server import app
from api.dept import get_dept_tree_api
from api.user import get_user_list_api, get_user_detail_api, add_user_api, edit_user_api, delete_user_api, reset_user_password_api, export_user_list_api
from api.role import get_role_select_option_api
from api.post import get_post_select_option_api


@app.callback(
    [Output('dept-tree', 'treeData'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    Input('dept-input-search', 'value'),
    prevent_initial_call=True
)
def get_search_dept_tree(dept_input):
    dept_params = dict(dept_name=dept_input)
    tree_info = get_dept_tree_api(dept_params)
    if tree_info['code'] == 200:
        tree_data = tree_info['data']

        return [tree_data, {'timestamp': time.time()}]

    return [dash.no_update, {'timestamp': time.time()}]


@app.callback(
    [Output('user-list-table', 'data', allow_duplicate=True),
     Output('user-list-table', 'pagination', allow_duplicate=True),
     Output('user-list-table', 'key'),
     Output('user-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('dept-tree', 'selectedKeys'),
     Input('user-search', 'nClicks'),
     Input('user-refresh', 'nClicks'),
     Input('user-list-table', 'pagination'),
     Input('user-operations-store', 'data')],
    [State('user-user_name-input', 'value'),
     State('user-phone_number-input', 'value'),
     State('user-status-select', 'value'),
     State('user-create_time-range', 'value'),
     State('user-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_user_table_data_by_dept_tree(selected_dept_tree, search_click, refresh_click, pagination, operations,
                                     user_name, phone_number, status_select, create_time_range, button_perms):
    dept_id = None
    create_time_start = None
    create_time_end = None
    if create_time_range:
        create_time_start = create_time_range[0]
        create_time_end = create_time_range[1]
    if selected_dept_tree:
        dept_id = int(selected_dept_tree[0])
    query_params = dict(
        dept_id=dept_id,
        user_name=user_name,
        phonenumber=phone_number,
        status=status_select,
        create_time_start=create_time_start,
        create_time_end=create_time_end,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'user-list-table':
        query_params = dict(
            dept_id=dept_id,
            user_name=user_name,
            phonenumber=phone_number,
            status=status_select,
            create_time_start=create_time_start,
            create_time_end=create_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if selected_dept_tree or search_click or refresh_click or pagination or operations:
        table_info = get_user_list_api(query_params)
        if table_info['code'] == 200:
            table_data = table_info['data']['rows']
            table_pagination = dict(
                pageSize=table_info['data']['page_size'],
                current=table_info['data']['page_num'],
                showSizeChanger=True,
                pageSizeOptions=[10, 30, 50, 100],
                showQuickJumper=True,
                total=table_info['data']['total']
            )
            for item in table_data:
                if item['status'] == '0':
                    item['status'] = dict(checked=True)
                else:
                    item['status'] = dict(checked=False)
                item['key'] = str(item['user_id'])
                if item['user_id'] == 1:
                    item['operation'] = []
                else:
                    item['operation'] = [
                        {
                            'title': '修改',
                            'icon': 'antd-edit'
                        } if 'system:user:edit' in button_perms else None,
                        {
                            'title': '删除',
                            'icon': 'antd-delete'
                        } if 'system:user:remove' in button_perms else None,
                        {
                            'title': '重置密码',
                            'icon': 'antd-key'
                        } if 'system:user:resetPwd' in button_perms else None
                    ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('dept-tree', 'selectedKeys'),
     Output('user-user_name-input', 'value'),
     Output('user-phone_number-input', 'value'),
     Output('user-status-select', 'value'),
     Output('user-create_time-range', 'value'),
     Output('user-operations-store', 'data')],
    Input('user-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_user_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 6


@app.callback(
    [Output('user-search-form-container', 'hidden'),
     Output('user-hidden-tooltip', 'title')],
    Input('user-hidden', 'nClicks'),
    State('user-search-form-container', 'hidden'),
    prevent_initial_call=True
)
def hidden_user_search_form(hidden_click, hidden_status):
    if hidden_click:

        return [not hidden_status, '隐藏搜索' if hidden_status else '显示搜索']
    return [dash.no_update] * 2


@app.callback(
    Output({'type': 'user-operation-button', 'index': 'edit'}, 'disabled'),
    Input('user-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_user_edit_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1 or '1' in table_rows_selected:
                return True

            return False

        return True

    return dash.no_update


@app.callback(
    Output({'type': 'user-operation-button', 'index': 'delete'}, 'disabled'),
    Input('user-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_user_delete_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if '1' in table_rows_selected:
                return True
            if len(table_rows_selected) > 1:
                return False

            return False

        return True

    return dash.no_update


@app.callback(
    [Output('user-add-modal', 'visible', allow_duplicate=True),
     Output('user-add-dept_id', 'treeData'),
     Output('user-add-post', 'options'),
     Output('user-add-role', 'options'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    Input('user-add', 'nClicks'),
    prevent_initial_call=True
)
def add_user_modal(add_click):
    if add_click:
        dept_params = dict(dept_name='')
        tree_info = get_dept_tree_api(dept_params)
        post_option_info = get_post_select_option_api()
        role_option_info = get_role_select_option_api()
        if tree_info['code'] == 200 and post_option_info['code'] == 200 and role_option_info['code'] == 200:
            tree_data = tree_info['data']
            post_option = post_option_info['data']
            role_option = role_option_info['data']

            return [
                True,
                tree_data,
                [dict(label=item['post_name'], value=item['post_id']) for item in post_option],
                [dict(label=item['role_name'], value=item['role_id']) for item in role_option],
                {'timestamp': time.time()}
            ]

        return [dash.no_update] * 4 + [{'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('user-add-nick_name-form-item', 'validateStatus'),
     Output('user-add-user_name-form-item', 'validateStatus'),
     Output('user-add-password-form-item', 'validateStatus'),
     Output('user-add-nick_name-form-item', 'help'),
     Output('user-add-user_name-form-item', 'help'),
     Output('user-add-password-form-item', 'help'),
     Output('user-add-modal', 'visible', allow_duplicate=True),
     Output('user-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('user-add-modal', 'okCounts'),
    [State('user-add-nick_name', 'value'),
     State('user-add-dept_id', 'value'),
     State('user-add-phone_number', 'value'),
     State('user-add-email', 'value'),
     State('user-add-user_name', 'value'),
     State('user-add-password', 'value'),
     State('user-add-sex', 'value'),
     State('user-add-status', 'value'),
     State('user-add-post', 'value'),
     State('user-add-role', 'value'),
     State('user-add-remark', 'value')],
    prevent_initial_call=True
)
def usr_add_confirm(add_confirm, nick_name, dept_id, phone_number, email, user_name, password, sex, status, post, role,
                    remark):
    if add_confirm:

        if all([nick_name, user_name, password]):
            params = dict(nick_name=nick_name, dept_id=dept_id, phonenumber=phone_number,
                          email=email, user_name=user_name, password=password, sex=sex,
                          status=status, post_id=','.join(map(str, post)), role_id=','.join(map(str, role)),
                          remark=remark)
            add_button_result = add_user_api(params)

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
            None if nick_name else 'error',
            None if user_name else 'error',
            None if password else 'error',
            None if nick_name else '请输入用户昵称！',
            None if user_name else '请输入用户名称！',
            None if password else '请输入用户密码！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('新增失败', type='error')
        ]

    return [dash.no_update] * 10


@app.callback(
    [Output('user-edit-modal', 'visible', allow_duplicate=True),
     Output('user-edit-dept_id', 'treeData'),
     Output('user-edit-post', 'options'),
     Output('user-edit-role', 'options'),
     Output('user-edit-nick_name', 'value'),
     Output('user-edit-dept_id', 'value'),
     Output('user-edit-phone_number', 'value'),
     Output('user-edit-email', 'value'),
     Output('user-edit-sex', 'value'),
     Output('user-edit-status', 'value'),
     Output('user-edit-post', 'value'),
     Output('user-edit-role', 'value'),
     Output('user-edit-remark', 'value'),
     Output('user-edit-id-store', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input({'type': 'user-operation-button', 'index': ALL}, 'nClicks'),
     Input('user-list-table', 'nClicksDropdownItem')],
    [State('user-list-table', 'selectedRowKeys'),
     State('user-list-table', 'recentlyClickedDropdownItemTitle'),
     State('user-list-table', 'recentlyDropdownItemClickedRow')],
    prevent_initial_call=True
)
def user_edit_modal(operation_click, dropdown_click,
                    selected_row_keys, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'edit', 'type': 'user-operation-button'} or (trigger_id == 'user-list-table' and recently_clicked_dropdown_item_title == '修改'):

        dept_params = dict(dept_name='')
        tree_data = get_dept_tree_api(dept_params)['data']
        post_option = get_post_select_option_api()['data']
        role_option = get_role_select_option_api()['data']

        if trigger_id == {'index': 'edit', 'type': 'user-operation-button'}:
            user_id = int(selected_row_keys[0])
        else:
            if recently_clicked_dropdown_item_title == '修改':
                user_id = int(recently_dropdown_item_clicked_row['key'])
            else:
                return [dash.no_update] * 15

        edit_button_info = get_user_detail_api(user_id)
        if edit_button_info['code'] == 200:
            edit_button_result = edit_button_info['data']
            user = edit_button_result['user']
            dept = edit_button_result['dept']
            role = edit_button_result['role']
            post = edit_button_result['post']

            return [
                True,
                tree_data,
                [dict(label=item['post_name'], value=item['post_id']) for item in post_option if item] or [],
                [dict(label=item['role_name'], value=item['role_id']) for item in role_option if item] or [],
                user['nick_name'],
                dept['dept_id'] if dept else None,
                user['phonenumber'],
                user['email'],
                user['sex'],
                user['status'],
                [item['post_id'] for item in post if item] or [],
                [item['role_id'] for item in role if item] or [],
                user['remark'],
                {'user_id': user_id},
                {'timestamp': time.time()}
            ]

        return [dash.no_update] * 14 + [{'timestamp': time.time()}]

    return [dash.no_update] * 15


@app.callback(
    [Output('user-edit-nick_name-form-item', 'validateStatus'),
     Output('user-edit-nick_name-form-item', 'help'),
     Output('user-edit-modal', 'visible', allow_duplicate=True),
     Output('user-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('user-edit-modal', 'okCounts'),
    [State('user-edit-nick_name', 'value'),
     State('user-edit-dept_id', 'value'),
     State('user-edit-phone_number', 'value'),
     State('user-edit-email', 'value'),
     State('user-edit-sex', 'value'),
     State('user-edit-status', 'value'),
     State('user-edit-post', 'value'),
     State('user-edit-role', 'value'),
     State('user-edit-remark', 'value'),
     State('user-edit-id-store', 'data')],
    prevent_initial_call=True
)
def usr_edit_confirm(edit_confirm, nick_name, dept_id, phone_number, email, sex, status, post, role, remark, user_id):
    if edit_confirm:

        if all([nick_name]):
            params = dict(user_id=user_id['user_id'], nick_name=nick_name, dept_id=dept_id if dept_id else -1,
                          phonenumber=phone_number, email=email, sex=sex, status=status,
                          post_id=','.join(map(str, post)), role_id=','.join(map(str, role)), remark=remark)
            edit_button_result = edit_user_api(params)

            if edit_button_result['code'] == 200:
                return [
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
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('编辑失败', type='error')
            ]

        return [
            None if nick_name else 'error',
            None if nick_name else '请输入用户昵称！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('编辑失败', type='error')
        ]

    return [dash.no_update] * 6


@app.callback(
    [Output('user-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    [Input('user-list-table', 'recentlySwitchDataIndex'),
     Input('user-list-table', 'recentlySwitchStatus'),
     Input('user-list-table', 'recentlySwitchRow')],
    prevent_initial_call=True
)
def table_switch_user_status(recently_switch_data_index, recently_switch_status, recently_switch_row):
    if recently_switch_data_index:
        if recently_switch_status:
            params = dict(user_id=int(recently_switch_row['key']), status='0', type='status')
        else:
            params = dict(user_id=int(recently_switch_row['key']), status='1', type='status')
        edit_button_result = edit_user_api(params)
        if edit_button_result['code'] == 200:

            return [
                {'type': 'switch-status'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('修改成功', type='success')
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('修改失败', type='error')
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('user-delete-text', 'children'),
     Output('user-delete-confirm-modal', 'visible'),
     Output('user-delete-ids-store', 'data')],
    [Input({'type': 'user-operation-button', 'index': ALL}, 'nClicks'),
     Input('user-list-table', 'nClicksDropdownItem')],
    [State('user-list-table', 'selectedRowKeys'),
     State('user-list-table', 'recentlyClickedDropdownItemTitle'),
     State('user-list-table', 'recentlyDropdownItemClickedRow')],
    prevent_initial_call=True
)
def user_delete_modal(operation_click, dropdown_click,
                      selected_row_keys, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'user-operation-button'} or (trigger_id == 'user-list-table' and recently_clicked_dropdown_item_title == '删除'):

        if trigger_id == {'index': 'delete', 'type': 'user-operation-button'}:
            user_ids = ','.join(selected_row_keys)
        else:
            if recently_clicked_dropdown_item_title == '删除':
                user_ids = recently_dropdown_item_clicked_row['key']
            else:
                return [dash.no_update] * 3

        return [
            f'是否确认删除用户编号为{user_ids}的用户？',
            True,
            {'user_ids': user_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('user-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('user-delete-confirm-modal', 'okCounts'),
    State('user-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def user_delete_confirm(delete_confirm, user_ids_data):
    if delete_confirm:

        params = user_ids_data
        delete_button_info = delete_user_api(params)
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


@app.callback(
    [Output('user-reset-password-confirm-modal', 'visible'),
     Output('reset-password-row-key-store', 'data'),
     Output('reset-password-input', 'value')],
    Input('user-list-table', 'nClicksDropdownItem'),
    [State('user-list-table', 'recentlyClickedDropdownItemTitle'),
     State('user-list-table', 'recentlyDropdownItemClickedRow')],
    prevent_initial_call=True
)
def user_reset_password_modal(dropdown_click, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    if dropdown_click:
        if recently_clicked_dropdown_item_title == '重置密码':
            user_id = recently_dropdown_item_clicked_row['key']
        else:
            return [dash.no_update] * 3

        return [
            True,
            {'user_id': user_id},
            None
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('user-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('user-reset-password-confirm-modal', 'okCounts'),
    [State('reset-password-row-key-store', 'data'),
     State('reset-password-input', 'value')],
    prevent_initial_call=True
)
def user_reset_password_confirm(reset_confirm, user_id_data, reset_password):
    if reset_confirm:

        user_id_data['password'] = reset_password
        params = user_id_data
        reset_button_info = reset_user_password_api(params)
        if reset_button_info['code'] == 200:
            return [
                {'type': 'reset-password'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('重置成功', type='success')
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('重置失败', type='error')
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('user-export-container', 'data', allow_duplicate=True),
     Output('user-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('user-export', 'nClicks'),
    prevent_initial_call=True
)
def export_user_list(export_click):
    if export_click:
        export_user_res = export_user_list_api({})
        if export_user_res.status_code == 200:
            export_user = export_user_res.content

            return [
                dcc.send_bytes(export_user, f'用户信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
                {'timestamp': time.time()},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('导出成功', type='success')
            ]

        return [
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('导出失败', type='error')
        ]

    return [dash.no_update] * 4


@app.callback(
    Output('user-export-container', 'data', allow_duplicate=True),
    Input('user-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_user_export_status(data):
    time.sleep(0.5)
    if data:

        return None

    return dash.no_update
