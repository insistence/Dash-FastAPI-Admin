from dash import ctx
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from api.system.user import UserApi
from server import app
from utils.feedback_util import MessageManager


@app.callback(
    Output('user_to_allocated_role-modal', 'visible', allow_duplicate=True),
    [
        Input('allocate_role-submit-button', 'nClicks'),
        Input('allocate_role-back-button', 'nClicks'),
    ],
    [
        State('allocate_role-list-table', 'selectedRowKeys'),
        State('allocate_role-user_id-container', 'data'),
    ],
    prevent_initial_call=True,
)
def allocate_user_add_confirm(
    add_confirm, back_confirm, selected_row_keys, user_id
):
    """
    添加角色确认回调，实现给用户分配角色操作
    """
    trigger_id = ctx.triggered_id
    if trigger_id == 'allocate_role-submit-button':
        params = {
            'user_id': int(user_id),
            'role_ids': ','.join(selected_row_keys)
            if selected_row_keys
            else '',
        }
        UserApi.update_auth_role(params)
        MessageManager.success(content='分配成功')

        return False
    if trigger_id == 'allocate_role-back-button':
        return False

    raise PreventUpdate
