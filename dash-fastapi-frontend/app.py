import dash
import time
from dash import html, dcc
from dash.dependencies import Input, Output, State
import feffery_antd_components as fac
import feffery_utils_components as fuc
from flask import session

from server import app
from config.global_config import RouterConfig
from store.store import render_store_container

# 载入子页面
import views

from callbacks import app_c
from api.login import get_current_user_info_api
from utils.tree_tool import find_node_values, find_key_by_href, deal_user_menu_info, get_search_panel_data

app.layout = html.Div(
    [
        # 注入url监听
        fuc.FefferyLocation(id='url-container'),
        # 用于回调pathname信息
        dcc.Location(id='dcc-url', refresh=False),

        # 注入js执行容器
        fuc.FefferyExecuteJs(
            id='execute-js-container'
        ),

        # 注入页面内容挂载点
        html.Div(id='app-mount'),

        # 注入全局配置容器
        fac.AntdConfigProvider(id='app-config-provider'),

        # 注入快捷搜索面板
        fuc.FefferyShortcutPanel(
            id='search-panel',
            data=[],
            placeholder='输入你想要搜索的菜单...',
            panelStyles={
                'accentColor': '#1890ff',
                'zIndex': 99999
            }
        ),

        # 辅助处理多输入 -> 存储接口返回token校验信息
        render_store_container(),

        # 重定向容器
        html.Div(id='redirect-container'),

        # 登录消息失效对话框提示
        fac.AntdModal(
            html.Div(
                [
                    fac.AntdIcon(icon='fc-high-priority', style={'font-size': '28px'}),
                    fac.AntdText('用户信息已过期，请重新登录', style={'margin-left': '5px'}),
                ]
            ),
            id='token-invalid-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),

        # 注入全局消息提示容器
        html.Div(id='global-message-container'),
        # 注入全局通知信息容器
        html.Div(id='global-notification-container')
    ]
)


@app.callback(
    [Output('app-mount', 'children'),
     Output('redirect-container', 'children', allow_duplicate=True),
     Output('global-message-container', 'children', allow_duplicate=True),
     Output('api-check-token', 'data', allow_duplicate=True),
     Output('current-key-container', 'data'),
     Output('menu-info-store-container', 'data'),
     Output('menu-list-store-container', 'data'),
     Output('search-panel', 'data')],
    Input('url-container', 'pathname'),
    [State('url-container', 'trigger'),
     State('token-container', 'data')],
    prevent_initial_call=True
)
def router(pathname, trigger, session_token):
    # 检查当前会话是否已经登录
    token_result = session.get('Authorization')
    # 若已登录
    if token_result and session_token and token_result == session_token:
        try:
            current_user_result = get_current_user_info_api()
            if current_user_result['code'] == 200:
                current_user = current_user_result['data']
                menu_list = current_user['menu']
                user_menu_list = [item for item in menu_list if item.get('visible') == '0']
                menu_info = deal_user_menu_info(0, menu_list)
                user_menu_info = deal_user_menu_info(0, user_menu_list)
                search_panel_data = get_search_panel_data(user_menu_list)
                session['user_info'] = current_user['user']
                session['dept_info'] = current_user['dept']
                session['role_info'] = current_user['role']
                session['post_info'] = current_user['post']
                dynamic_valid_pathname_list = find_node_values(menu_info, 'href')
                valid_href_list = dynamic_valid_pathname_list + RouterConfig.STATIC_VALID_PATHNAME
                if pathname in valid_href_list:
                    current_key = find_key_by_href(menu_info, pathname)
                    if pathname == '/':
                        current_key = '首页'
                    if pathname == '/user/profile':
                        current_key = '个人资料'
                    if trigger == 'load':

                        # 根据pathname控制渲染行为
                        if pathname == '/login' or pathname == '/forget':
                            # 重定向到主页面
                            return [
                                dash.no_update,
                                dcc.Location(
                                    pathname='/',
                                    id='router-redirect'
                                ),
                                None,
                                {'timestamp': time.time()},
                                {'current_key': current_key},
                                {'menu_info': menu_info},
                                {'menu_list': menu_list},
                                search_panel_data
                            ]

                        # 否则正常渲染主页面
                        return [
                            views.layout.render_content(user_menu_info),
                            None,
                            fuc.FefferyFancyNotification('进入主页面', type='success', autoClose=2000),
                            {'timestamp': time.time()},
                            {'current_key': current_key},
                            {'menu_info': menu_info},
                            {'menu_list': menu_list},
                            search_panel_data
                        ]

                    else:
                        return [
                            dash.no_update,
                            None,
                            None,
                            {'timestamp': time.time()},
                            {'current_key': current_key},
                            {'menu_info': menu_info},
                            {'menu_list': menu_list},
                            search_panel_data
                        ]

                else:
                    # 渲染404状态页
                    return [
                        views.page_404.render_content(),
                        None,
                        None,
                        {'timestamp': time.time()},
                        dash.no_update,
                        dash.no_update,
                        dash.no_update,
                        dash.no_update
                    ]

            else:
                return [
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    {'timestamp': time.time()},
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update
                ]

        except Exception as e:
            print(e)

            return [
                dash.no_update,
                None,
                fuc.FefferyFancyNotification('接口异常', type='error', autoClose=2000),
                {'timestamp': time.time()},
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update
            ]
    else:
        # 若未登录
        # 根据pathname控制渲染行为
        # 检验pathname合法性
        if pathname not in RouterConfig.BASIC_VALID_PATHNAME:
            # 渲染404状态页
            return [
                views.page_404.render_content(),
                None,
                None,
                {'timestamp': time.time()},
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update
            ]

        if pathname == '/login':
            return [
                views.login.render_content(),
                None,
                None,
                {'timestamp': time.time()},
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update
            ]

        if pathname == '/forget':
            return [
                views.forget.render_forget_content(),
                None,
                None,
                {'timestamp': time.time()},
                dash.no_update,
                dash.no_update,
                dash.no_update,
                dash.no_update
            ]

        # 否则重定向到登录页
        return [
            dash.no_update,
            dcc.Location(
                pathname='/login',
                id='router-redirect'
            ),
            None,
            {'timestamp': time.time()},
            dash.no_update,
            dash.no_update,
            dash.no_update,
            dash.no_update
        ]


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8088, debug=True)
