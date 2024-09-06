import base64
import time
import uuid
from io import BytesIO
from dash import ctx, dcc, no_update
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from api.system.user import UserApi
from server import app
from utils.common import validate_data_not_empty
from utils.feedback_util import MessageManager
from utils.permission_util import PermissionManager


app.clientside_callback(
    """(dept_input) => dept_input""",
    Output('dept-tree', 'searchKeyword'),
    Input('dept-input-search', 'value'),
    prevent_initial_call=True,
)


@app.callback(
    output=dict(
        user_table_data=Output('user-list-table', 'data', allow_duplicate=True),
        user_table_pagination=Output(
            'user-list-table', 'pagination', allow_duplicate=True
        ),
        user_table_key=Output('user-list-table', 'key'),
        user_table_selectedrowkeys=Output('user-list-table', 'selectedRowKeys'),
    ),
    inputs=dict(
        selected_dept_tree=Input('dept-tree', 'selectedKeys'),
        search_click=Input('user-search', 'nClicks'),
        refresh_click=Input('user-refresh', 'nClicks'),
        pagination=Input('user-list-table', 'pagination'),
        operations=Input('user-operations-store', 'data'),
    ),
    state=dict(
        user_name=State('user-user_name-input', 'value'),
        phone_number=State('user-phone_number-input', 'value'),
        status_select=State('user-status-select', 'value'),
        create_time_range=State('user-create_time-range', 'value'),
    ),
    prevent_initial_call=True,
)
def get_user_table_data_by_dept_tree(
    selected_dept_tree,
    search_click,
    refresh_click,
    pagination,
    operations,
    user_name,
    phone_number,
    status_select,
    create_time_range,
):
    """
    获取用户表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """
    dept_id = None
    begin_time = None
    end_time = None
    if create_time_range:
        begin_time = create_time_range[0]
        end_time = create_time_range[1]
    if selected_dept_tree:
        dept_id = int(selected_dept_tree[0])
    query_params = dict(
        dept_id=dept_id,
        user_name=user_name,
        phonenumber=phone_number,
        status=status_select,
        begin_time=begin_time,
        end_time=end_time,
        page_num=1,
        page_size=10,
    )
    triggered_id = ctx.triggered_id
    if triggered_id == 'user-list-table':
        query_params.update(
            {
                'page_num': pagination['current'],
                'page_size': pagination['pageSize'],
            }
        )
    if (
        selected_dept_tree
        or search_click
        or refresh_click
        or pagination
        or operations
    ):
        table_info = UserApi.list_user(query_params)
        table_data = table_info['rows']
        table_pagination = dict(
            pageSize=table_info['page_size'],
            current=table_info['page_num'],
            showSizeChanger=True,
            pageSizeOptions=[10, 30, 50, 100],
            showQuickJumper=True,
            total=table_info['total'],
        )
        for item in table_data:
            if item['status'] == '0':
                item['status'] = dict(
                    checked=True, disabled=item['user_id'] == 1
                )
            else:
                item['status'] = dict(
                    checked=False, disabled=item['user_id'] == 1
                )
            item['key'] = str(item['user_id'])
            if item['user_id'] == 1:
                item['operation'] = []
            else:
                item['operation'] = [
                    {'title': '修改', 'icon': 'antd-edit'}
                    if PermissionManager.check_perms('system:user:edit')
                    else None,
                    {'title': '删除', 'icon': 'antd-delete'}
                    if PermissionManager.check_perms('system:user:remove')
                    else None,
                    {'title': '重置密码', 'icon': 'antd-key'}
                    if PermissionManager.check_perms('system:user:resetPwd')
                    else None,
                    {'title': '分配角色', 'icon': 'antd-check-circle'}
                    if PermissionManager.check_perms('system:user:edit')
                    else None,
                ]

        return dict(
            user_table_data=table_data,
            user_table_pagination=table_pagination,
            user_table_key=str(uuid.uuid4()),
            user_table_selectedrowkeys=None,
        )

    raise PreventUpdate


