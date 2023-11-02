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
# from pandas.table.plotting import table # EDIT: see deprecation warnings below
import warnings

warnings.filterwarnings(action='ignore')

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

pd.set_option('mode.chained_assignment', None)



def draw_map(df, year, model):
    lst = [year - i for i in range(4, -1, -1)]

    kr_shp = './input/sig_20230729/sig.shp'
    kr = gpd.read_file(kr_shp, encoding='cp949')
    kr['SIG_KOR_ABBR'] = kr['SIG_KOR_NM'].str[:2]
    kr_gpd = pd.merge(kr, df, left_on='SIG_KOR_ABBR', right_on='지역', how='outer')

    date_vmin = kr_gpd[model].min()
    date_vmax = kr_gpd[model].max()

    temp_vmin = kr_gpd[f'{model}_tavg'].min()
    temp_vmax = kr_gpd[f'{model}_tavg'].max()

    fig, axes = plt.subplots(2, 5, figsize=(25, 12))
    divider = make_axes_locatable(axes[0, -1])
    cax = divider.append_axes("right", size="5%", pad=0.5)


    divider2 = make_axes_locatable(axes[1, -1])
    cax2 = divider2.append_axes("right", size="5%", pad=0.5)

    model_column = model
    kr_gpd[kr_gpd['year'] == lst[0]].plot(model_column, ax=axes[0, 0], legend=False, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=date_vmin, vmax=date_vmax)
    kr_gpd[kr_gpd['year'] == lst[1]].plot(model_column, ax=axes[0, 1], legend=False, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=date_vmin, vmax=date_vmax)
    kr_gpd[kr_gpd['year'] == lst[2]].plot(model_column, ax=axes[0, 2], legend=False, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=date_vmin, vmax=date_vmax)
    kr_gpd[kr_gpd['year'] == lst[3]].plot(model_column, ax=axes[0, 3], legend=False, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=date_vmin, vmax=date_vmax)
    kr_gpd[kr_gpd['year'] == lst[4]].plot(model_column, ax=axes[0, 4], legend=True, cax=cax, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=date_vmin, vmax=date_vmax)


    formatter = ScalarFormatter(useOffset=False, useMathText=True)
    formatter.set_scientific(False)
    cax.yaxis.set_major_formatter(formatter)

    ticks = cax.get_yticks()
    cax.set_yticklabels([datetime.fromordinal(int(tick)).strftime('%m-%d') for tick in ticks])

    temp_column = f'{model}_tavg'
    kr_gpd[kr_gpd['year'] == lst[0]].plot(temp_column, ax=axes[1, 0], legend=False, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=temp_vmin, vmax=temp_vmax)
    kr_gpd[kr_gpd['year'] == lst[1]].plot(temp_column, ax=axes[1, 1], legend=False, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=temp_vmin, vmax=temp_vmax)
    kr_gpd[kr_gpd['year'] == lst[2]].plot(temp_column, ax=axes[1, 2], legend=False, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=temp_vmin, vmax=temp_vmax)
    kr_gpd[kr_gpd['year'] == lst[3]].plot(temp_column, ax=axes[1, 3], legend=False, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=temp_vmin, vmax=temp_vmax)
    kr_gpd[kr_gpd['year'] == lst[4]].plot(temp_column, ax=axes[1, 4], legend=True, cax=cax2, cmap='rainbow',
                                          missing_kwds={'color': 'gray'}, k=7, vmin=temp_vmin, vmax=temp_vmax)


    for i, ax in enumerate(axes[0]):
        ax.set_title(f"{lst[i]}년 만개일")
        ax.set_axis_off()

    for i, ax in enumerate(axes[1]):
        ax.set_title(f"{lst[i]}년 만개달 평균 온도")
        ax.set_axis_off()

    plt.show()
    # plt.savefig('./output/figs/date_tavg_map.png')


    # years = [2016, 2017, 2018, 2019, 2020]
    #
    # fig, axes = plt.subplots(1, 5, figsize=(30, 5))
    # vmin = kr_gpd['DVR'].min()
    # vmax = kr_gpd['DVR'].max()
    #
    # for i, year in enumerate(years):
    #     ax = axes[i]
    #     divider = make_axes_locatable(ax)
    #     cax = divider.append_axes("right", size="5%", pad=0.1)
    #
    #     column = 'DVR'
    #     kr_gpd[kr_gpd['year'] == year].plot(column, ax=ax, legend=True, cax=cax, cmap='rainbow',
    #                                         missing_kwds={'color': 'gray'}, k=7,
    #                                         vmin=vmin, vmax=vmax)  # vmin과 vmax를 추가합니다.
    #
    #     formatter = ScalarFormatter(useOffset=False, useMathText=True)
    #     formatter.set_scientific(False)
    #     cax.yaxis.set_major_formatter(formatter)
    #
    #     ticks = cax.get_yticks()
    #     cax.set_yticklabels([datetime.fromordinal(int(tick)).strftime('%m-%d') for tick in ticks])
    #
    #     ax.set_title(f"{year}년")
    #     ax.set_axis_off()
    #
    # plt.show()


