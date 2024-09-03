import dash
import time
import uuid
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from utils.common import validate_data_not_empty
from api.system.dept import DeptApi
from utils.permission_util import PermissionManager
from utils.tree_tool import list_to_tree, list_to_tree_select


@app.callback(
    output=dict(
        dept_table_data=Output('dept-list-table', 'data', allow_duplicate=True),
        dept_table_key=Output('dept-list-table', 'key'),
        dept_table_defaultexpandedrowkeys=Output(
            'dept-list-table', 'defaultExpandedRowKeys'
        ),
        api_check_token_trigger=Output(
            'api-check-token', 'data', allow_duplicate=True
        ),
        fold_click=Output('dept-fold', 'nClicks'),
    ),
    inputs=dict(
        search_click=Input('dept-search', 'nClicks'),
        refresh_click=Input('dept-refresh', 'nClicks'),
        operations=Input('dept-operations-store', 'data'),
        fold_click=Input('dept-fold', 'nClicks'),
    ),
    state=dict(
        dept_name=State('dept-dept_name-input', 'value'),
        status_select=State('dept-status-select', 'value'),
        in_default_expanded_row_keys=State(
            'dept-list-table', 'defaultExpandedRowKeys'
        ),
    ),
    prevent_initial_call=True,
)
def get_dept_table_data(
    search_click,
    refresh_click,
    operations,
    fold_click,
    dept_name,
    status_select,
    in_default_expanded_row_keys,
):
    """
    获取部门表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """
    query_params = dict(dept_name=dept_name, status=status_select)
    if search_click or refresh_click or operations or fold_click:
        table_info = DeptApi.list_dept(query_params)
        default_expanded_row_keys = []
        if table_info['code'] == 200:
            table_data = table_info['data']
            for item in table_data:
                default_expanded_row_keys.append(str(item['dept_id']))
                item['key'] = str(item['dept_id'])
                if item['parent_id'] == 0:
                    item['operation'] = [
                        {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
                        if PermissionManager.check_perms('system:dept:edit')
                        else {},
                        {'content': '新增', 'type': 'link', 'icon': 'antd-plus'}
                        if PermissionManager.check_perms('system:dept:add')
                        else {},
                    ]
                elif item['status'] == '1':
                    item['operation'] = [
                        {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
                        if PermissionManager.check_perms('system:dept:edit')
                        else {},
                        {
                            'content': '删除',
                            'type': 'link',
                            'icon': 'antd-delete',
                        }
                        if PermissionManager.check_perms('system:dept:remove')
                        else {},
                    ]
                else:
                    item['operation'] = [
                        {'content': '修改', 'type': 'link', 'icon': 'antd-edit'}
                        if PermissionManager.check_perms('system:dept:edit')
                        else {},
                        {'content': '新增', 'type': 'link', 'icon': 'antd-plus'}
                        if PermissionManager.check_perms('system:dept:add')
                        else {},
                        {
                            'content': '删除',
                            'type': 'link',
                            'icon': 'antd-delete',
                        }
                        if PermissionManager.check_perms('system:dept:remove')
                        else {},
                    ]
                if item['status'] == '0':
                    item['status'] = dict(tag='正常', color='blue')
                else:
                    item['status'] = dict(tag='停用', color='volcano')
            table_data_new = list_to_tree(table_data, 'dept_id', 'parent_id')

            if fold_click:
                if in_default_expanded_row_keys:
                    return dict(
                        dept_table_data=table_data_new,
                        dept_table_key=str(uuid.uuid4()),
                        dept_table_defaultexpandedrowkeys=[],
                        api_check_token_trigger={'timestamp': time.time()},
                        fold_click=None,
                    )

            return dict(
                dept_table_data=table_data_new,
                dept_table_key=str(uuid.uuid4()),
                dept_table_defaultexpandedrowkeys=default_expanded_row_keys,
                api_check_token_trigger={'timestamp': time.time()},
                fold_click=None,
            )

        return dict(
            dept_table_data=dash.no_update,
            dept_table_key=dash.no_update,
            dept_table_defaultexpandedrowkeys=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()},
            fold_click=None,
        )

    return dict(
        dept_table_data=dash.no_update,
        dept_table_key=dash.no_update,
        dept_table_defaultexpandedrowkeys=dash.no_update,
        api_check_token_trigger=dash.no_update,
        fold_click=None,
    )


# 重置部门搜索表单数据回调
app.clientside_callback(
    """
    (reset_click) => {
        if (reset_click) {
            return [null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    """,
    [
        Output('dept-dept_name-input', 'value'),
        Output('dept-status-select', 'value'),
        Output('dept-operations-store', 'data'),
    ],
    Input('dept-reset', 'nClicks'),
    prevent_initial_call=True,
)

# 隐藏/显示部门搜索表单回调
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
        Output('dept-search-form-container', 'hidden'),
        Output('dept-hidden-tooltip', 'title'),
    ],
    Input('dept-hidden', 'nClicks'),
    State('dept-search-form-container', 'hidden'),
    prevent_initial_call=True,
)


