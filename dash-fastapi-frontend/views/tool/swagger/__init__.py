from dash import html
import feffery_utils_components as fuc
import feffery_antd_components as fac
from config.global_config import ApiBaseUrlConfig


def render(button_perms):

    return [
        html.Div(
            [
                fuc.FefferyStyle(
                    rawStyle="""
                    iframe {
                        border: none;
                        width: 100%;
                        height: 100%;
                        display: block
                    }
                    """
                ),
                html.Iframe(
                    src=f'{ApiBaseUrlConfig.BaseUrl}/docs'
                )
            ],
            id='swagger-docs-container',
            style={
                'position': 'relative',
                'height': 'calc(100vh - 120px)'
            }
        )
    ]
