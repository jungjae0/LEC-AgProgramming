from flask import Flask, render_template, request, send_file, Response
import requests
from urllib.parse import unquote
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
from io import BytesIO
import base64
from datetime import datetime, timedelta
import json
from matplotlib import font_manager, rc

font_path = "C:/Windows/Fonts/NGULIM.TTF"
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

app = Flask(__name__)


def get_reservoir_code(fac_name, county):
    url = 'http://apis.data.go.kr/B552149/reserviorWaterLevel/reservoircode/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    params = {
        'serviceKey': 'serviceKey',  # 서비스 키를 여기에 입력하세요.
        'pageNo': '1',
        'numOfRows': '1',
        'fac_name': fac_name,
        'county': county,
    }

    response = requests.get(url, params=params, headers=headers)
    decoded_content = unquote(response.content.decode("utf-8"))

    root = ET.fromstring(decoded_content)

    fac_code = root.find('.//fac_code').text
    return fac_code


def fetch_reservoir_data(fac_name, county):
    fac_code = get_reservoir_code(fac_name, county)

    url = 'http://apis.data.go.kr/B552149/reserviorWaterLevel/reservoirlevel/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    params = {
        'serviceKey': 'serviceKey',  # 서비스 키를 여기에 입력하세요.
        'pageNo': '1',
        'numOfRows': '720',
        'fac_code': fac_code,
        'date_s': f'20230101',
        'date_e': f'{datetime.now().strftime("%Y%m%d")}'
    }

    response = requests.get(url, params=params, headers=headers)
    decoded_content = unquote(response.content.decode("utf-8"))

    root = ET.fromstring(decoded_content)

    check_dates = []
    counties = []
    fac_codes = []
    fac_names = []
    rates = []
    water_levels = []

    for item in root.findall('.//item'):
        check_date = item.find('check_date').text
        county = item.find('county').text
        fac_code = item.find('fac_code').text
        fac_name = item.find('fac_name').text
        rate = float(item.find('rate').text)
        water_level = float(item.find('water_level').text)

        check_dates.append(check_date)
        counties.append(county)
        fac_codes.append(fac_code)
        fac_names.append(fac_name)
        rates.append(rate)
        water_levels.append(water_level)

    df = pd.DataFrame({
        'check_date': check_dates,
        'county': counties,
        'fac_code': fac_codes,
        'fac_name': fac_names,
        'rate': rates,
        'water_level': water_levels
    })
    df['check_date'] = pd.to_datetime(df['check_date'])
    df.fillna(0)

    return df


def create_line_chart(df):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()
    ax1.plot(df['check_date'], df['rate'], 'g-', label="green")
    ax2.plot(df['check_date'], df['water_level'], 'b-', label="blue")
    ax1.set_xlabel('측정 날짜')
    ax1.set_ylabel('저수율(%)', color='g')
    ax2.set_ylabel('저수지 수위(m)', color='b')

    ax1.set_xlim(df['check_date'].min(), df['check_date'].max())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=8))
    plt.xticks(rotation=45)

    fig.legend()

    plt.grid()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    plt.clf()
    plt.close()

    chart_data = base64.b64encode(buffer.read()).decode()
    return chart_data


@app.route("/")
def hello_world():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
<script
  src="https://code.jquery.com/jquery-3.7.1.min.js"
  integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo="
  crossorigin="anonymous"></script>
    <title>Title</title>
</head>
<body>
<h3>저수지 일별 그래프 확인<h3>
<form id="form_id" action="javascript:post_query()">
    <label>저수지 이름:</label>
    <input type="text" name="fac_name">
    <label>저수지 위치:</label>
    <input type="text" name="county">
    <button type="submit">그래프 그리기</button>
</form>
<div id="today_rate_container"></div>
<div id="chart_container"></div>
    <script>
        $(document).ready(function() {
            $("#form_id").submit(function(e) {
                e.preventDefault();
                $.ajax({
                    type: "GET",
                    url: "http://172.30.1.8:5000/reservoir",
                    data: $("#form_id").serialize(),
                    dataType: "json",

                    success: function(data) {
                        var todayRate = parseFloat(data.today_rate);
                        var color = "";
                        if (todayRate >= 60) {
                            color = "blue";
                        } else if (todayRate > 50) {
                            color = "gold";
                        } else if (todayRate > 40) {
                            color = "orange";
                        } else {
                            color = "red";
                        }

                        $("#today_rate_container").text("오늘 저수율: " + todayRate).css("color", color);
                        $("#chart_container").html("<img src='data:image/png;base64," + data.chart_data + "'>");
                    },
                    error: function() {
                        alert("Failed to retrieve chart data.");
                    }
                });
            });
        });
    </script>
</body>
</html>"""


@app.route("/reservoir")
def f2c():
    fac_name = request.args.get("fac_name")
    county = request.args.get("county")
    if fac_name and county:
        df = fetch_reservoir_data(fac_name, county)
        chart_data = create_line_chart(df)
        return json.dumps({"chart_data": chart_data,
                           "today_rate": df[df['check_date'] == datetime.now().strftime("%Y%m%d")]['rate'].values[0]})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")