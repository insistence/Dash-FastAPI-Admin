import dash
import time
import uuid
import json
from dash import dcc
from dash.dependencies import Input, Output, State, ALL
import feffery_utils_components as fuc

from server import app
from api.job import get_job_log_list_api, get_job_log_detail_api, delete_job_log_api, clear_job_log_api, export_job_log_list_api
from api.dict import query_dict_data_list_api


@app.callback(
    [Output('job_log-list-table', 'data', allow_duplicate=True),
     Output('job_log-list-table', 'pagination', allow_duplicate=True),
     Output('job_log-list-table', 'key'),
     Output('job_log-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('job_log-search', 'nClicks'),
     Input('job_log-refresh', 'nClicks'),
     Input('job_log-list-table', 'pagination'),
     Input('job_log-operations-store', 'data')],
    [State('job_log-job_name-input', 'value'),
     State('job_log-job_group-select', 'value'),
     State('job_log-status-select', 'value'),
     State('job_log-create_time-range', 'value'),
     State('job_log-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_job_log_table_data(search_click, refresh_click, pagination, operations, job_name, job_group, status_select, create_time_range, button_perms):

    create_time_start = None
    create_time_end = None
    if create_time_range:
        create_time_start = create_time_range[0]
        create_time_end = create_time_range[1]
    query_params = dict(
        job_name=job_name,
        job_group=job_group,
        status=status_select,
        create_time_start=create_time_start,
        create_time_end=create_time_end,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'job_log-list-table':
        query_params = dict(
            job_name=job_name,
            job_group=job_group,
            status=status_select,
            create_time_start=create_time_start,
            create_time_end=create_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        option_table = []
        info = query_dict_data_list_api(dict_type='sys_job_group')
        if info.get('code') == 200:
            data = info.get('data')
            option_table = [dict(label=item.get('dict_label'), value=item.get('dict_value'), css_class=item.get('css_class')) for item in data]
        option_dict = {item.get('value'): item for item in option_table}

        table_info = get_job_log_list_api(query_params)
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
                if str(item.get('job_group')) in option_dict.keys():
                    item['job_group'] = dict(
                        tag=option_dict.get(str(item.get('job_group'))).get('label'),
                        color=json.loads(option_dict.get(str(item.get('job_group'))).get('css_class')).get('color')
                    )
                item['key'] = str(item['job_log_id'])
                item['operation'] = [
                    {
                        'content': '详情',
                        'type': 'link',
                        'icon': 'antd-eye'
                    } if 'monitor:job:query' in button_perms else {},
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('job_log-job_name-input', 'value'),
     Output('job_log-job_group-select', 'value'),
     Output('job_log-status-select', 'value'),
     Output('job_log-create_time-range', 'value'),
     Output('job_log-operations-store', 'data')],
    Input('job_log-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_job_log_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 5


@app.callback(
    [Output('job_log-search-form-container', 'hidden'),
     Output('job_log-hidden-tooltip', 'title')],
    Input('job_log-hidden', 'nClicks'),
    State('job_log-search-form-container', 'hidden'),
    prevent_initial_call=True
)
def hidden_job_log_search_form(hidden_click, hidden_status):
    if hidden_click:

        return [not hidden_status, '隐藏搜索' if hidden_status else '显示搜索']
    return [dash.no_update] * 2


@app.callback(
    [Output('job_log-modal', 'visible', allow_duplicate=True),
     Output('job_log-modal', 'title'),
     Output('job_log-job_name-text', 'children'),
     Output('job_log-job_group-text', 'children'),
     Output('job_log-job_executor-text', 'children'),
     Output('job_log-invoke_target-text', 'children'),
     Output('job_log-job_args-text', 'children'),
     Output('job_log-job_kwargs-text', 'children'),
     Output('job_log-job_trigger-text', 'children'),
     Output('job_log-job_message-text', 'children'),
     Output('job_log-status-text', 'children'),
     Output('job_log-create_time-text', 'children'),
     Output('job_log-exception_info-text', 'children'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    Input('job_log-list-table', 'nClicksButton'),
    [State('job_log-list-table', 'clickedContent'),
     State('job_log-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_job_log_modal(button_click, clicked_content, recently_button_clicked_row):
    if button_click:
        job_log_id = int(recently_button_clicked_row['key'])
        job_log_info_res = get_job_log_detail_api(job_log_id=job_log_id)
        if job_log_info_res['code'] == 200:
            job_log_info = job_log_info_res['data']
            return [
                True,
                '任务执行日志详情',
                job_log_info.get('job_name'),
                job_log_info.get('job_group'),
                job_log_info.get('job_executor'),
                job_log_info.get('invoke_target'),
                job_log_info.get('job_args'),
                job_log_info.get('job_kwargs'),
                job_log_info.get('job_trigger'),
                job_log_info.get('job_message'),
                '成功' if job_log_info.get('status') == '0' else '失败',
                job_log_info.get('create_time'),
                job_log_info.get('exception_info'),
                {'timestamp': time.time()},
            ]

        return [dash.no_update] * 13 + [{'timestamp': time.time()}]

    return [dash.no_update] * 14


@app.callback(
    Output({'type': 'job_log-operation-button', 'index': 'delete'}, 'disabled'),
    Input('job_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_job_log_delete_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1:
                return False

            return False

        return True

    return dash.no_update


@app.callback(
    [Output('job_log-delete-text', 'children'),
     Output('job_log-delete-confirm-modal', 'visible'),
     Output('job_log-delete-ids-store', 'data')],
    Input({'type': 'job_log-operation-button', 'index': ALL}, 'nClicks'),
    State('job_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def job_log_delete_modal(operation_click, selected_row_keys):
    trigger_id = dash.ctx.triggered_id
    if trigger_id.index in ['delete', 'clear']:
        if trigger_id.index == 'delete':
            job_log_ids = ','.join(selected_row_keys)

            return [
                f'是否确认删除日志编号为{job_log_ids}的任务执行日志？',
                True,
                {'oper_type': 'delete', 'job_log_ids': job_log_ids}
            ]

        elif trigger_id.index == 'clear':
            return [
                f'是否确认清除所有的任务执行日志？',
                True,
                {'oper_type': 'clear', 'job_log_ids': ''}
            ]

    return [dash.no_update] * 3


@app.callback(
    [Output('job_log-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job_log-delete-confirm-modal', 'okCounts'),
    State('job_log-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def job_log_delete_confirm(delete_confirm, job_log_ids_data):
    if delete_confirm:

        oper_type = job_log_ids_data.get('oper_type')
        if oper_type == 'clear':
            params = dict(oper_type=job_log_ids_data.get('oper_type'))
            clear_button_info = clear_job_log_api(params)
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
            params = dict(job_log_ids=job_log_ids_data.get('job_log_ids'))
            delete_button_info = delete_job_log_api(params)
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


@app.callback(
    [Output('job_log-export-container', 'data', allow_duplicate=True),
     Output('job_log-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job_log-export', 'nClicks'),
    prevent_initial_call=True
)
def export_job_log_list(export_click):
    if export_click:
        export_job_log_res = export_job_log_list_api({})
        if export_job_log_res.status_code == 200:
            export_job_log = export_job_log_res.content

            return [
                dcc.send_bytes(export_job_log, f'任务执行日志信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
                {'timestamp': time.time()},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('导出成功', type='success')
            ]

        return [
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('导出失败', type='error')
        ]

    return [dash.no_update] * 4


@app.callback(
    Output('job_log-export-container', 'data', allow_duplicate=True),
    Input('job_log-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_job_log_export_status(data):
    time.sleep(0.5)
    if data:

        return None

    return dash.no_update