# 重置用户搜索表单数据回调
app.clientside_callback(
    """
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    """,
    [
        Output('dept-tree', 'selectedKeys'),
        Output('user-user_name-input', 'value'),
        Output('user-phone_number-input', 'value'),
        Output('user-status-select', 'value'),
        Output('user-create_time-range', 'value'),
        Output('user-operations-store', 'data'),
    ],
    Input('user-reset', 'nClicks'),
    prevent_initial_call=True,
)


# 隐藏/显示用户搜索表单回调
app.clientside_callback(
    """
    (hidden_click, hidden_status) => {
        if (hidden_click) {
            return [
                !hidden_status,
                hidden_status ? '隐藏搜索' : '显示搜索'
            ]
        }
        return window.dash_clientside.no_update;
    }
    """,
    [
        Output('user-search-form-container', 'hidden'),
        Output('user-hidden-tooltip', 'title'),
    ],
    Input('user-hidden', 'nClicks'),
    State('user-search-form-container', 'hidden'),
    prevent_initial_call=True,
)


@app.callback(
    Output({'type': 'user-operation-button', 'index': 'edit'}, 'disabled'),
    Input('user-list-table', 'selectedRowKeys'),
    prevent_initial_call=True,
)
def change_user_edit_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制编辑按钮状态回调
    """
    outputs_list = ctx.outputs_list
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
    prevent_initial_call=True,
)
def change_user_delete_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制删除按钮状态回调
    """
    outputs_list = ctx.outputs_list
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
        dept_tree=Output(
            {'type': 'user_add-form-value', 'index': 'dept_id'}, 'treeData'
        ),
        form_value=Output(
            {'type': 'user_add-form-value', 'index': ALL}, 'value'
        ),
        form_label_validate_status=Output(
            {'type': 'user_add-form-label', 'index': ALL, 'required': True},
            'validateStatus',
            allow_duplicate=True,
        ),
        form_label_validate_info=Output(
            {'type': 'user_add-form-label', 'index': ALL, 'required': True},
            'help',
            allow_duplicate=True,
        ),
        user_post=Output('user-add-post', 'value'),
        user_role=Output('user-add-role', 'value'),
        post_option=Output('user-add-post', 'options'),
        role_option=Output('user-add-role', 'options'),
    ),
    inputs=dict(add_click=Input('user-add', 'nClicks')),
    prevent_initial_call=True,
)
def add_user_modal(add_click):
    """
    显示新增用户弹窗回调
    """
    if add_click:
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in ctx.outputs_list[2]]
        # 获取所有输出表单项对应label的index
        form_label_list = [x['id']['index'] for x in ctx.outputs_list[3]]
        tree_info = UserApi.dept_tree_select()
        detail_info = UserApi.get_user(user_id='')
        tree_data = tree_info['data']
        post_option = detail_info['posts']
        role_option = detail_info['roles']
        user_info = dict(
            nick_name=None,
            dept_id=None,
            phonenumber=None,
            email=None,
            user_name=None,
            password=None,
            sex=None,
            status='0',
            remark=None,
        )

        return dict(
            modal_visible=True,
            dept_tree=tree_data,
            form_value=[user_info.get(k) for k in form_value_list],
            form_label_validate_status=[None] * len(form_label_list),
            form_label_validate_info=[None] * len(form_label_list),
            user_post=None,
            user_role=None,
            post_option=[
                dict(label=item['post_name'], value=item['post_id'])
                for item in post_option
            ],
            role_option=[
                dict(label=item['role_name'], value=item['role_id'])
                for item in role_option
            ],
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output(
            {'type': 'user_add-form-label', 'index': ALL, 'required': True},
            'validateStatus',
            allow_duplicate=True,
        ),
        form_label_validate_info=Output(
            {'type': 'user_add-form-label', 'index': ALL, 'required': True},
            'help',
            allow_duplicate=True,
        ),
        modal_visible=Output('user-add-modal', 'visible', allow_duplicate=True),
        operations=Output(
            'user-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(add_confirm=Input('user-add-modal', 'okCounts')),
    state=dict(
        post=State('user-add-post', 'value'),
        role=State('user-add-role', 'value'),
        form_value=State(
            {'type': 'user_add-form-value', 'index': ALL}, 'value'
        ),
        form_label=State(
            {'type': 'user_add-form-label', 'index': ALL, 'required': True},
            'label',
        ),
    ),
    prevent_initial_call=True,
)
def usr_add_confirm(add_confirm, post, role, form_value, form_label):
    if add_confirm:
        # 获取所有输出表单项对应label的index
        form_label_output_list = [x['id']['index'] for x in ctx.outputs_list[0]]
        # 获取所有输入表单项对应的value及label
        form_value_state = {
            x['id']['index']: x.get('value') for x in ctx.states_list[-2]
        }
        form_label_state = {
            x['id']['index']: x.get('value') for x in ctx.states_list[-1]
        }

        if all(
            validate_data_not_empty(item)
            for item in [
                form_value_state.get(k) for k in form_label_output_list
            ]
        ):
            params = form_value_state
            params['post_ids'] = post if post else ''
            params['role_ids'] = role if role else ''
            UserApi.add_user(params)
            MessageManager.success(content='新增成功')

            return dict(
                form_label_validate_status=[None] * len(form_label_output_list),
                form_label_validate_info=[None] * len(form_label_output_list),
                modal_visible=False,
                operations={'type': 'add'},
            )

        return dict(
            form_label_validate_status=[
                None
                if validate_data_not_empty(form_value_state.get(k))
                else 'error'
                for k in form_label_output_list
            ],
            form_label_validate_info=[
                None
                if validate_data_not_empty(form_value_state.get(k))
                else f'{form_label_state.get(k)}不能为空!'
                for k in form_label_output_list
            ],
            modal_visible=no_update,
            operations=no_update,
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        modal_visible=Output(
            'user-edit-modal', 'visible', allow_duplicate=True
        ),
        dept_tree=Output(
            {'type': 'user_edit-form-value', 'index': 'dept_id'}, 'treeData'
        ),
        form_value=Output(
            {'type': 'user_edit-form-value', 'index': ALL}, 'value'
        ),
        form_label_validate_status=Output(
            {'type': 'user_edit-form-label', 'index': ALL, 'required': True},
            'validateStatus',
            allow_duplicate=True,
        ),
        form_label_validate_info=Output(
            {'type': 'user_edit-form-label', 'index': ALL, 'required': True},
            'help',
            allow_duplicate=True,
        ),
        user_post=Output('user-edit-post', 'value'),
        user_role=Output('user-edit-role', 'value'),
        post_option=Output('user-edit-post', 'options'),
        role_option=Output('user-edit-role', 'options'),
        edit_row_info=Output('user-edit-id-store', 'data'),
    ),
    inputs=dict(
        operation_click=Input(
            {'type': 'user-operation-button', 'index': ALL}, 'nClicks'
        ),
        dropdown_click=Input('user-list-table', 'nClicksDropdownItem'),
    ),
    state=dict(
        selected_row_keys=State('user-list-table', 'selectedRowKeys'),
        recently_clicked_dropdown_item_title=State(
            'user-list-table', 'recentlyClickedDropdownItemTitle'
        ),
        recently_dropdown_item_clicked_row=State(
            'user-list-table', 'recentlyDropdownItemClickedRow'
        ),
    ),
    prevent_initial_call=True,
)
def user_edit_modal(
    operation_click,
    dropdown_click,
    selected_row_keys,
    recently_clicked_dropdown_item_title,
    recently_dropdown_item_clicked_row,
):
    """
    显示编辑用户弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id == {'index': 'edit', 'type': 'user-operation-button'} or (
        trigger_id == 'user-list-table'
        and recently_clicked_dropdown_item_title == '修改'
    ):
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in ctx.outputs_list[2]]
        # 获取所有输出表单项对应label的index
        form_label_list = [x['id']['index'] for x in ctx.outputs_list[3]]

        tree_data = UserApi.dept_tree_select()['data']

        if trigger_id == {'index': 'edit', 'type': 'user-operation-button'}:
            user_id = int(selected_row_keys[0])
        else:
            if recently_clicked_dropdown_item_title == '修改':
                user_id = int(recently_dropdown_item_clicked_row['key'])
            else:
                raise PreventUpdate

        edit_button_info = UserApi.get_user(user_id)
        edit_button_result = edit_button_info['data']
        post_option = edit_button_info['posts']
        role_option = edit_button_info['roles']
        role_ids = edit_button_result['role_ids']
        post_ids = edit_button_result['post_ids']

        return dict(
            modal_visible=True,
            dept_tree=tree_data,
            form_value=[edit_button_result.get(k) for k in form_value_list],
            form_label_validate_status=[None] * len(form_label_list),
            form_label_validate_info=[None] * len(form_label_list),
            user_post=[int(item) for item in post_ids.split(',')]
            if post_ids
            else [],
            user_role=[int(item) for item in role_ids.split(',')]
            if role_ids
            else [],
            post_option=[
                dict(label=item['post_name'], value=item['post_id'])
                for item in post_option
                if item
            ]
            or [],
            role_option=[
                dict(label=item['role_name'], value=item['role_id'])
                for item in role_option
                if item
            ]
            or [],
            edit_row_info={'user_id': user_id},
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output(
            {'type': 'user_edit-form-label', 'index': ALL, 'required': True},
            'validateStatus',
            allow_duplicate=True,
        ),
        form_label_validate_info=Output(
            {'type': 'user_edit-form-label', 'index': ALL, 'required': True},
            'help',
            allow_duplicate=True,
        ),
        modal_visible=Output(
            'user-edit-modal', 'visible', allow_duplicate=True
        ),
        operations=Output(
            'user-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(edit_confirm=Input('user-edit-modal', 'okCounts')),
    state=dict(
        post=State('user-edit-post', 'value'),
        role=State('user-edit-role', 'value'),
        edit_row_info=State('user-edit-id-store', 'data'),
        form_value=State(
            {'type': 'user_edit-form-value', 'index': ALL}, 'value'
        ),
        form_label=State(
            {'type': 'user_edit-form-label', 'index': ALL, 'required': True},
            'label',
        ),
    ),
    prevent_initial_call=True,
)
def usr_edit_confirm(
    edit_confirm, edit_row_info, post, role, form_value, form_label
):
    if edit_confirm:
        # 获取所有输出表单项对应label的index
        form_label_output_list = [x['id']['index'] for x in ctx.outputs_list[0]]
        # 获取所有输入表单项对应的value及label
        form_value_state = {
            x['id']['index']: x.get('value') for x in ctx.states_list[-2]
        }
        form_label_state = {
            x['id']['index']: x.get('value') for x in ctx.states_list[-1]
        }

        if all(
            validate_data_not_empty(item)
            for item in [
                form_value_state.get(k) for k in form_label_output_list
            ]
        ):
            params = form_value_state
            params['user_id'] = (
                edit_row_info.get('user_id') if edit_row_info else None
            )
            params['post_ids'] = ','.join(map(str, post)) if post else ''
            params['role_ids'] = ','.join(map(str, role)) if role else ''
            UserApi.update_user(params)
            MessageManager.success(content='编辑成功')

            return dict(
                form_label_validate_status=[None] * len(form_label_output_list),
                form_label_validate_info=[None] * len(form_label_output_list),
                modal_visible=False,
                operations={'type': 'edit'},
            )

        return dict(
            form_label_validate_status=[
                None
                if validate_data_not_empty(form_value_state.get(k))
                else 'error'
                for k in form_label_output_list
            ],
            form_label_validate_info=[
                None
                if validate_data_not_empty(form_value_state.get(k))
                else f'{form_label_state.get(k)}不能为空!'
                for k in form_label_output_list
            ],
            modal_visible=no_update,
            operations=no_update,
        )

    raise PreventUpdate


@app.callback(
    Output('user-operations-store', 'data', allow_duplicate=True),
    [
        Input('user-list-table', 'recentlySwitchDataIndex'),
        Input('user-list-table', 'recentlySwitchStatus'),
        Input('user-list-table', 'recentlySwitchRow'),
    ],
    prevent_initial_call=True,
)
def table_switch_user_status(
    recently_switch_data_index, recently_switch_status, recently_switch_row
):
    """
    表格内切换用户状态回调
    """
    if recently_switch_data_index:
        UserApi.change_user_status(
            user_id=int(recently_switch_row['key']),
            status='0' if recently_switch_status else '1',
        )
        MessageManager.success(content='修改成功')

        return {'type': 'switch-status'}

    raise PreventUpdate


@app.callback(
    [
        Output('user-delete-text', 'children'),
        Output('user-delete-confirm-modal', 'visible'),
        Output('user-delete-ids-store', 'data'),
    ],
    [
        Input({'type': 'user-operation-button', 'index': ALL}, 'nClicks'),
        Input('user-list-table', 'nClicksDropdownItem'),
    ],
    [
        State('user-list-table', 'selectedRowKeys'),
        State('user-list-table', 'recentlyClickedDropdownItemTitle'),
        State('user-list-table', 'recentlyDropdownItemClickedRow'),
    ],
    prevent_initial_call=True,
)
def user_delete_modal(
    operation_click,
    dropdown_click,
    selected_row_keys,
    recently_clicked_dropdown_item_title,
    recently_dropdown_item_clicked_row,
):
    """
    显示删除用户二次确认弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'user-operation-button'} or (
        trigger_id == 'user-list-table'
        and recently_clicked_dropdown_item_title == '删除'
    ):
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
            user_ids,
        ]

    raise PreventUpdate


