import dash
import time
import uuid
import json
from dash import dcc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from api.job import get_job_list_api, get_job_detail_api, add_job_api, edit_job_api, execute_job_api, delete_job_api, export_job_list_api
from api.dict import query_dict_data_list_api


@app.callback(
    output=dict(
        job_table_data=Output('job-list-table', 'data', allow_duplicate=True),
        job_table_pagination=Output('job-list-table', 'pagination', allow_duplicate=True),
        job_table_key=Output('job-list-table', 'key'),
        job_table_selectedrowkeys=Output('job-list-table', 'selectedRowKeys'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        search_click=Input('job-search', 'nClicks'),
        refresh_click=Input('job-refresh', 'nClicks'),
        pagination=Input('job-list-table', 'pagination'),
        operations=Input('job-operations-store', 'data')
    ),
    state=dict(
        job_name=State('job-job_name-input', 'value'),
        job_group=State('job-job_group-select', 'value'),
        status_select=State('job-status-select', 'value'),
        button_perms=State('job-button-perms-container', 'data')
    ),
    prevent_initial_call=True
)
def get_job_table_data(search_click, refresh_click, pagination, operations, job_name, job_group, status_select,
                       button_perms):
    """
    获取定时任务表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """
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

            return dict(
                job_table_data=table_data,
                job_table_pagination=table_pagination,
                job_table_key=str(uuid.uuid4()),
                job_table_selectedrowkeys=None,
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            job_table_data=dash.no_update,
            job_table_pagination=dash.no_update,
            job_table_key=dash.no_update,
            job_table_selectedrowkeys=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


# 重置定时任务搜索表单数据回调
app.clientside_callback(
    '''
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('job-job_name-input', 'value'),
     Output('job-job_group-select', 'value'),
     Output('job-status-select', 'value'),
     Output('job-operations-store', 'data')],
    Input('job-reset', 'nClicks'),
    prevent_initial_call=True
)


# 隐藏/显示定时任务搜索表单回调
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
    [Output('job-search-form-container', 'hidden'),
     Output('job-hidden-tooltip', 'title')],
    Input('job-hidden', 'nClicks'),
    State('job-search-form-container', 'hidden'),
    prevent_initial_call=True
)


@app.callback(
    Output({'type': 'job-operation-button', 'index': 'edit'}, 'disabled'),
    Input('job-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_job_edit_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制编辑按钮状态回调
    """
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1:
                return True

            return False

        return True

    raise PreventUpdate


@app.callback(
    Output({'type': 'job-operation-button', 'index': 'delete'}, 'disabled'),
    Input('job-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_job_delete_button_status(table_rows_selected):
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
    output=dict(
        modal_visible=Output('job-modal', 'visible', allow_duplicate=True),
        modal_title=Output('job-modal', 'title'),
        form_value=Output({'type': 'job-form-value', 'index': ALL}, 'value'),
        form_label_validate_status=Output({'type': 'job-form-label', 'index': ALL, 'required': True}, 'validateStatus', allow_duplicate=True),
        form_label_validate_info=Output({'type': 'job-form-label', 'index': ALL, 'required': True}, 'help', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        edit_row_info=Output('job-edit-id-store', 'data'),
        modal_type=Output('job-operations-store-bk', 'data')
    ),
    inputs=dict(
        operation_click=Input({'type': 'job-operation-button', 'index': ALL}, 'nClicks'),
        dropdown_click=Input('job-list-table', 'nClicksDropdownItem')
    ),
    state=dict(
        selected_row_keys=State('job-list-table', 'selectedRowKeys'),
        recently_clicked_dropdown_item_title=State('job-list-table', 'recentlyClickedDropdownItemTitle'),
        recently_dropdown_item_clicked_row=State('job-list-table', 'recentlyDropdownItemClickedRow')
    ),
    prevent_initial_call=True
)
def add_edit_job_modal(operation_click, dropdown_click, selected_row_keys, recently_clicked_dropdown_item_title,
                       recently_dropdown_item_clicked_row):
    """
    显示新增或编辑定时任务弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'add', 'type': 'job-operation-button'} \
            or trigger_id == {'index': 'edit', 'type': 'job-operation-button'} \
            or (trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '修改'):
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in dash.ctx.outputs_list[2]]
        # 获取所有输出表单项对应label的index
        form_label_list = [x['id']['index'] for x in dash.ctx.outputs_list[3]]
        if trigger_id == {'index': 'add', 'type': 'job-operation-button'}:
            job_info = dict(
                job_name=None,
                job_group=None,
                invoke_target=None,
                cron_expression=None,
                job_args=None,
                job_kwargs=None,
                misfire_policy='1',
                concurrent='1',
                status='0'
            )
            return dict(
                modal_visible=True,
                modal_title='新增任务',
                form_value=[job_info.get(k) for k in form_value_list],
                form_label_validate_status=[None] * len(form_label_list),
                form_label_validate_info=[None] * len(form_label_list),
                api_check_token_trigger=dash.no_update,
                edit_row_info=None,
                modal_type={'type': 'add'}
            )
        elif trigger_id == {'index': 'edit', 'type': 'job-operation-button'} or (trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'job-operation-button'}:
                job_id = int(','.join(selected_row_keys))
            else:
                job_id = int(recently_dropdown_item_clicked_row['key'])
            job_info_res = get_job_detail_api(job_id=job_id)
            if job_info_res['code'] == 200:
                job_info = job_info_res['data']
                return dict(
                    modal_visible=True,
                    modal_title='编辑任务',
                    form_value=[job_info.get(k) for k in form_value_list],
                    form_label_validate_status=[None] * len(form_label_list),
                    form_label_validate_info=[None] * len(form_label_list),
                    api_check_token_trigger={'timestamp': time.time()},
                    edit_row_info=job_info if job_info else None,
                    modal_type={'type': 'edit'}
                )

        return dict(
            modal_visible=dash.no_update,
            modal_title=dash.no_update,
            form_value=[dash.no_update] * len(form_value_list),
            form_label_validate_status=[dash.no_update] * len(form_label_list),
            form_label_validate_info=[dash.no_update] * len(form_label_list),
            api_check_token_trigger={'timestamp': time.time()},
            edit_row_info=None,
            modal_type=None
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        form_label_validate_status=Output({'type': 'job-form-label', 'index': ALL, 'required': True}, 'validateStatus',
                                          allow_duplicate=True),
        form_label_validate_info=Output({'type': 'job-form-label', 'index': ALL, 'required': True}, 'help',
                                        allow_duplicate=True),
        modal_visible=Output('job-modal', 'visible'),
        operations=Output('job-operations-store', 'data', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        confirm_trigger=Input('job-modal', 'okCounts')
    ),
    state=dict(
        modal_type=State('job-operations-store-bk', 'data'),
        edit_row_info=State('job-edit-id-store', 'data'),
        form_value=State({'type': 'job-form-value', 'index': ALL}, 'value'),
        form_label=State({'type': 'job-form-label', 'index': ALL, 'required': True}, 'label')
    ),
    prevent_initial_call=True
)
def job_confirm(confirm_trigger, modal_type, edit_row_info, form_value, form_label):
    """
    新增或编定时任务弹窗确认回调，实现新增或编辑操作
    """
    if confirm_trigger:
        # 获取所有输出表单项对应label的index
        form_label_output_list = [x['id']['index'] for x in dash.ctx.outputs_list[0]]
        # 获取所有输入表单项对应的value及label
        form_value_state = {x['id']['index']: x.get('value') for x in dash.ctx.states_list[-2]}
        form_label_state = {x['id']['index']: x.get('value') for x in dash.ctx.states_list[-1]}
        if all([form_value_state.get(k) for k in form_label_output_list]):
            params_add = form_value_state
            params_edit = params_add.copy()
            params_edit['job_id'] = edit_row_info.get('job_id') if edit_row_info else None
            api_res = {}
            modal_type = modal_type.get('type')
            if modal_type == 'add':
                api_res = add_job_api(params_add)
            if modal_type == 'edit':
                api_res = edit_job_api(params_edit)
            if api_res.get('code') == 200:
                if modal_type == 'add':
                    return dict(
                        form_label_validate_status=[None] * len(form_label_output_list),
                        form_label_validate_info=[None] * len(form_label_output_list),
                        modal_visible=False,
                        operations={'type': 'add'},
                        api_check_token_trigger={'timestamp': time.time()},
                        global_message_container=fuc.FefferyFancyMessage('新增成功', type='success')
                    )
                if modal_type == 'edit':
                    return dict(
                        form_label_validate_status=[None] * len(form_label_output_list),
                        form_label_validate_info=[None] * len(form_label_output_list),
                        modal_visible=False,
                        operations={'type': 'edit'},
                        api_check_token_trigger={'timestamp': time.time()},
                        global_message_container=fuc.FefferyFancyMessage('编辑成功', type='success')
                    )

            return dict(
                form_label_validate_status=[None] * len(form_label_output_list),
                form_label_validate_info=[None] * len(form_label_output_list),
                modal_visible=dash.no_update,
                operations=dash.no_update,
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage('处理失败', type='error')
            )

        return dict(
            form_label_validate_status=[None if form_value_state.get(k) else 'error' for k in form_label_output_list],
            form_label_validate_info=[None if form_value_state.get(k) else f'{form_label_state.get(k)}不能为空!' for k in form_label_output_list],
            modal_visible=dash.no_update,
            operations=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()},
            global_message_container=fuc.FefferyFancyMessage('处理失败', type='error')
        )

    raise PreventUpdate


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
    """
    表格内切换定时任务状态回调
    """
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
            {'type': 'switch-status'},
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('修改失败', type='error')
        ]

    raise PreventUpdate


@app.callback(
    output=dict(
        modal_visible=Output('job_detail-modal', 'visible', allow_duplicate=True),
        modal_title=Output('job_detail-modal', 'title'),
        form_value=Output({'type': 'job_detail-form-value', 'index': ALL}, 'children'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        dropdown_click=Input('job-list-table', 'nClicksDropdownItem')
    ),
    state=dict(
        recently_clicked_dropdown_item_title=State('job-list-table', 'recentlyClickedDropdownItemTitle'),
        recently_dropdown_item_clicked_row=State('job-list-table', 'recentlyDropdownItemClickedRow')
    ),
    prevent_initial_call=True
)
def get_job_detail_modal(dropdown_click, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row):
    """
    显示定时任务详情弹窗回调及执行一次定时任务回调
    """
    # 获取所有输出表单项对应value的index
    form_value_list = [x['id']['index'] for x in dash.ctx.outputs_list[-3]]
    # 显示定时任务详情弹窗
    if dropdown_click and recently_clicked_dropdown_item_title == '任务详细':
        job_id = int(recently_dropdown_item_clicked_row['key'])
        job_info_res = get_job_detail_api(job_id=job_id)
        if job_info_res['code'] == 200:
            job_info = job_info_res['data']
            if job_info.get('misfire_policy') == '1':
                job_info['misfire_policy'] = '立即执行'
            elif job_info.get('misfire_policy') == '2':
                job_info['misfire_policy'] = '执行一次'
            else:
                job_info['misfire_policy'] = '放弃执行'
            job_info['concurrent'] = '是' if job_info.get('concurrent') == '0' else '否'
            job_info['status'] = '正常' if job_info.get('status') == '0' else '停用'
            return dict(
                modal_visible=True,
                modal_title='任务详情',
                form_value=[job_info.get(k) for k in form_value_list],
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=None
            )

        return dict(
            modal_visible=dash.no_update,
            modal_title=dash.no_update,
            form_value=[dash.no_update] * len(form_value_list),
            api_check_token_trigger={'timestamp': time.time()},
            global_message_container=None
        )

    # 执行一次定时任务
    if dropdown_click and recently_clicked_dropdown_item_title == '执行一次':
        job_id = int(recently_dropdown_item_clicked_row['key'])
        job_info_res = execute_job_api(dict(job_id=job_id))
        if job_info_res['code'] == 200:
            return dict(
                modal_visible=False,
                modal_title=None,
                form_value=[None] * len(form_value_list),
                api_check_token_trigger={'timestamp': time.time()},
                global_message_container=fuc.FefferyFancyMessage('执行成功', type='success')
            )

        return dict(
            modal_visible=False,
            modal_title=None,
            form_value=[None] * len(form_value_list),
            api_check_token_trigger={'timestamp': time.time()},
            global_message_container=fuc.FefferyFancyMessage('执行失败', type='error')
        )

    raise PreventUpdate


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
    """
    显示删除定时任务二次确认弹窗回调
    """
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

    raise PreventUpdate


@app.callback(
    [Output('job-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job-delete-confirm-modal', 'okCounts'),
    State('job-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def job_delete_confirm(delete_confirm, job_ids_data):
    """
    删除定时任务弹窗确认回调，实现删除操作
    """
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

    raise PreventUpdate


@app.callback(
    output=dict(
        job_log_modal_visible=Output('job_to_job_log-modal', 'visible'),
        job_log_modal_title=Output('job_to_job_log-modal', 'title'),
        job_log_job_name=Output('job_log-job_name-input', 'value', allow_duplicate=True),
        job_log_job_group_options=Output('job_log-job_group-select', 'options'),
        job_log_search_nclick=Output('job_log-search', 'nClicks'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        operation_click=Input({'type': 'job-operation-log', 'index': ALL}, 'nClicks'),
        dropdown_click=Input('job-list-table', 'nClicksDropdownItem')
    ),
    state=dict(
        recently_clicked_dropdown_item_title=State('job-list-table', 'recentlyClickedDropdownItemTitle'),
        recently_dropdown_item_clicked_row=State('job-list-table', 'recentlyDropdownItemClickedRow'),
        job_log_search_nclick=State('job_log-search', 'nClicks')
    ),
    prevent_initial_call=True
)
def job_to_job_log_modal(operation_click, dropdown_click, recently_clicked_dropdown_item_title, recently_dropdown_item_clicked_row, job_log_search_nclick):
    """
    显示定时任务对应调度日志表格弹窗回调
    """

    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'log', 'type': 'job-operation-log'} or (trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '调度日志'):
        option_table = []
        info = query_dict_data_list_api(dict_type='sys_job_group')
        if info.get('code') == 200:
            data = info.get('data')
            option_table = [dict(label=item.get('dict_label'), value=item.get('dict_value')) for item in data]

            if trigger_id == 'job-list-table' and recently_clicked_dropdown_item_title == '调度日志':
                return dict(
                    job_log_modal_visible=True,
                    job_log_modal_title='任务调度日志',
                    job_log_job_name=recently_dropdown_item_clicked_row.get('job_name'),
                    job_log_job_group_options=option_table,
                    job_log_search_nclick=job_log_search_nclick + 1 if job_log_search_nclick else 1,
                    api_check_token_trigger={'timestamp': time.time()}
                )

        return dict(
            job_log_modal_visible=True,
            job_log_modal_title='任务调度日志',
            job_log_job_name=None,
            job_log_job_group_options=option_table,
            job_log_search_nclick=job_log_search_nclick + 1 if job_log_search_nclick else 1,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


@app.callback(
    [Output('job-export-container', 'data', allow_duplicate=True),
     Output('job-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('job-export', 'nClicks'),
    prevent_initial_call=True
)
def export_job_list(export_click):
    """
    导出定时任务信息回调
    """
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

    raise PreventUpdate


@app.callback(
    Output('job-export-container', 'data', allow_duplicate=True),
    Input('job-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_job_export_status(data):
    """
    导出完成后重置下载组件数据回调，防止重复下载文件
    """
    time.sleep(0.5)
    if data:
        return None

    raise PreventUpdate
