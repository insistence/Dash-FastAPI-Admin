from dash import html
import feffery_antd_components as fac
from config.global_config import IconConfig


def render_icon():

    return html.Div(
        [
            fac.AntdRadioGroup(
                id='icon-category',
                options=[
                    {
                        'label': fac.AntdIcon(
                            icon=icon,
                        ),
                        'value': icon
                    }
                    for icon in IconConfig.ICON_LIST
                ],
                style={
                    'width': 450,
                    'paddingLeft': '10px'
                }
            ),
        ],
        style={
            'maxHeight': '135px',
            'overflow': 'auto'
        }
    )
