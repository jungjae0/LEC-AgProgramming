import copy
from datetime import datetime
import aws2summary
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, dash_table, callback
import dash_bootstrap_components as dbc

app = Dash(__name__)

folder_path = "./output"
start_date_str = "20231029"
end_date_str = "20231104"
def week_temp_line(df):
    # fig = px.line(df, x='datetime', y='temp', title='Temperature Over Time')
    max_temp = df['temp'].max()
    min_temp = df['temp'].min()

    fig = go.Figure(data=[go.Scatter(x=df["datetime"], y=df['temp'], name='temp')])
    fig.update_layout(xaxis={"rangeslider": {"visible": True}, "type": "date",
                             "range": [df["datetime"].min(), df["datetime"].max()]})

    fig.add_trace(go.Scatter(x=[pd.to_datetime(df[df['temp'] == max_temp]['datetime'].values[0])],
                             y=[max_temp],
                             mode='markers',
                             marker=dict(size=10, color='red'),
                             name='최고기온'))
    fig.add_trace(go.Scatter(x=[pd.to_datetime(df[df['temp'] == min_temp]['datetime'].values[0])],
                             y=[min_temp],
                             mode='markers',
                             marker=dict(size=10, color='blue'),
                             name='최저기온'))
    fig.update_layout(title_text=f'{df["datetime"].min().date()} ~ {df["datetime"].max().date()}')

    return fig

def day_temp_line(df, date):
    df = df[df['datetime'].dt.date == pd.to_datetime(date)]

    max_temp = df['temp'].max()
    min_temp = df['temp'].min()

    fig = go.Figure(data=[go.Scatter(x=df["datetime"], y=df['temp'], name='temp')])
    fig.update_layout(xaxis={"rangeslider": {"visible": True}, "type": "date",
                             "range": [df["datetime"].min(), df["datetime"].max()]})

    fig.add_trace(go.Scatter(x=[pd.to_datetime(df[df['temp'] == max_temp]['datetime'].values[0])],
                             y=[max_temp],
                             mode='markers',
                             marker=dict(size=10, color='red'),
                             name='최고기온'))
    fig.add_trace(go.Scatter(x=[pd.to_datetime(df[df['temp'] == min_temp]['datetime'].values[0])],
                             y=[min_temp],
                             mode='markers',
                             marker=dict(size=10, color='blue'),
                             name='최저기온'))

    return fig
def daily_temprain_linebar(df):

    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df["날짜"], y=df['평균기온'], mode='lines', name='평균기온', line=dict(color='green')))
    fig.add_trace(go.Scatter(x=df["날짜"], y=df['최저기온'], mode='lines', name='최저기온', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df["날짜"], y=df['최고기온'], mode='lines', name='최고기온', line=dict(color='red')))

    fig.add_trace(go.Bar(x=df["날짜"], y=df["강수량"], name='강수량', yaxis='y2', marker=dict(color='blue')))

    fig.update_layout(yaxis=dict(title='온도 (℃)'))

    fig.update_layout(yaxis2=dict(title='강수량', overlaying='y', side='right', showgrid=False))
    fig.update_yaxes(range=[0, 100], tick0=0, dtick=10, secondary_y=True)

    return fig

def rain_count_pie(df):
    grouped_data = df.groupby('강수계급').size().reset_index(name='갯수')
    fig = px.pie(grouped_data, names='강수계급', values='갯수', title='강수계급별 분포',
                 hover_data=['강수계급', '갯수'])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

def wd_count_pie(df):
    grouped_data = df.groupby('풍향').size().reset_index(name='갯수')
    fig = px.pie(grouped_data, names='풍향', values='갯수', title='풍향계급별 분포',
                 hover_data=['풍향', '갯수'])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig




def show_df(minute_df, hour_df):
    show_cols = ['datetime', 'temp', 'hum', 'rad', 'wd', 'ws', 'rain', 'maxws']
    show_minute = copy.deepcopy(minute_df)
    show_minute = show_minute[show_cols]

    show_hour = copy.deepcopy(hour_df)
    show_hour = show_hour[show_cols]


minute_df, hour_df = aws2summary.get_dataframe(start_date_str, end_date_str, folder_path)
daily_df, wd_category = aws2summary.daily_data(minute_df, hour_df)
dates_df = aws2summary.weekly_date(daily_df)



daily_df['폭염일수'] = daily_df['폭염일수'].apply(lambda x: '-' if x == 0 else x)
daily_df['강수일수'] = daily_df['강수일수'].apply(lambda x: '-' if x == 0 else x)
daily_df['한파일수'] = daily_df['한파일수'].apply(lambda x: '-' if x == 0 else x)


min_date_allowed = datetime.strptime(start_date_str, "%Y%m%d").strftime("%Y-%m-%d")
max_date_allowed = datetime.strptime(end_date_str, "%Y%m%d").strftime("%Y-%m-%d")

app.layout = html.Div([
    dbc.Col(
        [
            dcc.Tabs(
                id="tabs",
                value="tab-1",
                children=[
                    dcc.Tab(
                        label="Week",
                        value="tab-1",
                        children=[dcc.Graph(figure=week_temp_line(minute_df))],
                    ),
                    dcc.Tab(
                        label="Day",
                        value="tab-2",
                        children=[dcc.DatePickerSingle(id='date-picker',
                                                       date=max_date_allowed,
                                                       min_date_allowed=min_date_allowed,
                                                       max_date_allowed=max_date_allowed),
                                  dcc.Graph(id='day-temp-line-graph')],
                    ),
                ],
            ),
        ],
        width=8,
    ),
    dash_table.DataTable(data=daily_df.to_dict('records'), page_size=10),
    dash_table.DataTable(data=dates_df.to_dict('records'), page_size=10),

    dcc.Graph(figure=daily_temprain_linebar(daily_df)),
    html.Div([
        dcc.Graph(figure=rain_count_pie(daily_df), style={'display': 'inline-block'}),
        dcc.Graph(figure=wd_count_pie(wd_category), style={'display': 'inline-block'})
    ])
])

@app.callback(
    Output('day-temp-line-graph', 'figure'),
    Input('date-picker', 'date')
)
def update_day_temp_line(selected_date):
    # 선택한 날짜에 따른 그래프를 생성
    fig = day_temp_line(minute_df, selected_date)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)