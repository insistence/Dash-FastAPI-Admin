from dash.dependencies import Input, Output, State
from server import app


# url-pathname控制currentKey回调
app.clientside_callback(
    """
    (currentPathname, routerList) => {
        if (currentPathname) {
            let currentKey = findKeyByPathname(routerList, currentPathname);
            let currentItem = findByKey(routerList, currentKey);
            let currentKeyPath = findKeyPath(routerList, currentKey);
            let currentItemPath = currentKeyPath?.map(item => findByKey(routerList, item));
            return [currentKey, currentKeyPath, currentItem, currentItemPath];
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    [
        Output('index-side-menu', 'currentKey'),
        Output('current-key_path-store', 'data'),
        Output('current-item-store', 'data'),
        Output('current-item_path-store', 'data'),
    ],
    Input('current-pathname-container', 'data'),
    State('router-list-container', 'data'),
    prevent_initial_call=True,
)
