### 후지 사과의 지역별 개화예측모델

1. GDH 모델
- 전날의 최고기온과 당일 최저기온으로 시간별 기온을 추정

![predict_time_temp](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/7520e830-7e8d-45ea-be90-7f9605696ae3)

- 휴면타파시점 이후 시간별 기온을 GDH로 변환·대입

![cal_GDH](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/3bbf2baa-e6b9-45a8-84de-5aa62b6250e8)

- 예상 만개일: 누적 GDH가 기준치에 도달한 시점

![GDH](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/1328d70f-e582-4a32-80d8-76bc146cb1dc)

후지 사과: GDH5579 모델 적용



2. Cesaraccio et al.(2004)의 휴면시계모델 (chill days model, CDmodel)

- 매일의 최고 및 최저기온을 이용하여 기준온도(Tc)로부터 유효한 온도범위에 따라 가중치를 달리하여 냉각량/가온량을 구함
    * 내생휴면해제 이전: 냉각량(chill unit)
    * 내생휴면해제 이후: 가온량(heat unit)

![chill_anti_chill_day](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/4db35ca2-6d3c-4220-a0d2-2c0c6c8ae8c5)

- 내생휴면해제: 누적 냉각량이 저온요구도(Cr)에 도달
    * 내생휴면 해제 종료일(2월 15일) 설정
- 강제휴면타파(발아): 누적 가온량이 저온요구도(Cr)에 도달
- 예상 만개일: 신고 배의 고온요구도(Hr)만큼 추가적인 가온량 누적

![CD](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/4bc091af-41cd-4fda-8799-6e8cf7e6fb0c)

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

![chill_unit](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/c4bfaefe-c86a-4274-95bf-cef401c6598d)

![dormancy](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/9400b26d-915c-451a-8f9a-b96fbc511fe4)

* 수확 적기는 만개 후 성숙기까지의 일수가 175일