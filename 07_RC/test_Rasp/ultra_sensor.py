import RPi.GPIO as GPIO
import time

# GPIO 핀 번호 설정
TRIG_PIN = 15  # 초음파 센서의 TRIG 핀
ECHO_PIN = 14  # 초음파 센서의 ECHO 핀

def setup():
    # GPIO 설정
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

def get_distance():
    # 초음파 발신 신호 전송
    GPIO.output(TRIG_PIN, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(TRIG_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, GPIO.LOW)

    # 초음파 수신 시간 측정
    while GPIO.input(ECHO_PIN) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO_PIN) == GPIO.HIGH:
        pulse_end = time.time()

    # 거리 계산 (음속: 343m/s, 거리 = 시간 * 속도 / 2)
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2

    return distance

if __name__ == "__main__":
    try:
        setup()
        while True:
            distance = get_distance()
            print("거리: {:.2f} 센티미터".format(distance))
            

    except KeyboardInterrupt:
        print("프로그램 종료")
        GPIO.cleanup()
