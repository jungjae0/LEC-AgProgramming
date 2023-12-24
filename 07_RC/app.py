from flask import Flask
from flask import render_template, request
import serial

ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600,)

def send_command(command):
    if (ser.readable()):
        ser.write(command.encode())
    else:
        print("message is not transferred")


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/user_forward")
def user_forward():
    send_command('u_g')
    return 'User Input Forward'

@app.route("/user_backward")
def user_backward():
    send_command('u_b')
    return 'User Input Backward'

@app.route("/user_right")
def user_right():
    send_command('u_r')
    return 'User Input Right'

@app.route("/user_left")
def user_left():
    send_command('u_l')
    return 'User Input Left'

@app.route("/user_stop")
def user_stop():
    send_command('u_s')
    return 'User Input Stop'

@app.route("/manual_water")
def manual_water():
    send_command('w')
    return 'Manual Water'

@app.route("/manual_seed")
def manual_seed():
    send_command('s')
    return 'Manual Seed'
@app.route("/manual_cam")
def manual_cam():
    send_command('c')
    return 'Manual Cam'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)