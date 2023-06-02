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
from utils.tree_tool import get_dept_tree
from api.dept import get_dept_list_api


@app.callback(
    [Output('dept-list-table', 'data', allow_duplicate=True),
     Output('dept-list-table', 'key'),
     Output('dept-list-table', 'defaultExpandedRowKeys'),
     Output('api-check-token', 'data', allow_duplicate=True)],
    [Input('dept-search', 'nClicks'),
     Input('dept-operations-store', 'data')],
    [State('dept-dept_name-input', 'value'),
     State('dept-status-select', 'value')],
    prevent_initial_call=True
)
def get_dept_table_data(search_click, operations, dept_name, status_select):

    query_params = dict(
        dept_name=dept_name,
        status=status_select
    )
    if search_click or operations:
        table_info = get_dept_list_api(query_params)
        default_expanded_row_keys = []
        if table_info['code'] == 200:
            table_data = table_info['data']['rows']
            for item in table_data:
                default_expanded_row_keys.append(str(item['dept_id']))
                if item['status'] == '0':
                    item['status'] = dict(tag='正常', color='blue')
                else:
                    item['status'] = dict(tag='停用', color='volcano')
                item['key'] = str(item['dept_id'])
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
            table_data_new = get_dept_tree(0, table_data)

            return [table_data_new, str(uuid.uuid4()), default_expanded_row_keys, {'timestamp': time.time()}]

        return [dash.no_update, dash.no_update, dash.no_update, {'timestamp': time.time()}]

    return [dash.no_update] * 4


@app.callback(
    [Output('dept-dept_name-input', 'value'),
     Output('dept-status-select', 'value'),
     Output('dept-operations-store', 'data')],
    Input('dept-reset', 'nClicks'),
    prevent_initial_call=True
)
def reset_dept_query_params(reset_click):
    if reset_click:
        return [None, None, {'type': 'reset'}]

    return [dash.no_update] * 3
