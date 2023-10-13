import os
import tqdm
import numpy as np
import pandas as pd

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


# -------DVR 모델
def dvr_model(df):
    A = 107.94
    B = 0.9

    # 발육속도 > 5°C 이상의 온도만 계산
    df['DVRi'] = df['temp'].apply(lambda x: 100 / (A * (B ** x)) if x >= 5 else 0)

    # 발육단계 > 누적발육속도(∑DVRi. DVS)
    df['DVS'] = df.groupby('year')['DVRi'].cumsum()

    # 예상만개기 > 발육단계 == 100
    expected_full_bloom = df[df['DVS'] >= 100].groupby('year').first()

    dvr_date = expected_full_bloom['date'].reset_index()
    dvr_date = dvr_date.rename(columns={"date" : "DVR"})
    return dvr_date

# -------mDVR 모델
# 발육속도 모델을 이용한 배 ‘신고’ 자발휴면타파시기 추정
def get_dvr1(x):
    dvr = None
    if x < -6:
        dvr = 0

    elif -6 <= x < 0:
        dvr = 1.333 * (10 ** (-3)) + 2.222 * (10 ** (-4)) * x

    elif 0 <= x < 6:
        dvr = 1.333 * (10 ** (-3))

    elif 6 <= x < 9:
        dvr = 2.276 * (10 ** (-3)) - 1.571 * (10 ** (-4)) * x

    elif 9 <= x < 12:
        dvr = 3.448 * (10 ** (-3)) - 2.784 * (10 ** (-4)) * x

    elif 12 <= x:
        dvr = 0

    return dvr

def get_dvr2(x):
    dvr2 = None

    if x < 20:
        a = 35.27 - 12094 * ((x + 273) ** (-1))
        dvr2 =  np.exp(a)
    elif x >= 20:
        a = 5.82 - 3474 * ((x + 273) ** (-1))
        dvr2 =  np.exp(a)

    elif x < 0:
        dvr2 = 0

    return dvr2

def predict_time_dvr(df):
    for hour in range(0, 24):
        # 기온 상승에 따른 ‘신고’ 배나무의 만개일 변동 예측(Han 2010)
        df[f'DVR1_{hour}시'] = df[f'temp_{hour}시'].apply(get_dvr1) # 자발휴면기-DVR1
        df[f'DVR2_{hour}시'] = df[f'temp_{hour}시'].apply(get_dvr2) # 타발휴면기-DVR2

    df = df.drop(columns=[col for col in df.columns if 'temp_' in col])
    return df

def modified_dvr_model(df):
    df['season_year'] = df['year']
    df.loc[(df["month"] >= 10), "season_year"] = df["year"] + 1
    df = df[~df['month'].isin([7, 8, 9])]
    df = df.sort_values(by=['year', 'date'], ascending=[True, True])
    df = predict_time_dvr(df)

    all_date = pd.DataFrame()

    # 내생휴면해제종료일 2월 15일로 설정
    for year in df['season_year'].unique():
        year_df = df[df['season_year'] == year]

        year_df = year_df[(year_df['date'] >= pd.to_datetime(f'{year}-02-15'))] # 내생휴면 해제 종료일 설정
        col_dvr2 = [col for col in year_df.columns if 'DVR2' in col]
        year_df['DVR2'] = year_df[col_dvr2].sum(axis=1) # 만개기에 도달할 때까지 필요한 발육속도
        year_df['DVS2'] = year_df['DVR2'].cumsum()

        year_date = year_df[year_df['DVS2'] >= 0.9593].head(1)
        all_date = pd.concat([all_date, year_date])

    mdvr_date = all_date[['season_year', 'date']].reset_index(drop=True)
    mdvr_date = mdvr_date.rename(columns={"date" : "mDVR",
                                          "season_year": "year"})


    # # 내생휴면해제종료일 누적 DVR 값에 따라 설정
    # all_date = pd.DataFrame()
    # for year in df['season_year'].unique():
    #     year_df = df[df['season_year'] == year]
    #     col_dvr1 = [col for col in year_df.columns if 'DVR1' in col]
    #     year_df['DVR1'] = year_df[col_dvr1].sum(axis=1)
    #     year_df['DVS1'] = year_df['DVR1'].cumsum()
    #     year_df = year_df[year_df['DVS1'] >= 1] # 내생휴면 해제
    #
    #     year_df['DVS1'] = year_df['DVR1'].cumsum()
    #     year_df = year_df[year_df['DVS1'] >= 2] # 저온감응기(내생휴면과 강제휴면이 겹치는 시기) 종료 이후
    #
    #     # df = df[(df['date'] >= pd.to_datetime(f'{year}-02-15'))] # 내생휴면 해제 종료일 설정
    #     col_dvr2 = [col for col in year_df.columns if 'DVR2' in col]
    #     year_df['DVR2'] = year_df[col_dvr2].sum(axis=1) # 만개기에 도달할 때까지 필요한 발육속도
    #     year_df['DVS2'] = year_df['DVR2'].cumsum()
    #
    #     # 배 만개기 예측식 표
    #     # df = df[df['DVS2'] >= 2] # 만개기 조건
    #     # df['DVIf'] = df['DVR2'].cumsum()
    #     # expected_full_bloom = df[df['DVIf'] >= 0.9525].head(1)
    #     # expected_full_bloom_df = pd.concat([expected_full_bloom_df, expected_full_bloom])
    #
    #     # 기온 상승에 따른 ‘신고’ 배나무의 만개일 변동 예측(Han 2010)
    #     expected_full_bloom = year_df[year_df['DVS2'] >= 0.9593].head(1)
    #     all_date = pd.concat([all_date, expected_full_bloom])
    #
    # mdvr_date = all_date[['year', 'date']].reset_index(drop=True)
    # mdvr_date = mdvr_date.rename(columns={"date" : "mDVR"})

    return mdvr_date

