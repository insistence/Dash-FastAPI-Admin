import feffery_antd_components as fac
from dash import html
from views.dashboard import render


def render_main_content():
    return [
        # 右侧主体内容区域
        fac.AntdCol(
            [
                html.Div(
                    fac.AntdTabs(
                        items=[
                            {
                                'label': '首页',
                                'key': 'Index/',
                                'closable': False,
                                'children': render(),
                                'contextMenu': [
                                    {
                                        'key': '刷新页面',
                                        'label': '刷新页面',
                                        'icon': 'antd-reload',
                                    },
                                    {
                                        'key': '关闭其他',
                                        'label': '关闭其他',
                                        'icon': 'antd-close-circle',
                                    },
                                    {
                                        'key': '全部关闭',
                                        'label': '全部关闭',
                                        'icon': 'antd-close-circle',
                                    },
                                ],
                            }
                        ],
                        id='tabs-container',
                        type='editable-card',
                        # defaultActiveKey='首页',
                        style={
                            'width': '100%',
                            'paddingLeft': '15px',
                            'paddingRight': '15px',
                        },
                    ),
                    # id='index-main-content-container',
                    style={
                        'width': '100%',
                        'height': '100%',
                        'backgroundColor': 'white',
                    },
                )
            ],
            flex='auto',
        )
    ]
