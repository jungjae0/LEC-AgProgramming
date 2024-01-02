import serial
import urllib.request as urllib2
import serial
import time
from datetime import datetime
import random  # Replace this with actual code to get temperature and humidity values
import pandas as pd

def get_aws(date):
    Site = 85
    Dev = 1
    Year = date.year
    Mon = f"{date.month:02d}"
    Day = f"{date.day:02d}"

    aws_url =f'http://203.239.47.148:8080/dspnet.aspx?Site={Site}&Dev={Dev}&Year={Year}&Mon={Mon}&Day={Day}'
    data = urllib2.urlopen(aws_url)

    df = pd.read_csv(data, header=None)
    df.columns = ['datetime', 'temp', 'hum', 'X', 'X', 'X', 'rad', 'wd', 'X', 'X', 'X', 'X', 'X', 'ws', 'rain', 'maxws', 'bv', 'X']
    drop_cols = [col for col in df.columns if 'X' in col]
    df = df.drop(columns=drop_cols)

    last_data = df.iloc[-1]
    temp = last_data['temp']
    humid = last_data['hum']

    return temp, humid


ser = serial.Serial('COM1', 115200)  # Replace 'COMx' with the correct serial port

while True:
    date = datetime.now()

    temp, humid = get_aws(date)
    data = f"{temp}, {humid}"
    print(data)
    ser.write(data.encode())
    time.sleep(60)  # Adjust the delay based on your requirements
