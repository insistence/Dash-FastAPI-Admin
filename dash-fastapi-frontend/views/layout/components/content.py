from dash import html
import feffery_antd_components as fac


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
                                'children': fac.AntdAlert(
                                    type='info',
                                    showIcon=True,
                                    message='这里是主标签页，通常建议设置为不可关闭并展示一些总览类型的信息'
                                )
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
