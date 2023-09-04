import dash
import time
import uuid
import json
from dash import dcc
from dash.dependencies import Input, Output, State, ALL
import feffery_utils_components as fuc

from server import app
from api.job import get_job_list_api, get_job_detail_api, add_job_api, edit_job_api, execute_job_api, delete_job_api, export_job_list_api
from api.dict import query_dict_data_list_api


@app.callback(
    [Output('job-list-table', 'data', allow_duplicate=True),
     Output('job-list-table', 'pagination', allow_duplicate=True),
     Output('job-list-table', 'key'),
     Output('job-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('job-search', 'nClicks'),
     Input('job-refresh', 'nClicks'),
     Input('job-list-table', 'pagination'),
     Input('job-operations-store', 'data')],
    [State('job-job_name-input', 'value'),
     State('job-job_group-select', 'value'),
     State('job-status-select', 'value'),
     State('job-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_job_table_data(search_click, refresh_click, pagination, operations, job_name, job_group, status_select,
                       button_perms):
    query_params = dict(
        job_name=job_name,
        job_group=job_group,
        status=status_select,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'job-list-table':
        query_params = dict(
            job_name=job_name,
            job_group=job_group,
            status=status_select,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        option_table = []
        info = query_dict_data_list_api(dict_type='sys_job_group')
        if info.get('code') == 200:
            data = info.get('data')
            option_table = [
                dict(label=item.get('dict_label'), value=item.get('dict_value'), css_class=item.get('css_class')) for
                item
                in data]
        option_dict = {item.get('value'): item for item in option_table}

        table_info = get_job_list_api(query_params)
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
                    item['status'] = dict(checked=True)
                else:
                    item['status'] = dict(checked=False)
                if str(item.get('job_group')) in option_dict.keys():
                    item['job_group'] = dict(
                        tag=option_dict.get(str(item.get('job_group'))).get('label'),
                        color=json.loads(option_dict.get(str(item.get('job_group'))).get('css_class')).get('color')
                    )
                item['key'] = str(item['job_id'])
                item['operation'] = [
                    {
                        'title': '修改',
                        'icon': 'antd-edit'
                    } if 'monitor:job:edit' in button_perms else None,
                    {
                        'title': '删除',
                        'icon': 'antd-delete'
                    } if 'monitor:job:remove' in button_perms else None,
                    {
                        'title': '执行一次',
                        'icon': 'antd-rocket'
                    } if 'monitor:job:changeStatus' in button_perms else None,
                    {
                        'title': '任务详细',
                        'icon': 'antd-eye'
                    } if 'monitor:job:query' in button_perms else None,
                    {
                        'title': '调度日志',
                        'icon': 'antd-history'
                    } if 'monitor:job:query' in button_perms else None
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('job-job_name-input', 'value'),
     Output('job-job_group-select', 'value'),
     Output('job-status-select', 'value'),
     Output('job-operations-store', 'data')],
    Input('job-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_job_query_params(reset_click):
    if reset_click:
        return [None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 4


@app.callback(
    [Output('job-search-form-container', 'hidden'),
     Output('job-hidden-tooltip', 'title')],
    Input('job-hidden', 'nClicks'),
    State('job-search-form-container', 'hidden'),
    prevent_initial_call=True
)
def hidden_job_search_form(hidden_click, hidden_status):
    if hidden_click:
        return [not hidden_status, '隐藏搜索' if hidden_status else '显示搜索']
    return [dash.no_update] * 2


@app.callback(
    Output({'type': 'job-operation-button', 'index': 'edit'}, 'disabled'),
    Input('job-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_job_edit_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1:
                return True

            return False

        return True

    return dash.no_update


@app.callback(
    Output({'type': 'job-operation-button', 'index': 'delete'}, 'disabled'),
    Input('job-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_job_delete_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1:
                return False

            return False

        return True

    return dash.no_update


@app.callback(
    [Output('job-modal', 'visible', allow_duplicate=True),
     Output('job-modal', 'title'),
     Output('job-job_name', 'value'),
     Output('job-job_group', 'value'),
     Output('job-invoke_target', 'value'),
     Output('job-cron_expression', 'value'),
     Output('job-job_args', 'value'),
     Output('job-job_kwargs', 'value'),
     Output('job-misfire_policy', 'value'),
     Output('job-concurrent', 'value'),
     Output('job-status', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('job-edit-id-store', 'data'),
     Output('job-operations-store-bk', 'data')],
    [Input({'type': 'job-operation-button', 'index': ALL}, 'nClicks'),
     Input('job-list-table', 'nClicksDropdownItem')],
    [State('job-list-table', 'selectedRowKeys'),
     State('job-list-table', 'recentlyClickedDropdownItemTitle'),
     State('job-list-table', 'recentlyDropdownItemClickedRow')],
    prevent_initial_call=True
)
def add_edit_job_modal(operation_click, dropdown_click, selected_row_keys, recently_clicked_dropdown_item_title,
                       recently_dropdown_item_clicked_row):
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'add', 'type': 'job-operation-button'} \
            or trigger_id == {'index': 'edit', 'type': 'job-operation-button'} \
            or (trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '修改'):
        if trigger_id == {'index': 'add', 'type': 'job-operation-button'}:
            return [
                True,
                '新增任务',
                None,
                None,
                None,
                None,
                None,
                None,
                '1',
                '1',
                '0',
                dash.no_update,
                None,
                {'type': 'add'}
            ]
        elif trigger_id == {'index': 'edit', 'type': 'job-operation-button'} or (trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'job-operation-button'}:
                job_id = int(','.join(selected_row_keys))
            else:
                job_id = int(recently_dropdown_item_clicked_row['key'])
            job_info_res = get_job_detail_api(job_id=job_id)
            if job_info_res['code'] == 200:
                job_info = job_info_res['data']
                return [
                    True,
                    '编辑任务',
                    job_info.get('job_name'),
                    job_info.get('job_group'),
                    job_info.get('invoke_target'),
                    job_info.get('cron_expression'),
                    job_info.get('job_args'),
                    job_info.get('job_kwargs'),
                    job_info.get('misfire_policy'),
                    job_info.get('concurrent'),
                    job_info.get('status'),
                    {'timestamp': time.time()},
                    job_info if job_info else None,
                    {'type': 'edit'}
                ]

        return [dash.no_update] * 11 + [{'timestamp': time.time()}, None, None]

    return [dash.no_update] * 12 + [None, None]


@app.callback(
    [Output('job-job_name-form-item', 'validateStatus'),
     Output('job-invoke_target-form-item', 'validateStatus'),
     Output('job-cron_expression-form-item', 'validateStatus'),
     Output('job-job_name-form-item', 'help'),
     Output('job-invoke_target-form-item', 'help'),
     Output('job-cron_expression-form-item', 'help'),
     Output('job-modal', 'visible'),
     Output('job-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job-modal', 'okCounts'),
    [State('job-operations-store-bk', 'data'),
     State('job-edit-id-store', 'data'),
     State('job-job_name', 'value'),
     State('job-job_group', 'value'),
     State('job-invoke_target', 'value'),
     State('job-cron_expression', 'value'),
     State('job-job_args', 'value'),
     State('job-job_kwargs', 'value'),
     State('job-misfire_policy', 'value'),
     State('job-concurrent', 'value'),
     State('job-status', 'value')],
    prevent_initial_call=True
)
def job_confirm(confirm_trigger, operation_type, cur_job_info, job_name, job_group, invoke_target, cron_expression,
                job_args, job_kwargs, misfire_policy, concurrent, status):
    if confirm_trigger:
        if all([job_name, invoke_target, cron_expression]):
            params_add = dict(job_name=job_name, job_group=job_group, invoke_target=invoke_target,
                              cron_expression=cron_expression, job_args=job_args, job_kwargs=job_kwargs,
                              misfire_policy=misfire_policy, concurrent=concurrent, status=status)
            params_edit = dict(job_id=cur_job_info.get('job_id') if cur_job_info else None, job_name=job_name,
                               job_group=job_group, invoke_target=invoke_target, cron_expression=cron_expression,
                               job_args=job_args, job_kwargs=job_kwargs,
                               misfire_policy=misfire_policy, concurrent=concurrent, status=status)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_job_api(params_add)
            if operation_type == 'edit':
                api_res = edit_job_api(params_edit)
            if api_res.get('code') == 200:
                if operation_type == 'add':
                    return [
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        False,
                        {'type': 'add'},
                        {'timestamp': time.time()},
                        fuc.FefferyFancyMessage('新增成功', type='success')
                    ]
                if operation_type == 'edit':
                    return [
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        False,
                        {'type': 'edit'},
                        {'timestamp': time.time()},
                        fuc.FefferyFancyMessage('编辑成功', type='success')
                    ]

            return [
                None,
                None,
                None,
                None,
                None,
                None,
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('处理失败', type='error')
            ]

        return [
            None if job_name else 'error',
            None if invoke_target else 'error',
            None if cron_expression else 'error',
            None if job_name else '请输入任务名称！',
            None if invoke_target else '请输入调用目标字符串！',
            None if cron_expression else '请输入cron执行表达式！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]

    return [dash.no_update] * 10


@app.callback(
    [Output('job-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    [Input('job-list-table', 'recentlySwitchDataIndex'),
     Input('job-list-table', 'recentlySwitchStatus'),
     Input('job-list-table', 'recentlySwitchRow')],
    prevent_initial_call=True
)
def table_switch_job_status(recently_switch_data_index, recently_switch_status, recently_switch_row):
    if recently_switch_data_index:
        if recently_switch_status:
            params = dict(job_id=int(recently_switch_row['key']), status='0', type='status')
        else:
            params = dict(job_id=int(recently_switch_row['key']), status='1', type='status')
        edit_button_result = edit_job_api(params)
        if edit_button_result['code'] == 200:

            return [
                {'type': 'switch-status'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('修改成功', type='success')
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('修改失败', type='error')
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('job_detail-modal', 'visible', allow_duplicate=True),
     Output('job_detail-modal', 'title'),
     Output('job_detail-job_name-text', 'children'),
     Output('job_detail-job_group-text', 'children'),
     Output('job_detail-job_executor-text', 'children'),
     Output('job_detail-invoke_target-text', 'children'),
     Output('job_detail-job_args-text', 'children'),
     Output('job_detail-job_kwargs-text', 'children'),
     Output('job_detail-cron_expression-text', 'children'),
     Output('job_detail-misfire_policy-text', 'children'),
     Output('job_detail-concurrent-text', 'children'),
     Output('job_detail-status-text', 'children'),
     Output('job_detail-create_time-text', 'children'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job-list-table', 'nClicksDropdownItem'),
    [State('job-list-table', 'recentlyClickedDropdownItemTitle'),
     State('job-list-table', 'recentlyDropdownItemClickedRow')],
    prevent_initial_call=True
)
def get_job_detail_modal(dropdown_click, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    if dropdown_click and recently_clicked_dropdown_item_title == '任务详细':
        job_id = int(recently_dropdown_item_clicked_row['key'])
        job_info_res = get_job_detail_api(job_id=job_id)
        if job_info_res['code'] == 200:
            job_info = job_info_res['data']
            if job_info.get('misfire_policy') == '1':
                misfire_policy = '立即执行'
            elif job_info.get('misfire_policy') == '2':
                misfire_policy = '执行一次'
            else:
                misfire_policy = '放弃执行'
            return [
                True,
                '任务详情',
                job_info.get('job_name'),
                job_info.get('job_group'),
                job_info.get('job_executor'),
                job_info.get('invoke_target'),
                job_info.get('job_args'),
                job_info.get('job_kwargs'),
                job_info.get('cron_expression'),
                misfire_policy,
                '是' if job_info.get('concurrent') == '0' else '否',
                '正常' if job_info.get('status') == '0' else '停用',
                job_info.get('create_time'),
                {'timestamp': time.time()},
                None
            ]

        return [dash.no_update] * 13 + [{'timestamp': time.time()}, None]

    if dropdown_click and recently_clicked_dropdown_item_title == '执行一次':
        job_id = int(recently_dropdown_item_clicked_row['key'])
        job_info_res = execute_job_api(dict(job_id=job_id))
        if job_info_res['code'] == 200:

            return [
                False,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('执行成功', type='success')
            ]

        return [
            False,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('执行失败', type='success')
        ]

    return [dash.no_update] * 15


@app.callback(
    [Output('job-delete-text', 'children'),
     Output('job-delete-confirm-modal', 'visible'),
     Output('job-delete-ids-store', 'data')],
    [Input({'type': 'job-operation-button', 'index': ALL}, 'nClicks'),
     Input('job-list-table', 'nClicksDropdownItem')],
    [State('job-list-table', 'selectedRowKeys'),
     State('job-list-table', 'recentlyClickedDropdownItemTitle'),
     State('job-list-table', 'recentlyDropdownItemClickedRow')],
    prevent_initial_call=True
)
def job_delete_modal(operation_click, dropdown_click,
                     selected_row_keys, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'job-operation-button'} or (
            trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '删除'):

        if trigger_id == {'index': 'delete', 'type': 'job-operation-button'}:
            job_ids = ','.join(selected_row_keys)
        else:
            if recently_clicked_dropdown_item_title == '删除':
                job_ids = recently_dropdown_item_clicked_row['key']
            else:
                return [dash.no_update] * 3

        return [
            f'是否确认删除任务编号为{job_ids}的任务？',
            True,
            {'job_ids': job_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('job-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job-delete-confirm-modal', 'okCounts'),
    State('job-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def job_delete_confirm(delete_confirm, job_ids_data):
    if delete_confirm:

        params = job_ids_data
        delete_button_info = delete_job_api(params)
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
    [Output('job_to_job_log-modal', 'visible'),
     Output('job_to_job_log-modal', 'title'),
     Output('job_log-job_name-input', 'value', allow_duplicate=True),
     Output('job_log-job_group-select', 'options'),
     Output('job_log-search', 'nClicks'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input({'type': 'job-operation-log', 'index': ALL}, 'nClicks'),
     Input('job-list-table', 'nClicksDropdownItem')],
    [State('job-list-table', 'recentlyClickedDropdownItemTitle'),
     State('job-list-table', 'recentlyDropdownItemClickedRow'),
     State('job_log-search', 'nClicks')],
    prevent_initial_call=True
)
def job_to_job_log_modal(operation_click, dropdown_click, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row, job_log_search_nclick):

    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'log', 'type': 'job-operation-log'} or (trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '调度日志'):
        option_table = []
        info = query_dict_data_list_api(dict_type='sys_job_group')
        if info.get('code') == 200:
            data = info.get('data')
            option_table = [dict(label=item.get('dict_label'), value=item.get('dict_value')) for item in data]

            if trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '调度日志':
                return [
                    True,
                    '任务调度日志',
                    recently_dropdown_item_clicked_row.get('job_name'),
                    option_table,
                    job_log_search_nclick + 1 if job_log_search_nclick else 1,
                    {'timestamp': time.time()},
                ]

        return [
                True,
                '任务调度日志',
                None,
                option_table,
                job_log_search_nclick + 1 if job_log_search_nclick else 1,
                {'timestamp': time.time()},
            ]

    return [dash.no_update] * 6


@app.callback(
    [Output('job-export-container', 'data', allow_duplicate=True),
     Output('job-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job-export', 'nClicks'),
    prevent_initial_call=True
)
def export_job_list(export_click):
    if export_click:
        export_job_res = export_job_list_api({})
        if export_job_res.status_code == 200:
            export_job = export_job_res.content

            return [
                dcc.send_bytes(export_job, f'定时任务信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
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
    Output('job-export-container', 'data', allow_duplicate=True),
    Input('job-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_job_export_status(data):
    time.sleep(0.5)
    if data:
        return None

    return dash.no_update
