import dash
import time
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from api.role import get_role_detail_api, role_datascope_api
from api.dept import get_dept_tree_api, get_dept_list_api


@app.callback(
    Output('role-dept-perms', 'expandedKeys'),
    Input('role-dept-perms-radio-fold-unfold', 'checked'),
    State('role-dept-store', 'data'),
    prevent_initial_call=True
)
def fold_unfold_role_dept(fold_unfold, dept_info):
    """
    数据权限表单中展开/折叠checkbox回调
    """
    if dept_info:
        default_expanded_keys = []
        for item in dept_info:
            if fold_unfold:
                default_expanded_keys.append(str(item.get('dept_id')))
            else:
                if item.get('parent_id') == 0:
                    default_expanded_keys.append(str(item.get('dept_id')))

        return default_expanded_keys

    return dash.no_update


@app.callback(
    Output('role-dept-perms', 'checkedKeys', allow_duplicate=True),
    Input('role-dept-perms-radio-all-none', 'checked'),
    State('role-dept-store', 'data'),
    prevent_initial_call=True
)
def all_none_role_dept_mode(all_none, dept_info):
    """
    数据权限表单中全选/全不选checkbox回调
    """
    if dept_info:
        default_expanded_keys = []
        for item in dept_info:
            if item.get('parent_id') == 0:
                default_expanded_keys.append(str(item.get('dept_id')))

        if all_none:
            return [str(item.get('dept_id')) for item in dept_info]
        else:
            return []

    return dash.no_update


@app.callback(
    [Output('role-dept-perms', 'checkStrictly'),
     Output('role-dept-perms', 'checkedKeys', allow_duplicate=True)],
    Input('role-dept-perms-radio-parent-children', 'checked'),
    State('current-role-dept-store', 'data'),
    prevent_initial_call=True
)
def change_role_dept_mode(parent_children, current_role_dept):
    """
    数据权限表单中父子联动checkbox回调
    """
    checked_dept = []
    if parent_children:
        if current_role_dept:
            for item in current_role_dept:
                has_children = False
                for other_item in current_role_dept:
                    if other_item['parent_id'] == item['dept_id']:
                        has_children = True
                        break
                if not has_children:
                    checked_dept.append(str(item.get('dept_id')))
        return [False, checked_dept]
    else:
        if current_role_dept:
            checked_dept = [str(item.get('dept_id')) for item in current_role_dept if item] or []
        return [True, checked_dept]


@app.callback(
    output=dict(
        dept_div=Output('role-dept-perms-div', 'hidden'),
        dept_perms_tree=Output('role-dept-perms', 'treeData'),
        dept_perms_expanded_check=Output('role-dept-perms-radio-fold-unfold', 'checked'),
        dept_perms_checkedkeys=Output('role-dept-perms', 'checkedKeys', allow_duplicate=True),
        dept_perms_halfcheckedkeys=Output('role-dept-perms', 'halfCheckedKeys', allow_duplicate=True),
        role_dept=Output('role-dept-store', 'data'),
        current_role_dept=Output('current-role-dept-store', 'data')
    ),
    inputs=dict(
        data_scope=Input({'type': 'datascope-form-value', 'index': 'data_scope'}, 'value'),
    ),
    state=dict(
        role_info=State('role-edit-id-store', 'data')
    ),
    prevent_initial_call=True
)
def get_role_dept_info(data_scope, role_info):
    if data_scope == '2':
        tree_info = get_dept_tree_api({})
        dept_list_info = get_dept_list_api({})
        if tree_info.get('code') == 200 and dept_list_info.get('code') == 200:
            tree_data = tree_info['data']
            dept_list = [item for item in dept_list_info['data']['rows'] if item.get('status') == '0']
            checked_dept = []
            checked_dept_all = []
            if role_info.get('dept')[0]:
                for item in role_info.get('dept'):
                    checked_dept_all.append(str(item.get('dept_id')))
                    has_children = False
                    for other_item in role_info.get('dept'):
                        if other_item['parent_id'] == item['dept_id']:
                            has_children = True
                            break
                    if not has_children:
                        checked_dept.append(str(item.get('dept_id')))
            half_checked_dept = [x for x in checked_dept_all if x not in checked_dept]

            return dict(
                dept_div=False,
                dept_perms_tree=tree_data,
                dept_perms_expanded_check=True,
                dept_perms_checkedkeys=checked_dept,
                dept_perms_halfcheckedkeys=half_checked_dept,
                role_dept=dept_list,
                current_role_dept=role_info.get('dept')
            )

        return dict(
            dept_div=False,
            dept_perms_tree=dash.no_update,
            dept_perms_expanded_check=dash.no_update,
            dept_perms_checkedkeys=dash.no_update,
            dept_perms_halfcheckedkeys=dash.no_update,
            role_dept=dash.no_update,
            current_role_dept=dash.no_update
        )

    return dict(
        dept_div=True,
        dept_perms_tree=dash.no_update,
        dept_perms_expanded_check=dash.no_update,
        dept_perms_checkedkeys=dash.no_update,
        dept_perms_halfcheckedkeys=dash.no_update,
        role_dept=dash.no_update,
        current_role_dept=dash.no_update
    )


