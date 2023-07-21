import dash
import time
import uuid
from dash import html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc

from server import app
from api.log import get_login_log_list_api, delete_login_log_api, clear_login_log_api


@app.callback(
    [Output('login_log-list-table', 'data', allow_duplicate=True),
     Output('login_log-list-table', 'pagination', allow_duplicate=True),
     Output('login_log-list-table', 'key'),
     Output('login_log-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('login_log-search', 'nClicks'),
     Input('login_log-list-table', 'pagination'),
     Input('login_log-operations-store', 'data')],
    [State('login_log-ipaddr-input', 'value'),
     State('login_log-user_name-input', 'value'),
     State('login_log-status-select', 'value'),
     State('login_log-login_time-range', 'value'),
     State('login_log-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_login_log_table_data(search_click, pagination, operations, ipaddr, user_name, status_select, login_time_range, button_perms):

    login_time_start = None
    login_time_end = None
    if login_time_range:
        login_time_start = login_time_range[0]
        login_time_end = login_time_range[1]
    query_params = dict(
        ipaddr=ipaddr,
        user_name=user_name,
        status=status_select,
        login_time_start=login_time_start,
        login_time_end=login_time_end,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'login_log-list-table':
        query_params = dict(
            ipaddr=ipaddr,
            user_name=user_name,
            status=status_select,
            login_time_start=login_time_start,
            login_time_end=login_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or pagination or operations:
        table_info = get_login_log_list_api(query_params)
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
                if item['status'] == '0':
                    item['status'] = dict(tag='成功', color='blue')
                else:
                    item['status'] = dict(tag='失败', color='volcano')
                item['key'] = str(item['info_id'])

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('login_log-ipaddr-input', 'value'),
     Output('login_log-user_name-input', 'value'),
     Output('login_log-status-select', 'value'),
     Output('login_log-login_time-range', 'value'),
     Output('login_log-operations-store', 'data')],
    Input('login_log-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_login_log_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 5


@app.callback(
    [Output('login_log-delete', 'disabled'),
     Output('login_log-unlock', 'disabled')],
    Input('login_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_login_log_delete_unlock_button_status(table_rows_selected):
    if table_rows_selected:
        if len(table_rows_selected) > 1:
            return [False, True]

        return [False, False]

    return [True, True]


@app.callback(
    [Output('login_log-delete-text', 'children'),
     Output('login_log-delete-confirm-modal', 'visible'),
     Output('login_log-delete-ids-store', 'data')],
    [Input('login_log-delete', 'nClicks'),
     Input('login_log-clear', 'nClicks')],
    State('login_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def login_log_delete_modal(delete_click, clear_click, selected_row_keys):
    if delete_click or clear_click:
        trigger_id = dash.ctx.triggered_id
        if trigger_id == 'login_log-delete':
            info_ids = ','.join(selected_row_keys)

            return [
                f'是否确认删除访问编号为{info_ids}的操作日志？',
                True,
                {'oper_type': 'delete', 'info_ids': info_ids}
            ]

        elif trigger_id == 'login_log-clear':
            return [
                f'是否确认清除所有的登录日志？',
                True,
                {'oper_type': 'clear', 'info_ids': ''}
            ]

    return [dash.no_update] * 3


@app.callback(
    [Output('login_log-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('login_log-delete-confirm-modal', 'okCounts'),
    State('login_log-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def login_log_delete_confirm(delete_confirm, info_ids_data):
    if delete_confirm:

        oper_type = info_ids_data.get('oper_type')
        if oper_type == 'clear':
            params = dict(oper_type=info_ids_data.get('oper_type'))
            clear_button_info = clear_login_log_api(params)
            if clear_button_info['code'] == 200:
                return [
                    {'type': 'delete'},
                    {'timestamp': time.time()},
                    fuc.FefferyFancyMessage('清除成功', type='success')
                ]

            return [
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('清除失败', type='error')
            ]
        else:
            params = dict(info_ids=info_ids_data.get('info_ids'))
            delete_button_info = delete_login_log_api(params)
            if delete_button_info['code'] == 200:
                return [
                    {'type': 'delete'},
                    {'timestamp': time.time()},
                    fuc.FefferyFancyMessage('删除成功', type='success')
                ]

            return [
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('删除失败', type='error')
            ]

    return [dash.no_update] * 3
