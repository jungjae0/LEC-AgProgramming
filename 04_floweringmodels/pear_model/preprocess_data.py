import os
import tqdm
import numpy as np
import pandas as pd

pd.set_option('mode.chained_assignment', None)

def add_lat_long():
    info = pd.read_csv('../input/종관기상_관측지점.csv', encoding='utf-8')[['지점명','위도','경도','고도']]
    df = pd.read_csv('../output/result.csv', encoding='utf-8')

    save = pd.merge(info, df, left_on='지점명', right_on='지역', how='inner')
    save.to_csv('../output/st.csv', index=False, encoding='utf-8')

def cal_gdd(df):
    df["season_year"] = df["year"]
    df.loc[df["month"] > 4, "season_year"] = df["year"] + 1
    df = df.sort_values(by=['year', 'season_year', 'month'], ascending=[True, False, True])
    df["GDD"] = df['temp']
    df["GDD"] = df["GDD"].apply(lambda x: 0 if x < 5 else x)
    df['GDD'] = df.groupby('season_year')['GDD'].cumsum()
    df.to_csv('../output/st.csv', index=False, encoding='utf-8')

    return df

def add_date_temp(input_dir):
    pred = pd.read_csv('../output/result.csv', encoding='utf-8')
    models = ['DVR', 'mDVR', 'CD']
    for model in models:
        pred[f'{model}'] = pd.to_datetime(pred[f'{model}'])
        pred[f'{model}-year'] = pred[f'{model}'].dt.year
        pred[f'{model}-month'] = pred[f'{model}'].dt.month

    result = []
    for station in tqdm.tqdm(pred['지역'].unique()):
        pred_date = pred[pred['지역'] == station].reset_index()
        weather = pd.read_csv(os.path.join(input_dir, f'{station}.csv'), encoding='utf-8')
        weather['date'] = pd.to_datetime(weather['date'])
        weather['year'] = weather['date'].dt.year
        weather['month'] = weather['date'].dt.month
        weather = cal_gdd(weather)
        tavg = weather.groupby(['year', 'month'])['temp'].mean().reset_index()

        for model in models:
            pred_date[f'{model}-temp'] = pd.merge(weather, pred_date, left_on='date', right_on=model, how='inner')['temp']
            pred_date[f'{model}-tavg'] = pd.merge(tavg, pred_date, left_on=['year', 'month'], right_on=[f'{model}-year', f'{model}-month'], how='inner')['temp']

        result.append(pred_date)

    save = pd.concat(result)
    save.to_csv('../output/result_temp_test.csv', index=False, encoding='utf-8')


def add_chill_unit(x):
    if x <= 1.4:
        return 0
    elif 1.5 <= x <= 2.4:
        return 0.5
    elif 2.5 <= x <= 9.1:
        return 1.0
    elif 9.2 <= x <= 12.4:
        return 0.5
    elif 12.5 <= x <= 15.9:
        return 0
    elif 16.0 <= x <= 18.0:
        return -0.5
    elif 18 <= x:
        return -1.0


def add_predict_temp(df):
    for hour in range(0, 24):
        if 0 <= hour <= 3:
            df[f'temp_{hour}시'] = (df['max_temp'].shift(1) - df['min_temp']) * (np.sin((4 - hour) * 3.14/30) ** 2) + df['min_temp']
        elif 4 <= hour <= 13:
            df[f'temp_{hour}시'] = (df['max_temp'] - df['min_temp']) * (np.sin((hour - 4) * 3.14 / 18) ** 2) + df['min_temp']
        elif 14 <= hour <= 23:
            df[f'temp_{hour}시'] = (df['max_temp'] - df['min_temp'].shift(-1)) * (np.sin((28 - hour) * 3.14 / 30) ** 2) + df['min_temp'].shift(-1)

        df[f'chill_{hour}시'] = df[f'temp_{hour}시'].apply(add_chill_unit)

    df = df.drop(columns=[col for col in df.columns if 'temp_' in col])

    col_dvr1 = [col for col in df.columns if 'chill_' in col]
    df['date_cumsum_chill'] = df[col_dvr1].sum(axis=1)#.cumsum()
    df = df.drop(columns=col_dvr1)

    return df

def add_dormancy_date():
    date_df = pd.read_csv("../output/result.csv")

    all_dormancy_list = []
    for station in tqdm.tqdm(date_df['지역'].unique()):
        all_weather = pd.read_csv(f"../output/weather/{station}.csv")
        all_weather['date'] = pd.to_datetime(all_weather['date'])
        all_weather = add_predict_temp(all_weather) # 일별 cumsum_chill_unit 값 생성

        # 연도별 휴면개시일 구하기
        all_weather['season_year'] = all_weather["year"]
        all_weather.loc[all_weather["month"] > 9, "season_year"] = all_weather["year"] + 1
        all_weather = all_weather.sort_values(by=['year', 'season_year', 'month'], ascending=[True, False, True])
        dormancy_dates = all_weather[all_weather['date_cumsum_chill'] >= 0].groupby('season_year')['date'].first().reset_index()

        start_dormancy = []
        for idx, row in dormancy_dates.iterrows():
            season_year = row['season_year']
            date = row['date']
            df =  all_weather[all_weather['season_year'] == season_year]
            df = df[(df['date'] >= pd.to_datetime(date))]
            start_dormancy.append(df)

        weather = pd.concat(start_dormancy)
        weather = add_predict_temp(weather)
        weather['chill_unit_cumsum'] = weather.groupby('season_year')['date_cumsum_chill'].cumsum()

        stop_dormancy_dates = weather[weather['chill_unit_cumsum'] >= 1200].groupby('season_year')['date'].first().reset_index()
        start_stop_dormancy_date = pd.merge(dormancy_dates, stop_dormancy_dates, on='season_year', how='inner')
        start_stop_dormancy_date = start_stop_dormancy_date.rename(columns={'season_year': 'year',
                                                                            'date_x': 'start_dormancy_date',
                                                                            'date_y': 'stop_dormancy_date',})
        start_stop_dormancy_date['지역'] = station
        all_dormancy_list.append(start_stop_dormancy_date)

    all_dormancy = pd.concat(all_dormancy_list)

    save = pd.merge(all_dormancy, date_df, on=['year', '지역'], how='inner')
    save.to_csv('../output/station_date.csv', index=False, encoding='utf-8')

    return save

def main():
    input_dir = '../output/weather'

    # add_date_temp(input_dir)

    add_dormancy_date()
if __name__ == '__main__':
    main()
