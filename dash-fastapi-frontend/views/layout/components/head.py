from dash import html
import feffery_antd_components as fac

import callbacks.layout_c.head_c


def render_head_content(user_name):
    return [
        # 页首左侧折叠按钮区域
        fac.AntdCol(
            html.Div(
                fac.AntdButton(
                    fac.AntdIcon(
                        id='fold-side-menu-icon',
                        icon='antd-menu-fold'
                    ),
                    id='fold-side-menu',
                    type='text',
                    shape='circle',
                    size='large',
                    style={
                        'marginLeft': '5px',
                        'background': 'white'
                    }
                ),
                style={
                    'height': '100%',
                    'display': 'flex',
                    'alignItems': 'center'
                }
            )
        ),

        # 页首面包屑区域
        fac.AntdCol(
            fac.AntdBreadcrumb(
                items=[
                    {
                        'title': '首页',
                        'icon': 'antd-dashboard',
                        'href': '/#'
                    }
                ],
                id='header-breadcrumb'
            ),
            style={
                'height': '100%',
                'display': 'flex',
                'alignItems': 'center',
                'paddingLeft': '5px'
            }
        ),

        # 页首右侧用户信息区域
        fac.AntdCol(
            fac.AntdSpace(
                [
                    fac.AntdTooltip(
                        fac.AntdAvatar(
                            mode='text',
                            size=36,
                            text=user_name,
                            style={
                                'background': 'gold'
                            }
                        ),
                        title='当前用户：' + user_name,
                        placement='bottom'
                    ),

                    fac.AntdDropdown(
                        id='index-header-dropdown',
                        title='个人中心',
                        arrow=True,
                        menuItems=[
                            {
                                'title': '个人资料',
                                'key': '个人资料',
                                'icon': 'antd-idcard'
                            },
                            {
                                'isDivider': True
                            },
                            {
                                'title': '退出登录',
                                'key': '退出登录',
                                'icon': 'antd-logout'
                            },
                        ],
                        placement='bottomRight',
                        overlayStyle={
                            'width': '100px'
                        }
                    )
                ],
                style={
                    'height': '100%',
                    'float': 'right',
                    'display': 'flex',
                    'alignItems': 'center'
                }
            ),
            flex=1
        ),
        fac.AntdCol(
            # 全局刷新按钮
            html.Div(
                fac.AntdTooltip(
                    fac.AntdButton(
                        fac.AntdIcon(
                            id='index-reload-icon',
                            icon='fc-synchronize'
                        ),
                        id='index-reload',
                        type='text',
                        shape='circle',
                        size='large',
                        style={
                            'backgroundColor': 'rgb(255 255 255 / 0%)',
                        }
                    ),
                    title='刷新',
                    placement='bottom'
                )
            ),
            style={
                'height': '100%',
                'paddingRight': '3px',
                'display': 'flex',
                'alignItems': 'center'
            }
        ),
    ]
