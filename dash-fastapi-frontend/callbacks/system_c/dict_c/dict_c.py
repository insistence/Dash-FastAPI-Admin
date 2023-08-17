import dash
import time
import uuid
from dash import html, dcc
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc

from server import app
from api.dict import get_dict_type_list_api, get_all_dict_type_api, get_dict_type_detail_api, add_dict_type_api, edit_dict_type_api, delete_dict_type_api, export_dict_type_list_api


@app.callback(
    [Output('dict_type-list-table', 'data', allow_duplicate=True),
     Output('dict_type-list-table', 'pagination', allow_duplicate=True),
     Output('dict_type-list-table', 'key'),
     Output('dict_type-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('dict_type-search', 'nClicks'),
     Input('dict_type-refresh', 'nClicks'),
     Input('dict_type-list-table', 'pagination'),
     Input('dict_type-operations-store', 'data')],
    [State('dict_type-dict_name-input', 'value'),
     State('dict_type-dict_type-input', 'value'),
     State('dict_type-status-select', 'value'),
     State('dict_type-create_time-range', 'value'),
     State('dict_type-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_dict_type_table_data(search_click, refresh_click, pagination, operations, dict_name, dict_type, status_select, create_time_range, button_perms):
    create_time_start = None
    create_time_end = None
    if create_time_range:
        create_time_start = create_time_range[0]
        create_time_end = create_time_range[1]

    query_params = dict(
        dict_name=dict_name,
        dict_type=dict_type,
        status=status_select,
        create_time_start=create_time_start,
        create_time_end=create_time_end,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'dict_type-list-table':
        query_params = dict(
            dict_name=dict_name,
            dict_type=dict_type,
            status=status_select,
            create_time_start=create_time_start,
            create_time_end=create_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        table_info = get_dict_type_list_api(query_params)
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
                    item['status'] = dict(tag='正常', color='blue')
                else:
                    item['status'] = dict(tag='停用', color='volcano')
                item['key'] = str(item['dict_id'])
                item['dict_type'] = {
                    'content': item['dict_type'],
                    'type': 'link',
                }
                item['operation'] = [
                    {
                        'content': '修改',
                        'type': 'link',
                        'icon': 'antd-edit'
                    } if 'system:dict:edit' in button_perms else {},
                    {
                        'content': '删除',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'system:dict:remove' in button_perms else {},
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('dict_type-dict_name-input', 'value'),
     Output('dict_type-dict_type-input', 'value'),
     Output('dict_type-status-select', 'value'),
     Output('dict_type-create_time-range', 'value'),
     Output('dict_type-operations-store', 'data')],
    Input('dict_type-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_dict_type_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 5


@app.callback(
    [Output('dict_type-search-form-container', 'hidden'),
     Output('dict_type-hidden-tooltip', 'title')],
    Input('dict_type-hidden', 'nClicks'),
    State('dict_type-search-form-container', 'hidden'),
    prevent_initial_call=True
)
def hidden_dict_type_search_form(hidden_click, hidden_status):
    if hidden_click:

        return [not hidden_status, '隐藏搜索' if hidden_status else '显示搜索']
    return [dash.no_update] * 2


@app.callback(
    [Output('dict_type-edit', 'disabled'),
     Output('dict_type-delete', 'disabled')],
    Input('dict_type-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_dict_type_edit_delete_button_status(table_rows_selected):
    if table_rows_selected:
        if len(table_rows_selected) > 1:
            return [True, False]

        return [False, False]

    return [True, True]


@app.callback(
    [Output('dict_type-modal', 'visible', allow_duplicate=True),
     Output('dict_type-modal', 'title'),
     Output('dict_type-dict_name', 'value'),
     Output('dict_type-dict_type', 'value'),
     Output('dict_type-status', 'value'),
     Output('dict_type-remark', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('dict_type-add', 'nClicks'),
     Output('dict_type-edit', 'nClicks'),
     Output('dict_type-edit-id-store', 'data'),
     Output('dict_type-operations-store-bk', 'data')],
    [Input('dict_type-add', 'nClicks'),
     Input('dict_type-edit', 'nClicks'),
     Input('dict_type-list-table', 'nClicksButton')],
    [State('dict_type-list-table', 'selectedRowKeys'),
     State('dict_type-list-table', 'clickedContent'),
     State('dict_type-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_dict_type_modal(add_click, edit_click, button_click, selected_row_keys, clicked_content,
                        recently_button_clicked_row):
    if add_click or edit_click or button_click:
        if add_click:
            return [
                True,
                '新增字典类型',
                None,
                None,
                '0',
                None,
                {'timestamp': time.time()},
                None,
                None,
                None,
                {'type': 'add'}
            ]
        elif edit_click or (button_click and clicked_content == '修改'):
            if edit_click:
                dict_id = int(','.join(selected_row_keys))
            else:
                dict_id = int(recently_button_clicked_row['key'])
            dict_type_info_res = get_dict_type_detail_api(dict_id=dict_id)
            if dict_type_info_res['code'] == 200:
                dict_type_info = dict_type_info_res['data']
                return [
                    True,
                    '编辑字典类型',
                    dict_type_info.get('dict_name'),
                    dict_type_info.get('dict_type'),
                    dict_type_info.get('status'),
                    dict_type_info.get('remark'),
                    {'timestamp': time.time()},
                    None,
                    None,
                    dict_type_info if dict_type_info else None,
                    {'type': 'edit'}
                ]

        return [dash.no_update] * 6 + [{'timestamp': time.time()}, None, None, None, None]

    return [dash.no_update] * 7 + [None, None, None, None]


@app.callback(
    [Output('dict_type-dict_name-form-item', 'validateStatus'),
     Output('dict_type-dict_type-form-item', 'validateStatus'),
     Output('dict_type-dict_name-form-item', 'help'),
     Output('dict_type-dict_type-form-item', 'help'),
     Output('dict_type-modal', 'visible'),
     Output('dict_type-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dict_type-modal', 'okCounts'),
    [State('dict_type-operations-store-bk', 'data'),
     State('dict_type-edit-id-store', 'data'),
     State('dict_type-dict_name', 'value'),
     State('dict_type-dict_type', 'value'),
     State('dict_type-status', 'value'),
     State('dict_type-remark', 'value')],
    prevent_initial_call=True
)
def dict_type_confirm(confirm_trigger, operation_type, cur_post_info, dict_name, dict_type, status, remark):
    if confirm_trigger:
        if all([dict_name, dict_type]):
            params_add = dict(dict_name=dict_name, dict_type=dict_type, status=status, remark=remark)
            params_edit = dict(dict_id=cur_post_info.get('dict_id') if cur_post_info else None, dict_name=dict_name,
                               dict_type=dict_type, status=status, remark=remark)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_dict_type_api(params_add)
            if operation_type == 'edit':
                api_res = edit_dict_type_api(params_edit)
            if api_res.get('code') == 200:
                if operation_type == 'add':
                    return [
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
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('处理失败', type='error')
            ]

        return [
            None if dict_name else 'error',
            None if dict_type else 'error',
            None if dict_name else '请输入字典名称！',
            None if dict_type else '请输入字典类型！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]

    return [dash.no_update] * 8


@app.callback(
    [Output('dict_type-delete-text', 'children'),
     Output('dict_type-delete-confirm-modal', 'visible'),
     Output('dict_type-delete-ids-store', 'data')],
    [Input('dict_type-delete', 'nClicks'),
     Input('dict_type-list-table', 'nClicksButton')],
    [State('dict_type-list-table', 'selectedRowKeys'),
     State('dict_type-list-table', 'clickedContent'),
     State('dict_type-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def dict_type_delete_modal(delete_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    if delete_click or button_click:
        trigger_id = dash.ctx.triggered_id

        if trigger_id == 'dict_type-delete':
            dict_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                dict_ids = recently_button_clicked_row['key']
            else:
                return dash.no_update

        return [
            f'是否确认删除字典编号为{dict_ids}的岗位？',
            True,
            {'dict_ids': dict_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('dict_type-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dict_type-delete-confirm-modal', 'okCounts'),
    State('dict_type-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def dict_type_delete_confirm(delete_confirm, dict_ids_data):
    if delete_confirm:

        params = dict_ids_data
        delete_button_info = delete_dict_type_api(params)
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
    [Output('dict_type_to_dict_data-modal', 'visible'),
     Output('dict_type_to_dict_data-modal', 'title'),
     Output('dict_data-dict_type-select', 'options'),
     Output('dict_data-dict_type-select', 'value', allow_duplicate=True),
     Output('dict_data-search', 'nClicks'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    Input('dict_type-list-table', 'nClicksButton'),
    [State('dict_type-list-table', 'clickedContent'),
     State('dict_type-list-table', 'recentlyButtonClickedRow'),
     State('dict_data-search', 'nClicks')],
    prevent_initial_call=True
)
def dict_type_to_dict_data_modal(button_click, clicked_content, recently_button_clicked_row, dict_data_search_nclick):

    if button_click and clicked_content == recently_button_clicked_row.get('dict_type').get('content'):
        all_dict_type_info = get_all_dict_type_api({})
        if all_dict_type_info.get('code') == 200:
            all_dict_type = all_dict_type_info.get('data')
            dict_data_options = [dict(label=item.get('dict_name'), value=item.get('dict_type')) for item in all_dict_type]

            return [
                True,
                '字典数据',
                dict_data_options,
                recently_button_clicked_row.get('dict_type').get('content'),
                dict_data_search_nclick + 1 if dict_data_search_nclick else 1,
                {'timestamp': time.time()},
            ]

        return [
                True,
                '字典数据',
                [],
                recently_button_clicked_row.get('dict_type').get('content'),
                dict_data_search_nclick + 1 if dict_data_search_nclick else 1,
                {'timestamp': time.time()},
            ]

    return [dash.no_update] * 6


@app.callback(
    [Output('dict_type-export-container', 'data', allow_duplicate=True),
     Output('dict_type-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dict_type-export', 'nClicks'),
    prevent_initial_call=True
)
def export_dict_type_list(export_click):
    if export_click:
        export_dict_type_res = export_dict_type_list_api({})
        if export_dict_type_res.status_code == 200:
            export_dict_type = export_dict_type_res.content

            return [
                dcc.send_bytes(export_dict_type, f'字典类型信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
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
    Output('dict_type-export-container', 'data', allow_duplicate=True),
    Input('dict_type-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_dict_type_export_status(data):
    time.sleep(0.5)
    if data:

        return None

    return dash.no_update
