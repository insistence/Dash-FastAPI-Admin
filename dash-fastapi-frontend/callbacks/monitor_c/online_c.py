import dash
import time
import uuid
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from api.online import get_online_list_api, force_logout_online_api, batch_logout_online_api


@app.callback(
    output=dict(
        online_table_data=Output('online-list-table', 'data', allow_duplicate=True),
        online_table_pagination=Output('online-list-table', 'pagination', allow_duplicate=True),
        online_table_key=Output('online-list-table', 'key'),
        online_table_selectedrowkeys=Output('online-list-table', 'selectedRowKeys'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        search_click=Input('online-search', 'nClicks'),
        refresh_click=Input('online-refresh', 'nClicks'),
        pagination=Input('online-list-table', 'pagination'),
        operations=Input('online-operations-store', 'data')
    ),
    state=dict(
        ipaddr=State('online-ipaddr-input', 'value'),
        user_name=State('online-user_name-input', 'value'),
        button_perms=State('online-button-perms-container', 'data')
    ),
    prevent_initial_call=True
)
def get_online_table_data(search_click, refresh_click, pagination, operations, ipaddr, user_name, button_perms):
    """
    获取在线用户表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """
    query_params = dict(
        ipaddr=ipaddr,
        user_name=user_name,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'online-list-table':
        query_params = dict(
            ipaddr=ipaddr,
            user_name=user_name,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        table_info = get_online_list_api(query_params)
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
                item['key'] = str(item['session_id'])
                item['operation'] = [
                    {
                        'content': '强退',
                        'type': 'link',
                        'icon': 'antd-delete'
                    } if 'monitor:online:forceLogout' in button_perms else {},
                ]

            return dict(
                online_table_data=table_data,
                online_table_pagination=table_pagination,
                online_table_key=str(uuid.uuid4()),
                online_table_selectedrowkeys=None,
                api_check_token_trigger= {'timestamp': time.time()}
            )

        return dict(
            online_table_data=dash.no_update,
            online_table_pagination=dash.no_update,
            online_table_key=dash.no_update,
            online_table_selectedrowkeys=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


# 重置在线用户搜索表单数据回调
app.clientside_callback(
    '''
    (reset_click) => {
        if (reset_click) {
            return [null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('online-ipaddr-input', 'value'),
     Output('online-user_name-input', 'value'),
     Output('online-operations-store', 'data')],
    Input('online-reset', 'nClicks'),
    prevent_initial_call=True
)


# 隐藏/显示在线用户搜索表单回调
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
    [Output('online-search-form-container', 'hidden'),
     Output('online-hidden-tooltip', 'title')],
    Input('online-hidden', 'nClicks'),
    State('online-search-form-container', 'hidden'),
    prevent_initial_call=True
)


@app.callback(
    Output({'type': 'online-operation-button', 'index': 'delete'}, 'disabled'),
    Input('online-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_online_edit_delete_button_status(table_rows_selected):
    """
    根据选择的表格数据行数控制批量强退按钮状态回调
    """
    outputs_list = dash.ctx.outputs_list
    if outputs_list:
        if table_rows_selected:

            return False

        return True

    raise PreventUpdate


@app.callback(
    [Output('online-delete-text', 'children'),
     Output('online-delete-confirm-modal', 'visible'),
     Output('online-delete-ids-store', 'data')],
    [Input({'type': 'online-operation-button', 'index': ALL}, 'nClicks'),
     Input('online-list-table', 'nClicksButton')],
    [State('online-list-table', 'selectedRowKeys'),
     State('online-list-table', 'clickedContent'),
     State('online-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def online_delete_modal(operation_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    """
    显示强退在线用户二次确认弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'online-operation-button'} or (
            trigger_id == 'online-list-table' and clicked_content == '强退'):
        logout_type = ''

        if trigger_id == {'index': 'delete', 'type': 'online-operation-button'}:
            session_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '强退':
                session_ids = recently_button_clicked_row['key']
                logout_type = 'force'
            else:
                return dash.no_update

        return [
            f'是否确认强退会话编号为{session_ids}的会话？',
            True,
            {'session_ids': session_ids, 'logout_type': logout_type}
        ]

    raise PreventUpdate


@app.callback(
    [Output('online-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('online-delete-confirm-modal', 'okCounts'),
    State('online-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def online_delete_confirm(delete_confirm, session_ids_data):
    """
    强退在线用户弹窗确认回调，实现强退操作
    """
    if delete_confirm:

        params = dict(session_ids=session_ids_data.get('session_ids'))
        logout_type = session_ids_data.get('logout_type')
        if logout_type == 'force':
            delete_button_info = force_logout_online_api(params)
        else:
            delete_button_info = batch_logout_online_api(params)
        if delete_button_info['code'] == 200:
            return [
                {'type': 'force'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage('强退成功', type='success')
            ]

        return [
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('强退失败', type='error')
        ]

    raise PreventUpdate
