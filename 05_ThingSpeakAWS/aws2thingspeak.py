import urllib.request
import pytz
from datetime import datetime
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
import requests

desired_timezone = pytz.timezone('Asia/Seoul')

def get_aws_list(write_api_key, Site, Dev, Year, Mon, Day):
    aws_url =f'http://203.239.47.148:8080/dspnet.aspx?Site={Site}&Dev={Dev}&Year={Year}&Mon={Mon}&Day={Day}'
    context = requests.get(aws_url).text
    data_sep = context.split("\r\n")

    data_list = [x.split(',')[:-1] for x in data_sep][:-1]

    last_data = data_list[-1]

    del last_data[3:6]
    del last_data[8:13]

    filed_text = 'field1={:0.1f}&field2={:0.1f}&field3={:0.1f}&field4={:0.1f}&field5={:0.1f}&field6={:0.1f}&field7={:0.1f}&field8={:0.1f}'.format(
            float(last_data[1]), float(last_data[2]), float(last_data[3]), float(last_data[4]), float(last_data[5]),
            float(last_data[6]), float(last_data[7]), float(last_data[8]))
    thing_write_url = f'https://api.thingspeak.com/update?api_key={write_api_key}&{filed_text}'
    urllib.request.urlopen(thing_write_url)


def get_aws(Site, Dev, Year, Mon, Day):
    aws_url =f'http://203.239.47.148:8080/dspnet.aspx?Site={Site}&Dev={Dev}&Year={Year}&Mon={Mon}&Day={Day}'
    data = urllib.request.urlopen(aws_url)

    df = pd.read_csv(data, header=None)

    df.columns = ['YYYY-MM-DD hh:mm:ss', '온도', '습도', 'X', 'X', 'X', '일사', '풍향', 'X', 'X', 'X', 'X', 'X', '풍속(1분 평균 풍속)', '강우', '최대순간풍속(60초 중 최고값)', '배터리전압', 'X']
    drop_cols = [col for col in df.columns if 'X' in col]
    df = df.drop(columns=drop_cols)

    return df

def get_filed_value(Site, Dev, Year, Mon, Day):
    data = get_aws(Site, Dev, Year, Mon, Day)
    last_data = data.iloc[-1]

    filed_text = 'field1={:0.1f}&field2={:0.1f}&field3={:0.1f}&field4={:0.1f}&field5={:0.1f}&field6={:0.1f}&field7={:0.1f}&field8={:0.1f}'.format(
        float(last_data['온도']), float(last_data['습도']), float(last_data['일사']), float(last_data['풍향']), float(last_data['풍속(1분 평균 풍속)']),
        float(last_data['강우']), float(last_data['최대순간풍속(60초 중 최고값)']), float(last_data['배터리전압']))

    return filed_text

def insertCloud(write_api_key, Site, Dev, Year, Mon, Day):
    filed_text = get_filed_value(Site, Dev, Year, Mon, Day)
    thing_write_url = f'https://api.thingspeak.com/update?api_key={write_api_key}&{filed_text}'
    urllib.request.urlopen(thing_write_url)

def exprotCloud(channel_id, read_api_key):
    number = 100
    thing_read_url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.csv?api_key={read_api_key}&results={number}'
    df = pd.read_csv(thing_read_url)

def main():
    write_api_key = 'write_api_key'
    read_api_key = 'read_api_key'
    channel_id = 'channel_id'

    date = datetime.now(desired_timezone)
    Year = date.year
    Mon = f"{date.month:02d}"
    Day = f"{date.day:02d}"
    Site = 85
    Dev = 1

    #----- Read ThingSpeak
    # exprotCloud(channel_id, read_api_key)


    #----- Write ThingSpeak
    scheduler = BackgroundScheduler()

    scheduler.add_job(insertCloud, 'interval', minutes=1, args=[write_api_key, Site, Dev, Year, Mon, Day])

    scheduler.start()
    try:

        while True:
            pass
    except (KeyboardInterrupt, SystemExit):

        scheduler.shutdown()

if __name__ == '__main__':
    main()