@app.callback(
    Output('user-operations-store', 'data', allow_duplicate=True),
    Input('user-delete-confirm-modal', 'okCounts'),
    State('user-delete-ids-store', 'data'),
    prevent_initial_call=True,
)
def user_delete_confirm(delete_confirm, user_ids_data):
    """
    删除用户弹窗确认回调，实现删除操作
    """
    if delete_confirm:
        params = user_ids_data
        UserApi.del_user(params)
        MessageManager.success(content='删除成功')

        return {'type': 'delete'}

    raise PreventUpdate


@app.callback(
    [
        Output('user-reset-password-confirm-modal', 'visible'),
        Output('reset-password-row-key-store', 'data'),
        Output('reset-password-input', 'value'),
    ],
    Input('user-list-table', 'nClicksDropdownItem'),
    [
        State('user-list-table', 'recentlyClickedDropdownItemTitle'),
        State('user-list-table', 'recentlyDropdownItemClickedRow'),
    ],
    prevent_initial_call=True,
)
def user_reset_password_modal(
    dropdown_click,
    recently_clicked_dropdown_item_title,
    recently_dropdown_item_clicked_row,
):
    """
    显示重置用户密码弹窗回调
    """
    if dropdown_click:
        if recently_clicked_dropdown_item_title == '重置密码':
            user_id = recently_dropdown_item_clicked_row['key']
        else:
            raise PreventUpdate

        return [True, user_id, None]

    raise PreventUpdate


