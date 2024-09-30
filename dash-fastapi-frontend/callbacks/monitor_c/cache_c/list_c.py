import uuid
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from api.monitor.cache import CacheApi
from server import app
from utils.feedback_util import MessageManager


@app.callback(
    [
        Output('cache_name-list-table', 'data'),
        Output('cache_name-list-table', 'key'),
    ],
    Input('refresh-cache_name', 'nClicks'),
    prevent_initial_call=True,
)
def get_cache_name_list(refresh_click):
    """
    刷新键名列表回调
    """
    if refresh_click:
        cache_name_res = CacheApi.list_cache_name()
        cache_name_list = cache_name_res.get('data')
        cache_name_data = [
            {
                'key': item.get('cache_name'),
                'id': index + 1,
                'operation': {'type': 'link', 'icon': 'antd-delete'},
                **item,
            }
            for index, item in enumerate(cache_name_list)
        ]

        return [
            cache_name_data,
            str(uuid.uuid4()),
        ]

    raise PreventUpdate


@app.callback(
    output=dict(
        cache_key_table_data=Output('cache_key-list-table', 'data'),
        cache_key_table_key=Output('cache_key-list-table', 'key'),
        cache_name_store=Output('current-cache_name-store', 'data'),
    ),
    inputs=dict(
        cache_name_table_row_click=Input(
            'cache_name-list-table', 'nClicksCell'
        ),
        cache_key_refresh_click=Input('refresh-cache_key', 'nClicks'),
        operations=Input('cache_list-operations-store', 'data'),
    ),
    state=dict(
        cache_name_table_click_row_record=State(
            'cache_name-list-table', 'recentlyCellClickRecord'
        ),
    ),
    prevent_initial_call=True,
)
def get_cache_key_list(
    cache_name_table_row_click,
    cache_key_refresh_click,
    operations,
    cache_name_table_click_row_record,
):
    """
    获取键名列表回调
    """
    if cache_name_table_click_row_record and (
        cache_name_table_row_click or cache_key_refresh_click or operations
    ):
        cache_key_res = CacheApi.list_cache_key(
            cache_name=cache_name_table_click_row_record.get('key')
        )
        cache_key_list = cache_key_res.get('data')
        cache_key_data = [
            {
                'key': item,
                'id': index + 1,
                'cache_key': item,
                'operation': {'type': 'link', 'icon': 'antd-delete'},
            }
            for index, item in enumerate(cache_key_list)
        ]

        return dict(
            cache_key_table_data=cache_key_data,
            cache_key_table_key=str(uuid.uuid4()),
            cache_name_store=cache_name_table_click_row_record.get('key'),
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        cache_name=Output('cache_name-input', 'value', allow_duplicate=True),
        cache_key=Output('cache_key-input', 'value', allow_duplicate=True),
        cache_value=Output('cache_value-input', 'value', allow_duplicate=True),
        cache_key_store=Output('current-cache_key-store', 'data'),
    ),
    inputs=dict(
        cache_key_table_row_click=Input('cache_key-list-table', 'nClicksCell')
    ),
    state=dict(
        cache_key_table_click_row_record=State(
            'cache_key-list-table', 'recentlyCellClickRecord'
        ),
        cache_name_store=State('current-cache_name-store', 'data'),
    ),
    prevent_initial_call=True,
)
def get_cache_value(
    cache_key_table_row_click,
    cache_key_table_click_row_record,
    cache_name_store,
):
    """
    获取缓存内容回调
    """
    if cache_key_table_row_click:
        cache_value_res = CacheApi.get_cache_value(
            cache_name=cache_name_store,
            cache_key=cache_key_table_click_row_record.get('key'),
        )
        cache = cache_value_res.get('data')

        return dict(
            cache_name=cache.get('cache_name'),
            cache_key=cache.get('cache_key'),
            cache_value=cache.get('cache_value'),
            cache_key_store=cache_key_table_click_row_record.get('key'),
        )

    raise PreventUpdate


@app.callback(
    Output('cache_list-operations-store', 'data', allow_duplicate=True),
    Input('cache_name-list-table', 'nClicksButton'),
    State('cache_name-list-table', 'recentlyButtonClickedRow'),
    prevent_initial_call=True,
)
def clear_cache_name(clear_click, recently_button_clicked_row):
    """
    缓存列表表格内部清除缓存回调
    """
    if clear_click:
        CacheApi.clear_cache_name(
            cache_name=recently_button_clicked_row.get('key')
        )
        MessageManager.success(content='清除成功')

        return {'type': 'clear_cache_name'}

    raise PreventUpdate


@app.callback(
    output=dict(
        cache_name=Output('cache_name-input', 'value', allow_duplicate=True),
        cache_key=Output('cache_key-input', 'value', allow_duplicate=True),
        cache_value=Output('cache_value-input', 'value', allow_duplicate=True),
        operations=Output(
            'cache_list-operations-store', 'data', allow_duplicate=True
        ),
    ),
    inputs=dict(clear_click=Input('cache_key-list-table', 'nClicksButton')),
    state=dict(
        recently_button_clicked_row=State(
            'cache_key-list-table', 'recentlyButtonClickedRow'
        ),
        cache_key_store=State('current-cache_key-store', 'data'),
    ),
    prevent_initial_call=True,
)
def clear_cache_key(clear_click, recently_button_clicked_row, cache_key_store):
    """
    键名列表表格内部清除键名回调
    """
    if clear_click:
        CacheApi.clear_cache_key(
            cache_key=recently_button_clicked_row.get('key'),
        )
        MessageManager.success(content='清除成功')

        return dict(
            cache_name=None,
            cache_key=None,
            cache_value=None,
            operations={'type': 'clear_cache_key'},
        )

    raise PreventUpdate


@app.callback(
    output=dict(
        cache_name=Output('cache_name-input', 'value', allow_duplicate=True),
        cache_key=Output('cache_key-input', 'value', allow_duplicate=True),
        cache_value=Output('cache_value-input', 'value', allow_duplicate=True),
        refresh_cache_name=Output('refresh-cache_name', 'nClicks'),
        refresh_cache_key=Output('refresh-cache_key', 'nClicks'),
    ),
    inputs=dict(clear_all_click=Input('clear-all-cache', 'nClicks')),
    state=dict(
        refresh_cache_name_click=State('refresh-cache_name', 'nClicks'),
        refresh_cache_key_click=State('refresh-cache_key', 'nClicks'),
    ),
    prevent_initial_call=True,
)
def clear_all_cache(
    clear_all_click, refresh_cache_name_click, refresh_cache_key_click
):
    """
    清除所有缓存回调
    """
    if clear_all_click:
        CacheApi.clear_cache_all()
        MessageManager.success(content='清除成功')

        return dict(
            cache_name=None,
            cache_key=None,
            cache_value=None,
            refresh_cache_name=refresh_cache_name_click + 1
            if refresh_cache_name_click
            else 1,
            refresh_cache_key=refresh_cache_key_click + 1
            if refresh_cache_key_click
            else 1,
        )

    raise PreventUpdate
