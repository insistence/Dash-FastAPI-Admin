import dash
import feffery_utils_components as fuc
import time
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from server import app

from api.user import reset_user_password_api


@app.callback(
    [Output('reset-old-password-form-item', 'validateStatus'),
     Output('reset-new-password-form-item', 'validateStatus'),
     Output('reset-confirm-password-form-item', 'validateStatus'),
     Output('reset-old-password-form-item', 'help'),
     Output('reset-new-password-form-item', 'help'),
     Output('reset-confirm-password-form-item', 'help'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('reset-password-submit', 'nClicks'),
    [State('reset-old-password', 'value'),
     State('reset-new-password', 'value'),
     State('reset-confirm-password', 'value')],
    prevent_initial_call=True
)
def reset_submit_user_info(reset_click, old_password, new_password, confirm_password):
    """
    重置当前用户密码回调
    """
    if reset_click:
        if all([old_password, new_password, confirm_password]):

            if new_password == confirm_password:

                params = dict(type='avatar', old_password=old_password, password=new_password)
                reset_password_result = reset_user_password_api(params)
                if reset_password_result.get('code') == 200:

                    return [
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        {'timestamp': time.time()},
                        fuc.FefferyFancyMessage('修改成功', type='success'),
                    ]

                return [
                    None,
                    None,
                    None,
                    None,
                    None,
                    None,
                    {'timestamp': time.time()},
                    fuc.FefferyFancyMessage('修改失败', type='error'),
                ]

            return [
                None,
                None if new_password else 'error',
                None if confirm_password else 'error',
                None,
                None if new_password else '前后两次密码不一致！',
                None if confirm_password else '前后两次密码不一致！',
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('修改失败', type='error'),
            ]

        return [
            None if old_password else 'error',
            None if new_password else 'error',
            None if confirm_password else 'error',
            None if old_password else '请输入旧密码！',
            None if new_password else '请输入新密码！',
            None if confirm_password else '请输入确认密码！',
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('修改失败', type='error'),
        ]

    raise PreventUpdate


@app.callback(
    Output('tabs-container', 'latestDeletePane', allow_duplicate=True),
    Input('reset-password-close', 'nClicks'),
    prevent_initial_call=True
)
def close_personal_info_modal(close_click):
    """
    关闭当前个人资料标签页回调
    """
    if close_click:

        return '个人资料'
    raise PreventUpdate
