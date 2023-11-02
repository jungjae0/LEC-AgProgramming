import urllib.request
import pytz
from datetime import datetime
import urllib.request as urllib2
import pandas as pd
import time
from apscheduler.schedulers.background import BackgroundScheduler

desired_timezone = pytz.timezone('Asia/Seoul')

def get_aws():
    today = datetime.now(desired_timezone)
    today_year, today_month, today_day = today.year, today.month, today.day
    today_month = f"{today_month:02d}"
    today_day = f"{today_day:02d}"

    aws_url =f'http://203.239.47.148:8080/dspnet.aspx?Site=85&Dev=1&Year={today_year}&Mon={today_month}&Day={today_day}'
    data = urllib2.urlopen(aws_url)

    df = pd.read_csv(data, header=None)

    df.columns = ['YYYY-MM-DD hh:mm:ss', '온도', '습도', 'X', 'X', 'X', '일사', '풍향', 'X', 'X', 'X', 'X', 'X', '풍속(1분 평균 풍속)', '강우', '최대순간풍속(60초 중 최고값)', '배터리전압', 'X']
    drop_cols = [col for col in df.columns if 'X' in col]

    df = df.drop(columns=drop_cols)

    return df

def get_filed_value():
    df = get_aws()
    last_data = df.iloc[-1]

    filed_text = 'field1={:0.1f}&field2={:0.1f}&field3={:0.1f}&field4={:0.1f}&field5={:0.1f}&field6={:0.1f}&field7={:0.1f}&field8={:0.1f}'.format(
        float(last_data['온도']), float(last_data['습도']), float(last_data['일사']), float(last_data['풍향']), float(last_data['풍속(1분 평균 풍속)']),
        float(last_data['강우']), float(last_data['최대순간풍속(60초 중 최고값)']), float(last_data['배터리전압']))

    return filed_text

def insertCloud(api_key):
    filed_text = get_filed_value()
    thing_write_url =  f'https://api.thingspeak.com/update?api_key={api_key}&{filed_text}'
    urllib.request.urlopen(thing_write_url)


def main():
    api_key = 'C2O88SRT54C3WRPU'

    scheduler = BackgroundScheduler()

    scheduler.add_job(insertCloud, 'interval', minutes=10, args=[api_key])

    scheduler.start()
    try:

        while True:
            pass
    except (KeyboardInterrupt, SystemExit):

        scheduler.shutdown()

if __name__ == '__main__':
    main()
