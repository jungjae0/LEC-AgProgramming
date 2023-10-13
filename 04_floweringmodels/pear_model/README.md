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

### 휴면타파시기

* 휴면
  * 식물체 내부적으로는 생리적 변화가 계속 일어나고 있으나 외관상 생장이 멈춘 상태
  * 유기 요인에 따라 외재휴면(para-dormancy), 내재휴면(endodormancy), 환경휴면(ecodormancy) 단계로 구분
  * 내재휴면은 계절적으로 식물 생장에 불리한 조건을 극복하기 위한 수체의 내부적인 생리반응이며, 휴면타파를 위해서는 저온축적이 필요하다.
* 저온요구도
  * 과종, 품종에 따라 다르며 대략 5 ~ 7.2℃ 내외에서 효과가 있음
  * 휴면의 깊이(심도)와 기긴에 매우 밀접한 관련이 있음
  * 겨울철 불충분한 저온의 축적으로 발아와 개화가 지연되거나 불량해지면 생산량에 영향을 미치게 됨
  * 사과(500~800CU), 배(1,000~1,200CU), 복숭아(800~1,000CU) 내외
* 유타모델

* 수확 적기는 만개 후 성숙기까지의 일수가 160일, 적산온도는 약 3,480±50℃ 정도가 알맞다
* 과실비대의 적온은 16∼18℃이며 적산온도는 1,650∼2,600℃

### 모델 결과 시각화
* 참고
  * https://www.nippon.com/en/japan-data/h01564/
  * https://highparknaturecentre.com/cherry-blossom-tracking/
  * https://www.researchgate.net/publication/360118309_Estimating_Heat_Requirement_for_Flowering_in_Peach_Germplasm/figures?lo=1

