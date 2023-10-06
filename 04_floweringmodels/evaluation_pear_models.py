import os
import pandas as pd

def main():
    input_dir = 'output/agweather'

    stations = [station.split('.')[0] for station in os.listdir(input_dir)]

if __name__ == '__main__':
    main()