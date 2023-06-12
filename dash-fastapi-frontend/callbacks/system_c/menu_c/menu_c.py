import dash
import time
import uuid
from dash import html
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc
from jsonpath_ng import parse
from flask import session, json
from collections import OrderedDict

from server import app
from utils.tree_tool import list_to_tree
from views.system.menu.components import content_type, menu_type, button_type
from api.menu import get_menu_tree_api, get_menu_tree_for_edit_option_api, get_menu_list_api, delete_menu_api, get_menu_detail_api


@app.callback(
    [Output('menu-list-table', 'data', allow_duplicate=True),
     Output('menu-list-table', 'key'),
     Output('menu-list-table', 'defaultExpandedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('menu-fold', 'nClicks')],
    [Input('menu-search', 'nClicks'),
     Input('menu-operations-store', 'data'),
     Input('menu-fold', 'nClicks')],
    [State('menu-menu_name-input', 'value'),
     State('menu-status-select', 'value'),
     State('menu-list-table', 'defaultExpandedRowKeys')],
    prevent_initial_call=True
)
def get_menu_table_data(search_click, operations, fold_click, menu_name, status_select, in_default_expanded_row_keys):

    query_params = dict(
        menu_name=menu_name,
        status=status_select
    )
    if search_click or operations or fold_click:
        table_info = get_menu_list_api(query_params)
        default_expanded_row_keys = []
        if table_info['code'] == 200:
            table_data = table_info['data']['rows']
            for item in table_data:
                default_expanded_row_keys.append(str(item['menu_id']))
                if item['status'] == '0':
                    item['status'] = dict(tag='正常', color='blue')
                else:
                    item['status'] = dict(tag='停用', color='volcano')
                item['key'] = str(item['menu_id'])
                item['icon'] = [
                    {
                        'type': 'link',
                        'icon': item['icon'],
                        'disabled': True,
                        'style': {
                            'color': 'rgba(0, 0, 0, 0.8)'
                        }
                    },
                ]
                item['operation'] = [
                    {
                        'content': '修改',
                        'type': 'link',
                        'icon': 'antd-edit'
                    },
                    {
                        'content': '新增',
                        'type': 'link',
                        'icon': 'antd-plus'
                    },
                    {
                        'content': '删除',
                        'type': 'link',
                        'icon': 'antd-delete'
                    },
                ]
            table_data_new = list_to_tree(table_data)

            if fold_click:
                if not in_default_expanded_row_keys:
                    return [table_data_new, str(uuid.uuid4()), default_expanded_row_keys, {'timestamp': time.time()}, None]

            return [table_data_new, str(uuid.uuid4()), [], {'timestamp': time.time()}, None]

        return [dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}, None]

    return [dash.no_update] * 4 + [None]


@app.callback(
    [Output('menu-menu_name-input', 'value'),
     Output('menu-status-select', 'value'),
     Output('menu-operations-store', 'data')],
    Input('menu-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_menu_query_params(reset_click):
    if reset_click:
        return [None, None, {'type': 'reset'}]

    return [dash.no_update] * 3


@app.callback(
    [Output('menu-icon', 'value'),
     Output('menu-icon', 'prefix')],
    Input('icon-category', 'value'),
    prevent_initial_call=True
)
def get_select_icon(icon):
    if icon:
        return [
            icon,
            fac.AntdIcon(icon=icon)
        ]

    return [dash.no_update] * 2



@app.callback(
    [Output('menu-modal', 'visible', allow_duplicate=True),
     Output('menu-modal', 'title'),
     Output('menu-parent_id', 'treeData'),
     Output('menu-parent_id', 'value'),
     Output('menu-menu_type', 'value'),
     Output('menu-icon', 'value', allow_duplicate=True),
     Output('menu-icon', 'prefix', allow_duplicate=True),
     Output('menu-menu_name', 'value'),
     Output('menu-order_num', 'value'),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('menu-add', 'nClicks'),
     Output('menu-edit-id-store', 'data'),
     Output('menu-operations-store-bk', 'data')],
    [Input('menu-add', 'nClicks'),
     Input('menu-list-table', 'nClicksButton')],
    [State('menu-list-table', 'clickedContent'),
     State('menu-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def add_edit_menu_modal(add_click, button_click, clicked_content, recently_button_clicked_row):
    if add_click or button_click:
        menu_params = dict(menu_name='')
        if clicked_content == '修改':
            tree_info = get_menu_tree_for_edit_option_api(menu_params)
        else:
            tree_info = get_menu_tree_api(menu_params)
        if tree_info['code'] == 200:
            tree_data = tree_info['data']

            if add_click:
                return [
                    True,
                    '新增菜单',
                    tree_data,
                    '0',
                    'M',
                    None,
                    None,
                    None,
                    None,
                    {'timestamp': time.time()},
                    None,
                    None,
                    {'type': 'add'}
                ]
            elif button_click and clicked_content == '新增':
                return [
                    True,
                    '新增菜单',
                    tree_data,
                    str(recently_button_clicked_row['key']),
                    'M',
                    None,
                    None,
                    None,
                    None,
                    {'timestamp': time.time()},
                    None,
                    None,
                    {'type': 'add'}
                ]
            elif button_click and clicked_content == '修改':
                menu_id = int(recently_button_clicked_row['key'])
                menu_info_res = get_menu_detail_api(menu_id=menu_id)
                if menu_info_res['code'] == 200:
                    menu_info = menu_info_res['data']
                    return [
                        True,
                        '编辑菜单',
                        tree_data,
                        str(menu_info.get('parent_id')),
                        menu_info.get('menu_type'),
                        menu_info.get('icon'),
                        fac.AntdIcon(icon=menu_info.get('icon')),
                        menu_info.get('menu_name'),
                        menu_info.get('order_num'),
                        {'timestamp': time.time()},
                        None,
                        menu_info,
                        {'type': 'edit'}
                    ]

        return [dash.no_update] * 9 + [{'timestamp': time.time()}, None, None, None]

    return [dash.no_update] * 10 + [None, None, None]


@app.callback(
    [Output('content-by-menu-type', 'children'),
     Output('content-by-menu-type', 'key'),
     Output('menu-modal-menu-type-store', 'data')],
    Input('menu-menu_type', 'value'),
    prevent_initial_call=True
)
def get_bottom_content(menu_value):
    """
    根据不同菜单类型渲染不同的子区域
    """
    if menu_value == 'M':
        return [content_type.render(), str(uuid.uuid4()), {'type': 'M'}]

    elif menu_value == 'C':
        return [menu_type.render(), str(uuid.uuid4()), {'type': 'C'}]

    elif menu_value == 'F':
        return [button_type.render(), str(uuid.uuid4()), {'type': 'F'}]

    return dash.no_update


@app.callback(
    [Output('menu-modal-M-trigger', 'data'),
     Output('menu-modal-C-trigger', 'data'),
     Output('menu-modal-F-trigger', 'data')],
    Input('menu-modal', 'okCounts'),
    State('menu-modal-menu-type-store', 'data'),
)
def modal_confirm_trigger(confirm, menu_type):
    """
    增加触发器，根据不同菜单类型触发不同的回调，解决组件不存在回调异常的问题
    """
    if confirm:
        if menu_type.get('type') == 'M':
            return [
                {'timestamp': time.time()},
                dash.no_update,
                dash.no_update
            ]
        if menu_type.get('type') == 'C':
            return [
                dash.no_update,
                {'timestamp': time.time()},
                dash.no_update
            ]
            
        if menu_type.get('type') == 'F':
            return [
                dash.no_update,
                dash.no_update,
                {'timestamp': time.time()}
            ]

    return [dash.no_update] * 3


@app.callback(
    [Output('menu-delete-text', 'children'),
     Output('menu-delete-confirm-modal', 'visible'),
     Output('menu-delete-ids-store', 'data')],
    [Input('menu-list-table', 'nClicksButton')],
    [State('menu-list-table', 'clickedContent'),
     State('menu-list-table', 'recentlyButtonClickedRow')],
    prevent_initial_call=True
)
def menu_delete_modal(button_click, clicked_content, recently_button_clicked_row):
    if button_click:

        if clicked_content == '删除':
            menu_ids = recently_button_clicked_row['key']
        else:
            return dash.no_update

        return [
            f'是否确认删除菜单编号为{menu_ids}的菜单？',
            True,
            {'menu_ids': menu_ids}
        ]

    return [dash.no_update] * 3


@app.callback(
    [Output('menu-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('menu-delete-confirm-modal', 'okCounts'),
    State('menu-delete-ids-store', 'data'),
    prevent_initial_call=True
)
def menu_delete_confirm(delete_confirm, menu_ids_data):
    if delete_confirm:

        params = menu_ids_data
        delete_button_info = delete_menu_api(params)
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
