from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from api.system.user import UserApi
from server import app
from utils.feedback_util import MessageManager


@app.callback(
    Output('user_to_allocated_role-modal', 'visible', allow_duplicate=True),
    Input('allocate_role-submit-button', 'nClicks'),
    [
        State('allocate_role-list-table', 'selectedRowKeys'),
        State('allocate_role-user_id-container', 'data'),
    ],
    running=[[Output('allocate_role-submit-button', 'loading'), True, False]],
    prevent_initial_call=True,
)
def allocate_user_add_confirm(add_confirm, selected_row_keys, user_id):
    """
    添加角色确认回调，实现给用户分配角色操作
    """
    if add_confirm:
        params = {
            'user_id': int(user_id),
            'role_ids': ','.join(selected_row_keys)
            if selected_row_keys
            else '',
        }
        UserApi.update_auth_role(params)
        MessageManager.success(content='分配成功')

        return False

    raise PreventUpdate


@app.callback(
    Output('user_to_allocated_role-modal', 'visible', allow_duplicate=True),
    Input('allocate_role-back-button', 'nClicks'),
    prevent_initial_call=True,
)
def allocate_user_back_confirm(back_confirm):
    """
    关闭分配角色弹框操作
    """
    if back_confirm:
        return False

    raise PreventUpdate
