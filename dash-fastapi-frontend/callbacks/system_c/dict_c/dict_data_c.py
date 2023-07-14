import dash
import time
import uuid
from dash import html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc

from server import app
from api.dict import get_dict_data_list_api, get_dict_data_detail_api, add_dict_data_api, edit_dict_data_api, delete_dict_data_api


@app.callback(
    [Output('dict_data-list-table', 'data', allow_duplicate=True),
     Output('dict_data-list-table', 'pagination', allow_duplicate=True),
     Output('dict_data-list-table', 'key'),
     Output('dict_data-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('dict_data-search', 'nClicks'),
     Input('dict_data-list-table', 'pagination'),
     Input('dict_data-operations-store', 'data')],
    [State('dict_data-dict_type-select', 'value'),
     State('dict_data-dict_label-input', 'value'),
     State('dict_data-status-select', 'value'),
     State('dict_data-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_dict_data_table_data(search_click, pagination, operations, dict_type, dict_label, status_select, button_perms):

    query_params = dict(
        dict_type=dict_type,
        dict_label=dict_label,
        status=status_select,
        page_num=1,
        page_size=10
    )
    if pagination:
        query_params = dict(
            dict_type=dict_type,
            dict_label=dict_label,
            status=status_select,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or pagination or operations:
        table_info = get_dict_data_list_api(query_params)
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
                item['key'] = str(item['dict_code'])
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
    [Output('dict_data-dict_type-select', 'value', allow_duplicate=True),
     Output('dict_data-dict_label-input', 'value'),
     Output('dict_data-status-select', 'value'),
     Output('dict_data-operations-store', 'data')],
    Input('dict_data-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_dict_data_query_params(reset_click):
    if reset_click:
        return [None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 4


@app.callback(
    [Output('dict_data-edit', 'disabled'),
     Output('dict_data-delete', 'disabled')],
    Input('dict_data-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_dict_data_edit_delete_button_status(table_rows_selected):
    if table_rows_selected:
        if len(table_rows_selected) > 1:
            return [True, False]

        return [False, False]

    return [True, True]


@app.callback(
    [Output('dict_data-modal', 'visible', allow_duplicate=True),
     Output('dict_data-modal', 'title'),
     Output('dict_data-dict_type', 'value'),
     Output('dict_data-dict_label', 'value'),
     Output('dict_data-dict_value', 'value'),
     Output('dict_data-css_class', 'value'),
     Output('dict_data-dict_sort', 'value'),
     Output('dict_data-list_class', 'value'),
     Output('dict_data-status', 'value'),
     Output('dict_data-remark', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('dict_data-add', 'nClicks'),
     Output('dict_data-edit', 'nClicks'),
     Output('dict_data-edit-id-store', 'data'),
     Output('dict_data-operations-store-bk', 'data')],
    [Input('dict_data-add', 'nClicks'),
     Input('dict_data-edit', 'nClicks'),
     Input('dict_data-list-table', 'nClicksButton')],
    [State('dict_data-list-table', 'selectedRowKeys'),
     State('dict_data-list-table', 'clickedContent'),
     State('dict_data-list-table', 'recentlyButtonClickedRow'),
     State('dict_data-dict_type-select', 'value')],
    prevent_initial_call=True
)
def add_edit_dict_data_modal(add_click, edit_click, button_click, selected_row_keys, clicked_content,
                        recently_button_clicked_row, dict_type_select):
    if add_click or edit_click or button_click:
        if add_click:
            return [
                True,
                '新增字典数据',
                dict_type_select,
                None,
                None,
                None,
                0,
                'default',
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
                dict_code = int(','.join(selected_row_keys))
            else:
                dict_code = int(recently_button_clicked_row['key'])
            dict_data_info_res = get_dict_data_detail_api(dict_code=dict_code)
            if dict_data_info_res['code'] == 200:
                dict_data_info = dict_data_info_res['data']
                return [
                    True,
                    '编辑字典数据',
                    dict_data_info.get('dict_type'),
                    dict_data_info.get('dict_label'),
                    dict_data_info.get('dict_value'),
                    dict_data_info.get('css_class'),
                    dict_data_info.get('dict_sort'),
                    dict_data_info.get('list_class'),
                    dict_data_info.get('status'),
                    dict_data_info.get('remark'),
                    {'timestamp': time.time()},
                    None,
                    None,
                    dict_data_info if dict_data_info else None,
                    {'type': 'edit'}
                ]

        return [dash.no_update] * 10 + [{'timestamp': time.time()}, None, None, None, None]

    return [dash.no_update] * 11 + [None, None, None, None]


@app.callback(
    [Output('dict_data-dict_label-form-item', 'validateStatus'),
     Output('dict_data-dict_value-form-item', 'validateStatus'),
     Output('dict_data-dict_sort-form-item', 'validateStatus'),
     Output('dict_data-dict_label-form-item', 'help'),
     Output('dict_data-dict_value-form-item', 'help'),
     Output('dict_data-dict_sort-form-item', 'help'),
     Output('dict_data-modal', 'visible'),
     Output('dict_data-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dict_data-modal', 'okCounts'),
    [State('dict_data-operations-store-bk', 'data'),
     State('dict_data-edit-id-store', 'data'),
     State('dict_data-dict_type', 'value'),
     State('dict_data-dict_label', 'value'),
     State('dict_data-dict_value', 'value'),
     State('dict_data-css_class', 'value'),
     State('dict_data-dict_sort', 'value'),
     State('dict_data-list_class', 'value'),
     State('dict_data-status', 'value'),
     State('dict_data-remark', 'value')],
    prevent_initial_call=True
)
def dict_data_confirm(confirm_trigger, operation_type, cur_post_info, dict_type, dict_label, dict_value, css_class, dict_sort, list_class, status, remark):
    if confirm_trigger:
        if all([dict_label, dict_value, dict_sort]):
            params_add = dict(dict_type=dict_type, dict_label=dict_label, dict_value=dict_value, css_class=css_class, dict_sort=dict_sort, list_class=list_class, status=status, remark=remark)
            params_edit = dict(dict_code=cur_post_info.get('dict_code') if cur_post_info else None, dict_type=dict_type, dict_label=dict_label, dict_value=dict_value, css_class=css_class, dict_sort=dict_sort, list_class=list_class, status=status, remark=remark)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_dict_data_api(params_add)
            if operation_type == 'edit':
                api_res = edit_dict_data_api(params_edit)
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
            None if dict_label else 'error',
            None if dict_value else 'error',
            None if dict_sort else 'error',
            None if dict_label else '请输入数据标签！',
            None if dict_value else '请输入数据键值！',
            None if dict_sort else '请输入显示排序！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]

    return [dash.no_update] * 10


@app.callback(
    [Output('dict_data-delete-text', 'children'),
     Output('dict_data-delete-confirm-modal', 'visible'),
     Output('dict_data-delete-ids-store', 'data')],
    [Input('dict_data-delete', 'nClicks'),
     Input('dict_data-list-table', 'nClicksButton')],
    [State('dict_data-list-table', 'selectedRowKeys'),
     State('dict_data-list-table', 'clickedContent'),
     State('dict_data-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def dict_data_delete_modal(delete_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    if delete_click or button_click:
        trigger_id = dash.ctx.triggered_id

        if trigger_id == 'dict_data-delete':
            dict_codes = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                dict_codes = recently_button_clicked_row['key']
            else:
                return dash.no_update

        return [
            f'是否确认删除字典编码为{dict_codes}的数据？',
            True,
            {'dict_codes': dict_codes}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('dict_data-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('dict_data-delete-confirm-modal', 'okCounts'),
    State('dict_data-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def dict_data_delete_confirm(delete_confirm, dict_codes_data):
    if delete_confirm:

        params = dict_codes_data
        delete_button_info = delete_dict_data_api(params)
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
