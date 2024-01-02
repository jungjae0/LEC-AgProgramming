# import RPi.GPIO as GPIO
# import time

# pin = 7

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(pin, GPIO.OUT)
# p = GPIO.PWM(pin, 50)

# p.start(0)

# try:
#     while True:
#         p.ChangeDutyCycle(2.5)
#         print("0")
#         time.sleep(1)
#         p.ChangeDutyCycle(6)
#         print("90")
#         time.sleep(1)

# except KeyboardInterrupt:
#     p.stop()

# finally:
#     GPIO.cleanup()
import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
servo_pin = 1

# GPIO 초기화
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# PWM 객체 생성
pwm = GPIO.PWM(servo_pin, 50)  # PWM 주파수는 50Hz로 설정

# 서보 모터의 최소 및 최대 펄스 폭 설정 (시간 단위: 밀리초)
servo_min = 2.5
servo_max = 12.5

# 영점 설정 (시간 단위: 밀리초)
neutral_position = 7.5

# PWM 시작
pwm.start(neutral_position)

try:
    while True:
        # 영점으로 이동
        pwm.ChangeDutyCycle(neutral_position)
        time.sleep(1)  # 예시로 1초 동안 영점에 머무르게 함

except KeyboardInterrupt:
    pass

finally:
    # 정리
    pwm.stop()
    GPIO.cleanup()