@app.callback(
    output=dict(
        modal_visible=Output('role-datascope-modal', 'visible', allow_duplicate=True),
        form_value=Output({'type': 'datascope-form-value', 'index': ALL}, 'value'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        edit_row_info=Output('role-edit-id-store', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        button_click=Input({'type': 'role-operation-table', 'operation': ALL, 'index': ALL}, 'nClicks')
    ),
    prevent_initial_call=True
)
def edit_role_datascope_modal(button_click):
    """
    显示角色数据权限弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id.operation == 'datascope':
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in dash.ctx.outputs_list[1]]
        role_id = int(trigger_id.index)
        role_info_res = get_role_detail_api(role_id=role_id)
        if role_info_res['code'] == 200:
            role_info = role_info_res['data']
            return dict(
                modal_visible=True,
                form_value=[role_info.get('role').get(k) for k in form_value_list],
                api_check_token_trigger={'timestamp': time.time()},
                edit_row_info=role_info
            )

        return dict(
            modal_visible=dash.no_update,
            form_value=[dash.no_update] * len(form_value_list),
            api_check_token_trigger={'timestamp': time.time()},
            edit_row_info=None
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        modal_visible=Output('role-datascope-modal', 'visible'),
        operations=Output('role-operations-store', 'data', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        confirm_trigger=Input('role-datascope-modal', 'okCounts')
    ),
    state=dict(
        edit_row_info=State('role-edit-id-store', 'data'),
        form_value=State({'type': 'datascope-form-value', 'index': ALL}, 'value'),
        dept_checked_keys=State('role-dept-perms', 'checkedKeys'),
        dept_half_checked_keys=State('role-dept-perms', 'halfCheckedKeys'),
        parent_checked=State('role-dept-perms-radio-parent-children', 'checked')
    ),
    prevent_initial_call=True
)
def role_datascope_confirm(confirm_trigger, edit_row_info, form_value, dept_checked_keys, dept_half_checked_keys, parent_checked):
    """
    角色数据权限弹窗确认回调，实现分配数据权限的操作
    """
    if confirm_trigger:
        # 获取所有输入表单项对应的value
        form_value_state = {x['id']['index']: x.get('value') for x in dash.ctx.states_list[1]}
        dept_half_checked_keys = dept_half_checked_keys if dept_half_checked_keys else []
        dept_checked_keys = dept_checked_keys if dept_checked_keys else []
        if parent_checked:
            dept_perms = dept_half_checked_keys + dept_checked_keys
        else:
            dept_perms = dept_checked_keys
        params_datascope = form_value_state
        params_datascope['dept_id'] = ','.join(dept_perms) if dept_perms else None
        params_datascope['role_id'] = edit_row_info.get('role').get('role_id') if edit_row_info else None
        api_res = role_datascope_api(params_datascope)
        if api_res.get('code') == 200:
            return dict(
                modal_visible=False,
                operations={'type': 'datascope'},
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage('分配成功', type='success')
            )

        return dict(
            modal_visible=dash.no_update,
            operations=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()},
            global_message_container=fuc.FefferyFancyMessage('分配失败', type='error')
        )

    raise PreventUpdate
