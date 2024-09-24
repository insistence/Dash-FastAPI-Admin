from dash import dcc, no_update
from dash.dependencies import Input, Output, State
from flask import session
from api.login import LoginApi
from api.router import RouterApi
from config.global_config import RouterConfig
from server import app
from utils.cache_util import CacheManager
from utils.router_util import RouterUtil
from utils.tree_tool import find_key_by_href, find_node_values
from views import forget, layout, login, page_404, register


@app.callback(
    output=dict(
        app_mount=Output('app-mount', 'children'),
        redirect_container=Output(
            'redirect-container', 'children', allow_duplicate=True
        ),
        menu_current_key=Output('current-key-container', 'data'),
        search_panel_data=Output('search-panel', 'data'),
    ),
    inputs=dict(pathname=Input('url-container', 'pathname')),
    state=dict(
        url_trigger=State('url-container', 'trigger'),
        session_token=State('token-container', 'data'),
    ),
    prevent_initial_call=True,
)
def router(pathname, url_trigger, session_token):
    """
    全局路由回调
    """
    # 检查当前会话是否已经登录
    token_result = session.get('Authorization')
    # 若已登录
    if token_result and session_token and token_result == session_token:
        if url_trigger == 'load':
            current_user = LoginApi.get_info()
            router_list_result = RouterApi.get_routers()
            router_list = router_list_result['data']
            menu_info = RouterUtil.generate_menu_tree(router_list)
            permissions = {
                'perms': current_user['permissions'],
                'roles': current_user['roles'],
            }
            cache_obj = dict(
                user_info=current_user['user'],
                permissions=permissions,
                menu_info=menu_info,
            )
            CacheManager.set(cache_obj)
        menu_info = CacheManager.get('menu_info')
        dynamic_valid_pathname_list = find_node_values(menu_info, 'href')
        valid_href_list = (
            dynamic_valid_pathname_list + RouterConfig.STATIC_VALID_PATHNAME
        )
        if pathname in valid_href_list:
            current_key = find_key_by_href(menu_info, pathname)
            if pathname == '/':
                current_key = '首页'
            if pathname == '/user/profile':
                current_key = '个人资料'
            if url_trigger == 'load':
                # 根据pathname控制渲染行为
                if pathname == '/login' or pathname == '/forget':
                    # 重定向到主页面
                    return dict(
                        app_mount=no_update,
                        redirect_container=dcc.Location(
                            pathname='/', id='router-redirect'
                        ),
                        menu_current_key=no_update,
                        search_panel_data=no_update,
                    )

                user_menu_info = RouterUtil.generate_menu_tree(
                    RouterUtil.get_visible_routers(router_list)
                )
                search_panel_data = RouterUtil.generate_search_panel_data(
                    user_menu_info
                )
                # 否则正常渲染主页面
                return dict(
                    app_mount=layout.render_content(user_menu_info),
                    redirect_container=None,
                    menu_current_key=current_key,
                    search_panel_data=search_panel_data,
                )

            else:
                return dict(
                    app_mount=no_update,
                    redirect_container=None,
                    menu_current_key=current_key,
                    search_panel_data=no_update,
                )

        else:
            # 渲染404状态页
            return dict(
                app_mount=page_404.render_content(),
                redirect_container=None,
                menu_current_key=no_update,
                search_panel_data=no_update,
            )

    else:
        # 若未登录
        # 根据pathname控制渲染行为
        if pathname == '/login':
            return dict(
                app_mount=login.render_content(),
                redirect_container=None,
                menu_current_key=no_update,
                search_panel_data=no_update,
            )

        if pathname == '/forget':
            return dict(
                app_mount=forget.render_forget_content(),
                redirect_container=None,
                menu_current_key=no_update,
                search_panel_data=no_update,
            )

        if pathname == '/register':
            return dict(
                app_mount=register.render_register_content(),
                redirect_container=None,
                menu_current_key=no_update,
                search_panel_data=no_update,
            )

        # 否则重定向到登录页
        return dict(
            app_mount=no_update,
            redirect_container=dcc.Location(
                pathname='/login', id='router-redirect'
            ),
            menu_current_key=no_update,
            search_panel_data=no_update,
        )
