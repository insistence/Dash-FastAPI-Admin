import dash
import time
import uuid
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import feffery_utils_components as fuc

from server import app
from api.cache import get_cache_key_list_api, get_cache_value_api, clear_cache_name_api, clear_cache_key_api


@app.callback(
    output=dict(
        cache_key_table_data=Output('cache_key-list-table', 'data'),
        cache_key_table_key=Output('cache_key-list-table', 'key'),
        cache_name_store=Output('current-cache_name-store', 'data'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        cache_name_table_row_click=Input('cache_name-list-table', 'nClicksCell'),
        operations=Input('cache_list-operations-store', 'data')
    ),
    state=dict(
        cache_name_table_click_row_record=State('cache_name-list-table', 'recentlyCellClickRecord'),
    ),
    prevent_initial_call=True
)
def get_cache_key_list(cache_name_table_row_click, operations, cache_name_table_click_row_record):
    """
    获取键名列表回调
    """
    if cache_name_table_row_click or operations:

        cache_key_res = get_cache_key_list_api(cache_name=cache_name_table_click_row_record.get('key'))
        if cache_key_res.get('code') == 200:
            cache_key_list = cache_key_res.get('data')
            cache_key_data = [
                {'key': item, 'id': index + 1, 'cache_key': item, 'operation': {'type': 'link', 'icon': 'antd-delete'}} for index, item in enumerate(cache_key_list)]

            return dict(
                cache_key_table_data=cache_key_data,
                cache_key_table_key=str(uuid.uuid4()),
                cache_name_store=cache_name_table_click_row_record.get('key'),
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            cache_key_table_data=dash.no_update,
            cache_key_table_key=dash.no_update,
            cache_name_store=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        cache_name=Output('cache_name-input', 'value', allow_duplicate=True),
        cache_key=Output('cache_key-input', 'value', allow_duplicate=True),
        cache_value=Output('cache_value-input', 'value', allow_duplicate=True),
        cache_key_store=Output('current-cache_key-store', 'data'),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True)
    ),
    inputs=dict(
        cache_key_table_row_click=Input('cache_key-list-table', 'nClicksCell')
    ),
    state=dict(
        cache_key_table_click_row_record=State('cache_key-list-table', 'recentlyCellClickRecord'),
        cache_name_store=State('current-cache_name-store', 'data'),
    ),
    prevent_initial_call=True
)
def get_cache_value(cache_key_table_row_click, cache_key_table_click_row_record, cache_name_store):
    """
    获取缓存内容回调
    """
    if cache_key_table_row_click:

        cache_value_res = get_cache_value_api(cache_name=cache_name_store, cache_key=cache_key_table_click_row_record.get('key'))
        if cache_value_res.get('code') == 200:
            cache = cache_value_res.get('data')

            return dict(
                cache_name=cache.get('cache_name'),
                cache_key=cache.get('cache_key'),
                cache_value=cache.get('cache_value'),
                cache_key_store=cache_key_table_click_row_record.get('key'),
                api_check_token_trigger={'timestamp': time.time()}
            )

        return dict(
            cache_name=dash.no_update,
            cache_key=dash.no_update,
            cache_value=dash.no_update,
            cache_key_store=dash.no_update,
            api_check_token_trigger={'timestamp': time.time()}
        )

    raise PreventUpdate


@app.callback(
    [Output('cache_list-operations-store', 'data', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True)],
    Input('cache_name-list-table', 'nClicksButton'),
    State('cache_name-list-table', 'recentlyButtonClickedRow'),
    prevent_initial_call=True
)
def clear_cache_name(clear_click, recently_button_clicked_row):
    """
    缓存列表表格内部清除缓存回调
    """
    if clear_click:
        clear_cache_name_res = clear_cache_name_api(cache_name=recently_button_clicked_row.get('key'))
        if clear_cache_name_res.get('code') == 200:

            return [
                {'type': 'clear_cache_name'},
                {'timestamp': time.time()},
                fuc.FefferyFancyMessage(clear_cache_name_res.get('message'), type='success')
            ]

        return [
            {'type': 'clear_cache_name'},
            {'timestamp': time.time()},
            fuc.FefferyFancyMessage(clear_cache_name_res.get('message'), type='error')
        ]

    raise PreventUpdate


@app.callback(
    output=dict(
        cache_name=Output('cache_name-input', 'value', allow_duplicate=True),
        cache_key=Output('cache_key-input', 'value', allow_duplicate=True),
        cache_value=Output('cache_value-input', 'value', allow_duplicate=True),
        operations=Output('cache_list-operations-store', 'data', allow_duplicate=True),
        api_check_token_trigger=Output('api-check-token', 'data', allow_duplicate=True),
        global_message_container=Output('global-message-container', 'children', allow_duplicate=True)
    ),
    inputs=dict(
        clear_click=Input('cache_key-list-table', 'nClicksButton')
    ),
    state=dict(
        recently_button_clicked_row=State('cache_key-list-table', 'recentlyButtonClickedRow'),
        cache_name_store=State('current-cache_name-store', 'data'),
        cache_key_store=State('current-cache_key-store', 'data')
    ),
    prevent_initial_call=True
)
def clear_cache_key(clear_click, recently_button_clicked_row, cache_name_store, cache_key_store):
    """
    键名列表表格内部清除键名回调
    """
    if clear_click:
        clear_cache_key_res = clear_cache_key_api(cache_name=cache_name_store, cache_key=recently_button_clicked_row.get('key'))
        if clear_cache_key_res.get('code') == 200:
            if cache_key_store == recently_button_clicked_row.get('key'):
                return dict(
                    cache_name=None,
                    cache_key=None,
                    cache_value=None,
                    operations={'type': 'clear_cache_key'},
                    api_check_token_trigger={'timestamp': time.time()},
                    global_message_container=fuc.FefferyFancyMessage(clear_cache_key_res.get('message'), type='success')
                )
            else:
                return dict(
                    cache_name=dash.no_update,
                    cache_key=dash.no_update,
                    cache_value=dash.no_update,
                    operations={'type': 'clear_cache_key'},
                    api_check_token_trigger={'timestamp': time.time()},
                    global_message_container=fuc.FefferyFancyMessage(clear_cache_key_res.get('message'), type='success')
                )

        return dict(
            cache_name=dash.no_update,
            cache_key=dash.no_update,
            cache_value=dash.no_update,
            operations={'type': 'clear_cache_key'},
            api_check_token_trigger={'timestamp': time.time()},
            global_message_container=fuc.FefferyFancyMessage(clear_cache_key_res.get('message'), type='error')
        )

    raise PreventUpdate
