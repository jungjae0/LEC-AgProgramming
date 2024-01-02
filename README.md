## 2023-02 스마트농업프로그래밍

### Task List
| Task               | Summary                                                                                                            |                                                                                                                     |
|-------------------|---------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| 농업용저수지 수위 정보 API  | - 저수지 위치와 이름을 입력<br/>- 농업용 저수지 코드 조회<br/>- 농업용 저수지 정보 조회<br/>- 웹에서 그래프 확인<br/>- 비동기식(Flask, javascript, ajax) | [app.py](02_ReservoirAPI)                                                                                    |
| 개화모델 시각화          | - 신고 배와 후지 사과 개화 모델 구현(DVR, mDVR, CD, GDH, Utah)<br/>- 개화 모델 결과 시각화                                           | [배](03_FloweringModels/pear_model)<br/>[사과](03_FloweringModels/apple_model)<br/>[app.py](03_FloweringModels) |
| 모니터링 서비스          | - 주기적으로 바뀌는 데이터 모니터링<br/>- 기상/농산물 가격 정보 API<br/>- GitHub Action                                               | [API-Action](https://github.com/jungjae0/Action-API)                                                                |
| AWS + ThingSpeak  | - AWS 데이터를 ThingSpeak로 전송<br/>- 일주일 AWS 데이터 분석                                                                | [ThingSpeakAWS](05_ThingSpeakAWS)                                                                                   |
| Python + Arduino  | - 파이썬으로 아두이노를 제어<br/>-파이썬으로 AWS 데이터를 받고 LCD 패널로 확인                                                               | [PyArduino](06_PyArduino) |  
| 관수&파종 RC카  | - 라즈베리파이와 아두이노를 사용한 RC카<br/>- Flask를 활용해 RC카를 웹에서 제어                                                               | [RC](07_RC) |
