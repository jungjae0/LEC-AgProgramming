from gpiozero import DigitalInputDevice, Motor, DistanceSensor
from time import sleep

RightMotor_E_pin = 13
LeftMotor_E_pin = 16
RightMotor_1_pin = 26 # Right Forward 
RightMotor_2_pin = 19 # Right Backward
LeftMotor_3_pin = 21 
LeftMotor_4_pin = 20

Ultrasonic_Trigger_pin = 23
Ultrasonic_Echo_pin = 24

L_Line = DigitalInputDevice(4) # GPIO 4
C_Line = DigitalInputDevice(17) # GPIO 17
R_Line = DigitalInputDevice(27) # GPIO 27

L_MotorSpeed = 120
R_MotorSpeed = 120 

motor = Motor(forward=RightMotor_1_pin, backward=RightMotor_2_pin)
ultrasonic = DistanceSensor(echo=Ultrasonic_Echo_pin, trigger=Ultrasonic_Trigger_pin)

def motor_role(R_motor, L_motor):
    motor.forward() if R_motor == 1 else motor.backward()
    motor.right() if L_motor == 1 else motor.left()

try:
    object_detected = False

    while True:
        distance = ultrasonic.distance
        L = L_Line.value
        C = C_Line.value
        R = R_Line.value

        print(f"digital: {L}, {C}, {R}, distance: {distance:.2f} m")

        if distance < 0.2:
            if not object_detected:
                motor.stop()
                object_detected = True
                print("object - stop")

        elif object_detected:
            object_detected = False
            print("no object - restart")
            continue

        if L == 0 and C == 0 and R == 0:  # 0 0 0
            L, C, R = SL, SC, SR

        if L == 0 and C == 1 and R == 0:  # 0 1 0
            motor_role(1, 1)
            print("Forward")

        elif L == 0 and R == 1:  # 0 0 1, 0 1 1
            motor_role(0, 1)
            print("Turn Right")

        elif L == 1 and R == 0:  # 1 0 0, 1 1 0
            motor_role(1, 0)
            print("Turn Left")

        elif L == 1 and R == 1:  # 1 1 1, 1 0 1
            motor.stop()
            print("Stop")

        SL, SC, SR = L, C, R
        sleep(0.1)

except KeyboardInterrupt:
    motor.stop()
    print("Car Stop")
