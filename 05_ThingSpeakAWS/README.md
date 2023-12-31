## 실시간 데이터 모니터링 & 통계

### 데이터 명세서

<details>
<summary>AWS 데이터 명세서</summary>

| 구분       | 단위                  |
|----------|---------------------|
| datetime | YYYY-MM-DD hh:mm:ss |
| 온도       | ℃                   |
| 습도       | %                   |
| 일사       | W/m^2               |
| 풍향       | degree              |
| 강우       | mm                  |
| 최대순간풍속(60초 중 최고값)  | m/s                 |
| 배터리전압(최저값)         |  V                  |
</details>

<details>
<summary>AWS Summary 데이터 명세서</summary>

| 구분   | 단위    | 설명                                            |
|------|-------|-----------------------------------------------|
| 평균기온 | ℃     | 일 평균 기온                                       |
| 최고기온 | ℃     | 일 최고 기온                                       |
| 최저기온 | ℃     | 일 최저 기온                                       |
| 강수량  | mm    | 일 총 강수량                                       |
| 최대일사 | W/m^2 | 일 최대 일사량                                      |
| 일교차  | ℃     | 일 최고 기온 - 일 최고 기온                             |
| 강수계급 | -     | 강수량에 따라 5개 단계로 구분                             |
| 풍향계급 | -     | 풍향에 따라 16개 방향으로 구분                            |
| 적산온도 | ℃     | 생육일수의 일평균기온을 적산                               |
| 강수일수 | 일     | 생육일수의 일평균기온을 적산                               |
| 폭염일수 | 일     | 생육일수의 일평균기온을 적산                               |
| 한파일수 | 일     | 생육일수의 일평균기온을 적산                               |
| 체감온도 | ℃     | 인간이 느끼는 더위나 추위를 수량적으로 나타낸 것                    |
| 실효습도 | %     | 수일 전부터의 상대습도에 경과 시간에 따른 가중치를 주어서 건조도를 나타내는 지수 |

※ 해당 데이터에서는 실효습도, 적산온도 무의미함

</details>


### Results
<details>
<summary>ThingSpeak</summary>

![그림1](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/9fc123f1-2536-4032-aced-b018fb6d2c4c)

</details>

<details>
<summary>Table</summary>

1. 기상 통계

| 날짜       |   평균기온 |   최고기온 |   최저기온 |   강수량 |   최대일사 |   일교차 | 강수일수   | 폭염일수   | 한파일수   | 강수계급               |   적산온도 | 체감온도   |   실효습도 |
|:-----------|-----------:|-----------:|-----------:|---------:|-----------:|---------:|:-----------|:-----------|:-----------|:-----------------------|-----------:|:-----------|-----------:|
| 2023-10-29 |      16.41 |      26.23 |       9.91 |      0   |     684.37 |    16.32 | -          | -          | -          | 무강수                 |      11.41 | -          |    20.7797 |
| 2023-10-30 |      16.47 |      25.5  |      10.83 |      0   |     646.22 |    14.67 | -          | -          | -          | 무강수                 |      22.88 | -          |    36.3461 |
| 2023-10-31 |      16.08 |      26.73 |       9.57 |      0   |     640.5  |    17.16 | -          | -          | -          | 무강수                 |      33.96 | -          |    46.5286 |
| 2023-11-01 |      19.05 |      27.57 |      11.73 |      0   |     565.35 |    15.84 | -          | -          | -          | 무강수                 |      48.01 | -          |    53.0555 |
| 2023-11-02 |      20.98 |      30.43 |      14.49 |      0   |     634.01 |    15.94 | -          | -          | -          | 무강수                 |      63.99 | -          |    55.0995 |
| 2023-11-03 |      19.93 |      28.46 |      13.8  |      0   |     735.87 |    14.66 | -          | -          | -          | 무강수                 |      78.92 | -          |    55.7323 |
| 2023-11-04 |      20.05 |      24.88 |      17.32 |      6.6 |     510.41 |     7.56 | 1          | -          | -          | 1.0mm 이상 10.0mm 미만 |      93.98 | -          |    60.6541 |

2. 풍향 계급

| date       |   남 |   남남동 |   남남서 |   남동 |   남서 |   동 |   동남동 |   동북동 |   북동 |   북북동 |   북북서 |   북서 |   서 |   서남서 |   서북서 |
|:-----------|-----:|---------:|---------:|-------:|-------:|-----:|---------:|---------:|-------:|---------:|---------:|-------:|-----:|---------:|---------:|
| 2023-10-29 |    3 |        5 |        5 |      0 |      2 |    1 |        0 |        6 |      1 |        0 |        0 |      0 |    0 |        1 |        0 |
| 2023-10-30 |    4 |        8 |        5 |      1 |      3 |    0 |        0 |        1 |      0 |        0 |        0 |      0 |    0 |        2 |        0 |
| 2023-10-31 |    4 |        1 |        7 |      1 |      2 |    1 |        2 |        4 |      0 |        0 |        0 |      0 |    0 |        2 |        0 |
| 2023-11-01 |    3 |        4 |        3 |      0 |      3 |    1 |        0 |        0 |      0 |        0 |        1 |      2 |    2 |        4 |        1 |
| 2023-11-02 |    9 |        4 |        2 |      0 |      0 |    1 |        0 |        0 |      0 |        0 |        0 |      0 |    7 |        1 |        0 |
| 2023-11-03 |    7 |        4 |        5 |      0 |      1 |    0 |        1 |        1 |      0 |        2 |        0 |      0 |    1 |        2 |        0 |
| 2023-11-04 |    4 |        4 |        2 |      1 |      2 |    4 |        3 |        1 |      0 |        0 |        0 |      0 |    1 |        2 |        0 |

3. 날짜

| 구분          | 날짜       |     값 |
|:--------------|:-----------|-------:|
| 최고 평균기온 | 2023-11-02 |  20.98 |
| 최저 평균기온 | 2023-10-31 |  16.08 |
| 최고 최고기온 | 2023-11-04 |  24.88 |
| 최저 최저기온 | 2023-10-31 |   9.57 |
| 강수일        | 2023-11-04 | nan    |

</details>


<details>
<summary>시각화</summary>

![그림2](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/131aefa9-1d3a-47b7-850b-e3410172eeaf)


</details>

### AWS → ThingSpeak

[ThingSpeak Data Write & Read 사용 방법](https://docs.google.com/document/d/1zvf_lpqmNLEhlzbh6U8FJ6flC6GFANtNqWIK6bju5l4/edit?usp=sharing)

```aws2thingspeak.py``` > AWS 데이터를 ThingSpeak에 1분 간격으로 전달, ThingSpeak에 저장된 값 불러오기
```python
write_api_key = 'write_api_key' # ThingSpeak Write API Key
read_api_key = 'read_api_key'   # ThingSpeak Read API Key
channel_id = 'channel_id'       # ThingSpeak Channel Id
```

### AWS → CSV
```aws2csv.py``` > AWS 데이터를 일별로 저장
```python
start_date_str = "20231024"            # 시작날짜
end_date_str = "20231104"              # 끝날짜
all_filename = './output/aws_data.csv' # 전체 AWS 데이터 파일 저장명
```

### AWS → Summary & Vis
```aws2summary.py``` > 일주일 AWS 데이터 요약 통계

```draw_figs.py``` > 시각화

```python
start_date_str = "20231024" # 시작날짜
end_date_str = "20231104"   # 끝날짜
folder_path = "./output"    # AWS 저장 폴더
```
