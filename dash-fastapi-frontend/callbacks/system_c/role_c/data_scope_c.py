import uuid
from dash import ctx, no_update
from dash.dependencies import ALL, Input, Output, State
from dash.exceptions import PreventUpdate
from api.system.role import RoleApi
from server import app
from utils.feedback_util import MessageManager
from utils.tree_util import TreeUtil


@app.callback(
    Output('role-dept-perms', 'expandedKeys'),
    Input('role-dept-perms-radio-fold-unfold', 'checked'),
    State('role-dept-perms', 'treeData'),
    prevent_initial_call=True,
)
def fold_unfold_role_dept(fold_unfold, dept_tree):
    """
    数据权限表单中展开/折叠checkbox回调
    """
    if dept_tree and fold_unfold is not None:
        expanded_keys = [
            dept.get('key') for dept in dept_tree[0].get('children')
        ]
        expanded_keys.append(dept_tree[0].get('key'))
        if fold_unfold:
            return expanded_keys
        else:
            return []

    return no_update


@app.callback(
    Output('role-dept-perms', 'checkedKeys', allow_duplicate=True),
    Input('role-dept-perms-radio-all-none', 'checked'),
    State('role-dept-perms', 'treeData'),
    prevent_initial_call=True,
)
def all_none_role_dept_mode(all_none, dept_tree):
    """
    数据权限表单中全选/全不选checkbox回调
    """
    if dept_tree and all_none is not None:
        if all_none:
            all_keys = TreeUtil.find_tree_all_keys(dept_tree, [])
            return all_keys
        else:
            return []

    return no_update


@app.callback(
    [
        Output('role-dept-perms', 'checkStrictly'),
        Output('role-dept-perms', 'keys', allow_duplicate=True),
    ],
    Input('role-dept-perms-radio-parent-children', 'checked'),
    prevent_initial_call=True,
)
def change_role_dept_mode(parent_children):
    """
    数据权限表单中父子联动checkbox回调
    """
    return [not parent_children, str(uuid.uuid4())]


@app.callback(
    output=dict(
        dept_div=Output('role-dept-perms-div', 'hidden'),
        dept_perms_tree=Output('role-dept-perms', 'treeData'),
        dept_perms_expanded_check=Output(
            'role-dept-perms-radio-fold-unfold', 'checked'
        ),
        dept_perms_checkedkeys=Output(
            'role-dept-perms', 'checkedKeys', allow_duplicate=True
        ),
        radio_parent_children=Output(
            'role-dept-perms-radio-parent-children', 'checked'
        ),
    ),
    inputs=dict(
        data_scope=Input(
            {'type': 'datascope-form-value', 'index': 'data_scope'}, 'value'
        ),
    ),
    state=dict(role_info=State('role-edit-id-store', 'data')),
    prevent_initial_call=True,
)
def get_role_dept_info(data_scope, role_info):
    if data_scope == '2':
        tree_info = RoleApi.dept_tree_select(
            role_id=int(role_info.get('role_id'))
        )
        tree_data = tree_info['depts']
        checked_keys = [str(item) for item in tree_info['checked_keys']]

        return dict(
            dept_div=False,
            dept_perms_tree=tree_data,
            dept_perms_expanded_check=True,
            dept_perms_checkedkeys=checked_keys,
            radio_parent_children=role_info.get('dept_check_strictly'),
        )

    return dict(
        dept_div=True,
        dept_perms_tree=no_update,
        dept_perms_expanded_check=no_update,
        dept_perms_checkedkeys=no_update,
        radio_parent_children=no_update,
    )


@app.callback(
    output=dict(
        modal_visible=Output(
            'role-datascope-modal', 'visible', allow_duplicate=True
        ),
        form_value=Output(
            {'type': 'datascope-form-value', 'index': ALL}, 'value'
        ),
        edit_row_info=Output(
            'role-edit-id-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(
        button_click=Input(
            {'type': 'role-operation-table', 'operation': ALL, 'index': ALL},
            'nClicks',
        )
    ),
    prevent_initial_call=True,
)
def edit_role_datascope_modal(button_click):
    """
    显示角色数据权限弹窗回调
    """
    trigger_id = ctx.triggered_id
    if trigger_id.operation == 'datascope':
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in ctx.outputs_list[1]]
        role_id = int(trigger_id.index)
        role_info_res = RoleApi.get_role(role_id=role_id)
        role_info = role_info_res['data']

        return dict(
            modal_visible=True,
            form_value=[role_info.get(k) for k in form_value_list],
            edit_row_info=role_info,
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        modal_visible=Output('role-datascope-modal', 'visible'),
        operations=Output(
            'role-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(confirm_trigger=Input('role-datascope-modal', 'okCounts')),
    state=dict(
        edit_row_info=State('role-edit-id-store', 'data'),
        form_value=State(
            {'type': 'datascope-form-value', 'index': ALL}, 'value'
        ),
        dept_checked_keys=State('role-dept-perms', 'checkedKeys'),
        dept_half_checked_keys=State('role-dept-perms', 'halfCheckedKeys'),
        parent_checked=State(
            'role-dept-perms-radio-parent-children', 'checked'
        ),
    ),
    running=[[Output('role-datascope-modal', 'confirmLoading'), True, False]],
    prevent_initial_call=True,
)
def role_datascope_confirm(
    confirm_trigger,
    edit_row_info,
    form_value,
    dept_checked_keys,
    dept_half_checked_keys,
    parent_checked,
):
    """
    角色数据权限弹窗确认回调，实现分配数据权限的操作
    """
    if confirm_trigger:
        # 获取所有输入表单项对应的value
        form_value_state = {
            x['id']['index']: x.get('value') for x in ctx.states_list[1]
        }
        dept_half_checked_keys = (
            dept_half_checked_keys if dept_half_checked_keys else []
        )
        dept_checked_keys = dept_checked_keys if dept_checked_keys else []
        if parent_checked:
            dept_perms = dept_half_checked_keys + dept_checked_keys
        else:
            dept_perms = dept_checked_keys
        params_datascope = form_value_state
        params_datascope['dept_ids'] = (
            [int(item) for item in dept_perms] if dept_perms else []
        )
        params_datascope['dept_check_strictly'] = parent_checked
        params_datascope['role_id'] = (
            edit_row_info.get('role_id') if edit_row_info else None
        )
        RoleApi.data_scope(params_datascope)
        MessageManager.success(content='分配成功')

        return dict(
            modal_visible=False,
            operations={'type': 'datascope'},
        )

    raise PreventUpdate
