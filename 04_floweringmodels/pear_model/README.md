* 자발휴면기 발육속도
* 타발휴면기 발육속도
* 생육단계별 만개일까지의 소요일수


### 신고 배의 지역별 개화예측모델
* 경과기온 양상에 따른 신고 배의 지역별 개화예측모델 평가

1. 농업기술연구소의 발육속도모델(DVR model, DVR 모델)

- 발육속도(development rate, DVR): 과수가 일평균기온에 영향을 받아 만개기에 다가가는 속도
- 발육단계(development stage, DVS): 누적되는 DVR의 누적값으로, DVS 값이 100에 도달하면 예상만개기

![image](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/89aecd4c-583e-469c-988d-db4423b1e920)

A = 107.94 / B = 0.9 / t = 일평균기온(5°C 이상)

2. Han et al.(2010)이 제시한 발육속도모델(modified DVR model, mDVR model)

- 저온감응기의 종료 이후 만개기에 도달할 때까지 필요한 발육속도(DVR2)를 계산해 누적했을 때 발육지수(∑DVR2)가 0.9593에 도달하면 예상 만개기
    * 내생휴면 해제일: 누적발육지수(∑DVR1) == 1
      * 내생휴면 해제 종료일(2월 15일) 설정
    * 저온감응기의 종료: 내생휴면과 강제휴면이 겹치는 시기 > 누적발육지수(∑DVR1) == 2
    * 예상만개기: 저온감응기 이후 만개기에 도달할 때까지 필요한 발육속도(DVR2)를 계산하여 누적했을 때 발육지수(∑DVR2)가 0.9593에 도달

- 전날의 최고기온과 당일 최저기온으로 시간별 기온을 추정

![image](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/670f5fd5-a2f0-4867-95b8-c0d764db33e7)

- DVR1 > 발육속도 모델을 이용한 배 ‘신고’ 자발휴면타파시기 추정(Han, 2008)

![image](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/41ae768d-57a6-49b2-981d-616757a3bd35)

- DVR2 > Prediction of full bloom date of pear using air temperature.(Sugiura, 1999)
    * 0°C보다 낮으면 발육속도 0으로 설정
![image](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/154b6372-54ab-4fbb-9741-bd526f2657f6)


- 배 '신고' 만개일 예측을 위한 시간발육속도모델(배 만개기 예측식 표)

![image](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/74fba1d4-03c3-4546-86aa-93b8ff1a1454)

3. Cesaraccio et al.(2004)의 휴면시계모델 (chill days model, CDmodel)

- 매일의 최고 및 최저기온을 이용하여 기준온도(Tc)로부터 유효한 온도범위에 따라 가중치를 달리하여 냉각량/가온량을 구함
    * 내생휴면해제 이전: 냉각량(chill unit)
    * 내생휴면해제 이후: 가온량(heat unit)

- 내생휴면해제: 누적 냉각량이 저온요구도(Cr)에 도달
    * 내생휴면 해제 종료일(2월 15일) 설정
- 강제휴면타파(발아): 누적 가온량이 저온요구도(Cr)에 도달
- 예상 만개일: 신고 배의 고온요구도(Hr)만큼 추가적인 가온량 누적
Tc = 5.4℃ / Cr = -86.4 / Hr = 272