@app.callback(
    Output('user-operations-store', 'data', allow_duplicate=True),
    Input('user-reset-password-confirm-modal', 'okCounts'),
    [
        State('reset-password-row-key-store', 'data'),
        State('reset-password-input', 'value'),
    ],
    prevent_initial_call=True,
)
def user_reset_password_confirm(reset_confirm, user_id_data, reset_password):
    """
    重置用户密码弹窗确认回调，实现重置密码操作
    """
    if reset_confirm:
        UserApi.reset_user_pwd(user_id=int(user_id_data), password=reset_password)
        MessageManager.success(content='重置成功')

        return {'type': 'reset-password'}

    raise PreventUpdate


@app.callback(
    [
        Output('user_to_allocated_role-modal', 'visible'),
        Output(
            {'type': 'allocate_role-search', 'index': 'allocated'}, 'nClicks'
        ),
        Output('allocate_role-user_id-container', 'data'),
    ],
    Input('user-list-table', 'nClicksDropdownItem'),
    [
        State('user-list-table', 'recentlyClickedDropdownItemTitle'),
        State('user-list-table', 'recentlyDropdownItemClickedRow'),
        State(
            {'type': 'allocate_role-search', 'index': 'allocated'}, 'nClicks'
        ),
    ],
    prevent_initial_call=True,
)
def role_to_allocated_user_modal(
    dropdown_click,
    recently_clicked_dropdown_item_title,
    recently_dropdown_item_clicked_row,
    allocated_role_search_nclick,
):
    """
    显示用户分配角色弹窗回调
    """
    if dropdown_click and recently_clicked_dropdown_item_title == '分配角色':
        return [
            True,
            allocated_role_search_nclick + 1
            if allocated_role_search_nclick
            else 1,
            recently_dropdown_item_clicked_row['key'],
        ]

    raise PreventUpdate


