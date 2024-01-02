import serial
import time

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,)

def send_command(command):
    ser.write(command.encode())
    # time.sleep(0.1)

try:
    while True:
        user_input = input("Enter command (s: Seed, w: Water, c: Cam, u: User, e:End): ")
        send_command(user_input)

except KeyboardInterrupt:
    print("\nExiting program.")
    ser.close()
