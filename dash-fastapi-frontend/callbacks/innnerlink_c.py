from dash.dependencies import Input, Output, State
from server import app


app.clientside_callback(
    """
    (_, current_item) => {
        if (current_item?.props?.modules === 'innerlink') {
            return [current_item?.props?.link, true];
        }
        throw window.dash_clientside.PreventUpdate;
    }
    """,
    [
        Output('innerlink-iframe', 'src'),
        Output('init-iframe-interval', 'disabled'),
    ],
    Input('init-iframe-interval', 'n_intervals'),
    State('index-side-menu', 'currentItem'),
)
