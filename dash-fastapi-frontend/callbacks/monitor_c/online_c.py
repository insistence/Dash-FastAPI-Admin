import dash
import time
import uuid
from dash.dependencies import Input, Output, State
import feffery_utils_components as fuc

from server import app
from api.online import get_online_list_api, force_logout_online_api, batch_logout_online_api


@app.callback(
    [Output('online-list-table', 'data', allow_duplicate=True),
     Output('online-list-table', 'pagination', allow_duplicate=True),
     Output('online-list-table', 'key'),
     Output('online-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('online-search', 'nClicks'),
     Input('online-list-table', 'pagination'),
     Input('online-operations-store', 'data')],
    [State('online-ipaddr-input', 'value'),
     State('online-user_name-input', 'value'),
     State('online-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_online_table_data(search_click, pagination, operations, ipaddr, user_name, button_perms):
    query_params = dict(
        ipaddr=ipaddr,
        user_name=user_name,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'post-list-table':
        query_params = dict(
            ipaddr=ipaddr,
            user_name=user_name,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or pagination or operations:
        table_info = get_online_list_api(query_params)
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
                item['key'] = str(item['session_id'])
                item['operation'] = [
                    {
                        'content': '强退',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'monitor:online:forceLogout' in button_perms else {},
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('online-ipaddr-input', 'value'),
     Output('online-user_name-input', 'value'),
     Output('online-operations-store', 'data')],
    Input('online-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_online_query_params(reset_click):
    if reset_click:
        return [None, None, {'type': 'reset'}]

    return [dash.no_update] * 3


@app.callback(
    Output('online-delete', 'disabled'),
    Input('online-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_online_edit_delete_button_status(table_rows_selected):
    if table_rows_selected:

        return False

    return True


@app.callback(
    [Output('online-delete-text', 'children'),
     Output('online-delete-confirm-modal', 'visible'),
     Output('online-delete-ids-store', 'data')],
    [Input('online-delete', 'nClicks'),
     Input('online-list-table', 'nClicksButton')],
    [State('online-list-table', 'selectedRowKeys'),
     State('online-list-table', 'clickedContent'),
     State('online-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def online_delete_modal(delete_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    if delete_click or button_click:
        trigger_id = dash.ctx.triggered_id
        logout_type = ''

        if trigger_id == 'online-delete':
            session_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '强退':
                session_ids = recently_button_clicked_row['key']
                logout_type = 'force'
            else:
                return dash.no_update

        return [
            f'是否确认强退会话编号为{session_ids}的会话？',
            True,
            {'session_ids': session_ids, 'logout_type': logout_type}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('online-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('online-delete-confirm-modal', 'okCounts'),
    State('online-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def online_delete_confirm(delete_confirm, session_ids_data):
    if delete_confirm:

        params = dict(session_ids=session_ids_data.get('session_ids'))
        logout_type = session_ids_data.get('logout_type')
        if logout_type == 'force':
            delete_button_info = force_logout_online_api(params)
        else:
            delete_button_info = batch_logout_online_api(params)
        if delete_button_info['code'] == 200:
            return [
                {'type': 'force'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('强退成功', type='success')
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('强退失败', type='error')
        ]

    return [dash.no_update] * 3
