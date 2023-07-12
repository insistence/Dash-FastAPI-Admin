import dash
import time
import uuid
from dash import html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc

from server import app
from api.post import get_post_list_api, get_post_detail_api, add_post_api, edit_post_api, delete_post_api


@app.callback(
    [Output('post-list-table', 'data', allow_duplicate=True),
     Output('post-list-table', 'pagination', allow_duplicate=True),
     Output('post-list-table', 'key'),
     Output('post-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('post-search', 'nClicks'),
     Input('post-list-table', 'pagination'),
     Input('post-operations-store', 'data')],
    [State('post-post_code-input', 'value'),
     State('post-post_name-input', 'value'),
     State('post-status-select', 'value'),
     State('post-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_post_table_data(search_click, pagination, operations, post_code, post_name, status_select, button_perms):

    query_params = dict(
        post_code=post_code,
        post_name=post_name,
        status=status_select,
        page_num=1,
        page_size=10
    )
    if pagination:
        query_params = dict(
            post_code=post_code,
            post_name=post_name,
            status=status_select,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or pagination or operations:
        table_info = get_post_list_api(query_params)
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
                item['key'] = str(item['post_id'])
                item['operation'] = [
                    {
                        'content': '修改',
                        'type': 'link',
                        'icon': 'antd-edit'
                    } if 'system:post:edit' in button_perms else {},
                    {
                        'content': '删除',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'system:post:remove' in button_perms else {},
                ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('post-post_code-input', 'value'),
     Output('post-post_name-input', 'value'),
     Output('post-status-select', 'value'),
     Output('post-operations-store', 'data')],
    Input('post-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_post_query_params(reset_click):
    if reset_click:
        return [None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 4


@app.callback(
    [Output('post-edit', 'disabled'),
     Output('post-delete', 'disabled')],
    Input('post-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_post_edit_delete_button_status(table_rows_selected):
    if table_rows_selected:
        if len(table_rows_selected) > 1:
            return [True, False]

        return [False, False]

    return [True, True]


@app.callback(
    [Output('post-modal', 'visible', allow_duplicate=True),
     Output('post-modal', 'title'),
     Output('post-post_name', 'value'),
     Output('post-post_code', 'value'),
     Output('post-post_sort', 'value'),
     Output('post-status', 'value'),
     Output('post-remark', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('post-add', 'nClicks'),
     Output('post-edit', 'nClicks'),
     Output('post-edit-id-store', 'data'),
     Output('post-operations-store-bk', 'data')],
    [Input('post-add', 'nClicks'),
     Input('post-edit', 'nClicks'),
     Input('post-list-table', 'nClicksButton')],
    [State('post-list-table', 'selectedRowKeys'),
     State('post-list-table', 'clickedContent'),
     State('post-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_post_modal(add_click, edit_click, button_click, selected_row_keys, clicked_content, recently_button_clicked_row):
    if add_click or edit_click or button_click:
        if add_click:
            return [
                True,
                '新增岗位',
                None,
                None,
                0,
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
                post_id = int(','.join(selected_row_keys))
            else:
                post_id = int(recently_button_clicked_row['key'])
            post_info_res = get_post_detail_api(post_id=post_id)
            if post_info_res['code'] == 200:
                post_info = post_info_res['data']
                return [
                    True,
                    '编辑岗位',
                    post_info.get('post_name'),
                    post_info.get('post_code'),
                    post_info.get('post_sort'),
                    post_info.get('status'),
                    post_info.get('remark'),
                    {'timestamp': time.time()},
                    None,
                    None,
                    post_info if post_info else None,
                    {'type': 'edit'}
                ]
                    
        return [dash.no_update] * 7 + [{'timestamp': time.time()}, None, None, None, None]

    return [dash.no_update] * 8 + [None, None, None, None]


@app.callback(
    [Output('post-post_name-form-item', 'validateStatus'),
     Output('post-post_code-form-item', 'validateStatus'),
     Output('post-post_sort-form-item', 'validateStatus'),
     Output('post-post_name-form-item', 'help'),
     Output('post-post_code-form-item', 'help'),
     Output('post-post_sort-form-item', 'help'),
     Output('post-modal', 'visible'),
     Output('post-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('post-modal', 'okCounts'),
    [State('post-operations-store-bk', 'data'),
     State('post-edit-id-store', 'data'),
     State('post-post_name', 'value'),
     State('post-post_code', 'value'),
     State('post-post_sort', 'value'),
     State('post-status', 'value'),
     State('post-remark', 'value')],
    prevent_initial_call=True
)
def post_confirm(confirm_trigger, operation_type, cur_post_info, post_name, post_code, post_sort, status, remark):
    if confirm_trigger:
        if all([post_name, post_code, post_sort]):
            params_add = dict(post_name=post_name, post_code=post_code, post_sort=post_sort, status=status, remark=remark)
            params_edit = dict(post_id=cur_post_info.get('post_id') if cur_post_info else None, post_name=post_name, 
                               post_code=post_code, post_sort=post_sort, status=status, remark=remark)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_post_api(params_add)
            if operation_type == 'edit':
                api_res = edit_post_api(params_edit)
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
            None if post_name else 'error',
            None if post_code else 'error',
            None if post_sort else 'error',
            None if post_name else '请输入岗位名称！',
            None if post_code else '请输入岗位编码！',
            None if post_sort else '请输入岗位顺序！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]         

    return [dash.no_update] * 10


@app.callback(
    [Output('post-delete-text', 'children'),
     Output('post-delete-confirm-modal', 'visible'),
     Output('post-delete-ids-store', 'data')],
    [Input('post-delete', 'nClicks'),
     Input('post-list-table', 'nClicksButton')],
    [State('post-list-table', 'selectedRowKeys'),
     State('post-list-table', 'clickedContent'),
     State('post-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def post_delete_modal(delete_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    if delete_click or button_click:
        trigger_id = dash.ctx.triggered_id

        if trigger_id == 'post-delete':
            post_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                post_ids = recently_button_clicked_row['key']
            else:
                return dash.no_update

        return [
            f'是否确认删除岗位编号为{post_ids}的岗位？',
            True,
            {'post_ids': post_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('post-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('post-delete-confirm-modal', 'okCounts'),
    State('post-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def post_delete_confirm(delete_confirm, post_ids_data):
    if delete_confirm:

        params = post_ids_data
        delete_button_info = delete_post_api(params)
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
