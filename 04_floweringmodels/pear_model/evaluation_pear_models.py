import os
import tqdm
import numpy as np
import pandas as pd
# https://api.taegon.kr/stations/156/?sy=2017&ey=2022&format=csv


def dvr_model(df):
    A = 107.94
    B = 0.9

    # 발육속도 > 5°C 이상의 온도만 계산
    df['DVRi'] = df['temp'].apply(lambda x: 100 / (A * (B ** x)) if x >= 5 else 0)

    # 발육단계 > 누적발육속도(∑DVRi. DVS)
    df['DVS'] = df.groupby('year')['DVRi'].cumsum()

    # 예상만개기 > 발육단계 == 100
    expected_full_bloom = df[df['DVS'] >= 100].groupby('year').first()

    date_df = expected_full_bloom['date'].reset_index()
    date_df = date_df.rename(columns={"date" : "DVR"})
    return date_df


# 배 만개기 예측식 표-> https://www.rda.go.kr/fileViewDw.do?boardId=farmprmninfo&dataNo=100000510318&sortNo=0
def spontaneous_rest(x):
    if x <= -6 or x >= 12:
        dvr1 = 0
        return dvr1
    elif 6 < x < 12:
        a = 0.5 * (((np.log((x + 273) / 275.2)) / 0.01595) ** 2)
        dvr1 = 2.533 * (10 ** (-4)) + 1.671 * (10 ** (-3)) *  np.exp(a)
        return dvr1


def imposed_rest(x):
    if x < 5:
        dvr2 = 0
        return dvr2
    elif x >= 5:
        a = (x + 273 - 292.3) / 3.616
        dvr2 = 4.646 * (10 ** (-4)) + (5.022 * (10 ** (-3))) / (1 + np.exp(a))
        return dvr2

# 기온 상승에 따른 ‘신고’ 배나무의 만개일 변동 예측
# 발육속도 모델을 이용한 배 ‘신고’ 자발휴면타파시기 추정
def get_dvr1(x):
    dvr = 0
    if x < -6:
        return dvr

    elif -6 <= x < 0:
        dvr = 1.333 * (10 ** (-3)) + 2.222 * (10 ** (-4)) * x
        return dvr

    elif 0 <= x < 6:
        dvr = 1.333 * (10 ** (-3))
        return dvr

    elif 6 <= x < 9:
        dvr = 2.276 * (10 ** (-3)) - 1.571 * (10 ** (-4)) * x
        return dvr

    elif 9 <= x < 12:
        dvr = 3.448 * (10 ** (-3)) - 2.784 * (10 ** (-4)) * x
        return dvr

    elif 12 <= x:
        return dvr

def get_dvr2(x):
    if x < 20:
        a = 35.27 - 12094 * ((x + 273) ** (-1))
        return np.exp(a)
    elif x >= 20:
        a = 5.82 - 3474 * ((x + 273) ** (-1))
        return np.exp(a)

    elif x < 0:
        return 0


def add_dvr_col(df):

    # 전날의 최고기온과 당일 최저기온으로 시간별 기온 추정
    # 최저기온(m)-df['min_temp'], 최고기온(h)-df['max_temp'], 전날의 최고기온(hy)-df['max_temp'].shift(1), 다음날의 최저기온(mt)-df['min_temp'].shift(-1) 으로 각 시간(c)별 기온을 추정
    # 0 ~ 3시 >  (hy-m)×sin{(4-c)×3.14/30)}^2+m
    # 4 ~ 13시 >  (h-m)×sin{(c-4)×3.14/18)}^2+m
    # 14 ~ 23시 > (h-mt)×sin{(28-c)×3.14/30)}^2+mt
    for hour in range(0, 24):
        if 0 <= hour <= 3:
            df[f'temp_{hour}시'] = (df['max_temp'].shift(1) - df['min_temp']) * (np.sin((4 - hour) * 3.14/30) ** 2) + df['min_temp']

        elif 4 <= hour <= 13:
            df[f'temp_{hour}시'] = (df['max_temp'] - df['min_temp']) * (np.sin((hour - 4) * 3.14 / 18) ** 2) + df['min_temp']

        elif 14 <= hour <= 23:
            df[f'temp_{hour}시'] = (df['max_temp'] - df['min_temp'].shift(-1)) * (np.sin((28 - hour) * 3.14 / 30) ** 2) + df['min_temp'].shift(-1)

        # 기온 상승에 따른 ‘신고’ 배나무의 만개일 변동 예측(Han 2010)
        df[f'DVR1_{hour}시'] = df[f'temp_{hour}시'].apply(get_dvr1) # 자발휴면기-DVR1
        df[f'DVR2_{hour}시'] = df[f'temp_{hour}시'].apply(get_dvr2) # 타발휴면기-DVR2

    df = df.drop(columns=[col for col in df.columns if 'temp_' in col])
    return df


# 배 만개기 예측식 표
# df[f'DVR1_{hour}시'] = df[f'temp_{hour}시'].apply(spontaneous_rest) # 자발휴면기-DVR1
# df[f'DVR2_{hour}시'] = df[f'temp_{hour}시'].apply(imposed_rest) # 타발휴면기-DVR2


