### 개화 모델 구현 및 시각화

#### 입력 자료 수집
[save_weather.py](save_weather.py)
- 전국 74개 지점의 2000-2022년 일별 기상데이터 수집


#### 과수별 개화 모델

- '신고' 배 > [pear_model](pear_model)
- '후지' 사과 > [apple_model](apple_model)

#### 만개일 예측 결과 시각화

- 시각화 데이터 생성 > [preprocess_data.py](preprocess_data.py)
- 시각화 코드 > [analysis.py](analysis.py)
- GUI APP > [app.py](app.py)

1. 일평균 기온 변화 추이: 평년 vs. 선택연도

![평년현재기온](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/be9a569f-552d-4b06-93a0-b2e7f01ca7af)


2. 일평균 기온 변화 추이: 3개년

![3년기온](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/f5abd7cd-00f8-4069-a2c0-fcd610e23850)


3. 저온축적량과 휴면타파시기

![휴면타파시기](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/19ef458d-99b2-4226-99a6-a05a65a2017b)


4. 만개일 예측 결과

![예측결과](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/620f98d2-5838-4c8b-8cc3-a0c6b2dd2bcf)


5. 만개월의 평균 기온과 만개일 변화 추이

![만개월기온만개일](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/9a96bc47-a211-4db6-bb06-3fcf23786456)


6. 만개일의 일평균 기온과 만개일 변화 추이

![만개일기온만개일](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/8cd6772f-e0d3-4b86-b148-327301488bf0)


7. 전국 만개일과 만개월 평균 기온 지도

![지도](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/8cc7092c-beb1-4fac-83ba-7ba17571f11f)


8. 전국 만개일 예측 범위

![범위](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/ac34b720-725f-46ca-bce4-0f5ef948eee3)


9. 여러 지역의 만개일 변화 추이

![지역들간만개일](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/4b6ff032-d8fc-4371-9e33-6e541b02e621)

