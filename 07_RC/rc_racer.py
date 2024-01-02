import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


STOP = 0
FORWARD = 1
BACKWARD = 2

RIGHT = 0
LEFT = 1

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

###--- Start GPIO
# Line
R_Line = 14
C_Line = 15
L_Line = 18

# Wheel
ENA = 26
ENB = 0
IN1 = 19
IN2 = 13
IN3 = 6
IN4 = 5 

# Ultra
TRIG = 23
ECHO = 24

# Water
# WATER = 8
# SEED = 7
###---- Done GPIO

speed = 80

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def setPinConfig(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm = GPIO.PWM(EN, 100)
    pwm.start(0)
    return pwm


def setMotorContorl(pwm, INA, INB, stat):
    pwm.ChangeDutyCycle(speed)

    if stat == FORWARD:
        GPIO.output(INA, HIGH)
        GPIO.output(INB, LOW)

    elif stat == BACKWARD:
        GPIO.output(INA, LOW)
        GPIO.output(INB, HIGH)

    elif stat == STOP:
        GPIO.output(INA, LOW)
        GPIO.output(INB, LOW)


def setMotor(ch, stat):
    if ch == RIGHT:
        setMotorContorl(pwmA, IN1, IN2, stat)
    else:
        setMotorContorl(pwmB, IN3, IN4, stat)


GPIO.setmode(GPIO.BCM)

pwmA = setPinConfig(ENA, IN1, IN2)
pwmB = setPinConfig(ENB, IN3, IN4)

def move_wheel(RIGHT_Control, LEFT_Control):
    setMotor(RIGHT, RIGHT_Control)
    setMotor(LEFT, LEFT_Control)


def obstacle_detect():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

    while GPIO.input(ECHO) == GPIO.LOW:
        pulse_start = time.time()
    while GPIO.input(ECHO) == GPIO.HIGH:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 34300 / 2

    return distance

def main():
    try:
        while True:
            obstacle_distance = obstacle_detect()


            if obstacle_distance < 20:
                move_wheel(STOP, STOP)
                print("장애물 감지 정지")

            else:
                user_input = input("Enter - go | back | right | left | stop | end : ")

                if user_input == 'go':
                    move_wheel(FORWARD, FORWARD)

                elif user_input == 'back':
                    move_wheel(BACKWARD, BACKWARD)

                elif user_input == 'stop':
                    move_wheel(STOP, STOP)

                elif user_input == 'right':
                    move_wheel(FORWARD, STOP)

                elif user_input == 'left':
                    move_wheel(STOP, FORWARD)

                elif user_input == 'end':
                    break
                else:
                    move_wheel(STOP, STOP)
                    print("Enabled - Retry")
                # time.sleep(2)


    except KeyboardInterrupt:
        pass 

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
    
