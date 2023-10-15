import os
import re
import numpy as np
import pandas as pd
import tqdm
pd.set_option('mode.chained_assignment', None)

# -------정시의 기온 예측
def predict_time_temp(df):
    for hour in range(0, 24):
        if 0 <= hour <= 3:
            df[f'temp_{hour}시'] = (df['max_temp'].shift(1) - df['min_temp']) * (np.sin((4 - hour) * 3.14 / 30) ** 2) + df[
                'min_temp']

        elif 4 <= hour <= 13:
            df[f'temp_{hour}시'] = (df['max_temp'] - df['min_temp']) * (np.sin((hour - 4) * 3.14 / 18) ** 2) + df['min_temp']

        elif 14 <= hour <= 23:
            df[f'temp_{hour}시'] = (df['max_temp'] - df['min_temp'].shift(-1)) * (np.sin((28 - hour) * 3.14 / 30) ** 2) + df[
                'min_temp'].shift(-1)
    return df

# -------GDH 모델
def cal_gdh_value(x):
    gdh = 0
    if 4 < x < 25:
        gdh = 10.5 * (1 + np.cos(np.pi + np.pi * ((x - 4) / 21)))
    elif 25 < x < 36:
        gdh = 21 * (1 + np.cos((np.pi / 2) + (np.pi / 2) * ((x - 4) / 25)))
    return gdh

def predict_time_gdh(df):
    id_vars = [col for col in df.columns if not 'temp_' in col]

    for hour in range(0, 24):
        df[f'gdh_{hour}시'] = df[f'temp_{hour}시'].apply(cal_gdh_value)

    col_gdh = [col for col in df.columns if 'gdh_' in col]
    df = df.melt(id_vars=id_vars, value_vars=col_gdh, var_name="time", value_name='gdh')
    df['time'] = df['time'].apply(lambda x: re.findall(r'\d+', x)[0]).astype(int)
    df = df.sort_values(by=['date', 'time'], ascending=[True, True]).reset_index().drop(columns='index')

    return df

def gdh_model(df):
    # after data 필요
    gdh_values = [1395, 1674, 2790, 5579]

    after_df = pd.DataFrame()

    for year in df['year'].unique():
        # year = row['year']
        year_df = df[df['year'] == year]
        year_df = year_df[year_df['date'] >= pd.to_datetime(f'{year}-02-20')]

        after_df = pd.concat([after_df, year_df], ignore_index=True)

    # after = pd.concat(after_df)
    after = predict_time_gdh(after_df)
    after['cumsum_gdh'] = after.groupby('year')['gdh'].cumsum()

    dates_list = []

    for gdh_value in gdh_values:
        dormancy_dates = after[after['cumsum_gdh'] >= gdh_value].groupby('year')['date'].first().reset_index()
        dormancy_dates = dormancy_dates.rename(columns={'date': f'gdh_{gdh_value}'})
        dates_list.append(dormancy_dates)

    gdh_date = pd.concat(dates_list, axis=1)
    gdh_date = gdh_date.loc[:, ~gdh_date.columns.duplicated()]
    # gdh_values = [1395, 1674, 2790, 5579]
    #
    # after_df = pd.DataFrame()
    # dates_list = []
    # for year in df['year'].unique():
    #     year_df = df[df['year'] == year]
    #     year_df = year_df[year_df['date'] >= pd.to_datetime(f'{year}-02-20')]
    #
    #     year_df = predict_time_gdh(year_df)
    #     year_df['cumsum_gdh'] = year_df['gdh'].cumsum()
    #     for gdh_value in gdh_values:
    #         dormancy_dates = year_df[year_df['cumsum_gdh'] >= gdh_value].groupby('year')['date'].first().reset_index()
    #         dormancy_dates = dormancy_dates.rename(columns={'date': f'gdh_{gdh_value}'})
    #         dates_list.append(dormancy_dates)
    #
    # gdh_date = pd.concat(dates_list, axis=1)
    # gdh_date = gdh_date.loc[:, ~gdh_date.columns.duplicated()]

    return gdh_date


# -------CD 모델
def add_chill_heat(row):
    tc = 6.1
    max = row['max_temp']
    min = row['min_temp']
    avg = row['temp']

    chill = 0
    anti_chill = 0

    if 0 <= tc <= min <= max:
        chill = 0
        anti_chill = avg - tc
    elif 0 <= min <= tc <= max:
        chill = -((avg - min) - (max - tc) / 2)
        anti_chill = (max - tc) / 2
    elif 0 <= min <= max <= tc:
        chill = -(avg - min)
        anti_chill = 0
    elif min < 0 <= max <= tc:
        chill = (max / (max - min)) * (max / 2)
        anti_chill = 0
    elif min < 0 < tc < max:
        chill = -(((max / (max - min)) * (max / 2)) - ((max - tc) / 2))
        anti_chill = (max - tc) / 2


    row['chill_unit'] = chill
    row['heat_unit'] = anti_chill

    return row

