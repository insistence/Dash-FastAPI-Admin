from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from api.system.user import UserApi
from server import app
from utils.feedback_util import MessageManager


@app.callback(
    [
        Output('reset-old-password-form-item', 'validateStatus'),
        Output('reset-new-password-form-item', 'validateStatus'),
        Output('reset-confirm-password-form-item', 'validateStatus'),
        Output('reset-old-password-form-item', 'help'),
        Output('reset-new-password-form-item', 'help'),
        Output('reset-confirm-password-form-item', 'help'),
    ],
    Input('reset-password-submit', 'nClicks'),
    [
        State('reset-old-password', 'value'),
        State('reset-new-password', 'value'),
        State('reset-confirm-password', 'value'),
    ],
    running=[[Output('reset-password-submit', 'loading'), True, False]],
    prevent_initial_call=True,
)
def reset_submit_user_info(
    reset_click, old_password, new_password, confirm_password
):
    """
    重置当前用户密码回调
    """
    if reset_click:
        if all([old_password, new_password, confirm_password]):
            if new_password == confirm_password:
                UserApi.update_user_pwd(
                    old_password=old_password, new_password=new_password
                )
                MessageManager.success(content='修改成功')

                return [None] * 6

            return [
                None,
                None if new_password else 'error',
                None if confirm_password else 'error',
                None,
                None if new_password else '前后两次密码不一致！',
                None if confirm_password else '前后两次密码不一致！',
            ]

        return [
            None if old_password else 'error',
            None if new_password else 'error',
            None if confirm_password else 'error',
            None if old_password else '请输入旧密码！',
            None if new_password else '请输入新密码！',
            None if confirm_password else '请输入确认密码！',
        ]

    raise PreventUpdate


@app.callback(
    [
        Output('tabs-container', 'latestDeletePane', allow_duplicate=True),
        Output('tabs-container', 'tabCloseCounts', allow_duplicate=True),
    ],
    Input('reset-password-close', 'nClicks'),
    State('tabs-container', 'tabCloseCounts'),
    prevent_initial_call=True,
)
def close_personal_info_modal(close_click, tab_close_counts):
    """
    关闭当前个人资料标签页回调
    """
    if close_click:
        return [
            'Profile/user/profile',
            tab_close_counts + 1 if tab_close_counts else 1,
        ]
    raise PreventUpdate
