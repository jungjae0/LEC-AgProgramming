import os
import numpy as np
import pandas as pd
import geopandas as gpd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib import font_manager, rc
from matplotlib.ticker import ScalarFormatter
import mapclassify as mc
from mpl_toolkits.axes_grid1 import make_axes_locatable

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

pd.set_option('mode.chained_assignment', None)

def draw_date_map(df):
    year = 2020
    df = df[df['year'] == year]
    kr_shp = '../input/sig_20230729/sig.shp'
    kr = gpd.read_file(kr_shp, encoding='cp949')
    kr['SIG_KOR_ABBR'] = kr['SIG_KOR_NM'].str[:2]

    kr_gpd = pd.merge(kr, df, left_on='SIG_KOR_ABBR', right_on='지역', how='outer')

    fig, ax = plt.subplots(1, 1)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)

    column = 'DVR'
    kr_gpd.plot(column, ax=ax, legend=True, cax=cax, cmap='OrRd', missing_kwds={'color': 'gray'}, k=7)

    formatter = ScalarFormatter(useOffset=False, useMathText=True)
    formatter.set_scientific(False)
    cax.yaxis.set_major_formatter(formatter)

    ticks = cax.get_yticks()
    cax.set_yticklabels([datetime.fromordinal(int(tick)).strftime('%m-%d') for tick in ticks])

    ax.set_title("만개일")
    ax.set_axis_off()
    plt.show()


