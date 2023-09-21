from dash.dependencies import Input, Output, State

from server import app


# 侧边栏折叠回调
app.clientside_callback(
    '''
    (nClicks, collapsed) => {
            if (nClicks) {
                return [
                        collapsed ? {'width': 210} : {'width': 60},
                        !collapsed,
                        collapsed ? {'fontSize': '22px', 'color': 'rgb(255, 255, 255)'} : {'display': 'none'},
                        collapsed ? 'antd-menu-fold' : 'antd-menu-unfold',
                    ];
            }
            return window.dash_clientside.no_update;
    }
    ''',
    [Output('left-side-menu-container', 'style'),
     Output('menu-collapse-sider-custom', 'collapsed'),
     Output('logo-text', 'style'),
     Output('fold-side-menu-icon', 'icon')],
    Input('fold-side-menu', 'nClicks'),
    State('menu-collapse-sider-custom', 'collapsed'),
    prevent_initial_call=True
)
