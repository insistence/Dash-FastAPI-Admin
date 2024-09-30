from dash import dcc, no_update
from dash.dependencies import Input, Output, State
from flask import session
from importlib import import_module
import views
from api.login import LoginApi
from api.router import RouterApi
from config.router import RouterConfig
from server import app
from utils.cache_util import CacheManager
from utils.router_util import RouterUtil


@app.callback(
    output=dict(
        app_mount=Output('app-mount', 'children'),
        redirect_container=Output(
            'redirect-container', 'children', allow_duplicate=True
        ),
        current_pathname=Output('current-pathname-container', 'data'),
        router_list=Output('router-list-container', 'data'),
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
            router_list = RouterConfig.CONSTANT_ROUTES + router_list
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
        valid_pathname_list = RouterUtil.generate_validate_pathname_list(
            menu_info
        )
        if pathname in valid_pathname_list:
            if url_trigger == 'load':
                # 根据pathname控制渲染行为
                if pathname in [
                    route.get('path')
                    for route in RouterConfig.WHITE_ROUTES_LIST
                ]:
                    # 重定向到主页面
                    return dict(
                        app_mount=no_update,
                        redirect_container=dcc.Location(
                            pathname='/', id='router-redirect'
                        ),
                        current_pathname=no_update,
                        router_list=no_update,
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
                    app_mount=views.layout.render(user_menu_info),
                    redirect_container=None,
                    current_pathname=pathname,
                    router_list=menu_info,
                    search_panel_data=search_panel_data,
                )

            else:
                return dict(
                    app_mount=no_update,
                    redirect_container=None,
                    current_pathname=pathname,
                    router_list=no_update,
                    search_panel_data=no_update,
                )

        else:
            # 渲染404状态页
            return dict(
                app_mount=views.page_404.render(),
                redirect_container=None,
                current_pathname=no_update,
                router_list=no_update,
                search_panel_data=no_update,
            )

    else:
        # 若未登录
        # 根据pathname控制渲染行为
        for route in RouterConfig.WHITE_ROUTES_LIST:
            if pathname == route.get('path'):
                component = route.get('component') or 'page_404'

                return dict(
                    app_mount=import_module('views.' + component).render(),
                    redirect_container=None,
                    current_pathname=no_update,
                    router_list=no_update,
                    search_panel_data=no_update,
                )

        # 否则重定向到登录页
        return dict(
            app_mount=no_update,
            redirect_container=dcc.Location(
                pathname='/login', id='router-redirect'
            ),
            current_pathname=no_update,
            router_list=no_update,
            search_panel_data=no_update,
        )
