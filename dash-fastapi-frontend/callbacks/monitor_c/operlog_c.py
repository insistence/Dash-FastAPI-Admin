import dash
import time
import uuid
from dash import html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc

from server import app
from api.log import get_operation_log_list_api, get_operation_log_detail_api, delete_operation_log_api, clear_operation_log_api


@app.callback(
    [Output('operation_log-list-table', 'data', allow_duplicate=True),
     Output('operation_log-list-table', 'pagination', allow_duplicate=True),
     Output('operation_log-list-table', 'key'),
     Output('operation_log-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('operation_log-search', 'nClicks'),
     Input('operation_log-list-table', 'pagination'),
     Input('operation_log-operations-store', 'data')],
    [State('operation_log-title-input', 'value'),
     State('operation_log-oper_name-input', 'value'),
     State('operation_log-business_type-select', 'value'),
     State('operation_log-status-select', 'value'),
     State('operation_log-oper_time-range', 'value'),
     State('operation_log-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_operation_log_table_data(search_click, pagination, operations, title, oper_name, business_type, status_select, oper_time_range, button_perms):

    oper_time_start = None
    oper_time_end = None
    if oper_time_range:
        oper_time_start = oper_time_range[0]
        oper_time_end = oper_time_range[1]
    query_params = dict(
        title=title,
        oper_name=oper_name,
        business_type=business_type,
        status=status_select,
        oper_time_start=oper_time_start,
        oper_time_end=oper_time_end,
        page_num=1,
        page_size=10
    )
    if pagination:
        query_params = dict(
            title=title,
            oper_name=oper_name,
            business_type=business_type,
            status=status_select,
            oper_time_start=oper_time_start,
            oper_time_end=oper_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or pagination or operations:
        table_info = get_operation_log_list_api(query_params)
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
                if item['status'] == 0:
                    item['status'] = dict(tag='成功', color='blue')
                else:
                    item['status'] = dict(tag='失败', color='volcano')
                if item['business_type'] == 0:
                    item['business_type'] = dict(tag='其他', color='purple')
                elif item['business_type'] == 1:
                    item['business_type'] = dict(tag='新增', color='green')
                elif item['business_type'] == 2:
                    item['business_type'] = dict(tag='修改', color='orange')
                elif item['business_type'] == 3:
                    item['business_type'] = dict(tag='删除', color='red')
                elif item['business_type'] == 4:
                    item['business_type'] = dict(tag='授权', color='lime')
                elif item['business_type'] == 5:
                    item['business_type'] = dict(tag='导出', color='geekblue')
                elif item['business_type'] == 6:
                    item['business_type'] = dict(tag='导入', color='blue')
                elif item['business_type'] == 7:
                    item['business_type'] = dict(tag='强退', color='magenta')
                elif item['business_type'] == 8:
                    item['business_type'] = dict(tag='生成代码', color='cyan')
                elif item['business_type'] == 9:
                    item['business_type'] = dict(tag='清空数据', color='volcano')
                item['key'] = str(item['oper_id'])
                item['cost_time'] = f"{item['cost_time']}毫秒"
                item['operation'] = [
                    {
                        'content': '详情',
                        'type': 'link',
                        'icon': 'antd-eye'
                    } if 'monitor:operlog:query' in button_perms else {},
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('operation_log-title-input', 'value'),
     Output('operation_log-oper_name-input', 'value'),
     Output('operation_log-business_type-select', 'value'),
     Output('operation_log-status-select', 'value'),
     Output('operation_log-oper_time-range', 'value'),
     Output('operation_log-operations-store', 'data')],
    Input('operation_log-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_operation_log_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 6


@app.callback(
    [Output('operation_log-modal', 'visible', allow_duplicate=True),
     Output('operation_log-modal', 'title'),
     Output('operation_log-title-text', 'children'),
     Output('operation_log-oper_url-text', 'children'),
     Output('operation_log-login_info-text', 'children'),
     Output('operation_log-request_method-text', 'children'),
     Output('operation_log-method-text', 'children'),
     Output('operation_log-oper_param-text', 'children'),
     Output('operation_log-json_result-text', 'children'),
     Output('operation_log-status-text', 'children'),
     Output('operation_log-cost_time-text', 'children'),
     Output('operation_log-oper_time-text', 'children'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    Input('operation_log-list-table', 'nClicksButton'),
    [State('operation_log-list-table', 'clickedContent'),
     State('operation_log-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_operation_log_modal(button_click, clicked_content, recently_button_clicked_row):
    if button_click:
        oper_id = int(recently_button_clicked_row['key'])
        operation_log_info_res = get_operation_log_detail_api(oper_id=oper_id)
        if operation_log_info_res['code'] == 200:
            operation_log_info = operation_log_info_res['data']
            oper_name = operation_log_info.get('oper_name') if operation_log_info.get('oper_name') else ''
            oper_ip = operation_log_info.get('oper_ip') if operation_log_info.get('oper_ip') else ''
            oper_location = operation_log_info.get('oper_location') if operation_log_info.get('oper_location') else ''
            login_info = f'{oper_name} / {oper_ip} / {oper_location}'
            return [
                True,
                '操作日志详情',
                operation_log_info.get('title'),
                operation_log_info.get('oper_url'),
                login_info,
                operation_log_info.get('request_method'),
                operation_log_info.get('method'),
                operation_log_info.get('oper_param'),
                operation_log_info.get('json_result'),
                '正常' if operation_log_info.get('status') == 0 else '失败',
                f"{operation_log_info.get('cost_time')}毫秒",
                operation_log_info.get('oper_time'),
                {'timestamp': time.time()},
            ]

        return [dash.no_update] * 12 + [{'timestamp': time.time()}]

    return [dash.no_update] * 13


@app.callback(
    Output('operation_log-delete', 'disabled'),
    Input('operation_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_operation_log_delete_button_status(table_rows_selected):
    if table_rows_selected:
        if len(table_rows_selected) > 1:
            return False

        return False

    return True


@app.callback(
    [Output('operation_log-delete-text', 'children'),
     Output('operation_log-delete-confirm-modal', 'visible'),
     Output('operation_log-delete-ids-store', 'data')],
    [Input('operation_log-delete', 'nClicks'),
     Input('operation_log-clear', 'nClicks')],
    State('operation_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def operation_log_delete_modal(delete_click, clear_click, selected_row_keys):
    if delete_click or clear_click:
        trigger_id = dash.ctx.triggered_id
        if trigger_id == 'operation_log-delete':
            oper_ids = ','.join(selected_row_keys)

            return [
                f'是否确认删除日志编号为{oper_ids}的操作日志？',
                True,
                {'oper_type': 'delete', 'oper_ids': oper_ids}
            ]

        elif trigger_id == 'operation_log-clear':
            return [
                f'是否确认清除所有的操作日志？',
                True,
                {'oper_type': 'clear', 'oper_ids': ''}
            ]

    return [dash.no_update] * 3


@app.callback(
    [Output('operation_log-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('operation_log-delete-confirm-modal', 'okCounts'),
    State('operation_log-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def operation_log_delete_confirm(delete_confirm, oper_ids_data):
    if delete_confirm:

        oper_type = oper_ids_data.get('oper_type')
        if oper_type == 'clear':
            params = dict(oper_type=oper_ids_data.get('oper_type'))
            clear_button_info = clear_operation_log_api(params)
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
            params = dict(oper_ids=oper_ids_data.get('oper_ids'))
            delete_button_info = delete_operation_log_api(params)
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
