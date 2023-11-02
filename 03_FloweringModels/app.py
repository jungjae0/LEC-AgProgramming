import PySimpleGUI as sg
import analysis
import pandas as pd

text_length = 60
text_layer_length = 10

sg.theme('DarkAmber')

infos = pd.read_csv(f'./output/apple_analysis.csv', encoding='utf-8')
tree_options = ['apple', 'pear']
year_options = list(infos['year'].unique())
station_options = list(infos['지역'].unique())
model_options = {
    'apple': ['gdh_5579', 'CD'],
    'pear': ['DVR', 'mDVR', 'CD'],
}

checkboxes_per_row = 7

station_rows = [station_options[i:i+checkboxes_per_row] for i in range(0, len(station_options), checkboxes_per_row)]

checkbox_elements = []
for row in station_rows:
    checkbox_elements.append([sg.Checkbox(station, key='stations') for station in row])

layout = [
    [sg.Text('사과 & 배 만개일 예측(2000-2022)')],
    [sg.HSeparator(pad=(0, 10))],
    [sg.Text('과수 선택'),
     sg.Radio('apple', "tree_selection", default=True, key='tree'),
     sg.Radio('pear', "tree_selection", key='tree'),
     sg.Button('선택 완료')],
    [sg.Text('모델 선택'), sg.DropDown(model_options['apple'], key='model', size=(10, 1))],
    [sg.Text('연도 선택'), sg.DropDown(year_options, key='year', size=(10, 1))],
    [sg.Text('지역 선택'), sg.DropDown(station_options, key='station', size=(10, 1))],

    [sg.HSeparator(pad=(0, 10))],
    [sg.Text('예측 만개일 비교 지역 선택')],
    [sg.Listbox(values=station_options, select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, size=(20, 5), key='stations')],

    # *checkbox_elements,
    [sg.HSeparator(pad=(0, 10))],
    [sg.Checkbox('만개일 예측 결과 확인', default=True, key='function0')],
    [sg.Checkbox('일평균 기온 변화 추이: 평년', key='function1')],
    [sg.Checkbox('일평균 기온 변화 추이: 3개년', key='function2')],
    [sg.Checkbox('휴면타파시기', key='function3')],
    [sg.Checkbox('만개월 평균 기온과 만개일 변화 추이', key='function4')],
    [sg.Checkbox('만개일 일평균 기온과 만개일 변화 추이', key='function5')],
    [sg.Checkbox('전국 만개일과 만개월 평균 기온 지도', key='function6')],
    [sg.Checkbox('전국 만개일 예측 범위', key='function7')],
    [sg.Checkbox('여러 지역의 만개일 변화 추이', key='function8')],
    [sg.Button('시각화', size=(60, 1))],
]


window = sg.Window('Function Selection', layout)
weather_dir = './output/weather'
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == '선택 완료':
        selected_tree = 'apple' if values['tree'] else 'pear'

        window['model'].update(values=model_options[selected_tree])


    if event == '시각화':
        selected_tree = 'apple' if values['tree'] else 'pear'

        tree = selected_tree
        year = int(values['year'])
        station = values['station']
        model = values['model']
        stations = values['stations']


        df = pd.read_csv(f'./output/{tree}_analysis.csv', encoding='utf-8')

        models, maxCU, stopCU = analysis.select_tree(tree)

        for column in models:
            df[column] = pd.to_datetime(df[column]).dt.strftime('%j').astype(int)

        if values['function0']:
            analysis.draw_models_date_line(df, station, models)
        if values['function1']:
            analysis.draw_commom_temp_line(df, year, station, weather_dir)
        if values['function2']:
            analysis.draw_temp_line(df, year, station, weather_dir)
        if values['function3']:
            analysis.draw_date_cr_line(df, station, year, maxCU, stopCU, weather_dir)
        if values['function4']:
            analysis.draw_date_tavg_line(df, station, model)
        if values['function5']:
            analysis.draw_date_temp_line(df, station, model)
        if values['function6']:
            analysis.draw_map(df, year, model)
        if values['function7']:
            analysis.table_date_station(df, year, models)
        if values['function8']:
            analysis.draw_stations_date_line(df, stations, model)

        sg.popup('완료')

window.close()