# -------CD 모델
def add_chill_heat(row):
    tc = 5.4
    max = row['max_temp']
    min = row['min_temp']
    avg = row['temp']

    chill = 0
    anti_chill = 0

    # # Tab. 1. Equations for the five cases of Chill day Model
    # if 0 <= tc <= min <= max:
    #     chill = 0
    #     anti_chill = avg - tc
    # elif 0 <= min <= tc <= max:
    #     chill = -((avg - min) - (((max - tc) ** 2) / (2 * (max - min))))
    #     anti_chill = ((max - tc) ** 2) / (2 * (max - min))
    # elif 0 <= min <= max <= tc:
    #     chill = -(avg - min)
    #     anti_chill = 0
    # elif min < 0 <= max <= tc:
    #     chill = -((max ** 2) / (2 * (max - min)))
    #     anti_chill = 0
    # elif min < 0 < tc < max:
    #     chill = -((max ** 2) / (2 * (max - min))) - (((max - tc) ** 2) / (2 * (max - min)))
    #     anti_chill = ((max - tc) ** 2) / (2 * (max - min))

    # # Tab. 2. Equations for the five cases of NEW Model.
    # if 0 <= tc <= min <= max:
    #     chill = 0
    #     anti_chill = avg - tc
    # elif 0 <= min <= tc <= max:
    #     chill = ((min - tc) ** 2) / (2 * (min - max))
    #     anti_chill = ((max - tc) ** 2) / (2 * (max - min))
    # elif 0 <= min <= max <= tc:
    #     chill = avg - tc
    #     anti_chill = 0
    # elif min < 0 <= max <= tc:
    #     chill = (avg - tc) - ((min ** 2) / (2 * (min - max)))
    #     anti_chill = 0
    # elif min < 0 < tc < max:
    #     chill = -(((min - tc) ** 2) / (2 * (min - max))) - ((min ** 2) / (2 * (min - max)))
    #     anti_chill = ((max - tc) ** 2) / (2 * (max - min))

    # # Tab. 3. Equations for the five cases of FT Model.
    # if 0 <= tc <= min <= max:
    #     chill = 0
    #     anti_chill = 1
    # elif 0 <= min <= tc <= max:
    #     chill = -((tc - min) / (max - min))
    #     anti_chill = ((max - tc) / (max - min))
    # elif 0 <= min <= max <= tc:
    #     chill = -1
    #     anti_chill = 0
    # elif min < 0 <= max <= tc:
    #     chill = (max / (max - min))
    #     anti_chill = 0
    # elif min < 0 < tc < max:
    #     chill = -(tc / (max - min))
    #     anti_chill = ((max - tc) / (max - min))

    # https://koreascience.kr/article/JAKO200617033621107.pdf
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
    cr = -86.4 # 저온요구도
    hr = 272 # 고온요구도

    df['date'] = pd.to_datetime(df['date'])
    df['season_year'] = df['year']
    df.loc[(df["month"] >= 10), "season_year"] = df["year"] + 1
    df = df[~df['month'].isin([7, 8, 9])]
    df = df.sort_values(by=['year', 'date'], ascending=[True, True])

    # chill days 계산
    df = df.apply(add_chill_heat, axis=1)

    all_date = pd.DataFrame()
    for year in df['season_year'].unique():
        year_df = df[df['season_year'] == year]

        # 내생 휴면 해제
        # year_df['cumsum_chill_unit'] = year_df['chill_unit'].cumsum()
        # year_df = year_df[year_df['cumsum_chill_unit'] >= cr]
        year_df = year_df[(year_df['date'] >= pd.to_datetime(f'{year}-02-15'))]

        year_df['cumsum_heat_unit'] = year_df['heat_unit'].cumsum()
        year_df = year_df[year_df['cumsum_heat_unit'] >= cr]

        # 만개예상일
        # year_df['cumsum_heat_unit'] = year_df['heat_unit'].cumsum()
        year_date = year_df[year_df['cumsum_heat_unit'] >= hr].head(1)

        all_date = pd.concat([all_date, year_date])

    cd_date = all_date[['year', 'date']].reset_index(drop=True)
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
    df['date_cumsum_chill'] = df[col_chill].sum(axis=1)#.cumsum()
    df = df.drop(columns=col_chill)
    return df

def utah_model(df):
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

    stop_dormancy_dates = after[after['chill_unit_cumsum'] >= 800].groupby('season_year')['date'].first().reset_index()
    dormancy_dates = pd.merge(dormancy_dates, stop_dormancy_dates, on='season_year', how='inner')
    dormancy_dates = dormancy_dates.rename(columns={'season_year': 'year',
                                                    'date_x': 'start_dormancy_date',
                                                    'date_y': 'stop_dormancy_date', })

    return dormancy_dates

def full_bloom_dates(df):
    df = predict_time_temp(df)
    df['date'] = pd.to_datetime(df['date'])


    dvr_dates = dvr_model(df)
    mdvr_dates = modified_dvr_model(df)
    cd_dates = cd_model(df)
    dormancy_dates = utah_model(df)

    all_dates = pd.merge(dvr_dates, mdvr_dates, on='year', how='inner')
    all_dates = pd.merge(all_dates, cd_dates, on='year', how='inner')
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

    all_station.to_csv('../output/pear_result.csv', index=False, encoding='utf-8')

def main():
    weather_dir = '../output/weather'
    output_filename = '../output/apple_result.csv'
    run(weather_dir, output_filename)


if __name__ == '__main__':
    main()