def draw_models_date_line(df, station, models):
    df = df[df['지역'] == station]

    plt.figure(figsize=(12, 6))

    for model in models:
        plt.plot(df['year'], df[model], label=model, linestyle='-', marker='o')

    def format_date(x, pos=None):
        month = int(x // 30) + 1
        day = int(x % 30) + 1
        return f'{month:02d}-{day:02d}'


    date_format = mdates.DateFormatter('%m-%d')
    plt.gca().yaxis.set_major_formatter(date_format)

    plt.xlim(df['year'].min()-1, df['year'].max()+1)
    plt.xlabel('Year')
    plt.ylabel(f'예측 만개일')
    plt.title(f'{station} 예측만개일')
    plt.grid(True)
    plt.legend()

    plt.show()

#---------- 만개일과 만개달의 평균온도 변화추이
def draw_date_temp_line(df, station, model):
    df = df[df['지역'] == station]

    years = df['year'].astype(int)
    dates = df[model]

    tavg = df[f'{model}_temp']
    plt.figure(figsize=(12, 6))
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Temperature (℃)', color='tab:red')
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

    plt.legend(handles=(line1, line2), labels=('만개일 일평균 기온', f'{model} 예측 만개일'), loc='upper left')
    plt.yticks(np.arange(dates.min(), dates.max(), 2))
    plt.title(f'{station} - 만개일 일평균 기온 vs. 만개일')

    plt.tight_layout()
    plt.show()
    # plt.savefig('./output/figs/date_tavg_line.png')

def draw_date_tavg_line(df, station, model):
    df = df[df['지역'] == station]

    years = df['year'].astype(int)
    dates = df[model]

    tavg = df[f'{model}_tavg']
    # tavg = df[f'{model}_temp']
    plt.figure(figsize=(12, 6))
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Year')
    ax1.set_ylabel('Temperature (℃)', color='tab:red')
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


    plt.legend(handles=(line1, line2), labels=('만개월 평균 기온', f'{model} 예측 만개일'), loc='upper left')
    plt.yticks(np.arange(dates.min(), dates.max(), 2))
    plt.title(f'{station} - 만개월 평균 기온 vs. 만개일')
    plt.tight_layout()
    plt.show()
    # plt.savefig('./output/figs/date_tavg_line.png')


#---------- 예측 만개일 범위 표
def table_date_station(df, year, models):
    df = df[df['year'] == year]
    df['max_date'] = df[models].max(axis=1)
    df['min_date'] = df[models].min(axis=1)

    num_rows = 2
    num_cols = 4
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(24, 6), sharex=True)

    for i in range(num_rows):
        for j in range(num_cols):
            ax = axes[i, j]

            # 데이터를 8등분하여 각 서브플롯에 표시
            start_idx = (i * num_cols + j) * (len(df) // (num_rows * num_cols))
            end_idx = ((i * num_cols + j + 1) * (len(df) // (num_rows * num_cols)))
            sub_df = df[start_idx:end_idx]
            regions = sub_df['지역'].unique()

            bar_height = 0.9
            ax.barh(regions, width=(sub_df['max_date'] - sub_df['min_date']), height=bar_height,
                    left=sub_df['min_date'], color='pink')
            ax.set_xticks(np.arange(df['min_date'].min() - 10, df['max_date'].max() + 10, 10))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m%d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
            ax.tick_params(axis='x', rotation=45)

            for k, (min_date, max_date) in enumerate(zip(sub_df['min_date'], sub_df['max_date'])):
                min_datetime = pd.to_datetime(f'{year}-01-01') + pd.DateOffset(days=min_date - 1)
                max_datetime = pd.to_datetime(f'{year}-01-01') + pd.DateOffset(days=max_date - 1)
                min_date_str = min_datetime.strftime('%m-%d')
                max_date_str = max_datetime.strftime('%m-%d')
                ax.text(min_date, k, min_date_str, ha='right', va='center', color='blue')
                ax.text(max_date, k, max_date_str, ha='left', va='center', color='red')

            ax.axvline(x=59, color='gray', linestyle='--')
            ax.axvline(x=90, color='gray', linestyle='--')
            ax.axvline(x=120, color='gray', linestyle='--')

    plt.tight_layout()
    plt.show()

    # plt.savefig('./output/figs/date_table.png')

#---------- 휴면타파시기
def predict_chill(df):
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


def common_after_dormancy(df, current_year, start_date, max_CU):
    all_df = pd.DataFrame()
    for year in df['year'].unique():
        try:
            each_chill_unit = current_after_dormancy(df, pd.to_datetime(f'{year - 1}-{start_date}'), max_CU)
            all_df = pd.concat([all_df, each_chill_unit], ignore_index=True)
        except:
            pass

    chill_unit = all_df.groupby(['month', 'day'])['date_cumsum_chill'].mean().reset_index()
    chill_unit['year'] = current_year
    chill_unit.loc[chill_unit["month"] > 9, "year"] = chill_unit["year"] - 1
    chill_unit = chill_unit[(chill_unit['month'] != 2) | (chill_unit['day'] != 29)]

    chill_unit['date'] = pd.to_datetime(chill_unit[['year', 'month', 'day']])
    chill_unit = chill_unit.sort_values(by='date')

    chill_unit = chill_unit.loc[(chill_unit['date_cumsum_chill'] > 0).idxmax():]

    return chill_unit

def current_after_dormancy(df, start_date, max_CU):
    df = df[(df['date'] >= start_date)]
    df['date_cumsum_chill'] = df['date_cumsum_chill'].cumsum()
    cr_max_date = pd.to_datetime(df[df['date_cumsum_chill'] >= max_CU]['date'].values[0])
    chill_unit = df[(df['date'] <= cr_max_date) & (df['date'] >= start_date)]

    return chill_unit

def plt_values(df, stop_CU):
    stop_date = df[df['date_cumsum_chill'] >= stop_CU].groupby('year')['date'].first().values[0]
    stop_date = pd.to_datetime(stop_date)
    dot_value = stop_CU

    cr = df['date_cumsum_chill']
    dates = df['date']

    return cr, dates, stop_date, dot_value


def draw_date_cr_line(df, station, year, max_CU, stop_CU, weather_dir):
    import datetime
    common = df[(df['지역'] == station) & (df['year'] >= 2009) & (df['year'] <= 2022)]
    # 평년 휴면개시일과 휴면타파일
    common_start_date = pd.to_datetime(common['start_dormancy_date']).dt.strftime('%j').astype(float).mean()
    common_start_date = datetime.date.fromordinal(datetime.date(year, 1, 1).toordinal() + int(common_start_date) - 1).strftime('%m-%d')

    df = df[(df['year'] == year)]

    # 특정 연도 휴면개시일과 휴면타파일
    current_start_date = pd.to_datetime(df['start_dormancy_date'].values[0])

    # 기상데이터 불러오기 & season_year & chill unit 열 추가
    weather = pd.read_csv(os.path.join(weather_dir, f'{station}.csv'), encoding='utf-8')
    weather['season_year'] = weather["year"]
    weather.loc[weather["month"] > 9, "season_year"] = weather["year"] + 1
    weather['date'] = pd.to_datetime(weather['date'])
    weather = predict_chill(weather)

    # 평년 chill
    common_chill_unit = common_after_dormancy(weather, year, common_start_date, max_CU)

    # 해당연도의 chill
    current_chill_unit = current_after_dormancy(weather, current_start_date, max_CU)

    current_cr, current_dates, current_stop_date, current_value = plt_values(current_chill_unit, stop_CU)
    common_cr, common_dates, common_stop_date, common_value = plt_values(common_chill_unit, stop_CU)

    plt.figure(figsize=(10, 10))
    fig, ax1 = plt.subplots()

    ax1.set_xlabel('Date')
    ax1.set_ylabel('저온 축적량(CU)')
    ax1.plot(current_dates, current_cr, color='tab:blue', label=f'{year}년')
    ax1.plot(common_dates, common_cr, color='black', label='평년')
    plt.scatter(current_stop_date, current_value, marker='o', color='blue', s=30)
    plt.text(current_stop_date, current_value, current_stop_date.strftime('%Y-%m-%d'), ha='right', va='bottom', color='black', fontsize=12)

    plt.scatter(common_stop_date, common_value, marker='o', color='black', s=30)
    plt.text(common_stop_date, common_value, common_stop_date.strftime('%Y-%m-%d'), ha='left', va='bottom', color='black', fontsize=12)

    ax1.tick_params(axis='y')
    ax1.yaxis.grid(True)


    plt.yticks(rotation=-45)
    plt.xticks(rotation=45)

    plt.title(f'{station} - {year}년 휴면타파시기')
    plt.tight_layout()
    plt.legend()
    plt.show()

    # plt.savefig('./output/figs/cumsum_chill.png')

#---------- 일별 온도 변화 추이
def draw_temp_line(df, year, station, weather_dir):
    import seaborn as sns
    lst = [year - i for i in range(2, -1, -1)]

    weather = pd.read_csv(os.path.join(weather_dir, f'{station}.csv'), encoding='utf-8')
    weather['Day of Year'] = pd.to_datetime(weather['date']).dt.day_of_year

    sns.set_palette("Set1")

    for i, year in enumerate(lst):
        year_weather = weather[weather['year'] == year]
        sns.lineplot(data=year_weather, x="Day of Year", y="temp", label=f'{year}')

    plt.title(f'{station} - {lst[0]} ~ {lst[-1]} 일평균 기온 변화 추이')
    plt.legend()
    plt.show()

    # plt.savefig('./output/figs/temp_line.png')


#---------- 평년 + 선택 연도 온도 변화 추이
def draw_commom_temp_line(df, year, station, weather_dir):
    df = df[(df['year'] == year) & (df['지역'] == station)]
    stop_date = df['mean_date'].values[0]
    cul_date = df['cul_date'].values[0]

    stop_date = datetime.strptime(stop_date, '%Y-%m-%d')
    cul_date = datetime.strptime(cul_date, '%Y-%m-%d')

    weather = pd.read_csv(os.path.join(weather_dir, f'{station}.csv'), encoding='utf-8')
    weather['date'] = pd.to_datetime(weather['date'])

    weather = weather[(weather['month'] != 2) | (weather['day'] != 29)]

    common = weather.groupby(['month', 'day'])[['temp', 'max_temp', 'min_temp']].mean().reset_index()
    common['year'] = year
    common['date'] = pd.to_datetime(common[['year', 'month', 'day']])


    current = weather[weather['year'] == year]

    plt.figure(figsize=(12, 6))

    plt.plot(common['date'], common['temp'], color='orange', label='평년')
    plt.plot(current['date'], current['temp'], color='blue', label=f'{year}년')
    plt.fill_between(current['date'], current['min_temp'], current['max_temp'], color='gray', alpha=0.5, label='온도 범위')

    plt.axvline(x=stop_date, color='black', linestyle='--')
    plt.axvline(x=cul_date, color='black', linestyle='--')

    plt.ylabel('Temperature (℃)')
    plt.xlabel('Date')
    plt.title(f'{station} - 평년 vs. {year} 일평균기온 그래프')
    plt.legend()
    plt.tight_layout()

    plt.show()

    # plt.savefig('./output/figs/common_current_temp_line.png')


# def show_dataframe(df, station, models):
#     for model in models:
#         df[model] = pd.to_datetime(df[model], origin=pd.Timestamp('2023-01-01'), unit='D').dt.strftime('%m-%d')
#
#     models.append('year')
#     df = df[df['지역'] == station][models]
#
#     font_size = 10
#     bbox = [0, 0, 1, 1]
#     plt.axis('off')
#     mpl_table = plt.table(cellText=df.values, rowLabels=df.index, bbox=bbox, colLabels=df.columns)
#     mpl_table.auto_set_font_size(False)
#     mpl_table.set_fontsize(font_size)
#     plt.title(station)
#     plt.show()


def draw_stations_date_line(df, stations, model):

    plt.figure(figsize=(12, 6))


    for station in stations:
        station_df = df[df['지역'] == station]
        plt.plot(station_df['year'], station_df[model], marker='o', label=station)

        # for i, txt in enumerate(station_df[model]):
        #     txt = datetime.strptime(str(txt), '%j').strftime('%m-%d')
        #     plt.annotate(txt, (station_df['year'].iloc[i], station_df[model].iloc[i]),
        #                  textcoords='offset points', xytext=(0, 10), ha='center')

    date_format = mdates.DateFormatter('%m-%d')
    plt.gca().yaxis.set_major_formatter(date_format)

    plt.xlim(df['year'].min()-1, df['year'].max()+1)
    plt.xlabel('Year')
    plt.ylabel(f'{model} 예측 만개일')
    plt.title(f'지역별 {model} 예측 만개일')
    plt.grid(True)
    plt.legend()

    plt.show()


def select_tree(tree):
    if tree == 'pear':
        models = ['DVR', 'mDVR', 'CD']
        maxCU = 1600
        stop_CU = 1200
        return models, maxCU, stop_CU

    elif tree == 'apple':
        # models = ['gdh_1395', 'gdh_1674', 'gdh_2790', 'gdh_5579', 'CD']
        models = ['gdh_5579', 'CD']

        maxCU = 1000
        stop_CU = 800

        return models, maxCU, stop_CU


# def main():
#     weather_dir = './output/weather'
#
#     tree = 'pear'
#     year = 2020
#     station = '전주'
#     model = 'CD'
#
#     df = pd.read_csv(f'./output/{tree}_analysis.csv', encoding='utf-8')
#     models, maxCU, stopCU = select_tree(tree)
#
#     for column in models:
#         df[column] = pd.to_datetime(df[column]).dt.strftime('%j').astype(int)
#
#     stations = ['전주', '강릉', '광주']
#     draw_models_date_line(df, station, models)
#
#     # # line plat > stations 만개일 변화 추이
#     # draw_stations_date_line(df, stations, model)
#     #
#     # # 지도 > 전국 연도별 만개 예측 지도
#     # draw_map(df, year, model)
#     #
#     # # line plot > 만개달의 평균 온도 + 만개일
#     # draw_date_temp_line(df, station, model)
#     #
#     # # line plot > 휴면타파시기-저온축적(평년 + 선택)
#     # draw_date_cr_line(df, station, year, maxCU, stopCU, weather_dir)
#     #
#     # # 만개일 범위 표 > 전체 모델의 최대/최소 값을 범위로
#     # table_date_station(df, year, models)
#     #
#     # # 휴면타파 이후 ~ 10월 까지 일별 온도 변화 추이
#     #
#     # draw_temp_line(df, year, station, weather_dir)
#     #
#     # # 평년 + 선택 연도 온도 변화 추이
#     # draw_commom_temp_line(df, year, station, weather_dir)
#
# if __name__ == '__main__':
#     main()


