from dash import html
import feffery_antd_components as fac

from views.dashboard import render_dashboard


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
                                'key': '首页',
                                'closable': False,
                                'children': render_dashboard()
                            }
                        ],
                        id='tabs-container',
                        type='editable-card',
                        # defaultActiveKey='首页',
                        style={
                            'width': '100%',
                            'paddingLeft': '15px',
                            'paddingRight': '15px'
                        }
                    ),
                    # id='index-main-content-container',
                    style={
                        'width': '100%',
                        'height': '100%',
                        'backgroundColor': 'white',
                    }
                )
            ],
            flex='auto'
        )
    ]
