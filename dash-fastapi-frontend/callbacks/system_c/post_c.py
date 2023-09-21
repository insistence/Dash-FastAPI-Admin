import dash
import time
import uuid
from dash import dcc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from api.post import get_post_list_api, get_post_detail_api, add_post_api, edit_post_api, delete_post_api, export_post_list_api


@app.callback(
    output=dict(
        post_table_data=Output('post-list-table', 'data', allow_duplicate=True),
        post_table_pagination=Output('post-list-table', 'pagination', allow_duplicate=True),
        post_table_key=Output('post-list-table', 'key'),
        post_table_selectedrowkeys=Output('post-list-table', 'selectedRowKeys'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        search_click=Input('post-search', 'nClicks'),
        refresh_click=Input('post-refresh', 'nClicks'),
        pagination=Input('post-list-table', 'pagination'),
        operations=Input('post-operations-store', 'data')
    ),
    state=dict(
        post_code=State('post-post_code-input', 'value'),
        post_name=State('post-post_name-input', 'value'),
        status_select=State('post-status-select', 'value'),
        button_perms=State('post-button-perms-container', 'data')
    ),
    prevent_initial_call=True
)
def get_post_table_data(search_click, refresh_click, pagination, operations, post_code, post_name, status_select, button_perms):
    """
    获取岗位表格数据回调（进行表格相关增删查改操作后均会触发此回调）
    """

    query_params = dict(
        post_code=post_code,
        post_name=post_name,
        status=status_select,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'post-list-table':
        query_params = dict(
            post_code=post_code,
            post_name=post_name,
            status=status_select,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
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
            return dict(
                post_table_data=table_data,
                post_table_pagination=table_pagination,
                post_table_key=str(uuid.uuid4()),
                post_table_selectedrowkeys=None,
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            post_table_data=dash.no_update,
            post_table_pagination=dash.no_update,
            post_table_key=dash.no_update,
            post_table_selectedrowkeys=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


# 重置岗位搜索表单数据回调
app.clientside_callback(
    '''
    (reset_click) => {
        if (reset_click) {
            return [null, null, null, {'type': 'reset'}]
        }
        return window.dash_clientside.no_update;
    }
    ''',
    [Output('post-post_code-input', 'value'),
     Output('post-post_name-input', 'value'),
     Output('post-status-select', 'value'),
     Output('post-operations-store', 'data')],
    Input('post-reset', 'nClicks'),
    prevent_initial_call=True
)


# 隐藏/显示岗位搜索表单回调
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
    [Output('post-search-form-container', 'hidden'),
     Output('post-hidden-tooltip', 'title')],
    Input('post-hidden', 'nClicks'),
    State('post-search-form-container', 'hidden'),
    prevent_initial_call=True
)


@app.callback(
    Output({'type': 'post-operation-button', 'index': 'edit'}, 'disabled'),
    Input('post-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_post_edit_button_status(table_rows_selected):
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
    Output({'type': 'post-operation-button', 'index': 'delete'}, 'disabled'),
    Input('post-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_post_delete_button_status(table_rows_selected):
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
        modal_visible=Output('post-modal', 'visible', allow_duplicate=True),
        modal_title=Output('post-modal', 'title'),
        form_value=Output({'type': 'post-form-value', 'index': ALL}, 'value'),
        form_label_validate_status=Output({'type': 'post-form-label', 'index': ALL, 'required': True}, 'validateStatus', allow_duplicate=True),
        form_label_validate_info=Output({'type': 'post-form-label', 'index': ALL, 'required': True}, 'help', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        edit_row_info=Output('post-edit-id-store', 'data'),
        modal_type=Output('post-operations-store-bk', 'data')
    ),
    inputs=dict(
        operation_click=Input({'type': 'post-operation-button', 'index': ALL}, 'nClicks'),
        button_click=Input('post-list-table', 'nClicksButton')
    ),
    state=dict(
        selected_row_keys=State('post-list-table', 'selectedRowKeys'),
        clicked_content=State('post-list-table', 'clickedContent'),
        recently_button_clicked_row=State('post-list-table', 'recentlyButtonClickedRow')
    ),
    prevent_initial_call=True
)
def add_edit_post_modal(operation_click, button_click, selected_row_keys, clicked_content, recently_button_clicked_row):
    """
    显示新增或编辑岗位弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'add', 'type': 'post-operation-button'} \
            or trigger_id == {'index': 'edit', 'type': 'post-operation-button'} \
            or (trigger_id == 'post-list-table' and clicked_content == '修改'):
        # 获取所有输出表单项对应value的index
        form_value_list = [x['id']['index'] for x in dash.ctx.outputs_list[2]]
        # 获取所有输出表单项对应label的index
        form_label_list = [x['id']['index'] for x in dash.ctx.outputs_list[3]]
        if trigger_id == {'index': 'add', 'type': 'post-operation-button'}:
            post_info = dict(post_name=None, post_code=None, post_sort=0, status='0', remark=None)
            return dict(
                modal_visible=True,
                modal_title='新增岗位',
                form_value=[post_info.get(k) for k in form_value_list],
                form_label_validate_status=[None] * len(form_label_list),
                form_label_validate_info=[None] * len(form_label_list),
                api_check_token_trigger=dash.no_update,
                edit_row_info=None,
                modal_type={'type': 'add'}
            )
        elif trigger_id == {'index': 'edit', 'type': 'post-operation-button'} or (trigger_id == 'post-list-table' and clicked_content == '修改'):
            if trigger_id == {'index': 'edit', 'type': 'post-operation-button'}:
                post_id = int(','.join(selected_row_keys))
            else:
                post_id = int(recently_button_clicked_row['key'])
            post_info_res = get_post_detail_api(post_id=post_id)
            if post_info_res['code'] == 200:
                post_info = post_info_res['data']
                return dict(
                    modal_visible=True,
                    modal_title='编辑岗位',
                    form_value=[post_info.get(k) for k in form_value_list],
                    form_label_validate_status=[None] * len(form_label_list),
                    form_label_validate_info=[None] * len(form_label_list),
                    api_check_token_trigger={'timestamp': time.time()},
                    edit_row_info=post_info if post_info else None,
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
        form_label_validate_status=Output({'type': 'post-form-label', 'index': ALL, 'required': True}, 'validateStatus',
                                          allow_duplicate=True),
        form_label_validate_info=Output({'type': 'post-form-label', 'index': ALL, 'required': True}, 'help',
                                        allow_duplicate=True),
        modal_visible=Output('post-modal', 'visible'),
        operations=Output('post-operations-store', 'data', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        confirm_trigger=Input('post-modal', 'okCounts')
    ),
    state=dict(
        modal_type=State('post-operations-store-bk', 'data'),
        edit_row_info=State('post-edit-id-store', 'data'),
        form_value=State({'type': 'post-form-value', 'index': ALL}, 'value'),
        form_label=State({'type': 'post-form-label', 'index': ALL, 'required': True}, 'label')
    ),
    prevent_initial_call=True
)
def post_confirm(confirm_trigger, modal_type, edit_row_info, form_value, form_label):
    """
    新增或编辑岗位弹窗确认回调，实现新增或编辑操作
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
            params_edit['post_id'] = edit_row_info.get('post_id') if edit_row_info else None
            api_res = {}
            modal_type = modal_type.get('type')
            if modal_type == 'add':
                api_res = add_post_api(params_add)
            if modal_type == 'edit':
                api_res = edit_post_api(params_edit)
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
    [Output('post-delete-text', 'children'),
     Output('post-delete-confirm-modal', 'visible'),
     Output('post-delete-ids-store', 'data')],
    [Input({'type': 'post-operation-button', 'index': ALL}, 'nClicks'),
     Input('post-list-table', 'nClicksButton')],
    [State('post-list-table', 'selectedRowKeys'),
     State('post-list-table', 'clickedContent'),
     State('post-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def post_delete_modal(operation_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    """
    显示删除岗位二次确认弹窗回调
    """
    trigger_id = dash.ctx.triggered_id
    if trigger_id == {'index': 'delete', 'type': 'post-operation-button'} or (trigger_id == 'post-list-table' and clicked_content == '删除'):

        if trigger_id == {'index': 'delete', 'type': 'post-operation-button'}:
            post_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                post_ids = recently_button_clicked_row['key']
            else:
                raise PreventUpdate

        return [
            f'是否确认删除岗位编号为{post_ids}的岗位？',
            True,
            {'post_ids': post_ids}
        ]

    raise PreventUpdate


@app.callback(
    [Output('post-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('post-delete-confirm-modal', 'okCounts'),
    State('post-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def post_delete_confirm(delete_confirm, post_ids_data):
    """
    删除岗位弹窗确认回调，实现删除操作
    """
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

    raise PreventUpdate


@app.callback(
    [Output('post-export-container', 'data', allow_duplicate=True),
     Output('post-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('post-export', 'nClicks'),
    prevent_initial_call=True
)
def export_post_list(export_click):
    """
    导出岗位信息回调
    """
    if export_click:
        export_post_res = export_post_list_api({})
        if export_post_res.status_code == 200:
            export_post = export_post_res.content

            return [
                dcc.send_bytes(export_post, f'岗位信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
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
    Output('post-export-container', 'data', allow_duplicate=True),
    Input('post-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_post_export_status(data):
    """
    导出完成后重置下载组件数据回调，防止重复下载文件
    """
    time.sleep(0.5)
    if data:

        return None

    raise PreventUpdate
