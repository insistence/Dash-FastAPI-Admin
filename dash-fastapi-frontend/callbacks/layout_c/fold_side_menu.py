from dash.dependencies import Input, Output, State
from server import app


# 侧边栏折叠回调
app.clientside_callback(
    """
    (nClicks, collapsed, responsive) => {
            if (nClicks) {
                return [
                        collapsed ? {width: 256} : (!responsive?.sm ? {display: 'none'} : {width: 64}),
                        !collapsed,
                        collapsed ? {fontSize: '22px', color: 'rgb(255, 255, 255)'} : {display: 'none'},
                        collapsed ? 'antd-menu-fold' : 'antd-menu-unfold',
                    ];
            }
            throw window.dash_clientside.PreventUpdate;
    }
    """,
    [
        Output('left-side-menu-container', 'style', allow_duplicate=True),
        Output('menu-collapse-sider-custom', 'collapsed', allow_duplicate=True),
        Output('logo-text', 'style', allow_duplicate=True),
        Output('fold-side-menu-icon', 'icon', allow_duplicate=True),
    ],
    Input('fold-side-menu', 'nClicks'),
    [
        State('menu-collapse-sider-custom', 'collapsed'),
        State('responsive-layout-container', 'responsive'),
    ],
    prevent_initial_call=True,
)


# 页面响应式监听自动折叠侧边栏
app.clientside_callback(
    """
    (responsive) => {
        if (!responsive?.sm) {
            return [
                {display: 'none'},
                true,
                {display: 'none'},
                'antd-menu-unfold',
                {display: 'none'},
                {display: 'none'},
                {display: 'none'},
                '6',
                'none',
                'none',
                'none',
            ];
        } else if (!responsive?.lg) {
            return [
                {width: 64},
                true,
                {display: 'none'},
                'antd-menu-unfold',
                {display: 'none'},
                {display: 'none'},
                {display: 'none'},
                '12',
                'none',
                'none',
                'none',
            ];
        } else {
            return [
                {width: 256},
                false,
                {fontSize: '22px', color: 'rgb(255, 255, 255)'},
                'antd-menu-fold',
                {},
                {},
                {},
                '1',
                '21',
                '6',
                '3',
            ];
        }
    }
    """,
    [
        Output('left-side-menu-container', 'style', allow_duplicate=True),
        Output('menu-collapse-sider-custom', 'collapsed', allow_duplicate=True),
        Output('logo-text', 'style', allow_duplicate=True),
        Output('fold-side-menu-icon', 'icon', allow_duplicate=True),
        Output('header-breadcrumb-col', 'style'),
        Output('header-search-col', 'style'),
        Output('header-gitee-col', 'style'),
        Output('fold-side-menu-col', 'flex'),
        Output('header-breadcrumb-col', 'flex'),
        Output('header-search-col', 'flex'),
        Output('header-gitee-col', 'flex'),
    ],
    Input('responsive-layout-container', 'responsive'),
    prevent_initial_call=True,
)
