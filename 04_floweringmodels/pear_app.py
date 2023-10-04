import requests
import pandas as pd
from urllib.parse import unquote
import xml.etree.ElementTree as ET
# https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15078057
# https://weather.rda.go.kr/w/weather/observationInfo.do
def get_weather():
    raw_info = pd.read_csv('./input/농업기상_관측정보.csv', encoding='cp949')
    stations = ['이천시 장호원', '천안시 직산읍', '영천시 금호읍', '완주군 반교리',
                '사천시 송포동', '상주시 외서면', '나주시 금천면', '울주군 서생면']

    station_info = raw_info[raw_info['지점명'].isin(stations)]


    url = 'http://apis.data.go.kr/1390802/AgriWeather/WeatherObsrInfo/GnrlWeather/getWeatherTermDayList'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    params = {
        'serviceKey': '8rRt9OVUEJmBrSsNYKceGV5IXGTa0FdqQmFqfJBECkkTZ8kAFrklLdOAr5WusKLTi2PMVy06WvibIqQozsblJQ==',  # 서비스 키를 여기에 입력하세요.
        'Page_No': '1',
        'Page_Size': '10',
        'frc_Code': '060200'
    }

    response = requests.get(url, params=params, headers=headers)
    decoded_content = unquote(response.content.decode("utf-8"))

def main():
    get_weather()

if __name__ == '__main__':
    main()