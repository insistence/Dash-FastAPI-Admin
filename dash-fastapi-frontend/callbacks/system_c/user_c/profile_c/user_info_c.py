import dash
import feffery_utils_components as fuc
import time
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from server import app

from api.user import change_user_info_api


@app.callback(
    [Output('reset-user-nick_name-form-item', 'validateStatus'),
     Output('reset-user-phonenumber-form-item', 'validateStatus'),
     Output('reset-user-email-form-item', 'validateStatus'),
     Output('reset-user-nick_name-form-item', 'help'),
     Output('reset-user-phonenumber-form-item', 'help'),
     Output('reset-user-email-form-item', 'help'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('reset-submit', 'nClicks'),
    [State('reset-user-nick_name', 'value'),
     State('reset-user-phonenumber', 'value'),
     State('reset-user-email', 'value'),
     State('reset-user-sex', 'value')],
    prevent_initial_call=True
)
def reset_submit_user_info(reset_click, nick_name, phonenumber, email, sex):
    """
    修改当前用户信息回调
    """
    if reset_click:
        if all([nick_name, phonenumber, email]):

            params = dict(type='avatar', nick_name=nick_name, phonenumber=phonenumber, email=email, sex=sex)
            change_user_info_result = change_user_info_api(params)
            if change_user_info_result.get('code') == 200:

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
            None if nick_name else 'error',
            None if phonenumber else 'error',
            None if email else 'error',
            None if nick_name else '请输入用户昵称！',
            None if phonenumber else '请输入手机号码！',
            None if email else '请输入邮箱！',
            dash.no_update,
            fuc.FefferyFancyMessage('修改失败', type='error'),
        ]

    raise PreventUpdate


@app.callback(
    [Output('tabs-container', 'latestDeletePane', allow_duplicate=True),
     Output('tabs-container', 'tabCloseCounts', allow_duplicate=True)],
    Input('reset-close', 'nClicks'),
    State('tabs-container', 'tabCloseCounts'),
    prevent_initial_call=True
)
def close_personal_info_modal(close_click, tab_close_counts):
    """
    关闭当前个人资料标签页回调
    """
    if close_click:

        return ['个人资料', tab_close_counts + 1 if tab_close_counts else 1]
    raise PreventUpdate
