from dash.dependencies import Input, Output, State

from server import app


app.clientside_callback(
    '''
    (nClicks, collapsed, oldStyle) => {
            if (nClicks) {
                if (oldStyle.flex === '1') {
                    return [
                        {},
                        !collapsed,
                        {'display': 'none'},
                        collapsed ? 'antd-menu-fold' : 'antd-menu-unfold',
                    ];
                }
                return [
                        {'flex': '1'},
                        !collapsed,
                        {'fontSize': '22px', 'color': 'rgb(255, 255, 255)'},
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
    [State('menu-collapse-sider-custom', 'collapsed'),
     State('left-side-menu-container', 'style')],
    prevent_initial_call=True
)
