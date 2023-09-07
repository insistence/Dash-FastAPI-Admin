from dash.dependencies import Input, Output, State, ClientsideFunction

from server import app


app.clientside_callback(
    '''
    (n_intervals, data) => {
        return [data, true];
    }
    ''',
    [Output('echarts-data-container', 'data'),
     Output('init-echarts-interval', 'disabled')],
    Input('init-echarts-interval', 'n_intervals'),
    State('init-echarts-data-container', 'data'),
    prevent_initial_call=True
)


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside_command_stats',
        function_name='render_command_stats_chart'
    ),
    Output('command-stats-charts-container', 'children'),
    Input('echarts-data-container', 'data')
)


app.clientside_callback(
    ClientsideFunction(
        namespace='clientside_memory',
        function_name='render_memory_chart'
    ),
    Output('memory-charts-container', 'children'),
    Input('echarts-data-container', 'data')
)

