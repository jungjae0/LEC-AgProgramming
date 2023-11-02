import pytz
import pandas as pd
import urllib.request as urllib2
from datetime import datetime, timedelta

desired_timezone = pytz.timezone('Asia/Seoul')

def get_aws(date):
    today_year, today_month, today_day = date.year, date.month, date.day
    today_month = f"{today_month:02d}"
    today_day = f"{today_day:02d}"

    aws_url =f'http://203.239.47.148:8080/dspnet.aspx?Site=85&Dev=1&Year={today_year}&Mon={today_month}&Day={today_day}'
    data = urllib2.urlopen(aws_url)

    df = pd.read_csv(data, header=None)
    df.columns = ['Datetime', 'temp', 'hum', 'X', 'X', 'X', 'rad', 'wd', 'X', 'X', 'X', 'X', 'X', 'ws', 'rain', 'maxws', 'bv', 'X']
    drop_cols = [col for col in df.columns if 'X' in col]
    df = df.drop(columns=drop_cols)
    return df

def main():
    start_date = datetime(2023, 10, 24)
    end_date = datetime(2023, 10, 31)
    date_list = []

    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)

    all_data = pd.DataFrame()
    for date in date_list:
        each_data = get_aws(date)
        all_data = pd.concat([all_data, each_data])

    filename = './output/aws_data.csv'
    all_data.to_csv(filename, index=False)

if __name__ == '__main__':
    main()
