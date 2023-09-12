import dash
import time
import uuid
from dash.dependencies import Input, Output, State, ALL, MATCH
import feffery_utils_components as fuc

from server import app
from api.user import get_allocated_role_list_api, get_unallocated_role_list_api, auth_role_select_all_api, auth_role_cancel_api


@app.callback(
    [Output({'type': 'allocate_role-list-table', 'index': MATCH}, 'data', allow_duplicate=True),
     Output({'type': 'allocate_role-list-table', 'index': MATCH}, 'pagination', allow_duplicate=True),
     Output({'type': 'allocate_role-list-table', 'index': MATCH}, 'key'),
     Output({'type': 'allocate_role-list-table', 'index': MATCH}, 'selectedRowKeys')],
    [Input({'type': 'allocate_role-search', 'index': MATCH}, 'nClicks'),
     Input({'type': 'allocate_role-refresh', 'index': MATCH}, 'nClicks'),
     Input({'type': 'allocate_role-list-table', 'index': MATCH}, 'pagination'),
     Input({'type': 'allocate_role-operations-container', 'index': MATCH}, 'data')],
    [State({'type': 'allocate_role-role_name-input', 'index': MATCH}, 'value'),
     State({'type': 'allocate_role-role_key-input', 'index': MATCH}, 'value'),
     State('allocate_role-user_id-container', 'data'),
     State('allocate_role-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_allocate_role_table_data(search_click, refresh_click, pagination, operations, role_name, role_key, user_id, button_perms):

    query_params = dict(
        user_id=int(user_id),
        role_name=role_name,
        role_key=role_key,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id.type == 'allocate_role-list-table':
        query_params = dict(
            user_id=int(user_id),
            role_name=role_name,
            role_key=role_key,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        table_info = {}
        if triggered_id.index == 'allocated':
            table_info = get_allocated_role_list_api(query_params)
        if triggered_id.index == 'unallocated':
            table_info = get_unallocated_role_list_api(query_params)
        if table_info.get('code') == 200:
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
                item['key'] = str(item['role_id'])
                if triggered_id.index == 'allocated':
                    item['operation'] = [
                        {
                            'content': '取消授权',
                            'type': 'link',
                            'icon': 'antd-close-circle'
                        } if 'system:user:edit' in button_perms else {},
                    ]

            return [table_data, table_pagination, str(uuid.uuid4()), None]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update]

    return [dash.no_update] * 4


app.clientside_callback(
    '''
    (reset_click) => {
        if (reset_click) {
            return [null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output({'type': 'allocate_role-role_name-input', 'index': MATCH}, 'value'),
     Output({'type': 'allocate_role-role_key-input', 'index': MATCH}, 'value'),
     Output({'type': 'allocate_role-operations-container', 'index': MATCH}, 'data')],
    Input({'type': 'allocate_role-reset', 'index': MATCH}, 'nClicks'),
    prevent_initial_call=True
)


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
    [Output({'type': 'allocate_role-search-form-container', 'index': MATCH}, 'hidden'),
     Output({'type': 'allocate_role-hidden-tooltip', 'index': MATCH}, 'title')],
    Input({'type': 'allocate_role-hidden', 'index': MATCH}, 'nClicks'),
    State({'type': 'allocate_role-search-form-container', 'index': MATCH}, 'hidden'),
    prevent_initial_call=True
)


@app.callback(
    Output({'type': 'allocate_role-operation-button', 'index': 'delete'}, 'disabled'),
    Input({'type': 'allocate_role-list-table', 'index': 'allocated'}, 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_allocated_role_delete_button_status(table_rows_selected):
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:
            return False

        return True

    return dash.no_update


@app.callback(
    [Output('allocate_role-modal', 'visible'),
     Output({'type': 'allocate_role-search', 'index': 'unallocated'}, 'nClicks')],
    Input('allocate_role-add', 'nClicks'),
    State({'type': 'allocate_role-search', 'index': 'unallocated'}, 'nClicks'),
    prevent_initial_call=True
)
def allocate_role_modal(add_click, unallocated_role):
    if add_click:

        return [True, unallocated_role + 1 if unallocated_role else 1]

    return [dash.no_update] * 2


@app.callback(
    [Output({'type': 'allocate_role-operations-container', 'index': 'allocated'}, 'data', allow_duplicate=True),
     Output({'type': 'allocate_role-operations-container', 'index': 'unallocated'}, 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('allocate_role-modal', 'okCounts'),
    [State({'type': 'allocate_role-list-table', 'index': 'unallocated'}, 'selectedRowKeys'),
     State('allocate_role-user_id-container', 'data')],
    prevent_initial_call=True
)
def allocate_user_add_confirm(add_confirm, selected_row_keys, user_id):
    if add_confirm:
        if selected_row_keys:

            params = {'user_ids': user_id, 'role_ids': ','.join(selected_row_keys)}
            add_button_info = auth_role_select_all_api(params)
            if add_button_info['code'] == 200:
                return [
                    {'type': 'delete'},
                    {'type': 'delete'},
                    {'timestamp': time.time()},
                    fuc.FefferyFancyMessage('授权成功', type='success')
                ]

            return [
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('授权失败', type='error')
            ]

        return [
            dash.no_update,
            dash.no_update,
            dash.no_update,
            fuc.FefferyFancyMessage('请选择角色', type='error')
        ]

    return [dash.no_update] * 4


@app.callback(
    [Output('allocate_role-delete-text', 'children'),
     Output('allocate_role-delete-confirm-modal', 'visible'),
     Output('allocate_role-delete-ids-store', 'data')],
    [Input({'type': 'allocate_role-operation-button', 'index': ALL}, 'nClicks'),
     Input({'type': 'allocate_role-list-table', 'index': 'allocated'}, 'nClicksButton')],
    [State({'type': 'allocate_role-list-table', 'index': 'allocated'}, 'selectedRowKeys'),
     State({'type': 'allocate_role-list-table', 'index': 'allocated'}, 'clickedContent'),
     State({'type': 'allocate_role-list-table', 'index': 'allocated'}, 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def allocate_role_delete_modal(operation_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    trigger_id = dash.ctx.triggered_id
    if trigger_id.type == 'allocate_role-operation-button' or (
            trigger_id.type == 'allocate_role-list-table' and clicked_content == '取消授权'):

        if trigger_id.type == 'allocate_role-operation-button':
            role_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '取消授权':
                role_ids = recently_button_clicked_row['key']
            else:
                return dash.no_update

        return [
            f'是否确认取消角色id为{role_ids}的授权？',
            True,
            role_ids
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output({'type': 'allocate_role-operations-container', 'index': 'allocated'}, 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('allocate_role-delete-confirm-modal', 'okCounts'),
    [State('allocate_role-delete-ids-store', 'data'),
     State('allocate_role-user_id-container', 'data')],
    prevent_initial_call=True
)
def allocate_role_delete_confirm(delete_confirm, role_ids_data, user_id):
    if delete_confirm:

        params = {'user_ids': user_id, 'role_ids': role_ids_data}
        delete_button_info = auth_role_cancel_api(params)
        if delete_button_info['code'] == 200:
            return [
                {'type': 'delete'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('取消授权成功', type='success')
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('取消授权失败', type='error')
        ]

    return [dash.no_update] * 3
