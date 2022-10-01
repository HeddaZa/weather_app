from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd



def subplots(reset, start_date = None, end_date = None):
    # if start_date and end_date:
    #     reset = filter_for_date(reset, start_date=start_date, end_date=end_date)


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

def period_index(df, period):
    df = df.reset_index(drop = False)
    df['date'] = pd.to_datetime(df['date'])
    if period == 'year':
        df['period'] = df['date'].dt.year
        df['period_xaxis'] = df['date'].apply(lambda x: x.replace(year = 2000))
    elif period == 'month':
        df['period'] = df['date'].dt.month
        df['period_xaxis'] = df['date'].dt.day
    elif period == 'week':
        df['period'] = df['date'].dt.isocalendar().week
        df['period_xaxis'] = df['date'].dt.day_name()
    else:
        raise ValueError('Wrong period format')
    return df.set_index(['period','date'])

def plot_period(df, period = 'week'):
    df = period_index(df, period = period)
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    for index in df.index.levels[0]:
        period_data = df.loc[index]
        fig.add_trace(
            go.Scatter(x = period_data['period_xaxis'],y=period_data['t'],
            name = str(index)),
            row = 1, col = 1
        )
    fig.update_layout( title_text=f"Comparison by {period}")
    return fig

def filter_for_date(df, start_date, end_date):
    return df[df.index.to_series().between(start_date, end_date)]

def plot_period_choose_date(df, start_date, end_date, period = 'week'):
    df = filter_for_date(df, start_date, end_date)
    #df = df.loc[start_date:end_date]
    df = period_index(df, period = period)
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    for index in df.index.levels[0]:
        period_data = df.loc[index]
        fig.add_trace(
            go.Scatter(x = period_data['period_xaxis'],y=period_data['t'],
            name = str(index)),
            row = 1, col = 1
        )
    fig.update_layout( title_text=f"Comparison by {period}")
    return fig
