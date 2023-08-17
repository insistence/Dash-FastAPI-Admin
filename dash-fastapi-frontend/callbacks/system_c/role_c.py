import dash
import time
import uuid
from dash import html, dcc
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc

from server import app
from api.role import get_role_list_api, get_role_detail_api, add_role_api, edit_role_api, delete_role_api, export_role_list_api
from api.menu import get_menu_tree_api


@app.callback(
    [Output('role-list-table', 'data', allow_duplicate=True),
     Output('role-list-table', 'pagination', allow_duplicate=True),
     Output('role-list-table', 'key'),
     Output('role-list-table', 'selectedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('role-search', 'nClicks'),
     Input('role-refresh', 'nClicks'),
     Input('role-list-table', 'pagination'),
     Input('role-operations-store', 'data')],
    [State('role-role_name-input', 'value'),
     State('role-role_key-input', 'value'),
     State('role-status-select', 'value'),
     State('role-create_time-range', 'value'),
     State('role-button-perms-container', 'data')],
    prevent_initial_call=True
)
def get_role_table_data(search_click, refresh_click, pagination, operations, role_name, role_key, status_select, create_time_range, button_perms):

    create_time_start = None
    create_time_end = None
    if create_time_range:
        create_time_start = create_time_range[0]
        create_time_end = create_time_range[1]
    query_params = dict(
        role_name=role_name,
        role_key=role_key,
        status=status_select,
        create_time_start=create_time_start,
        create_time_end=create_time_end,
        page_num=1,
        page_size=10
    )
    triggered_id = dash.ctx.triggered_id
    if triggered_id == 'role-list-table':
        query_params = dict(
            role_name=role_name,
            role_key=role_key,
            status=status_select,
            create_time_start=create_time_start,
            create_time_end=create_time_end,
            page_num=pagination['current'],
            page_size=pagination['pageSize']
        )
    if search_click or refresh_click or pagination or operations:
        table_info = get_role_list_api(query_params)
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
                item['key'] = str(item['role_id'])
                if item['role_id'] == 1:
                    item['operation'] = []
                else:
                    item['operation'] = [
                        {
                            'content': '修改',
                            'type': 'link',
                            'icon': 'antd-edit'
                        } if 'system:role:edit' in button_perms else {},
                        {
                            'content': '删除',
                            'type': 'link',
                            'icon': 'antd-delete'
                        } if 'system:role:remove' in button_perms else {},
                    ]

            return [table_data, table_pagination, str(uuid.uuid4()), None, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 5


@app.callback(
    [Output('role-role_name-input', 'value'),
     Output('role-role_key-input', 'value'),
     Output('role-status-select', 'value'),
     Output('role-create_time-range', 'value'),
     Output('role-operations-store', 'data')],
    Input('role-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_role_query_params(reset_click):
    if reset_click:
        return [None, None, None, None, {'type': 'reset'}]

    return [dash.no_update] * 5


@app.callback(
    [Output('role-search-form-container', 'hidden'),
     Output('role-hidden-tooltip', 'title')],
    Input('role-hidden', 'nClicks'),
    State('role-search-form-container', 'hidden'),
    prevent_initial_call=True
)
def hidden_role_search_form(hidden_click, hidden_status):
    if hidden_click:

        return [not hidden_status, '隐藏搜索' if hidden_status else '显示搜索']
    return [dash.no_update] * 2


@app.callback(
    [Output('role-edit', 'disabled'),
     Output('role-delete', 'disabled')],
    Input('role-list-table', 'selectedRowKeys'),
    prevent_initial_call=True
)
def change_post_edit_delete_button_status(table_rows_selected):
    if table_rows_selected:
        if len(table_rows_selected) > 1:
            return [True, False]

        return [False, False]

    return [True, True]


@app.callback(
    Output('role-menu-perms', 'expandedKeys', allow_duplicate=True),
    Input('role-menu-perms-radio-fold-unfold', 'checked'),
    State('role-menu-store', 'data'),
    prevent_initial_call=True
)
def fold_unfold_role_menu(fold_unfold, menu_info):
    if menu_info:
        default_expanded_keys = []
        for item in menu_info:
            if item.get('parent_id') == 0:
                default_expanded_keys.append(str(item.get('menu_id')))
                
        if fold_unfold:
            return default_expanded_keys
        else:
            return []
    
    return dash.no_update


@app.callback(
    Output('role-menu-perms', 'checkedKeys', allow_duplicate=True),
    Input('role-menu-perms-radio-all-none', 'checked'),
    State('role-menu-store', 'data'),
    prevent_initial_call=True
)
def all_none_role_menu_mode(all_none, menu_info):
    if menu_info:
        default_expanded_keys = []
        for item in menu_info:
            if item.get('parent_id') == 0:
                default_expanded_keys.append(str(item.get('menu_id')))
                
        if all_none:
            return [str(item.get('menu_id')) for item in menu_info]
        else:
            return []
    
    return dash.no_update


@app.callback(
    [Output('role-menu-perms', 'checkStrictly'),
     Output('role-menu-perms', 'checkedKeys', allow_duplicate=True)],
    Input('role-menu-perms-radio-parent-children', 'checked'),
    State('current-role-menu-store', 'data'),
    prevent_initial_call=True
)
def change_role_menu_mode(parent_children, current_role_menu):
    if parent_children:
        checked_menu = []
        if current_role_menu[0]:
            for item in current_role_menu:
                has_children = False
                for other_item in current_role_menu:
                    if other_item['parent_id'] == item['menu_id']:
                        has_children = True
                        break
                if not has_children:
                    checked_menu.append(str(item.get('menu_id')))
        return [False, checked_menu]
    else:
        checked_menu = [str(item.get('menu_id')) for item in current_role_menu if item] or []
        return [True, checked_menu]


@app.callback(
    [Output('role-modal', 'visible', allow_duplicate=True),
     Output('role-modal', 'title'),
     Output('role-role_name', 'value'),
     Output('role-role_key', 'value'),
     Output('role-role_sort', 'value'),
     Output('role-status', 'value'),
     Output('role-menu-perms', 'treeData'),
     Output('role-menu-perms', 'expandedKeys', allow_duplicate=True),
     Output('role-menu-perms', 'checkedKeys', allow_duplicate=True),
     Output('role-menu-store', 'data'),
     Output('current-role-menu-store', 'data'),
     Output('role-remark', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('role-add', 'nClicks'),
     Output('role-edit', 'nClicks'),
     Output('role-edit-id-store', 'data'),
     Output('role-operations-store-bk', 'data')],
    [Input('role-add', 'nClicks'),
     Input('role-edit', 'nClicks'),
     Input('role-list-table', 'nClicksButton')],
    [State('role-list-table', 'selectedRowKeys'),
     State('role-list-table', 'clickedContent'),
     State('role-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_role_modal(add_click, edit_click, button_click, selected_row_keys, clicked_content, recently_button_clicked_row):
    if add_click or edit_click or button_click:
        menu_params = dict(menu_name='', type='role')
        tree_info = get_menu_tree_api(menu_params)
        if tree_info.get('code') == 200:
            tree_data = tree_info['data']
            if add_click:
                return [
                    True,
                    '新增角色',
                    None,
                    None,
                    None,
                    '0',
                    tree_data[0],
                    [],
                    None,
                    tree_data[1],
                    None,
                    None,
                    {'timestamp': time.time()},
                    None,
                    None,
                    None,
                    {'type': 'add'}
                ]
            elif edit_click or (button_click and clicked_content == '修改'):
                if edit_click:
                    role_id = int(','.join(selected_row_keys))
                else:
                    role_id = int(recently_button_clicked_row['key'])
                role_info_res = get_role_detail_api(role_id=role_id)
                if role_info_res['code'] == 200:
                    role_info = role_info_res['data']
                    checked_menu = []
                    if role_info.get('menu')[0]:
                        for item in role_info.get('menu'):
                            has_children = False
                            for other_item in role_info.get('menu'):
                                if other_item['parent_id'] == item['menu_id']:
                                    has_children = True
                                    break
                            if not has_children:
                                checked_menu.append(str(item.get('menu_id')))
                    return [
                        True,
                        '编辑角色',
                        role_info.get('role').get('role_name'),
                        role_info.get('role').get('role_key'),
                        role_info.get('role').get('role_sort'),
                        role_info.get('role').get('status'),
                        tree_data[0],
                        [],
                        checked_menu,
                        tree_data[1],
                        role_info.get('menu'),
                        role_info.get('role').get('remark'),
                        {'timestamp': time.time()},
                        None,
                        None,
                        role_info.get('role') if role_info else None,
                        {'type': 'edit'}
                    ]
                    
        return [dash.no_update] * 12 + [{'timestamp': time.time()}, None, None, None, None]

    return [dash.no_update] * 13 + [None, None, None, None]


@app.callback(
    [Output('role-role_name-form-item', 'validateStatus'),
     Output('role-role_Key-form-item', 'validateStatus'),
     Output('role-role_sort-form-item', 'validateStatus'),
     Output('role-role_name-form-item', 'help'),
     Output('role-role_Key-form-item', 'help'),
     Output('role-role_sort-form-item', 'help'),
     Output('role-modal', 'visible'),
     Output('role-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('role-modal', 'okCounts'),
    [State('role-operations-store-bk', 'data'),
     State('role-edit-id-store', 'data'),
     State('role-role_name', 'value'),
     State('role-role_key', 'value'),
     State('role-role_sort', 'value'),
     State('role-status', 'value'),
     State('role-menu-perms', 'checkedKeys'),
     State('role-menu-perms', 'halfCheckedKeys'),
     State('role-remark', 'value')],
    prevent_initial_call=True
)
def role_confirm(confirm_trigger, operation_type, cur_role_info, role_name, role_key, role_sort, status, menu_checked_keys, menu_half_checked_eys, remark):
    if confirm_trigger:
        if all([role_name, role_key, role_sort]):
            menu_perms = menu_half_checked_eys + menu_checked_keys
            params_add = dict(role_name=role_name, role_key=role_key, role_sort=role_sort, menu_id=','.join(menu_perms) if menu_perms else None, status=status, remark=remark)
            params_edit = dict(role_id=cur_role_info.get('role_id') if cur_role_info else None, role_name=role_name, role_key=role_key, role_sort=role_sort, 
                               menu_id=','.join(menu_perms) if menu_perms else '', status=status, remark=remark)
            api_res = {}
            operation_type = operation_type.get('type')
            if operation_type == 'add':
                api_res = add_role_api(params_add)
            if operation_type == 'edit':
                api_res = edit_role_api(params_edit)
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
            None if role_name else 'error',
            None if role_key else 'error',
            None if role_sort else 'error',
            None if role_name else '请输入角色名称！',
            None if role_key else '请输入权限字符！',
            None if role_sort else '请输入角色排序！',
            dash.no_update,
            dash.no_update,
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage('处理失败', type='error')
        ]         

    return [dash.no_update] * 10


@app.callback(
    [Output('role-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    [Input('role-list-table', 'recentlySwitchDataIndex'),
     Input('role-list-table', 'recentlySwitchStatus'),
     Input('role-list-table', 'recentlySwitchRow')],
    prevent_initial_call=True
)
def table_switch_role_status(recently_switch_data_index, recently_switch_status, recently_switch_row):
    if recently_switch_data_index:
        if recently_switch_status:
            params = dict(role_id=int(recently_switch_row['key']), status='0', type='status')
        else:
            params = dict(role_id=int(recently_switch_row['key']), status='1', type='status')
        edit_button_result = edit_role_api(params)
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
    [Output('role-delete-text', 'children'),
     Output('role-delete-confirm-modal', 'visible'),
     Output('role-delete-ids-store', 'data')],
    [Input('role-delete', 'nClicks'),
     Input('role-list-table', 'nClicksButton')],
    [State('role-list-table', 'selectedRowKeys'),
     State('role-list-table', 'clickedContent'),
     State('role-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def role_delete_modal(delete_click, button_click,
                      selected_row_keys, clicked_content, recently_button_clicked_row):
    if delete_click or button_click:
        trigger_id = dash.ctx.triggered_id

        if trigger_id == 'role-delete':
            role_ids = ','.join(selected_row_keys)
        else:
            if clicked_content == '删除':
                role_ids = recently_button_clicked_row['key']
            else:
                return dash.no_update

        return [
            f'是否确认删除角色编号为{role_ids}的角色？',
            True,
            {'role_ids': role_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('role-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('role-delete-confirm-modal', 'okCounts'),
    State('role-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def role_delete_confirm(delete_confirm, role_ids_data):
    if delete_confirm:

        params = role_ids_data
        delete_button_info = delete_role_api(params)
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
    [Output('role-export-container', 'data', allow_duplicate=True),
     Output('role-export-complete-judge-container', 'data'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('role-export', 'nClicks'),
    prevent_initial_call=True
)
def export_role_list(export_click):
    if export_click:
        export_role_res = export_role_list_api({})
        if export_role_res.status_code == 200:
            export_role = export_role_res.content

            return [
                dcc.send_bytes(export_role, f'角色信息_{time.strftime("%Y%m%d%H%M%S", time.localtime())}.xlsx'),
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
    Output('role-export-container', 'data', allow_duplicate=True),
    Input('role-export-complete-judge-container', 'data'),
    prevent_initial_call=True
)
def reset_role_export_status(data):
    time.sleep(0.5)
    if data:

        return None

    return dash.no_update