# 显示用户导入弹窗及重置上传弹窗组件状态回调
app.clientside_callback(
    """
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
    """,
    [
        Output('user-import-confirm-modal', 'visible'),
        Output('user-upload-choose', 'listUploadTaskRecord'),
        Output('user-upload-choose', 'defaultFileList'),
        Output('user-import-update-check', 'checked'),
    ],
    Input('user-import', 'nClicks'),
    prevent_initial_call=True,
)


@app.callback(
    output=dict(
        confirm_loading=Output('user-import-confirm-modal', 'confirmLoading'),
        modal_visible=Output('batch-result-modal', 'visible'),
        batch_result=Output('batch-result-content', 'children'),
        operations=Output(
            'user-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(import_confirm=Input('user-import-confirm-modal', 'okCounts')),
    state=dict(
        contents=State('user-upload-choose', 'contents'),
        is_update=State('user-import-update-check', 'checked'),
    ),
    prevent_initial_call=True,
)
def user_import_confirm(import_confirm, contents, is_update):
    """
    用户导入弹窗确认回调，实现批量导入用户操作
    """
    if import_confirm:
        if contents:
            # url = list_upload_task_record[-1].get('url')
            # batch_param = dict(url=url, is_update=is_update)
            batch_import_result = UserApi.import_user(
                file=BytesIO(base64.b64decode(contents.split(',', 1)[1])),
                update_support=is_update,
            )
            MessageManager.success(content='导入成功')

            return dict(
                confirm_loading=False,
                modal_visible=True if batch_import_result.get('msg') else False,
                batch_result=batch_import_result.get('msg'),
                operations={'type': 'batch-import'},
            )
        else:
            MessageManager.warning(content='请上传需要导入的文件')

            return dict(
                confirm_loading=False,
                modal_visible=no_update,
                batch_result=no_update,
                operations=no_update,
            )

    raise PreventUpdate


@app.callback(
    [
        Output('user-export-container', 'data', allow_duplicate=True),
        Output('user-export-complete-judge-container', 'data'),
    ],
    [
        Input('user-export', 'nClicks'),
        Input('download-user-import-template', 'nClicks'),
    ],
    prevent_initial_call=True,
)
def export_user_list(export_click, download_click):
    """
    导出用户信息回调
    """
    trigger_id = ctx.triggered_id
    if export_click or download_click:
        if trigger_id == 'user-export':
            export_user_res = UserApi.export_user({})
            MessageManager.success(content='导出成功')

            export_user = export_user_res.content

            return [
                dcc.send_bytes(
                    export_user,
                    f'用户信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx',
                ),
                {'timestamp': time.time()},
            ]

        if trigger_id == 'download-user-import-template':
            download_template_res = UserApi.download_template()
            download_template = download_template_res.content
            MessageManager.success(content='下载成功')

            return [
                dcc.send_bytes(
                    download_template,
                    f'用户导入模板_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx',
                ),
                {'timestamp': time.time()},
            ]

    raise PreventUpdate


@app.callback(
    Output('user-export-container', 'data', allow_duplicate=True),
    Input('user-export-complete-judge-container', 'data'),
    prevent_initial_call=True,
)
def reset_user_export_status(data):
    """
    导出完成后重置下载组件数据回调，防止重复下载文件
    """
    time.sleep(0.5)
    if data:
        return None

    raise PreventUpdate
