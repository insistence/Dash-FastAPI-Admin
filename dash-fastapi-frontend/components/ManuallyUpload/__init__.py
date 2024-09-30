import feffery_antd_components as fac
from dash import dcc, html
from feffery_utils_components import FefferyShadowDom, FefferyStyle
from typing import Dict, Optional, Union
from uuid import uuid4


class ManuallyUpload(FefferyShadowDom):
    def __init__(
        self,
        id: Optional[Union[str, Dict]] = str(uuid4()),
        accept: Optional[str] = None,
        disabled: Optional[bool] = False,
        max_size: Optional[Union[float, int]] = -1,
        min_size: Optional[Union[float, int]] = 0,
        multiple: Optional[bool] = False,
    ):
        children = [
            dcc.Upload(
                html.Div(
                    html.Span(
                        html.Div(
                            html.Span(
                                html.Div(
                                    [
                                        html.P(
                                            fac.AntdIcon(
                                                icon='antd-cloud-upload',
                                            ),
                                            className='ant-upload-drag-icon',
                                        ),
                                        html.P(
                                            '用户导入',
                                            className='ant-upload-text',
                                        ),
                                        html.P(
                                            '点击或拖拽文件至此处进行上传',
                                            className='ant-upload-hint',
                                        ),
                                    ],
                                    className='ant-upload-drag-container',
                                ),
                                tabIndex='0',
                                role='button',
                                className='ant-upload ant-upload-btn',
                            ),
                            className='ant-upload ant-upload-drag',
                        ),
                        className='ant-upload-wrapper',
                    ),
                    className='ant-droag-upload-container',
                ),
                id=id,
                accept=accept,
                disabled=disabled,
                max_size=max_size,
                min_size=min_size,
                multiple=multiple,
            ),
            FefferyStyle(
                rawStyle="""
                            .ant-droag-upload-container {
                                border: 1px solid transparent; 
                                transition: border 0.3s;
                            }
                            .ant-upload-wrapper {
                                box-sizing: border-box;
                                margin: 0;
                                padding: 0;
                                color: rgba(0, 0, 0, 0.88);
                                font-size: 14px;
                                line-height: 1.5714285714285714;
                                list-style: none;
                                font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,'Noto Sans',sans-serif,'Apple Color Emoji','Segoe UI Emoji','Segoe UI Symbol','Noto Color Emoji';
                            }
                            .ant-upload-wrapper .ant-upload-drag {
                                position: relative;
                                width: 100%;
                                height: 100%;
                                text-align: center;
                                background: rgba(0, 0, 0, 0.02);
                                border: 1px dashed #d9d9d9;
                                border-radius: 8px;
                                cursor: pointer;
                                transition: border-color 0.3s;
                            }
                            .ant-upload-wrapper .ant-upload-drag:not(.ant-upload-disabled):hover, .ant-upload-wrapper .ant-upload-drag-hover:not(.ant-upload-disabled) {
                                border-color: #4096ff;
                            }
                            .ant-upload-wrapper .ant-upload-drag .ant-upload-btn {
                                display: table;
                                width: 100%;
                                height: 100%;
                                outline: none;
                                border-radius: 8px;
                            }
                            .ant-upload-wrapper .ant-upload-drag .ant-upload {
                                padding: 16px;
                            }
                            .ant-upload-wrapper .ant-upload-drag .ant-upload-drag-container {
                                display: table-cell;
                                vertical-align: middle;
                            }
                            .ant-upload-wrapper .ant-upload-drag p.ant-upload-drag-icon {
                                margin-bottom: 16px;
                            }
                            .ant-upload-wrapper .ant-upload-drag p.ant-upload-drag-icon .anticon {
                                color: #1677ff;
                                font-size: 48px;
                            }
                            .ant-upload-wrapper .ant-upload-drag p.ant-upload-text {
                                margin: 0 0 4px;
                                color: rgba(0, 0, 0, 0.88);
                                font-size: 16px;
                            }
                            .ant-upload-wrapper .ant-upload-drag p.ant-upload-hint {
                                color: rgba(0, 0, 0, 0.45);
                                font-size: 14px;
                            }
                            .ant-upload-wrapper [class^="ant-upload"], .ant-upload-wrapper [class*=" ant-upload"] {
                                box-sizing: border-box;
                            }
                            """
            ),
        ]
        super().__init__(children=children)