@app.callback(
    output=dict(
        modal_visible=Output('dept-modal', 'visible', allow_duplicate=True),
        modal_title=Output('dept-modal', 'title'),
        parent_id_div_ishidden=Output('dept-parent_id-div', 'hidden'),
        parent_id_tree=Output(
            {'type': 'dept-form-value', 'index': 'parent_id'}, 'treeData'
        ),
        form_value=Output({'type': 'dept-form-value', 'index': ALL}, 'value'),
        form_label_validate_status=Output(
            {'type': 'dept-form-label', 'index': ALL, 'required': True},
            'validateStatus',
            allow_duplicate=True,
        ),
        form_label_validate_info=Output(
            {'type': 'dept-form-label', 'index': ALL, 'required': True},
            'help',
            allow_duplicate=True,
        ),
        api_check_token_trigger=Output(
            'api-check-token', 'data', allow_duplicate=True
        ),
        edit_row_info=Output('dept-edit-id-store', 'data'),
        modal_type=Output('dept-operations-store-bk', 'data'),
    ),
    inputs=dict(
        operation_click=Input(
            {'type': 'dept-operation-button', 'index': ALL}, 'nClicks'
        ),
        button_click=Input('dept-list-table', 'nClicksButton'),
    ),
    state=dict(
        clicked_content=State('dept-list-table', 'clickedContent'),
        recently_button_clicked_row=State(
            'dept-list-table', 'recentlyButtonClickedRow'
        ),
    ),
    prevent_initial_call=True,
)
def add_edit_dept_modal(
    operation_click, button_click, clicked_content, recently_button_clicked_row
):
    """
    显示新增或编辑部门弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'add', 'type': 'dept-operation-button'} or (
        trigger_id == 'dept-list-table' and clicked_content != '删除'
    ):
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in dash.ctx.outputs_list[4]]
        # 获取所有输出表单项对应label的index
        form_label_list = [x['id']['index'] for x in dash.ctx.outputs_list[5]]
        if trigger_id == 'dept-list-table' and clicked_content == '修改':
            tree_info = DeptApi.list_dept_exclude_child(
                dept_id=int(recently_button_clicked_row['key'])
            )
        else:
            dept_params = dict(dept_name='')
            tree_info = DeptApi.list_dept(dept_params)
        if tree_info['code'] == 200:
            tree_data = list_to_tree_select(
                tree_info['data'],
                'dept_name',
                'dept_id',
                'dept_id',
                'parent_id',
            )

            if trigger_id == {
                'index': 'add',
                'type': 'dept-operation-button',
            } or (
                trigger_id == 'dept-list-table' and clicked_content == '新增'
            ):
                dept_info = dict(
                    parent_id=None
                    if trigger_id
                    == {'index': 'add', 'type': 'dept-operation-button'}
                    else str(recently_button_clicked_row['key']),
                    dept_name=None,
                    order_num=None,
                    leader=None,
                    phone=None,
                    email=None,
                    status='0',
                )
                return dict(
                    modal_visible=True,
                    modal_title='新增部门',
                    parent_id_div_ishidden=False,
                    parent_id_tree=tree_data,
                    form_value=[dept_info.get(k) for k in form_value_list],
                    form_label_validate_status=[None] * len(form_label_list),
                    form_label_validate_info=[None] * len(form_label_list),
                    api_check_token_trigger={'timestamp': time.time()},
                    edit_row_info=None,
                    modal_type={'type': 'add'},
                )
            elif trigger_id == 'dept-list-table' and clicked_content == '修改':
                dept_id = int(recently_button_clicked_row['key'])
                dept_info_res = DeptApi.get_dept(dept_id=dept_id)
                if dept_info_res['code'] == 200:
                    dept_info = dept_info_res['data']
                    return dict(
                        modal_visible=True,
                        modal_title='编辑部门',
                        parent_id_div_ishidden=dept_info.get('parent_id') == 0,
                        parent_id_tree=tree_data,
                        form_value=[dept_info.get(k) for k in form_value_list],
                        form_label_validate_status=[None]
                        * len(form_label_list),
                        form_label_validate_info=[None] * len(form_label_list),
                        api_check_token_trigger={'timestamp': time.time()},
                        edit_row_info=dept_info,
                        modal_type={'type': 'edit'},
                    )

        return dict(
            modal_visible=dash.no_update,
            modal_title=dash.no_update,
            parent_id_div_ishidden=dash.no_update,
            parent_id_tree=dash.no_update,
            form_value=[dash.no_update] * len(form_value_list),
            form_label_validate_status=[dash.no_update] * len(form_label_list),
            form_label_validate_info=[dash.no_update] * len(form_label_list),
            api_check_token_trigger={'timestamp': time.time()},
            edit_row_info=None,
            modal_type=None,
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output(
            {'type': 'dept-form-label', 'index': ALL, 'required': True},
            'validateStatus',
            allow_duplicate=True,
        ),
        form_label_validate_info=Output(
            {'type': 'dept-form-label', 'index': ALL, 'required': True},
            'help',
            allow_duplicate=True,
        ),
        modal_visible=Output('dept-modal', 'visible'),
        operations=Output(
            'dept-operations-store', 'data', allow_duplicate=True
        ),
        api_check_token_trigger=Output(
            'api-check-token', 'data', allow_duplicate=True
        ),
        global_message_container=Output(
            'global-message-container', 'children', allow_duplicate=True
        ),
    ),
    inputs=dict(confirm_trigger=Input('dept-modal', 'okCounts')),
    state=dict(
        modal_type=State('dept-operations-store-bk', 'data'),
        edit_row_info=State('dept-edit-id-store', 'data'),
        form_value=State({'type': 'dept-form-value', 'index': ALL}, 'value'),
        form_label=State(
            {'type': 'dept-form-label', 'index': ALL, 'required': True}, 'label'
        ),
    ),
    prevent_initial_call=True,
)
def dept_confirm(
    confirm_trigger, modal_type, edit_row_info, form_value, form_label
):
    """
    新增或编辑部门弹窗确认回调，实现新增或编辑操作
    """
    if confirm_trigger:
        # 获取所有输出表单项对应label的index
        form_label_output_list = [
            x['id']['index'] for x in dash.ctx.outputs_list[0]
        ]
        # 获取所有输入表单项对应的value及label
        form_value_state = {
            x['id']['index']: x.get('value') for x in dash.ctx.states_list[-2]
        }
        form_label_state = {
            x['id']['index']: x.get('value') for x in dash.ctx.states_list[-1]
        }
        if all(
            validate_data_not_empty(item)
            for item in [
                form_value_state.get(k) for k in form_label_output_list
            ]
        ):
            params_add = form_value_state
            params_edit = params_add.copy()
            params_edit['dept_id'] = (
                edit_row_info.get('dept_id') if edit_row_info else None
            )
            api_res = {}
            modal_type = modal_type.get('type')
            if modal_type == 'add':
                api_res = DeptApi.add_dept(params_add)
            if modal_type == 'edit':
                api_res = DeptApi.update_dept(params_edit)
            if api_res.get('code') == 200:
                if modal_type == 'add':
                    return dict(
                        form_label_validate_status=[None]
                        * len(form_label_output_list),
                        form_label_validate_info=[None]
                        * len(form_label_output_list),
                        modal_visible=False,
                        operations={'type': 'add'},
                        api_check_token_trigger={'timestamp': time.time()},
                        global_message_container=fuc.FefferyFancyMessage(
                            '新增成功', type='success'
                        ),
                    )
                if modal_type == 'edit':
                    return dict(
                        form_label_validate_status=[None]
                        * len(form_label_output_list),
                        form_label_validate_info=[None]
                        * len(form_label_output_list),
                        modal_visible=False,
                        operations={'type': 'edit'},
                        api_check_token_trigger={'timestamp': time.time()},
                        global_message_container=fuc.FefferyFancyMessage(
                            '编辑成功', type='success'
                        ),
                    )

            return dict(
                form_label_validate_status=[None] * len(form_label_output_list),
                form_label_validate_info=[None] * len(form_label_output_list),
                modal_visible=dash.no_update,
                operations=dash.no_update,
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage(
                    '处理失败', type='error'
                ),
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
            modal_visible=dash.no_update,
            operations=dash.no_update,
            api_check_token_trigger=dash.no_update,
            global_message_container=fuc.FefferyFancyMessage(
                '处理失败', type='error'
            ),
        )

    raise PreventUpdate


@app.callback(
    [
        Output('dept-delete-text', 'children'),
        Output('dept-delete-confirm-modal', 'visible'),
        Output('dept-delete-ids-store', 'data'),
    ],
    [Input('dept-list-table', 'nClicksButton')],
    [
        State('dept-list-table', 'clickedContent'),
        State('dept-list-table', 'recentlyButtonClickedRow'),
    ],
    prevent_initial_call=True,
)
def dept_delete_modal(
    button_click, clicked_content, recently_button_clicked_row
):
    """
    显示删除部门二次确认弹窗回调
    """
    if button_click:
        if clicked_content == '删除':
            dept_ids = recently_button_clicked_row['key']
        else:
            return dash.no_update

        return [
            f'是否确认删除部门编号为{dept_ids}的部门？',
            True,
            dept_ids,
        ]

    raise PreventUpdate


@app.callback(
    [
        Output('dept-operations-store', 'data', allow_duplicate=True),
        Output('api-check-token', 'data', allow_duplicate=True),
        Output('global-message-container', 'children', allow_duplicate=True),
    ],
    Input('dept-delete-confirm-modal', 'okCounts'),
    State('dept-delete-ids-store', 'data'),
    prevent_initial_call=True,
)
def dept_delete_confirm(delete_confirm, dept_ids_data):
    """
    删除部门弹窗确认回调，实现删除操作
    """
    if delete_confirm:
        params = dept_ids_data
        delete_button_info = DeptApi.del_dept(params)
        if delete_button_info['code'] == 200:
            return [
                {'type': 'delete'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('删除成功', type='success'),
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('删除失败', type='error'),
        ]

    raise PreventUpdate
