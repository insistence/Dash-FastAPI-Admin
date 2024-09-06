import feffery_antd_components as fac
from dash import dcc, html
from api.monitor.cache import CacheApi
from callbacks.monitor_c.cache_c import list_c  # noqa: F401


def render(*args, **kwargs):
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

    return html.Div(
        [
            dcc.Store(id='cache_list-operations-store'),
            dcc.Store(id='current-cache_name-store'),
            dcc.Store(id='current-cache_key-store'),
            fac.AntdRow(
                [
                    fac.AntdCol(
                        fac.AntdCard(
                            fac.AntdSpin(
                                fac.AntdTable(
                                    id='cache_name-list-table',
                                    data=cache_name_data,
                                    columns=[
                                        {
                                            'dataIndex': 'id',
                                            'title': '序号',
                                            'renderOptions': {
                                                'renderType': 'ellipsis'
                                            },
                                        },
                                        {
                                            'dataIndex': 'cache_name',
                                            'title': '缓存名称',
                                            'renderOptions': {
                                                'renderType': 'ellipsis'
                                            },
                                        },
                                        {
                                            'dataIndex': 'remark',
                                            'title': '备注',
                                            'renderOptions': {
                                                'renderType': 'ellipsis'
                                            },
                                        },
                                        {
                                            'title': '操作',
                                            'dataIndex': 'operation',
                                            'renderOptions': {
                                                'renderType': 'button'
                                            },
                                        },
                                    ],
                                    enableCellClickListenColumns=[
                                        'id',
                                        'cache_name',
                                        'remark',
                                    ],
                                    bordered=False,
                                    pagination={
                                        'showSizeChanger': True,
                                        'showQuickJumper': True,
                                        'hideOnSinglePage': True,
                                    },
                                )
                            ),
                            title=fac.AntdSpace(
                                [
                                    fac.AntdIcon(icon='antd-book'),
                                    fac.AntdText('缓存列表'),
                                ]
                            ),
                            extra=fac.AntdButton(
                                id='refresh-cache_name',
                                type='link',
                                icon=fac.AntdIcon(icon='antd-reload'),
                            ),
                            size='small',
                            style={
                                'boxShadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px'
                            },
                        ),
                        span=8,
                    ),
                    fac.AntdCol(
                        fac.AntdCard(
                            fac.AntdSpin(
                                fac.AntdTable(
                                    id='cache_key-list-table',
                                    data=[],
                                    columns=[
                                        {
                                            'dataIndex': 'id',
                                            'title': '序号',
                                            'renderOptions': {
                                                'renderType': 'ellipsis'
                                            },
                                        },
                                        {
                                            'dataIndex': 'cache_key',
                                            'title': '缓存键名',
                                            'renderOptions': {
                                                'renderType': 'ellipsis'
                                            },
                                        },
                                        {
                                            'title': '操作',
                                            'dataIndex': 'operation',
                                            'renderOptions': {
                                                'renderType': 'button'
                                            },
                                        },
                                    ],
                                    enableCellClickListenColumns=[
                                        'id',
                                        'cache_key',
                                    ],
                                    bordered=False,
                                    pagination={
                                        'showSizeChanger': True,
                                        'showQuickJumper': True,
                                        'hideOnSinglePage': True,
                                    },
                                )
                            ),
                            title=fac.AntdSpace(
                                [
                                    fac.AntdIcon(icon='antd-key'),
                                    fac.AntdText('键名列表'),
                                ]
                            ),
                            extra=fac.AntdButton(
                                id='refresh-cache_key',
                                type='link',
                                icon=fac.AntdIcon(icon='antd-reload'),
                            ),
                            size='small',
                            style={
                                'boxShadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px'
                            },
                        ),
                        span=8,
                    ),
                    fac.AntdCol(
                        fac.AntdCard(
                            fac.AntdForm(
                                [
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='cache_name-input',
                                            readOnly=True,
                                            style={'width': '100%'},
                                        ),
                                        label='缓存名称',
                                    ),
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='cache_key-input',
                                            readOnly=True,
                                            style={'width': '100%'},
                                        ),
                                        label='缓存键名',
                                    ),
                                    fac.AntdFormItem(
                                        fac.AntdInput(
                                            id='cache_value-input',
                                            mode='text-area',
                                            readOnly=True,
                                            autoSize={
                                                'minRows': 5,
                                                'maxRows': 10,
                                            },
                                            style={'width': '100%'},
                                        ),
                                        label='缓存内容',
                                    ),
                                ],
                                layout='vertical',
                                style={'width': '100%'},
                            ),
                            title=fac.AntdSpace(
                                [
                                    fac.AntdIcon(icon='antd-file-text'),
                                    fac.AntdText('缓存内容'),
                                ]
                            ),
                            extra=fac.AntdButton(
                                '清除全部',
                                id='clear-all-cache',
                                type='link',
                                icon=fac.AntdIcon(icon='antd-clear'),
                            ),
                            size='small',
                            style={
                                'boxShadow': 'rgba(99, 99, 99, 0.2) 0px 2px 8px 0px'
                            },
                        ),
                        span=8,
                    ),
                ],
                gutter=10,
            ),
        ]
    )
