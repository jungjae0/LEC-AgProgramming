import os
import tqdm
import requests
import pandas as pd
from urllib.parse import unquote
import xml.etree.ElementTree as ET
# https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15078057
# https://weather.rda.go.kr/w/weather/observationInfo.do

def call_api(serviceKey, page, year, station_code):
    url = 'http://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/GnrlWeather/getWeatherYearDayList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    params = {
        'serviceKey': serviceKey,
        'Page_No': f'{page}',
        'Page_Size': '100',
        'search_Year': f'{year}',
        'obsr_Spot_Code': f'{station_code}'
    }

    response = requests.get(url, params=params, headers=headers)
    xml_content = unquote(response.content.decode("utf-8"))
    return xml_content

def xml2df(xml_content):
    root = ET.fromstring(xml_content)
    xml_item = root.findall('.//item')

    stn_Code_list = [item.find('stn_Code').text for item in xml_item]
    stn_Name_list = [item.find('stn_Name').text for item in xml_item]
    date_list = [item.find('date').text for item in xml_item]
    max_Temp_list = [item.find('max_Temp').text for item in xml_item]
    min_Temp_list = [item.find('min_Temp').text for item in xml_item]
    temp_list = [item.find('temp').text for item in xml_item]

    # Create a DataFrame
    df = pd.DataFrame({
        'stn_code': stn_Code_list,
        'stn_name': stn_Name_list,
        'date': date_list,
        'max_temp': max_Temp_list,
        'min_temp': min_Temp_list,
        'temp': temp_list
    })
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day

    return df


def save_weather_data(output_dir, serviceKey, stations, years):
    raw_info = pd.read_csv('../input/농업기상_관측정보.csv', encoding='cp949')
    station_info = raw_info[raw_info['지점명'].isin(stations)]

    for idx, row in station_info.iterrows():
        station_code = row['지점코드']
        station_name = row['지점명'].replace(" ", "")
        station_data = pd.DataFrame()
        for year in tqdm.tqdm(years, desc=station_name):
            cache_file = os.path.join(output_dir, f'cache_dir/{station_name}_{year}.csv')
            year_data = pd.DataFrame()
            if not os.path.exists(cache_file):
                for page in range(1, 6):
                    xml_content = call_api(serviceKey, page, year, station_code)
                    each_data = xml2df(xml_content)
                    year_data = pd.concat([year_data, each_data], ignore_index=True)
                year_data.to_csv(cache_file, index=False, encoding='cp949')
            else:
                year_data = pd.read_csv(cache_file, encoding='cp949')

            station_data = pd.concat([year_data, station_data], ignore_index=True)
        station_data.to_csv(os.path.join(output_dir, f'agweather/{station_name}.csv'), index=False, encoding='cp949')

def save_ag_weather(output_dir):
    serviceKey = '8rRt9OVUEJmBrSsNYKceGV5IXGTa0FdqQmFqfJBECkkTZ8kAFrklLdOAr5WusKLTi2PMVy06WvibIqQozsblJQ=='
    stations = ['이천시 장호원', '천안시 직산읍', '영천시 금호읍', '완주군 반교리',
                '사천시 송포동', '상주시 외서면', '나주시 금천면', '울주군 서생면']
    years = [2017, 2018, 2019, 2020]

    save_weather_data(output_dir, serviceKey, stations, years)

def save_aws_weather(output_dir):
    station_info = pd.read_csv("../input/종관기상_관측지점.csv", encoding='utf-8')

    for idx, row in tqdm.tqdm(station_info.iterrows()):
        code = row['지점코드']
        name = row['지점명']
        file_name = os.path.join(output_dir, f"{name}.csv")
        if not os.path.exists(file_name):
            url = f"https://api.taegon.kr/stations/{code}/?sy=2002&ey=2022&format=csv"
            df = pd.read_csv(url, sep='\\s*,\\s*', engine="python")
            df.columns = [col.strip() for col in df.columns]
            df = df.rename(columns={'tavg': 'temp', 'tmax': 'max_temp', 'tmin': 'min_temp'})
            df['date'] = pd.to_datetime(dict(year=df.year, month=df.month, day=df.day))
            df = df[['date', 'year', 'month', 'day', 'temp', 'max_temp', 'min_temp']]

            df.to_csv(file_name, index=False, encoding='utf-8')

def main():
    output_dir = '../output/weather'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # save_ag_weather(output_dir)
    # save_aws_weather(output_dir)

if __name__ == '__main__':
    main()