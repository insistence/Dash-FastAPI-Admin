import dash
import time
import uuid
from dash import dcc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from api.dept import get_dept_tree_api
from api.user import get_user_list_api, get_user_detail_api, add_user_api, edit_user_api, delete_user_api, reset_user_password_api, batch_import_user_api, download_user_import_template_api, export_user_list_api
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
    output=dict(
        user_table_data=Output('user-list-table', 'data', allow_duplicate=True),
        user_table_pagination=Output('user-list-table', 'pagination', allow_duplicate=True),
        user_table_key=Output('user-list-table', 'key'),
        user_table_selectedrowkeys=Output('user-list-table', 'selectedRowKeys'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        selected_dept_tree=Input('dept-tree', 'selectedKeys'),
        search_click=Input('user-search', 'nClicks'),
        refresh_click=Input('user-refresh', 'nClicks'),
        pagination=Input('user-list-table', 'pagination'),
        operations=Input('user-operations-store', 'data')
    ),
    state=dict(
        user_name=State('user-user_name-input', 'value'),
        phone_number=State('user-phone_number-input', 'value'),
        status_select=State('user-status-select', 'value'),
        create_time_range=State('user-create_time-range', 'value'),
        button_perms=State('user-button-perms-container', 'data')
    ),
    prevent_initial_call=True
)
def get_user_table_data_by_dept_tree(selected_dept_tree, search_click, refresh_click, pagination, operations,
                                     user_name, phone_number, status_select, create_time_range, button_perms):
    """
    获取用户表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """
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
                    item['status'] = dict(checked=True, disabled=item['user_id'] == 1)
                else:
                    item['status'] = dict(checked=False, disabled=item['user_id'] == 1)
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
                        } if 'system:user:resetPwd' in button_perms else None,
                        {
                            'title': '分配角色',
                            'icon': 'antd-check-circle'
                        } if 'system:user:edit' in button_perms else None
                    ]

            return dict(
                user_table_data=table_data,
                user_table_pagination=table_pagination,
                user_table_key=str(uuid.uuid4()),
                user_table_selectedrowkeys=None,
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            user_table_data=dash.no_update,
            user_table_pagination=dash.no_update,
            user_table_key=dash.no_update,
            user_table_selectedrowkeys=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


# 重置用户搜索表单数据回调
app.clientside_callback(
    '''
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('dept-tree', 'selectedKeys'),
     Output('user-user_name-input', 'value'),
     Output('user-phone_number-input', 'value'),
     Output('user-status-select', 'value'),
     Output('user-create_time-range', 'value'),
     Output('user-operations-store', 'data')],
    Input('user-reset', 'nClicks'),
    prevent_initial_call=True
)


# 隐藏/显示用户搜索表单回调
app.clientside_callback(
    '''
    (hidden_click, hidden_status) => {
        if (hidden_click) {
            return [
                !hidden_status,
                hidden_status ? '隐藏搜索' : '显示搜索'
            ]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('user-search-form-container', 'hidden'),
     Output('user-hidden-tooltip', 'title')],
    Input('user-hidden', 'nClicks'),
    State('user-search-form-container', 'hidden'),
    prevent_initial_call=True
)


@app.callback(
    Output({'type': 'user-operation-button', 'index': 'edit'}, 'disabled'),
    Input('user-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_user_edit_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制编辑按钮状态回调
    """
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1 or '1' in table_rows_selected:
                return True

            return False

        return True

    raise PreventUpdate


@app.callback(
    Output({'type': 'user-operation-button', 'index': 'delete'}, 'disabled'),
    Input('user-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_user_delete_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制删除按钮状态回调
    """
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if '1' in table_rows_selected:
                return True

            return False

        return True

    raise PreventUpdate


@app.callback(
    output=dict(
        modal_visible=Output('user-add-modal', 'visible', allow_duplicate=True),
        dept_tree=Output({'type': 'user_add-form-value', 'index': 'dept_id'}, 'treeData'),
        form_value=Output({'type': 'user_add-form-value', 'index': ALL}, 'value'),
        form_label_validate_status=Output({'type': 'user_add-form-label', 'index': ALL, 'required': True}, 'validateStatus', allow_duplicate=True),
        form_label_validate_info=Output({'type': 'user_add-form-label', 'index': ALL, 'required': True}, 'help', allow_duplicate=True),
        user_post=Output('user-add-post', 'value'),
        user_role=Output('user-add-role', 'value'),
        post_option=Output('user-add-post', 'options'),
        role_option=Output('user-add-role', 'options'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        add_click=Input('user-add', 'nClicks')
    ),
    prevent_initial_call=True
)
def add_user_modal(add_click):
    """
    显示新增用户弹窗回调
    """
    if add_click:
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in dash.ctx.outputs_list[2]]
        # 获取所有输出表单项对应label的index
        form_label_list = [x['id']['index'] for x in dash.ctx.outputs_list[3]]
        dept_params = dict(dept_name='')
        tree_info = get_dept_tree_api(dept_params)
        post_option_info = get_post_select_option_api()
        role_option_info = get_role_select_option_api()
        if tree_info['code'] == 200 and post_option_info['code'] == 200 and role_option_info['code'] == 200:
            tree_data = tree_info['data']
            post_option = post_option_info['data']
            role_option = role_option_info['data']
            user_info = dict(nick_name=None, dept_id=None, phonenumber=None, email=None, user_name=None, password=None, sex=None, status='0', remark=None)

            return dict(
                modal_visible=True,
                dept_tree=tree_data,
                form_value=[user_info.get(k) for k in form_value_list],
                form_label_validate_status=[None] * len(form_label_list),
                form_label_validate_info=[None] * len(form_label_list),
                user_post=None,
                user_role=None,
                post_option=[dict(label=item['post_name'], value=item['post_id']) for item in post_option],
                role_option=[dict(label=item['role_name'], value=item['role_id']) for item in role_option],
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            modal_visible=dash.no_update,
            dept_tree=dash.no_update,
            form_value=[dash.no_update] * len(form_value_list),
            form_label_validate_status=[dash.no_update] * len(form_label_list),
            form_label_validate_info=[dash.no_update] * len(form_label_list),
            user_post=dash.no_update,
            user_role=dash.no_update,
            post_option=dash.no_update,
            role_option=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output({'type': 'user_add-form-label', 'index': ALL, 'required': True}, 'validateStatus', allow_duplicate=True),
        form_label_validate_info=Output({'type': 'user_add-form-label', 'index': ALL, 'required': True}, 'help', allow_duplicate=True),
        modal_visible=Output('user-add-modal', 'visible', allow_duplicate=True),
        operations=Output('user-operations-store', 'data', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        add_confirm=Input('user-add-modal', 'okCounts')
    ),
    state=dict(
        post=State('user-add-post', 'value'),
        role=State('user-add-role', 'value'),
        form_value=State({'type': 'user_add-form-value', 'index': ALL}, 'value'),
        form_label=State({'type': 'user_add-form-label', 'index': ALL, 'required': True}, 'label')
    ),
    prevent_initial_call=True
)
def usr_add_confirm(add_confirm, post, role, form_value, form_label):
    if add_confirm:
        # 获取所有输出表单项对应label的index
        form_label_output_list = [x['id']['index'] for x in dash.ctx.outputs_list[0]]
        # 获取所有输入表单项对应的value及label
        form_value_state = {x['id']['index']: x.get('value') for x in dash.ctx.states_list[-2]}
        form_label_state = {x['id']['index']: x.get('value') for x in dash.ctx.states_list[-1]}

        if all([form_value_state.get(k) for k in form_label_output_list]):
            params = form_value_state
            params['post_id'] = ','.join(map(str, post)) if post else ''
            params['role_id'] = ','.join(map(str, role)) if role else ''
            add_button_result = add_user_api(params)

            if add_button_result['code'] == 200:
                return dict(
                    form_label_validate_status=[None] * len(form_label_output_list),
                    form_label_validate_info=[None] * len(form_label_output_list),
                    modal_visible=False,
                    operations={'type': 'add'},
                    api_check_token_trigger={'timestamp': time.time()},
                    global_message_container=fuc.FefferyFancyMessage('新增成功', type='success')
                )

            return dict(
                form_label_validate_status=[None] * len(form_label_output_list),
                form_label_validate_info=[None] * len(form_label_output_list),
                modal_visible=dash.no_update,
                operations=dash.no_update,
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage('新增失败', type='error')
            )

        return dict(
            form_label_validate_status=[None if form_value_state.get(k) else 'error' for k in form_label_output_list],
            form_label_validate_info=[None if form_value_state.get(k) else f'{form_label_state.get(k)}不能为空!' for k in form_label_output_list],
            modal_visible=dash.no_update,
            operations=dash.no_update,
            api_check_token_trigger=dash.no_update,
            global_message_container=fuc.FefferyFancyMessage('新增失败', type='error')
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        modal_visible=Output('user-edit-modal', 'visible', allow_duplicate=True),
        dept_tree=Output({'type': 'user_edit-form-value', 'index': 'dept_id'}, 'treeData'),
        form_value=Output({'type': 'user_edit-form-value', 'index': ALL}, 'value'),
        form_label_validate_status=Output({'type': 'user_edit-form-label', 'index': ALL, 'required': True}, 'validateStatus', allow_duplicate=True),
        form_label_validate_info=Output({'type': 'user_edit-form-label', 'index': ALL, 'required': True}, 'help', allow_duplicate=True),
        user_post=Output('user-edit-post', 'value'),
        user_role=Output('user-edit-role', 'value'),
        post_option=Output('user-edit-post', 'options'),
        role_option=Output('user-edit-role', 'options'),
        edit_row_info=Output('user-edit-id-store', 'data'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        operation_click=Input({'type': 'user-operation-button', 'index': ALL}, 'nClicks'),
        dropdown_click=Input('user-list-table', 'nClicksDropdownItem')
    ),
    state=dict(
        selected_row_keys=State('user-list-table', 'selectedRowKeys'),
        recently_clicked_dropdown_item_title=State('user-list-table', 'recentlyClickedDropdownItemTitle'),
        recently_dropdown_item_clicked_row=State('user-list-table', 'recentlyDropdownItemClickedRow')
    ),
    prevent_initial_call=True
)
def user_edit_modal(operation_click, dropdown_click,
                    selected_row_keys, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    """
    显示编辑用户弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'edit', 'type': 'user-operation-button'} or (trigger_id == 'user-list-table' and recently_clicked_dropdown_item_title == '修改'):
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in dash.ctx.outputs_list[2]]
        # 获取所有输出表单项对应label的index
        form_label_list = [x['id']['index'] for x in dash.ctx.outputs_list[3]]

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
                raise PreventUpdate

        edit_button_info = get_user_detail_api(user_id)
        if edit_button_info['code'] == 200:
            edit_button_result = edit_button_info['data']
            user = edit_button_result['user']
            role = edit_button_result['role']
            post = edit_button_result['post']

            return dict(
                modal_visible=True,
                dept_tree=tree_data,
                form_value=[user.get(k) for k in form_value_list],
                form_label_validate_status=[None] * len(form_label_list),
                form_label_validate_info=[None] * len(form_label_list),
                user_post=[item['post_id'] for item in post if item] or [],
                user_role=[item['role_id'] for item in role if item] or [],
                post_option=[dict(label=item['post_name'], value=item['post_id']) for item in post_option if item] or [],
                role_option=[dict(label=item['role_name'], value=item['role_id']) for item in role_option if item] or [],
                edit_row_info={'user_id': user_id},
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            modal_visible=dash.no_update,
            dept_tree=dash.no_update,
            form_value=[dash.no_update] * len(form_value_list),
            form_label_validate_status=[dash.no_update] * len(form_label_list),
            form_label_validate_info=[dash.no_update] * len(form_label_list),
            user_post=dash.no_update,
            user_role=dash.no_update,
            post_option=dash.no_update,
            role_option=dash.no_update,
            edit_row_info=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output({'type': 'user_edit-form-label', 'index': ALL, 'required': True}, 'validateStatus', allow_duplicate=True),
        form_label_validate_info=Output({'type': 'user_edit-form-label', 'index': ALL, 'required': True}, 'help', allow_duplicate=True),
        modal_visible=Output('user-edit-modal', 'visible', allow_duplicate=True),
        operations=Output('user-operations-store', 'data', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        edit_confirm=Input('user-edit-modal', 'okCounts')
    ),
    state=dict(
        post=State('user-edit-post', 'value'),
        role=State('user-edit-role', 'value'),
        edit_row_info=State('user-edit-id-store', 'data'),
        form_value=State({'type': 'user_edit-form-value', 'index': ALL}, 'value'),
        form_label=State({'type': 'user_edit-form-label', 'index': ALL, 'required': True}, 'label')
    ),
    prevent_initial_call=True
)
def usr_edit_confirm(edit_confirm, edit_row_info, post, role, form_value, form_label):
    if edit_confirm:
        # 获取所有输出表单项对应label的index
        form_label_output_list = [x['id']['index'] for x in dash.ctx.outputs_list[0]]
        # 获取所有输入表单项对应的value及label
        form_value_state = {x['id']['index']: x.get('value') for x in dash.ctx.states_list[-2]}
        form_label_state = {x['id']['index']: x.get('value') for x in dash.ctx.states_list[-1]}

        if all([form_value_state.get(k) for k in form_label_output_list]):
            params = form_value_state
            params['user_id'] = edit_row_info.get('user_id') if edit_row_info else None
            params['post_id'] = ','.join(map(str, post)) if post else ''
            params['role_id'] = ','.join(map(str, role)) if role else ''
            edit_button_result = edit_user_api(params)

            if edit_button_result['code'] == 200:
                return dict(
                    form_label_validate_status=[None] * len(form_label_output_list),
                    form_label_validate_info=[None] * len(form_label_output_list),
                    modal_visible=False,
                    operations={'type': 'edit'},
                    api_check_token_trigger={'timestamp': time.time()},
                    global_message_container=fuc.FefferyFancyMessage('编辑成功', type='success')
                )

            return dict(
                form_label_validate_status=[None] * len(form_label_output_list),
                form_label_validate_info=[None] * len(form_label_output_list),
                modal_visible=dash.no_update,
                operations=dash.no_update,
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage('编辑失败', type='error')
            )

        return dict(
            form_label_validate_status=[None if form_value_state.get(k) else 'error' for k in form_label_output_list],
            form_label_validate_info=[None if form_value_state.get(k) else f'{form_label_state.get(k)}不能为空!' for k in form_label_output_list],
            modal_visible=dash.no_update,
            operations=dash.no_update,
            api_check_token_trigger=dash.no_update,
            global_message_container=fuc.FefferyFancyMessage('编辑失败', type='error')
        )

    raise PreventUpdate


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
    """
    表格内切换用户状态回调
    """
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
            {'type': 'switch-status'},
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('修改失败', type='error')
        ]

    raise PreventUpdate


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
    """
    显示删除用户二次确认弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'user-operation-button'} or (trigger_id == 'user-list-table' and recently_clicked_dropdown_item_title == '删除'):

        if trigger_id == {'index': 'delete', 'type': 'user-operation-button'}:
            user_ids = ','.join(selected_row_keys)
        else:
            if recently_clicked_dropdown_item_title == '删除':
                user_ids = recently_dropdown_item_clicked_row['key']
            else:
                raise PreventUpdate

        return [
            f'是否确认删除用户编号为{user_ids}的用户？',
            True,
            {'user_ids': user_ids}
        ]

    raise PreventUpdate


@app.callback(
    [Output('user-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('user-delete-confirm-modal', 'okCounts'),
    State('user-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def user_delete_confirm(delete_confirm, user_ids_data):
    """
    删除用户弹窗确认回调，实现删除操作
    """
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

    raise PreventUpdate


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
    """
    显示重置用户密码弹窗回调
    """
    if dropdown_click:
        if recently_clicked_dropdown_item_title == '重置密码':
            user_id = recently_dropdown_item_clicked_row['key']
        else:
            raise PreventUpdate

        return [
            True,
            {'user_id': user_id},
            None
        ]

    raise PreventUpdate


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
    """
    重置用户密码弹窗确认回调，实现重置密码操作
    """
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

    raise PreventUpdate


@app.callback(
    [Output('user_to_allocated_role-modal', 'visible'),
     Output({'type': 'allocate_role-search', 'index': 'allocated'}, 'nClicks'),
     Output('allocate_role-user_id-container', 'data')],
    Input('user-list-table', 'nClicksDropdownItem'),
    [State('user-list-table', 'recentlyClickedDropdownItemTitle'),
     State('user-list-table', 'recentlyDropdownItemClickedRow'),
     State({'type': 'allocate_role-search', 'index': 'allocated'}, 'nClicks')],
    prevent_initial_call=True
)
def role_to_allocated_user_modal(dropdown_click, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row, allocated_role_search_nclick):
    """
    显示用户分配角色弹窗回调
    """
    if dropdown_click and recently_clicked_dropdown_item_title == '分配角色':

        return [
            True,
            allocated_role_search_nclick + 1 if allocated_role_search_nclick else 1,
            recently_dropdown_item_clicked_row['key']
        ]

    raise PreventUpdate


# 显示用户导入弹窗及重置上传弹窗组件状态回调
app.clientside_callback(
    '''
    (nClicks) => {
        if (nClicks) {
            return [
                true, 
                [], 
                [],
                false
            ];
        }
        return [
            false,
            window.dash_clientside.no_update,
            window.dash_clientside.no_update,
            window.dash_clientside.no_update
        ];
    }
    ''',
    [Output('user-import-confirm-modal', 'visible'),
     Output('user-upload-choose', 'listUploadTaskRecord'),
     Output('user-upload-choose', 'defaultFileList'),
     Output('user-import-update-check', 'checked')],
    Input('user-import', 'nClicks'),
    prevent_initial_call=True
)


@app.callback(
    output=dict(
        confirm_loading=Output('user-import-confirm-modal', 'confirmLoading'),
        modal_visible=Output('batch-result-modal', 'visible'),
        batch_result=Output('batch-result-content', 'children'),
        operations=Output('user-operations-store', 'data', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        import_confirm=Input('user-import-confirm-modal', 'okCounts')
    ),
    state=dict(
        list_upload_task_record=State('user-upload-choose', 'listUploadTaskRecord'),
        is_update=State('user-import-update-check', 'checked')
    ),
    prevent_initial_call=True
)
def user_import_confirm(import_confirm, list_upload_task_record, is_update):
    """
    用户导入弹窗确认回调，实现批量导入用户操作
    """
    if import_confirm:
        if list_upload_task_record:
            url = list_upload_task_record[-1].get('url')
            batch_param = dict(url=url, is_update=is_update)
            batch_import_result = batch_import_user_api(batch_param)
            if batch_import_result.get('code') == 200:
                return dict(
                    confirm_loading=False,
                    modal_visible=True if batch_import_result.get('message') else False,
                    batch_result=batch_import_result.get('message'),
                    operations={'type': 'batch-import'},
                    api_check_token_trigger={'timestamp': time.time()},
                    global_message_container=fuc.FefferyFancyMessage('导入成功', type='success')
                )

            return dict(
                confirm_loading=False,
                modal_visible=True,
                batch_result=batch_import_result.get('message'),
                operations=dash.no_update,
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage('导入失败', type='error')
            )
        else:
            return dict(
                confirm_loading=False,
                modal_visible=dash.no_update,
                batch_result=dash.no_update,
                operations=dash.no_update,
                api_check_token_trigger=dash.no_update,
                global_message_container=fuc.FefferyFancyMessage('请上传需要导入的文件', type='error')
            )

    raise PreventUpdate


@app.callback(
    [Output('user-export-container', 'data', allow_duplicate=True),
     Output('user-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    [Input('user-export', 'nClicks'),
     Input('download-user-import-template', 'nClicks')],
    prevent_initial_call=True
)
def export_user_list(export_click, download_click):
    """
    导出用户信息回调
    """
    trigger_id = dash.ctx.triggered_id
    if export_click or download_click:

        if trigger_id == 'user-export':
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

        if trigger_id == 'download-user-import-template':
            download_template_res = download_user_import_template_api()
            if download_template_res.status_code == 200:
                download_template = download_template_res.content

                return [
                    dcc.send_bytes(download_template, f'用户导入模板_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
                    {'timestamp': time.time()},
                    {'timestamp': time.time()},
                    fuc.FefferyFancyMessage('下载成功', type='success')
                ]

            return [
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('下载失败', type='error')
            ]

    raise PreventUpdate


@app.callback(
    Output('user-export-container', 'data', allow_duplicate=True),
    Input('user-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_user_export_status(data):
    """
    导出完成后重置下载组件数据回调，防止重复下载文件
    """
    time.sleep(0.5)
    if data:

        return None

    raise PreventUpdate
