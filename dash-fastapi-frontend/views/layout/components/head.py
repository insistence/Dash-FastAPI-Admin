import feffery_antd_components as fac
from dash import html
from callbacks.layout_c import head_c  # noqa: F401
from config.global_config import ApiBaseUrlConfig
from utils.cache_util import CacheManager


def render_head_content():
    return [
        # 页首左侧折叠按钮区域
        fac.AntdCol(
            html.Div(
                fac.AntdButton(
                    fac.AntdIcon(
                        id='fold-side-menu-icon', icon='antd-menu-fold'
                    ),
                    id='fold-side-menu',
                    type='text',
                    shape='circle',
                    size='large',
                    style={'marginLeft': '5px', 'background': 'white'},
                ),
                style={
                    'height': '100%',
                    'display': 'flex',
                    'alignItems': 'center',
                },
            ),
            flex='1',
        ),
        # 页首面包屑区域
        fac.AntdCol(
            fac.AntdBreadcrumb(
                items=[
                    {'title': '首页', 'icon': 'antd-dashboard', 'href': '/#'}
                ],
                id='header-breadcrumb',
            ),
            style={'height': '100%', 'display': 'flex', 'alignItems': 'center'},
            flex='21',
        ),
        # 页首中部搜索区域
        fac.AntdCol(
            fac.AntdParagraph(
                [
                    fac.AntdText(
                        'Ctrl', keyboard=True, style={'color': '#8c8c8c'}
                    ),
                    fac.AntdText(
                        'K', keyboard=True, style={'color': '#8c8c8c'}
                    ),
                    fac.AntdText('唤出搜索面板', style={'color': '#8c8c8c'}),
                ],
                style={
                    'height': '100%',
                    'display': 'flex',
                    'alignItems': 'center',
                },
            ),
            flex='6',
        ),
        # 页首开源项目地址
        fac.AntdCol(
            html.A(
                html.Img(
                    src='https://gitee.com/insistence2022/dash-fastapi-admin/badge/star.svg?theme=dark'
                ),
                href='https://gitee.com/insistence2022/dash-fastapi-admin',
                target='_blank',
            ),
            style={'height': '100%', 'display': 'flex', 'alignItems': 'center'},
            flex='3',
        ),
        # 页首右侧用户信息区域
        fac.AntdCol(
            fac.AntdSpace(
                [
                    fac.AntdPopover(
                        fac.AntdBadge(
                            fac.AntdAvatar(
                                id='avatar-info',
                                mode='image',
                                src=f"{ApiBaseUrlConfig.BaseUrl}{CacheManager.get('user_info').get('avatar')}"
                                if CacheManager.get('user_info').get('avatar')
                                else '/assets/imgs/profile.jpg',
                                size=36,
                            ),
                            count=6,
                            size='small',
                        ),
                        content=fac.AntdTabs(
                            items=[
                                {
                                    'key': '未读消息',
                                    'label': '未读消息',
                                    'children': [
                                        fac.AntdSpace(
                                            [
                                                html.Div(
                                                    fac.AntdText(
                                                        f'消息示例{i}'
                                                    ),
                                                    style={
                                                        'padding': '5px 10px',
                                                        'height': 40,
                                                        'width': 300,
                                                        'borderBottom': '1px solid #f1f3f5',
                                                    },
                                                )
                                                for i in range(1, 8)
                                            ],
                                            direction='vertical',
                                            style={
                                                'height': 280,
                                                'overflowY': 'auto',
                                            },
                                        )
                                    ],
                                },
                                {
                                    'key': '已读消息',
                                    'label': '已读消息',
                                    'children': [
                                        fac.AntdSpace(
                                            [
                                                html.Div(
                                                    fac.AntdText(
                                                        f'消息示例{i}'
                                                    ),
                                                    style={
                                                        'padding': '5px 10px',
                                                        'height': 40,
                                                        'width': 300,
                                                        'borderBottom': '1px solid #f1f3f5',
                                                    },
                                                )
                                                for i in range(8, 15)
                                            ],
                                            direction='vertical',
                                            style={
                                                'height': 280,
                                                'overflowY': 'auto',
                                            },
                                        )
                                    ],
                                },
                            ],
                            centered=True,
                        ),
                        placement='bottomRight',
                    ),
                    fac.AntdDropdown(
                        id='index-header-dropdown',
                        title=CacheManager.get('user_info').get('user_name'),
                        arrow=True,
                        menuItems=[
                            {
                                'title': '个人资料',
                                'key': '个人资料',
                                'icon': 'antd-idcard',
                            },
                            {
                                'title': '布局设置',
                                'key': '布局设置',
                                'icon': 'antd-layout',
                            },
                            {'isDivider': True},
                            {
                                'title': '退出登录',
                                'key': '退出登录',
                                'icon': 'antd-logout',
                            },
                        ],
                        placement='bottomRight',
                        overlayStyle={'width': '100px'},
                    ),
                ],
                style={
                    'height': '100%',
                    'float': 'right',
                    'display': 'flex',
                    'alignItems': 'center',
                },
            ),
            flex='3',
        ),
        fac.AntdCol(
            # 全局刷新按钮
            html.Div(
                fac.AntdTooltip(
                    fac.AntdButton(
                        fac.AntdIcon(
                            id='index-reload-icon', icon='fc-synchronize'
                        ),
                        id='index-reload',
                        type='text',
                        shape='circle',
                        size='large',
                        style={
                            'backgroundColor': 'rgb(255 255 255 / 0%)',
                        },
                    ),
                    title='刷新',
                    placement='bottom',
                )
            ),
            style={
                'height': '100%',
                'paddingRight': '3px',
                'display': 'flex',
                'alignItems': 'center',
            },
            flex='1',
        ),
    ]
