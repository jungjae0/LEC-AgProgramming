import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

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
WATER = 8
# SEED = 7
###---- Done GPIO

STOP = 0
FORWARD = 1
BACKWARD = 2

RIGHT = 0
LEFT = 1

OUTPUT = 1
INPUT = 0

HIGH = 1
LOW = 0

SPEED = 60

def pwmSetPin(EN, INA, INB):
    GPIO.setup(EN, GPIO.OUT)
    GPIO.setup(INA, GPIO.OUT)
    GPIO.setup(INB, GPIO.OUT)
    pwm = GPIO.PWM(EN, 100)
    pwm.start(0)
    return pwm

GPIO.setup(R_Line, GPIO.IN)
GPIO.setup(C_Line, GPIO.IN)
GPIO.setup(L_Line, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(WATER, GPIO.OUT)
# GPIO.setup(SEED, GPIO/.OUT)/
pwmA = pwmSetPin(ENA, IN1, IN2)
pwmB = pwmSetPin(ENB, IN3, IN4)



def setMotorContorl(pwm, INA, INB, stat):
    pwm.ChangeDutyCycle(SPEED)

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


def move_wheel(RIGHT_Control, LEFT_Control):
    setMotor(RIGHT, RIGHT_Control)
    setMotor(LEFT, LEFT_Control)


def obstacle_detect():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.00001)
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

def mode_seed():
    pass


SL = 1
SC = 1
SR = 1 



def main():
    print("운행을 시작합니다.")
    try:
        while True:
            R = GPIO.input(R_Line)
            C = GPIO.input(C_Line)
            L = GPIO.input(L_Line)
            obstacle_distance = obstacle_detect()

            if obstacle_distance > 20:
                if R == LOW and C == LOW and L == LOW:
                    R == SL
                    L == SC
                    C == SR


                if R == LOW and C == HIGH and L == LOW:
                    move_wheel(FORWARD, FORWARD)
                    GPIO.output(WATER, GPIO.HIGH)
                    print('직진')

                elif R == HIGH and L == HIGH:
                    move_wheel(STOP, STOP)
                    GPIO.output(WATER, GPIO.LOW)

                    print('정지')

                elif R == HIGH and L == HIGH and C == HIGH:
                    move_wheel(STOP, STOP)
                    print('정지')
                    GPIO.output(WATER, GPIO.LOW)

                elif R == HIGH and L == LOW:
                    move_wheel(STOP, FORWARD)
                    print('우회전')
                    GPIO.output(WATER, GPIO.LOW)

                elif R == LOW and L == HIGH:
                    move_wheel(FORWARD, STOP)
                    print('좌회전')
                    GPIO.output(WATER, GPIO.LOW)

                # L = SL
                # R = SR
                # C = SC


            else:
                move_wheel(STOP, STOP)
                print("장애물 감지")
            




    except KeyboardInterrupt:
        move_wheel(STOP, STOP) 
        print("운행을 종료합니다.")

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()