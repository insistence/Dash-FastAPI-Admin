import dash
from dash.dependencies import Input, Output

from server import app


# url-pathname控制currentKey回调
@app.callback(
    Output('index-side-menu', 'currentKey'),
    Input('current-key-container', 'data'),
    prevent_initial_call=True
)
def pathname_update_current_key(data):
    if data:
        return data['current_key']

    return dash.no_update
