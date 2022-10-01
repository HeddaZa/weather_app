from plotly.subplots import make_subplots
import plotly.graph_objects as go


def subplots(reset):
    ''' 
    plots three subplots: 
    - temperature (mean temperature, min temperature, max temperature)
    - precipitation
    - wind (mean velocity, max velocity)
    '''
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)

    fig.add_trace(
        go.Scatter(x=reset.index, y=reset['t'],
        name = 'mean temperature',
        legendgroup = '1',
        line = dict(color = 'rgb(255,102,102)')
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=reset.index, y=reset['tmax'],
        name = 'max temperature',
        legendgroup = '1',
        line = dict(color = 'rgb(204,0,0)')
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=reset.index, y=reset['tmin'],
        name= 'min temperature',
        showlegend= True,
        legendgroup = '1',
        line = dict(color = 'rgb(0,128,255)')),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=reset.index, y=reset['nied'],
        name = 'rain',
        #hoverinfo= 'name',
        legendgroup = '2',
        line = dict(color = 'rgb(0,100,255)'),
        fill='tozeroy'),
        row=2, col=1
    )


    fig.add_trace(
        go.Scatter(x=reset.index, y=reset['vv'],
        name = 'wind',
        legendgroup = '3',
        line = dict(color = 'rgb(204,0,204)')),
        row=3, col=1
    )
    fig.add_trace(
        go.Scatter(x=reset.index, y=reset['vvmax'],
        name = 'wind max',
        legendgroup = '3',
        line = dict(color = 'rgb(204,0,102)')),
        row=3, col=1
    )

    fig.update_layout(
        height=1000, 
        width=1000, 
        title_text="Plots of Temperature, Precipitation, and Wind Speed",
        legend_tracegroupgap = 270,
        xaxis3_title = 'Date',
        yaxis1_title = 'Celsius',
        yaxis2_title = 'mm',
        yaxis3_title = 'm/s',
        xaxis_showticklabels=True, 
        xaxis2_showticklabels=True
        )
    return fig
