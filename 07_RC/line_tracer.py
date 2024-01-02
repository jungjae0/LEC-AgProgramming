import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins for analog input
right = 14
center = 15
left = 18

# Setup the GPIO pins as input
GPIO.setup(right, GPIO.IN)
GPIO.setup(center, GPIO.IN)
GPIO.setup(left, GPIO.IN)

while True:
    # Read analog-like values using PWM duty cycle
    val_1 = GPIO.input(right)
    val_2 = GPIO.input(center)
    val_3 = GPIO.input(left)

    # Print values
    print(f"right: {val_1} center: {val_2} left: {val_3}")

    # Adjust delay as needed
    time.sleep(0.1)