def modified_dvr_model(data):
    # 전날의 최고기온과 당일 최저기온으로 시간별 기온 추정 및 DVR1, DVR2
    data = add_dvr_col(data)

    expected_full_bloom_df = pd.DataFrame()
    for year in data['season_year'].unique():
        df = data[data['season_year'] == year]
        col_dvr1 = [col for col in df.columns if 'DVR1' in col]
        df['DVR1'] = df[col_dvr1].sum(axis=1)
        df['DVS1'] = df['DVR1'].cumsum()
        df = df[df['DVS1'] >= 1] # 내생휴면 해제

        df['DVS1'] = df['DVR1'].cumsum()
        df = df[df['DVS1'] >= 2] # 저온감응기(내생휴면과 강제휴면이 겹치는 시기) 종료 이후

        # df = df[(df['date'] >= pd.to_datetime(f'{year}-02-15'))] # 내생휴면 해제 종료일 설정
        col_dvr2 = [col for col in df.columns if 'DVR2' in col]
        df['DVR2'] = df[col_dvr2].sum(axis=1) # 만개기에 도달할 때까지 필요한 발육속도
        df['DVS2'] = df['DVR2'].cumsum()

        # 배 만개기 예측식 표
        # df = df[df['DVS2'] >= 2] # 만개기 조건
        # df['DVIf'] = df['DVR2'].cumsum()
        # expected_full_bloom = df[df['DVIf'] >= 0.9525].head(1)
        # expected_full_bloom_df = pd.concat([expected_full_bloom_df, expected_full_bloom])

        # 기온 상승에 따른 ‘신고’ 배나무의 만개일 변동 예측(Han 2010)
        expected_full_bloom = df[df['DVS2'] >= 0.9593].head(1)
        expected_full_bloom_df = pd.concat([expected_full_bloom_df, expected_full_bloom])

    date_df = expected_full_bloom_df[['year', 'date']].reset_index(drop=True)
    date_df = date_df.rename(columns={"date" : "mDVR"})

    return date_df

# https://koreascience.kr/article/JAKO200617033621107.pdf
# MPROVEMENT_OF_CHILLING_AND_FORCING_MODE.pdf
def add_chill_days(row):
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



def cd_model(data):
    cr = -86.4 # 저온요구도
    hr = 272 # 고온요구도

    # chill days 계산
    data = data.apply(add_chill_days, axis=1)

    expected_full_bloom_df = pd.DataFrame()
    for year in data['season_year'].unique():
        df = data[data['season_year'] == year]

        # 내생 휴면 해제
        # df['cumsum_chill_unit'] = df['chill_unit'].cumsum()
        # df = df[df['cumsum_chill_unit'] >= cr]
        df = df[(df['date'] >= pd.to_datetime(f'{year}-02-15'))]

        # 강제 휴면 타파
        df['cumsum_heat_unit'] = df['heat_unit'].cumsum()
        df = df[df['cumsum_heat_unit'] >= cr]

        # 만개예상일
        # df['cumsum_heat_unit'] = df['heat_unit'].cumsum()
        expected_full_bloom = df[df['cumsum_heat_unit'] >= hr].head(1)

        expected_full_bloom_df = pd.concat([expected_full_bloom_df, expected_full_bloom])

    date_df = expected_full_bloom_df[['year', 'date']].reset_index(drop=True)
    date_df = date_df.rename(columns={"date": "CD"})

    return date_df

def naju(input_dir):
    df = pd.read_csv(os.path.join(input_dir, '나주시금천면.csv'), encoding='cp949')
    df['date'] = pd.to_datetime(df['date'])
    # df = df[(df['date'] >= pd.to_datetime('2017-10-01')) & (df['date'] <= pd.to_datetime('2020-06-30'))]
    df['season_year'] = df['year']
    df.loc[(df["month"] >= 10), "season_year"] = df["year"] + 1
    # df = df[~df['month'].isin([7, 8, 9])]
    df = df.sort_values(by=['year', 'date'], ascending=[True, True])

    dvr = dvr_model(df)
    mdvr = modified_dvr_model(df)
    cd = cd_model(df)

    dates = pd.merge(dvr, mdvr, on='year', how='inner')
    dates = pd.merge(dates, cd, on='year', how='inner')
    print(dates)

def all(input_dir):
    weather_filenames = os.listdir(input_dir)

    all_date = pd.DataFrame()
    for filename in tqdm.tqdm(weather_filenames):
        df = pd.read_csv(os.path.join(input_dir, filename), encoding='cp949')

        df['date'] = pd.to_datetime(df['date'])
        df['season_year'] = df['year']
        df.loc[(df["month"] >= 10), "season_year"] = df["year"] + 1
        df = df[~df['month'].isin([7, 8, 9])]
        df = df.sort_values(by=['year', 'date'], ascending=[True, True])

        dvr = dvr_model(df)
        mdvr = modified_dvr_model(df)
        cd = cd_model(df)

        dates = pd.merge(dvr, mdvr, on='year', how='inner')
        dates = pd.merge(dates, cd, on='year', how='inner')
        dates['지역'] = filename.split('.')[0]
        all_date = pd.concat([all_date, dates], ignore_index=True)

    print(all_date)
    all_date.to_csv('../output/result.csv', index=False, encoding='utf-8')

def main():
    input_dir = '../output/weather'

    all(input_dir)



if __name__ == '__main__':
    main()