def cd_model(df):
    cr = -100.5 # 저온요구도
    hr = 275.1 # 고온요구도

    df['date'] = pd.to_datetime(df['date'])
    df['season_year'] = df['year']
    df.loc[(df["month"] >= 10), "season_year"] = df["year"] + 1
    df = df[~df['month'].isin([7, 8, 9])]
    df = df.sort_values(by=['year', 'date'], ascending=[True, True])

    # chill days 계산
    df = df.apply(add_chill_heat, axis=1)

    expected_full_bloom_df = pd.DataFrame()
    for year in df['season_year'].unique():
        year_df = df[df['season_year'] == year]

        year_df = year_df[(year_df['date'] >= pd.to_datetime(f'{year}-02-20'))]

        year_df['cumsum_heat_unit'] = year_df['heat_unit'].cumsum()
        year_df = year_df[year_df['cumsum_heat_unit'] >= cr]

        expected_full_bloom = year_df[year_df['cumsum_heat_unit'] >= hr].head(1)

        expected_full_bloom_df = pd.concat([expected_full_bloom_df, expected_full_bloom])

    cd_date = expected_full_bloom_df[['year', 'date']].reset_index(drop=True)
    cd_date = cd_date.rename(columns={"date": "CD"})

    return cd_date

# -------Utah 모델
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

def predict_chill_unit(df):
    for hour in range(0, 24):
        df[f'chill_{hour}시'] = df[f'temp_{hour}시'].apply(add_chill_unit)

    col_chill = [col for col in df.columns if 'chill_' in col]
    df['date_cumsum_chill'] = df[col_chill].sum(axis=1) # 일별 저온요구도
    df = df.drop(columns=col_chill)
    return df

def utah_model(df,cu_MAX):
    df = predict_chill_unit(df)

    # 휴면개시일
    df['season_year'] = df["year"]
    df.loc[df["month"] > 9, "season_year"] = df["year"] + 1
    df = df.sort_values(by=['year', 'season_year', 'month'], ascending=[True, False, True])
    dormancy_dates = df[df['date_cumsum_chill'] >= 0].groupby('season_year')['date'].first().reset_index()

    start_dormancy = []
    for idx, row in dormancy_dates.iterrows():
        season_year = row['season_year']
        date = row['date']
        year_df = df[df['season_year'] == season_year]
        year_df = year_df[(year_df['date'] >= pd.to_datetime(date))]
        start_dormancy.append(year_df)

    after = pd.concat(start_dormancy)
    after = predict_chill_unit(after)
    after['chill_unit_cumsum'] = after.groupby('season_year')['date_cumsum_chill'].cumsum()

    stop_dormancy_dates = after[after['chill_unit_cumsum'] >= cu_MAX].groupby('season_year')['date'].first().reset_index()
    dormancy_dates = pd.merge(dormancy_dates, stop_dormancy_dates, on='season_year', how='inner')
    dormancy_dates = dormancy_dates.rename(columns={'season_year': 'year',
                                                    'date_x': 'start_dormancy_date',
                                                    'date_y': 'stop_dormancy_date', })

    return dormancy_dates

def full_bloom_dates(df):
    cu_MAX = 800
    df = predict_time_temp(df)
    df['date'] = pd.to_datetime(df['date'])


    cd_dates = cd_model(df)
    gdh_dates = gdh_model(df)
    dormancy_dates = utah_model(df, cu_MAX)

    all_dates = pd.merge(cd_dates, gdh_dates, on='year', how='inner')
    all_dates = pd.merge(all_dates, dormancy_dates, on='year', how='inner')

    return all_dates

def run(weather_dir, output_filename):
    weather_filenames = os.listdir(weather_dir)
    all_station = pd.DataFrame()
    for filename in tqdm.tqdm(weather_filenames):
        df = pd.read_csv(os.path.join(weather_dir, filename), encoding='cp949')

        all_dates = full_bloom_dates(df)
        all_dates['지역'] = filename.split('.')[0]

        all_station = pd.concat([all_station, all_dates], ignore_index=True)

    all_station.to_csv(output_filename, index=False, encoding='utf-8')



def main():
    weather_dir = '../output/weather'
    output_filename = '../output/apple_result.csv'
    run(weather_dir, output_filename)


if __name__ == '__main__':
    main()
