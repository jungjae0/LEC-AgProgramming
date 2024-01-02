import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the servo
left_servo = 7
right_servo = 1

# Set the GPIO pin as an output
GPIO.setup(left_servo, GPIO.OUT)
GPIO.setup(right_servo, GPIO.OUT)

# Create a PWM instance with a frequency of 50Hz
left_pwm = GPIO.PWM(left_servo, 50)
right_pwm = GPIO.PWM(right_servo, 50)
# Start PWM with a duty cycle of 7.5% (neutral position)
left_pwm.start(7.5)
right_pwm.start(7.5)

try:
    while True:
        duty_cycle = 2.5 + 90 / 18.0
        right_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.1)

        duty_cycle = 2.5 + 0 /18.0
        right_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.1)
        
        duty_cycle = 2.5 + 90 / 18.0
        left_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)

        duty_cycle = 2.5 + 0 /18.0
        left_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(2)


except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    pass

finally:
    # Cleanup GPIO on exit
    right_pwm.stop()
    left_pwm.stop()

    GPIO.cleanup()