def draw_date_temp_line(df):
    station = '강릉'
    df = df[df['지역'] == station]

    years = df['year'].astype(int)
    dates = df['DVR']#.dt.strftime('%j').astype(float)

    tavg = df['DVR-tavg']
    temp = df['DVR-temp']
    plt.figure(figsize=(10, 10))
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Temp', color='tab:red')
    line1, = ax1.plot(years, tavg, color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    locs = np.arange(years.min(), years.max() + 1, 2)
    labels = locs.astype(int)
    ax1.set_xticks(locs)
    ax1.set_xticklabels(labels, rotation=45)
    ax1.yaxis.grid(True)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Date', color='tab:blue')
    line2, = ax2.plot(years, dates, color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    def format_date(x, pos=None):
        month = int(x // 30) + 1
        day = int(x % 30) + 1
        return f'{month:02d}-{day:02d}'

    formatter = ticker.FuncFormatter(format_date)
    ax2.yaxis.set_major_formatter(formatter)

    plt.legend(handles=(line1, line2), labels=('Avg Daily Temp', 'Date'), loc='upper left')
    plt.yticks(np.arange(dates.min(), dates.max(), 2))
    plt.title('DVR and DVR-temp Over the Years')
    plt.tight_layout()
    plt.show()

def table_date_station(df):
    year = 2020
    df = df[df['year'] == year].tail(10)
    regions = df['지역'].unique()

    df['max_date'] = df[['mDVR', 'DVR', 'CD']].max(axis=1)#.dt.strftime('%j').astype(float)
    df['min_date'] = df[['mDVR', 'DVR', 'CD']].min(axis=1)#.dt.strftime('%j').astype(float)
    bar_height = 0.9
    plt.barh(regions, width=(df['max_date'] - df['min_date']), height=bar_height, left=df['min_date'], color='pink')
    plt.xticks(np.arange(df['min_date'].min() - 10, df['max_date'].max() + 10, 10))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.xticks(rotation=45)


    for i, (min_date, max_date) in enumerate(zip(df['min_date'], df['max_date'])):

        min_datetime = pd.to_datetime('2020-01-01') + pd.DateOffset(days=min_date - 1)
        max_datetime = pd.to_datetime('2020-01-01') + pd.DateOffset(days=max_date - 1)

        min_date_str = min_datetime.strftime('%m-%d')
        max_date_str = max_datetime.strftime('%m-%d')

        plt.text(min_date, i, min_date_str, ha='right', va='center', color='blue')
        plt.text(max_date, i, max_date_str, ha='left', va='center', color='red')

    plt.axvline(x=59, color='gray', linestyle='--')
    plt.axvline(x=90, color='gray', linestyle='--')
    plt.axvline(x=120, color='gray', linestyle='--')

    plt.tight_layout()
    plt.show()

def add_chill_unit(x):
    if x <= 1.4:
        return 0
    elif 1.5 <= x <= 2.4:
        return 0.5
    elif 2.5 <= x <= 9.1:
        return 1.0
    elif 9.2 <= x <= 12.4:
        return 0.5
    elif 12.5 <= x <= 15.9:
        return 0
    elif 16.0 <= x <= 18.0:
        return -0.5
    elif 18 <= x:
        return -1.0

def add_predict_temp(df):
    for hour in range(0, 24):
        if 0 <= hour <= 3:
            df[f'temp_{hour}시'] = (df['max_temp'].shift(1) - df['min_temp']) * (np.sin((4 - hour) * 3.14/30) ** 2) + df['min_temp']
        elif 4 <= hour <= 13:
            df[f'temp_{hour}시'] = (df['max_temp'] - df['min_temp']) * (np.sin((hour - 4) * 3.14 / 18) ** 2) + df['min_temp']
        elif 14 <= hour <= 23:
            df[f'temp_{hour}시'] = (df['max_temp'] - df['min_temp'].shift(-1)) * (np.sin((28 - hour) * 3.14 / 30) ** 2) + df['min_temp'].shift(-1)

        df[f'chill_{hour}시'] = df[f'temp_{hour}시'].apply(add_chill_unit)

    df = df.drop(columns=[col for col in df.columns if 'temp_' in col])

    col_chill = [col for col in df.columns if 'chill_' in col]
    df['date_cumsum_chill'] = df[col_chill].sum(axis=1)#.cumsum()
    df = df.drop(columns=col_chill)

    return df

def draw_date_cr_line(df):
    station = '강릉'
    year = 2020
    df = df[(df['지역'] == station) & (df['year'] == year)]
    # date_columns = ['start_dormancy_date', 'stop_dormancy_date']
    # df[date_columns] = df[date_columns].applymap(pd.to_datetime)
    start_date = pd.to_datetime(df['start_dormancy_date'].values[0])
    stop_date = pd.to_datetime(df['stop_dormancy_date'].values[0])
    # print(stop_date, start_date)
    weather = pd.read_csv(f'../output/weather/{station}.csv', encoding='utf-8')
    weather['season_year'] = weather["year"]
    weather.loc[weather["month"] > 9, "season_year"] = weather["year"] + 1
    weather['date'] = pd.to_datetime(weather['date'])
    weather = weather[(weather['date'] >= start_date)]
    weather = add_predict_temp(weather)
    weather['date_cumsum_chill'] = weather['date_cumsum_chill'].cumsum()
    cr1600 = pd.to_datetime(weather[weather['date_cumsum_chill'] >= 1600]['date'].values[0])#.reset_index()

    chill_unit = weather[(weather['date'] <= cr1600) & (weather['date'] >= start_date)]
    chill_unit['jday'] = pd.to_datetime(chill_unit['date']).dt.strftime('%j').astype(float)

    dot_date = stop_date
    dot_value = chill_unit[chill_unit['date'] == dot_date]['date_cumsum_chill'].values[0]

    cr = chill_unit['date_cumsum_chill']
    dates = chill_unit['date']
    plt.figure(figsize=(10, 10))
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Year')
    ax1.set_ylabel('저온 축적량(CU)')
    ax1.plot(dates, cr, color='tab:blue')
    plt.scatter(dot_date, dot_value, marker='o', color='blue', s=50, label='Special Date')
    plt.text(dot_date, dot_value, dot_date.strftime('%Y-%m-%d'), ha='right', va='bottom', color='black', fontsize=12)

    ax1.tick_params(axis='y')
    ax1.yaxis.grid(True)
    plt.yticks(rotation=-45)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('./figs/date_cu.png')


def main():
    df = pd.read_csv('../output/analysis_data.csv', encoding='utf-8')
    date_columns = ['DVR', 'mDVR', 'CD']

    for column in date_columns:
        df[column] = pd.to_datetime(df[column]).dt.strftime('%j').astype(float)

    # 지도 > 전국 연도별 만개 예측 지도
    # draw_date_map(df)

    # box plot >

    # line plot > 만개달의 평균 온도 + 만개일 https://highparknaturecentre.com/cherry-blossom-tracking/
    # draw_date_temp_line(df)

    # line plot > 휴면타파시기-저온축적(평년 + 선택) https://fruit.nihhs.go.kr/pear/dormancy/dormancyInfo.do
    # draw_date_cr_line(df)
    
    # 만개일 범위 표 > 세 개 모델의 최대/최소 값을 범위로 https://www.nippon.com/en/japan-data/h01564/
    # table_date_station(df)


if __name__ == '__main__':
    main()

