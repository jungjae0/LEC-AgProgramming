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

app = Flask(__name__)

def get_reservoir_code(fac_name, county):
    url = 'http://apis.data.go.kr/B552149/reserviorWaterLevel/reservoircode/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    params = {
        'serviceKey': '8rRt9OVUEJmBrSsNYKceGV5IXGTa0FdqQmFqfJBECkkTZ8kAFrklLdOAr5WusKLTi2PMVy06WvibIqQozsblJQ==',  # 서비스 키를 여기에 입력하세요.
        'pageNo': '1',
        'numOfRows': '1',
        'fac_name': fac_name,
        'county': county,
    }

    response = requests.get(url, params=params, headers=headers)
    decoded_content = unquote(response.content.decode("utf-8"))

    root = ET.fromstring(decoded_content)

    # fac_code 엘리먼트 값을 읽어옴
    fac_code = root.find('.//fac_code').text
    return fac_code

def fetch_reservoir_data(fac_name, county):
    fac_code = get_reservoir_code(fac_name, county)

    url = 'http://apis.data.go.kr/B552149/reserviorWaterLevel/reservoirlevel/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

    params = {
        'serviceKey': '8rRt9OVUEJmBrSsNYKceGV5IXGTa0FdqQmFqfJBECkkTZ8kAFrklLdOAr5WusKLTi2PMVy06WvibIqQozsblJQ==',  # 서비스 키를 여기에 입력하세요.
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
    fig, ax1 = plt.subplots(figsize=(12,6))
    ax2 = ax1.twinx()
    ax1.plot(df['check_date'], df['rate'], 'g-', label="green")
    ax2.plot(df['check_date'], df['water_level'], 'b-', label="blue")
    ax1.set_xlabel('Check Date')
    ax1.set_ylabel('Rate', color='g')
    ax2.set_ylabel('Water Level', color='b')

    ax1.set_xlim(df['check_date'].min(), df['check_date'].max())
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=8))
    plt.xticks(rotation=45)

    fig.legend(loc="upper center")

    plt.grid()

    # Save the plot as a BytesIO object
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Clear the Matplotlib plot to release resources
    plt.clf()
    plt.close()

    # Convert the plot to base64 for embedding in HTML
    chart_data = base64.b64encode(buffer.read()).decode()
    return chart_data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        fac_name = request.form.get("fac_name")
        county = request.form.get("county")
        if fac_name and county:
            df = fetch_reservoir_data(fac_name, county)
            chart_data = create_line_chart(df)
            return render_template("index.html", df=df.to_html(classes='data'), chart_data=chart_data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
