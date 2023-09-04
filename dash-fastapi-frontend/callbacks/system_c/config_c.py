import dash
import time
import uuid
from dash import dcc
from dash.dependencies import Input, Output, State, ALL
import feffery_utils_components as fuc

from server import app
from api.config import get_config_list_api, get_config_detail_api, add_config_api, edit_config_api, delete_config_api, export_config_list_api, refresh_config_api


@app.callback(
    [Output('config-list-table', 'data', allow_duplicate=True),
     Output('config-list-table', 'pagination', allow_duplicate=True),
     Output('config-list-table', 'key'),
     Output('config-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('config-search', 'nClicks'),
     Input('config-refresh', 'nClicks'),
     Input('config-list-table', 'pagination'),
     Input('config-operations-store', 'data')],
    [State('config-config_name-input', 'value'),
     State('config-config_key-input', 'value'),
     State('config-config_type-select', 'value'),
     State('config-create_time-range', 'value'),
     State('config-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_config_table_data(search_click, refresh_click, pagination, operations, config_name, config_key, config_type, create_time_range, button_perms):
    create_time_start = None
    create_time_end = None
    if create_time_range:
        create_time_start = create_time_range[0]
        create_time_end = create_time_range[1]

    query_params = dict(
        config_name=config_name,
        config_key=config_key,
        config_type=config_type,
        create_time_start=create_time_start,
        create_time_end=create_time_end,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'config-list-table':
        query_params = dict(
            config_name=config_name,
            config_key=config_key,
            config_type=config_type,
            create_time_start=create_time_start,
            create_time_end=create_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        table_info = get_config_list_api(query_params)
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
                if item['config_type'] == 'Y':
                    item['config_type'] = dict(tag='是', color='blue')
                else:
                    item['config_type'] = dict(tag='否', color='volcano')
                item['key'] = str(item['config_id'])
                item['operation'] = [
                    {
                        'content': '修改',
                        'type': 'link',
                        'icon': 'antd-edit'
                    } if 'system:config:edit' in button_perms else {},
                    {
                        'content': '删除',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'system:config:remove' in button_perms else {},
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('config-config_name-input', 'value'),
     Output('config-config_key-input', 'value'),
     Output('config-config_type-select', 'value'),
     Output('config-create_time-range', 'value'),
     Output('config-operations-store', 'data')],
    Input('config-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_config_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 5


@app.callback(
    [Output('config-search-form-container', 'hidden'),
     Output('config-hidden-tooltip', 'title')],
    Input('config-hidden', 'nClicks'),
    State('config-search-form-container', 'hidden'),
    prevent_initial_call=True
)
def hidden_config_search_form(hidden_click, hidden_status):
    if hidden_click:

        return [not hidden_status, '隐藏搜索' if hidden_status else '显示搜索']
    return [dash.no_update] * 2


@app.callback(
    Output({'type': 'config-operation-button', 'index': 'edit'}, 'disabled'),
    Input('config-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_config_edit_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1:
                return True

            return False

        return True

    return dash.no_update


@app.callback(
    Output({'type': 'config-operation-button', 'index': 'delete'}, 'disabled'),
    Input('config-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_config_delete_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            if len(table_rows_selected) > 1:
                return False

            return False

        return True

    return dash.no_update


@app.callback(
    [Output('config-modal', 'visible', allow_duplicate=True),
     Output('config-modal', 'title'),
     Output('config-config_name', 'value'),
     Output('config-config_key', 'value'),
     Output('config-config_value', 'value'),
     Output('config-config_type', 'value'),
     Output('config-remark', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('config-edit-id-store', 'data'),
     Output('config-operations-store-bk', 'data')],
    [Input({'type': 'config-operation-button', 'index': ALL}, 'nClicks'),
     Input('config-list-table', 'nClicksButton')],
    [State('config-list-table', 'selectedRowKeys'),
     State('config-list-table', 'clickedContent'),
     State('config-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_config_modal(operation_click, button_click, selected_row_keys, clicked_content, recently_button_clicked_row):
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'add', 'type': 'config-operation-button'} \
            or trigger_id == {'index': 'edit', 'type': 'config-operation-button'} \
            or (trigger_id == 'config-list-table' and clicked_content == '修改'):
        if trigger_id == {'index': 'add', 'type': 'config-operation-button'}:
            return [
                True,
                '新增参数',
                None,
                None,
                None,
                'Y',
                None,
                dash.no_update,
                None,
                {'type': 'add'}
            ]
        elif trigger_id == {'index': 'edit', 'type': 'config-operation-button'} or (trigger_id == 'config-list-table' and clicked_content == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'config-operation-button'}:
                config_id = int(','.join(selected_row_keys))
            else:
                config_id = int(recently_button_clicked_row['key'])
            config_info_res = get_config_detail_api(config_id=config_id)
            if config_info_res['code'] == 200:
                config_info = config_info_res['data']
                return [
                    True,
                    '编辑参数',
                    config_info.get('config_name'),
                    config_info.get('config_key'),
                    config_info.get('config_value'),
                    config_info.get('config_type'),
                    config_info.get('remark'),
                    {'timestamp': time.time()},
                    config_info if config_info else None,
                    {'type': 'edit'}
                ]

        return [dash.no_update] * 7 + [{'timestamp': time.time()}, None, None]

    return [dash.no_update] * 8 + [None, None]


@app.callback(
    [Output('config-config_name-form-item', 'validateStatus'),
     Output('config-config_key-form-item', 'validateStatus'),
     Output('config-config_value-form-item', 'validateStatus'),
     Output('config-config_name-form-item', 'help'),
     Output('config-config_key-form-item', 'help'),
     Output('config-config_value-form-item', 'help'),
     Output('config-modal', 'visible'),
     Output('config-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('config-modal', 'okCounts'),
    [State('config-operations-store-bk', 'data'),
     State('config-edit-id-store', 'data'),
     State('config-config_name', 'value'),
     State('config-config_key', 'value'),
     State('config-config_value', 'value'),
     State('config-config_type', 'value'),
     State('config-remark', 'value')],
    prevent_initial_call=True
)
def dict_type_confirm(confirm_trigger, operation_type, cur_config_info, config_name, config_key, config_value, config_type, remark):
    if confirm_trigger:
        if all([config_name, config_key, config_value]):
            params_add = dict(config_name=config_name, config_key=config_key, config_value=config_value,
                              config_type=config_type, remark=remark)
            params_edit = dict(config_id=cur_config_info.get('config_id') if cur_config_info else None,
                               config_name=config_name, config_key=config_key, config_value=config_value,
                               config_type=config_type, remark=remark)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_config_api(params_add)
            if operation_type == 'edit':
                api_res = edit_config_api(params_edit)
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
            None if config_name else 'error',
            None if config_key else 'error',
            None if config_value else 'error',
            None if config_name else '请输入参数名称！',
            None if config_key else '请输入参数键名！',
            None if config_value else '请输入参数键值！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]

    return [dash.no_update] * 10


@app.callback(
    [Output('config-delete-text', 'children'),
     Output('config-delete-confirm-modal', 'visible'),
     Output('config-delete-ids-store', 'data')],
    [Input({'type': 'config-operation-button', 'index': ALL}, 'nClicks'),
     Input('config-list-table', 'nClicksButton')],
    [State('config-list-table', 'selectedRowKeys'),
     State('config-list-table', 'clickedContent'),
     State('config-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def config_delete_modal(operation_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'config-operation-button'} or (
            trigger_id == 'config-list-table' and clicked_content == '删除'):

        if trigger_id == {'index': 'delete', 'type': 'config-operation-button'}:
            config_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                config_ids = recently_button_clicked_row['key']
            else:
                return dash.no_update

        return [
            f'是否确认删除参数编号为{config_ids}的参数设置？',
            True,
            {'config_ids': config_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('config-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('config-delete-confirm-modal', 'okCounts'),
    State('config-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def config_delete_confirm(delete_confirm, config_ids_data):
    if delete_confirm:

        params = config_ids_data
        delete_button_info = delete_config_api(params)
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
    [Output('config-export-container', 'data', allow_duplicate=True),
     Output('config-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('config-export', 'nClicks'),
    prevent_initial_call=True
)
def export_config_list(export_click):
    if export_click:
        export_config_res = export_config_list_api({})
        if export_config_res.status_code == 200:
            export_config = export_config_res.content

            return [
                dcc.send_bytes(export_config, f'参数配置信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
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
    Output('config-export-container', 'data', allow_duplicate=True),
    Input('config-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_config_export_status(data):
    time.sleep(0.5)
    if data:

        return None

    return dash.no_update


@app.callback(
    [Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('config-refresh-cache', 'nClicks'),
    prevent_initial_call=True
)
def refresh_config_cache(refresh_click):
    if refresh_click:
        refresh_info_res = refresh_config_api({})
        if refresh_info_res.get('code') == 200:
            return [
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('刷新成功', type='success')
            ]

        return [
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('刷新失败', type='error')
        ]

    return [dash.no_update] * 2
