import dash
import time
import uuid
import json
from dash import dcc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from api.job import get_job_log_list_api, get_job_log_detail_api, delete_job_log_api, clear_job_log_api, export_job_log_list_api
from api.dict import query_dict_data_list_api


@app.callback(
    output=dict(
        job_log_table_data=Output('job_log-list-table', 'data', allow_duplicate=True),
        job_log_table_pagination=Output('job_log-list-table', 'pagination', allow_duplicate=True),
        job_log_table_key=Output('job_log-list-table', 'key'),
        job_log_table_selectedrowkeys=Output('job_log-list-table', 'selectedRowKeys'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        search_click=Input('job_log-search', 'nClicks'),
        refresh_click=Input('job_log-refresh', 'nClicks'),
        pagination=Input('job_log-list-table', 'pagination'),
        operations=Input('job_log-operations-store', 'data')
    ),
    state=dict(
        job_name=State('job_log-job_name-input', 'value'),
        job_group=State('job_log-job_group-select', 'value'),
        status_select=State('job_log-status-select', 'value'),
        create_time_range=State('job_log-create_time-range', 'value'),
        button_perms=State('job_log-button-perms-container', 'data')
    ),
    prevent_initial_call=True
)
def get_job_log_table_data(search_click, refresh_click, pagination, operations, job_name, job_group, status_select, create_time_range, button_perms):
    """
    获取定时任务对应调度日志表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """

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

            return dict(
                job_log_table_data=table_data,
                job_log_table_pagination=table_pagination,
                job_log_table_key=str(uuid.uuid4()),
                job_log_table_selectedrowkeys=None,
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            job_log_table_data=dash.no_update,
            job_log_table_pagination=dash.no_update,
            job_log_table_key=dash.no_update,
            job_log_table_selectedrowkeys=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


# 重置定时任务调度日志搜索表单数据回调
app.clientside_callback(
    '''
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('job_log-job_name-input', 'value'),
     Output('job_log-job_group-select', 'value'),
     Output('job_log-status-select', 'value'),
     Output('job_log-create_time-range', 'value'),
     Output('job_log-operations-store', 'data')],
    Input('job_log-reset', 'nClicks'),
    prevent_initial_call=True
)


# 隐藏/显示定时任务调度日志搜索表单回调
app.clientside_callback(
    '''
    (hidden_click, hidden_status) => {
        if (hidden_click) {
            return [
                !hidden_status,
                hidden_status ? '隐藏搜索' : '显示搜索'
            ]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('job_log-search-form-container', 'hidden'),
     Output('job_log-hidden-tooltip', 'title')],
    Input('job_log-hidden', 'nClicks'),
    State('job_log-search-form-container', 'hidden'),
    prevent_initial_call=True
)


@app.callback(
    output=dict(
        modal_visible=Output('job_log-modal', 'visible', allow_duplicate=True),
        modal_title=Output('job_log-modal', 'title'),
        form_value=Output({'type': 'job_log-form-value', 'index': ALL}, 'children'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        button_click=Input('job_log-list-table', 'nClicksButton')
    ),
    state=dict(
        clicked_content=State('job_log-list-table', 'clickedContent'),
        recently_button_clicked_row=State('job_log-list-table', 'recentlyButtonClickedRow')
    ),
    prevent_initial_call=True
)
def add_edit_job_log_modal(button_click, clicked_content, recently_button_clicked_row):
    if button_click:
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in dash.ctx.outputs_list[-2]]
        job_log_id = int(recently_button_clicked_row['key'])
        job_log_info_res = get_job_log_detail_api(job_log_id=job_log_id)
        if job_log_info_res['code'] == 200:
            job_log_info = job_log_info_res['data']
            job_log_info['status'] = '成功' if job_log_info.get('status') == '0' else '失败'
            return dict(
                modal_visible=True,
                modal_title='任务执行日志详情',
                form_value=[job_log_info.get(k) for k in form_value_list],
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            modal_visible=dash.no_update,
            modal_title=dash.no_update,
            form_value=[dash.no_update] * len(form_value_list),
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


@app.callback(
    Output({'type': 'job_log-operation-button', 'index': 'delete'}, 'disabled'),
    Input('job_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_job_log_delete_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制删除按钮状态回调
    """
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:

            return False

        return True

    raise PreventUpdate


@app.callback(
    [Output('job_log-delete-text', 'children'),
     Output('job_log-delete-confirm-modal', 'visible'),
     Output('job_log-delete-ids-store', 'data')],
    Input({'type': 'job_log-operation-button', 'index': ALL}, 'nClicks'),
    State('job_log-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def job_log_delete_modal(operation_click, selected_row_keys):
    """
    显示删除或清空定时任务调度日志二次确认弹窗回调
    """
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

    raise PreventUpdate


@app.callback(
    [Output('job_log-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job_log-delete-confirm-modal', 'okCounts'),
    State('job_log-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def job_log_delete_confirm(delete_confirm, job_log_ids_data):
    """
    删除或清空定时任务调度日志弹窗确认回调，实现删除或清空操作
    """
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

    raise PreventUpdate


@app.callback(
    [Output('job_log-export-container', 'data', allow_duplicate=True),
     Output('job_log-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job_log-export', 'nClicks'),
    prevent_initial_call=True
)
def export_job_log_list(export_click):
    """
    导出定时任务调度日志信息回调
    """
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

    raise PreventUpdate


@app.callback(
    Output('job_log-export-container', 'data', allow_duplicate=True),
    Input('job_log-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_job_log_export_status(data):
    """
    导出完成后重置下载组件数据回调，防止重复下载文件
    """
    time.sleep(0.5)
    if data:

        return None

    raise PreventUpdate
