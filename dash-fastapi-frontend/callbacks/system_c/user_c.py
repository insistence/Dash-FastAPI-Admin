import dash
import time
from dash import html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc
from jsonpath_ng import parse
from flask import session, json
from collections import OrderedDict

from server import app
from api.dept import get_dept_tree_api
from api.user import get_user_list_api, get_user_detail_api, add_user_api, edit_user_api, delete_user_api
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
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('dept-tree', 'selectedKeys'),
     Input('user-search', 'nClicks'),
     Input('user-list-table', 'pagination'),
     Input('operations-store', 'data')],
    [State('user-user_name-input', 'value'),
     State('user-phone_number-input', 'value'),
     State('user-status-select', 'value'),
     State('user-create_time-range', 'value')],
    prevent_initial_call=True
)
def get_user_table_data_by_dept_tree(selected_dept_tree, search_click, pagination, operations,
                                     user_name, phone_number, status_select, create_time_range):
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
    if pagination:
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
    if selected_dept_tree or search_click or pagination or operations:
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
                item['operation'] = [
                    {
                        'title': '修改',
                        'icon': 'antd-edit'
                    },
                    {
                        'title': '删除',
                        'icon': 'antd-delete'
                    },
                    {
                        'title': '重置密码',
                        'icon': 'antd-key'
                    }
                ]

            return [table_data, table_pagination, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return dash.no_update


@app.callback(
    [Output('dept-tree', 'selectedKeys'),
     Output('user-user_name-input', 'value'),
     Output('user-phone_number-input', 'value'),
     Output('user-status-select', 'value'),
     Output('user-create_time-range', 'value')],
    Input('user-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_user_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, None]

    return dash.no_update


@app.callback(
    [Output('user-edit', 'disabled'),
     Output('user-delete', 'disabled')],
    Input('user-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_edit_delete_button_status(table_rows_selected):
    if table_rows_selected:
        if len(table_rows_selected) > 1:
            return [True, False]

        return [False, False]

    return dash.no_update


@app.callback(
    [Output('user-add-modal', 'visible'),
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

    return dash.no_update


@app.callback(
    [Output('user-add-nick_name-form-item', 'validateStatus'),
     Output('user-add-user_name-form-item', 'validateStatus'),
     Output('user-add-password-form-item', 'validateStatus'),
     Output('user-add-nick_name-form-item', 'help'),
     Output('user-add-user_name-form-item', 'help'),
     Output('user-add-password-form-item', 'help'),
     Output('operations-store', 'data', allow_duplicate=True),
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
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('新增失败', type='error')
        ]

    return dash.no_update


@app.callback(
    [Output('user-edit-modal', 'visible'),
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
     Output('edit-id-store', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('user-edit', 'nClicks'),
     Input('user-list-table', 'nClicksDropdownItem')],
    [State('user-list-table', 'selectedRowKeys'),
     State('user-list-table', 'recentlyClickedDropdownItemTitle'),
     State('user-list-table', 'recentlyDropdownItemClickedRow')],
    prevent_initial_call=True
)
def user_edit_modal(edit_click, dropdown_click,
                    selected_row_keys, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    if edit_click or dropdown_click:
        trigger_id = dash.ctx.triggered_id

        dept_params = dict(dept_name='')
        tree_data = get_dept_tree_api(dept_params)['data']
        post_option = get_post_select_option_api()['data']
        role_option = get_role_select_option_api()['data']

        if trigger_id == 'user-edit':
            user_id = int(selected_row_keys[0])
        else:
            if recently_clicked_dropdown_item_title == '修改':
                user_id = int(recently_dropdown_item_clicked_row['key'])
            else:
                return dash.no_update

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
                [dict(label=item['post_name'], value=item['post_id']) for item in post_option],
                [dict(label=item['role_name'], value=item['role_id']) for item in role_option],
                user['nick_name'],
                dept['dept_id'],
                user['phonenumber'],
                user['email'],
                user['sex'],
                user['status'],
                [item['post_id'] for item in post],
                [item['role_id'] for item in role],
                user['remark'],
                {'user_id': user_id},
                {'timestamp': time.time()}
            ]

        return [dash.no_update] * 14 + [{'timestamp': time.time()}]

    return dash.no_update


@app.callback(
    [Output('user-edit-nick_name-form-item', 'validateStatus'),
     Output('user-edit-nick_name-form-item', 'help'),
     Output('operations-store', 'data', allow_duplicate=True),
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
     State('edit-id-store', 'data')],
    prevent_initial_call=True
)
def usr_edit_confirm(edit_confirm, nick_name, dept_id, phone_number, email, sex, status, post, role, remark, user_id):
    if edit_confirm:

        if all([nick_name]):
            params = dict(user_id=user_id['user_id'], nick_name=nick_name, dept_id=dept_id, phonenumber=phone_number,
                          email=email, sex=sex, status=status, post_id=','.join(map(str, post)),
                          role_id=','.join(map(str, role)), remark=remark)
            edit_button_result = edit_user_api(params)

            if edit_button_result['code'] == 200:
                return [
                    None,
                    None,
                    {'type': 'edit'},
                    {'timestamp': time.time()},
                    fuc.FefferyFancyMessage('编辑成功', type='success')
                ]

            return [
                None,
                None,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('编辑失败', type='error')
            ]

        return [
            None if nick_name else 'error',
            None if nick_name else '请输入用户昵称！',
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('编辑失败', type='error')
        ]

    return dash.no_update


@app.callback(
    [Output('delete-text', 'children'),
     Output('user-delete-confirm-modal', 'visible'),
     Output('delete-ids-store', 'data')],
    [Input('user-delete', 'nClicks'),
     Input('user-list-table', 'nClicksDropdownItem')],
    [State('user-list-table', 'selectedRowKeys'),
     State('user-list-table', 'recentlyClickedDropdownItemTitle'),
     State('user-list-table', 'recentlyDropdownItemClickedRow')],
    prevent_initial_call=True
)
def user_delete_modal(delete_click, dropdown_click,
                      selected_row_keys, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    if delete_click or dropdown_click:
        trigger_id = dash.ctx.triggered_id

        if trigger_id == 'user-delete':
            user_ids = ','.join(selected_row_keys)
        else:
            if recently_clicked_dropdown_item_title == '删除':
                user_ids = recently_dropdown_item_clicked_row['key']
            else:
                return dash.no_update

        return [
            f'是否确认删除user_id为{user_ids}的用户？',
            True,
            {'user_ids': user_ids}
        ]

    return dash.no_update


@app.callback(
    [Output('operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('user-delete-confirm-modal', 'okCounts'),
    State('delete-ids-store', 'data'),
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

    return dash.no_update
