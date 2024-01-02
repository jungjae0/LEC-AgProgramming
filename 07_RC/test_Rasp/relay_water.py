import RPi.GPIO as GPIO
import time


relay_pin = 8


GPIO.setmode(GPIO.BCM)


GPIO.setup(relay_pin, GPIO.OUT)

try:
    while True:

        GPIO.output(relay_pin, GPIO.HIGH)
        print("릴레이 켜짐")
        time.sleep(2)

        GPIO.output(relay_pin, GPIO.LOW)
        print("릴레이 꺼짐")
        time.sleep(2)

except KeyboardInterrupt:
    GPIO.cleanup()
