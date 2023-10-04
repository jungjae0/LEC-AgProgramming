### [농업용저수지 일별 수위정보 그래프](03_api/app.py)

- 저수지 이름과 저수지 위치 입력
- 금일 저수율 확인
- 일별 저수율과 저수지 수위 그래프 확인

![image](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/4b9341ea-0ba3-4a30-bc9c-7c6c6a2eb2bc)

#### 작동방식

![image](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/32830398-615d-4a70-8048-6de36e3f5e8c)

#### 주요코드

1. 농업용 저수지 코드 조회

![그림1](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/10045c14-2b3e-44eb-bded-9d7733f9e29c)

2. 농업용 저수지 수위 조회

![그림2](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/fc5533e6-251e-400a-b495-55b2d0d7e13d)

3. 저수지 정보 일별 그래프

![그림3](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/515c72be-83ae-4982-a65e-512e5eac27c5)

* 그래프를 그리고 이미지로 저장 후, 이 이미지 데이터를 Base64로 인코딩해 웹 페이지에 포함
  * 웹에 표시하려면 이미지 형식으로 제공해야 함
  * 이미지 데이터를 웹 페이졸 전달하기 위해서는 이미지 데이터를 특정 형식으로 인코딩해야 함
  * Base64 인코딩을 사용해 이미지 데이터를 문자열로 변환함

4. Flask

![그림4](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/f530ad3e-ea01-4d2b-8f96-763a652958ff)


5. javascript

![그림5](https://github.com/jungjae0/LEC-AgProgramming/assets/93760723/359a31eb-ea98-4e23-91ac-74339b93fff7)