from dash.dependencies import Input, Output

from server import app


# url-pathname控制currentKey回调
app.clientside_callback(
    '''
    (data) => {
        if (data) {
            return data['current_key'];
        }
        return window.dash_clientside.no_update;
    }
    ''',
    Output('index-side-menu', 'currentKey'),
    Input('current-key-container', 'data'),
    prevent_initial_call=True
)
