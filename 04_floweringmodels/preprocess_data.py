import os
import tqdm
import numpy as np
import pandas as pd

pd.set_option('mode.chained_assignment', None)


def add_date_temp(weather_dir, models_result_file, output_filename):
    pred = pd.read_csv(models_result_file, encoding='utf-8')

    cols = pred.columns
    drop_cols = ['date', 'start_dormancy_date', 'stop_dormancy_date', '지역', 'year']
    models = list(set(cols) - set(drop_cols))

    for model in models:
        pred[f'{model}'] = pd.to_datetime(pred[f'{model}'])
        pred[f'{model}_year'] = pred[f'{model}'].dt.year
        pred[f'{model}_month'] = pred[f'{model}'].dt.month

    result = pd.DataFrame()
    for station in tqdm.tqdm(pred['지역'].unique()):
        pred_date = pred[pred['지역'] == station].reset_index()
        weather = pd.read_csv(os.path.join(weather_dir, f'{station}.csv'), encoding='utf-8')
        weather['date'] = pd.to_datetime(weather['date'])
        weather['year'] = weather['date'].dt.year
        weather['month'] = weather['date'].dt.month

        tavg = weather.groupby(['year', 'month'])['temp'].mean().reset_index()

        for model in models:
            pred_date[f'{model}_temp'] = pd.merge(weather, pred_date, left_on='date', right_on=model, how='inner')['temp']
            pred_date[f'{model}_tavg'] = pd.merge(tavg, pred_date, left_on=['year', 'month'], right_on=[f'{model}_year', f'{model}_month'], how='inner')['temp']

        result = pd.concat([result, pred_date], ignore_index=True)

    return result


def add_mean_date(models_result_file, output_filename):
    pred = pd.read_csv(models_result_file, encoding='utf-8')

    # cols = pred.columns
    # drop_cols = ['date', 'start_dormancy_date', 'stop_dormancy_date', '지역', 'year']
    # models = list(set(cols) - set(drop_cols))
    models = ['CD', 'gdh_5579']
    for model in models:
        pred[f'{model}'] = pd.to_datetime(pred[f'{model}']).dt.strftime('%j').astype(float)

    pred['mean_j'] = pred[models].mean(axis=1).astype(int)
    pred['cul_j'] = pred['mean_j'] + 160


    pred['mean_j'] = pred['year'].astype(str) + '' + pred['mean_j'].astype(str)
    pred['mean_j'] = pd.to_datetime(pred['mean_j'], format='%Y%j', errors='coerce')
    pred['mean_date'] = pred['mean_j'].dt.strftime('%Y-%m-%d')


    pred['cul_j'] = pred['year'].astype(str) + '' + pred['cul_j'].astype(str)
    pred['cul_j'] = pd.to_datetime(pred['cul_j'], format='%Y%j', errors='coerce')
    pred['cul_date'] = pred['cul_j'].dt.strftime('%Y-%m-%d')

    return pred[['year', 'mean_date', 'cul_date', '지역']]

def main():
    name = 'apple'

    output_dir = './output'
    weather_dir = os.path.join(output_dir, 'weather')
    models_result_file = os.path.join(output_dir, f'{name}_result.csv')
    output_filename = os.path.join(output_dir, f'{name}_analysis.csv')

    add_temp = add_date_temp(weather_dir, models_result_file, output_filename)
    mean_date = add_mean_date(models_result_file, output_filename)

    save = pd.merge(add_temp, mean_date, on=['year', '지역'], how='inner')

    save.to_csv(output_filename, index=False, encoding='utf-8')

if __name__ == '__main__':
    main()


