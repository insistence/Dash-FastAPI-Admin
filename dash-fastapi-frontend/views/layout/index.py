from dash import html
import feffery_utils_components as fuc
import feffery_antd_components as fac

from views.layout.components.head import render_head_content
from views.layout.components.content import render_main_content
from views.layout.components.aside import render_aside_content
# import callbacks.index_c
import callbacks.layout_c.fold_side_menu
import callbacks.layout_c.index_c


def render_content(user_name, nick_name, phone_number, menu_info):

    return fuc.FefferyTopProgress(
        html.Div(
            [
                # 全局重载
                fuc.FefferyReload(id='trigger-reload-output'),

                html.Div(id='idle-placeholder-container'),

                # 注入相关modal
                html.Div(
                    [
                        # 个人资料面板
                        fac.AntdModal(
                            [
                                fac.AntdForm(
                                    [
                                        fac.AntdFormItem(
                                            fac.AntdText(
                                                user_name,
                                                copyable=True
                                            ),
                                            label='账号'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdText(
                                                nick_name,
                                                copyable=True
                                            ),
                                            label='姓名'
                                        ),
                                        fac.AntdFormItem(
                                            fac.AntdText(
                                                phone_number,
                                                copyable=True
                                            ),
                                            label='电话'
                                        )
                                    ],
                                    labelCol={
                                        'span': 4
                                    }
                                )
                            ],
                            id='index-personal-info-modal',
                            title='个人资料',
                            mask=False
                        ),
                    ]
                ),

                # 退出登录对话框提示
                fac.AntdModal(
                    html.Div(
                        [
                            fac.AntdIcon(icon='fc-info', style={'font-size': '28px'}),
                            fac.AntdText('确定注销并退出系统吗？', style={'margin-left': '5px'}),
                        ]
                    ),
                    id='logout-modal',
                    visible=False,
                    title='提示',
                    renderFooter=True,
                    centered=True
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
                                        'overflowY': 'auto',
                                        'transition': 'width 1s',
                                        'background': '#001529'
                                    }
                                ),
                            ),
                            # flex='1',
                            id='left-side-menu-container',
                            style={
                                'flex': '1'
                            }
                        ),

                        # 右侧区域
                        fac.AntdCol(
                            [
                                fac.AntdRow(
                                    render_head_content(user_name),
                                    style={
                                        'height': '50px',
                                        'boxShadow': 'rgb(240 241 242) 0px 2px 14px',
                                        'background': 'white',
                                        'marginBottom': '10px',
                                        'position': 'sticky',
                                        'top': 0,
                                        'zIndex': 999
                                    }
                                ),
                                fac.AntdRow(
                                    render_main_content(user_name, nick_name, phone_number),
                                    wrap=False
                                )
                            ],
                            # flex='5',
                            style={
                                'flex': '6',
                                'width': '300px'
                            }
                        ),
                    ],
                )
            ],
            id='index-main-content-container',
        ),
        listenPropsMode='include',
        includeProps=[
            'tabs-container.items'
        ]
    )
