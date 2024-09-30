import feffery_antd_components as fac
import feffery_utils_components as fuc
from dash import html
from callbacks.layout_c import fold_side_menu  # noqa: F401
from callbacks.layout_c import index_c  # noqa: F401
from views.layout.components.aside import render_aside_content
from views.layout.components.content import render_main_content
from views.layout.components.head import render_head_content


def render(menu_info):
    return fuc.FefferyTopProgress(
        html.Div(
            [
                # 全局重载
                fuc.FefferyReload(id='trigger-reload-output'),
                # 响应式监听组件
                fuc.FefferyResponsive(id='responsive-layout-container'),
                # 布局设置抽屉
                fac.AntdDrawer(
                    [
                        fac.AntdText(
                            '主题颜色',
                            style={'fontSize': 16, 'fontWeight': 500},
                        ),
                        fuc.FefferyHexColorPicker(
                            id='hex-color-picker',
                            color='#1890ff',
                            showAlpha=True,
                            style={'width': '100%', 'marginTop': '10px'},
                        ),
                        fac.AntdInput(
                            id='selected-color-input',
                            value='#1890ff',
                            readOnly=True,
                            style={
                                'marginTop': '15px',
                                'background': '#1890ff',
                            },
                        ),
                        fac.AntdSpace(
                            [
                                fac.AntdButton(
                                    [
                                        fac.AntdIcon(icon='antd-save'),
                                        '保存配置',
                                    ],
                                    id='save-setting',
                                    type='primary',
                                ),
                                fac.AntdButton(
                                    [
                                        fac.AntdIcon(icon='antd-sync'),
                                        '重置配置',
                                    ],
                                    id='reset-setting',
                                ),
                            ],
                            style={'marginTop': '15px'},
                        ),
                    ],
                    id='layout-setting-drawer',
                    visible=False,
                    title='布局设置',
                    width=320,
                ),
                # 退出登录对话框提示
                fac.AntdModal(
                    html.Div(
                        [
                            fac.AntdIcon(
                                icon='fc-info', style={'font-size': '28px'}
                            ),
                            fac.AntdText(
                                '确定注销并退出系统吗？',
                                style={'margin-left': '5px'},
                            ),
                        ]
                    ),
                    id='logout-modal',
                    visible=False,
                    title='提示',
                    renderFooter=True,
                    centered=True,
                ),
                # 平台主页面
                fac.AntdRow(
                    [
                        # 左侧固定菜单区域
                        fac.AntdCol(
                            fac.AntdAffix(
                                html.Div(
                                    render_aside_content(menu_info),
                                    id='side-menu',
                                    style={
                                        'height': '100vh',
                                        'overflowX': 'hidden',
                                        'overflowY': 'auto',
                                        'transition': 'width 1s',
                                        'background': '#001529',
                                    },
                                ),
                            ),
                            id='left-side-menu-container',
                            flex='none',
                        ),
                        # 右侧区域
                        fac.AntdCol(
                            [
                                fac.AntdRow(
                                    render_head_content(),
                                    style={
                                        'height': '50px',
                                        'boxShadow': 'rgb(240 241 242) 0px 2px 14px',
                                        'background': 'white',
                                        'marginBottom': '10px',
                                        'position': 'sticky',
                                        'top': 0,
                                        'zIndex': 999,
                                    },
                                ),
                                fac.AntdRow(render_main_content(), wrap=False),
                            ],
                            flex='auto',
                            style={'width': 0},
                        ),
                    ],
                ),
            ],
            id='index-main-content-container',
        ),
        listenPropsMode='include',
        includeProps=['tabs-container.items'],
    )
