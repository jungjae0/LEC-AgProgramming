import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from matplotlib import font_manager, rc
from matplotlib.ticker import ScalarFormatter


# warnings.filterwarnings(action='ignore')

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

pd.set_option('mode.chained_assignment', None)


def draw_commom_temp_line(year= 2020, station='강릉', weather_dir = './output/weather'):
    # df = df[(df['year'] == year) & (df['지역'] == station)]
    # stop_date = df['mean_date'].values[0]
    # cul_date = df['cul_date'].values[0]

    # stop_date = datetime.strptime(stop_date, '%Y-%m-%d')
    # cul_date = datetime.strptime(cul_date, '%Y-%m-%d')

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

    # plt.axvline(x=stop_date, color='black', linestyle='--')
    # plt.axvline(x=cul_date, color='black', linestyle='--')

    plt.ylabel('Temperature (℃)')
    plt.xlabel('Date')
    plt.title(f'{station} - 평년 vs. {year} 일평균기온 그래프')
    plt.legend()
    plt.tight_layout()

    plt.show()

def main():
    draw_commom_temp_line()


if __name__ == '__main__':
    main()


