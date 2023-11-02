import os
import requests
import pandas as pd


def download(url, file_name):
    with open(file_name, 'wb') as file:
        response = requests.get(url)
        file.write(response.content)

def download_weather(weather_file):
    url = "https://api.taegon.kr/station/146/?sy=2022&ey=2022&format=csv"
    download(url, weather_file)

def get_gdd(weather_file, month, day):
    df = pd.read_csv(weather_file, skipinitialspace=True)
    base_temp = 5
    df['eff_tavg'] = df['tavg'] - base_temp
    df.loc[df['eff_tavg'] < 0, 'eff_tavg'] = 0

    df['monthday'] = df['month'] * 100 + df['day']
    monthday = month * 100 + day

    # df['eff_tavg'] = df['eff_tavg'].apply(lambda x: x if x > 0 else 0)
    # df['gdd'] = df['eff_tavg'].cumsum()
    # print(df[(df['month'] == month) & (df['day'] == day)]['gdd'])

    return df[df['monthday'] <= monthday]['eff_tavg'].sum()

def main():
    weather_file = "weather_jeonju_2022.csv"
    if not os.path.exists(weather_file):
        download_weather(weather_file)

    month = 6
    day = 20
    GDD = get_gdd(weather_file, month, day)

    print(f"{month}월 {day}일까지 GDD는 {GDD}degree-day입니다.")

if __name__ == '__main__':
    main()