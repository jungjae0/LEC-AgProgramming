#include <Stepper.h>

int RightMotor_E_pin = 8;
int LeftMotor_E_pin = 9;
int RightMotor_1_pin = 4;
int RightMotor_2_pin = 5;
int LeftMotor_3_pin = 6;
int LeftMotor_4_pin = 7;

int L_MotorSpeed = 153;
int R_MotorSpeed = 153;

const int stepsPerRevolution = 1024;
Stepper Seed(stepsPerRevolution, 13, 11, 12, 10);

int Water = 3;


void setup() {
  Seed.setSpeed(30);

  pinMode(RightMotor_E_pin, OUTPUT);
  pinMode(RightMotor_1_pin, OUTPUT);
  pinMode(RightMotor_2_pin, OUTPUT);
  pinMode(LeftMotor_3_pin, OUTPUT);
  pinMode(LeftMotor_4_pin, OUTPUT);
  pinMode(LeftMotor_E_pin, OUTPUT);
  pinMode(Water, OUTPUT);

  Serial.begin(9600);
}

void loop() {
  control_arduino();
}

void control_arduino() {
  if (Serial.available() > 0) {
    String strRead = Serial.readStringUntil('\n');
    strRead.trim();  // 개행 문자 및 공백 제거

    if (strRead.equals("s")) {
      control_time_seed();
    } else if (strRead.equals("w")) {
      control_time_water();
    } else if (strRead.equals("c")) {
      control_time_cam();
    } else if (strRead.equals("u_g")) {
      motor_role(LOW, LOW);
    } else if (strRead.equals("u_b")) {
      motor_role(HIGH, HIGH);
    } else if (strRead.equals("u_l")) {
      turn_left();
    } else if (strRead.equals("u_r")) {
      turn_right();
    } else if (strRead.equals("user_stop")) {
      stop_motors();
    } else {
      stop_motors();
    }
  }
}



void control_time_seed() {
  char option = 'S';
  move_forward(5000, option);
  delay(1000);
  turn_left_manual(3000);
  delay(1000);
    turn_right_manual(3000);
  delay(1000);
  move_forward(5000,option);
  delay(1000);
}

void control_time_water() {
  char option = 'W';

  move_forward(4000, option);
  stop_motors();
  delay(1000);

  // turn_right_manual(3000);
  // delay(1000);
  // move_forward(5000, option);
  // delay(1000);
}


void control_time_cam() {
  char option = 'C';

  move_forward(5000, option);
  delay(1000);
  turn_right_manual(2000);
  delay(500);
  turn_left_manual(2000);
  delay(500);
  move_forward(5000, option);
  delay(1000);
}

void move_forward(int duration, char option) {
  if (option == 'W') {
    digitalWrite(Water, HIGH);  // Turn on relay module
    motor_role(LOW, LOW);
    delay(duration);
    stop_motors();
    digitalWrite(Water, LOW);   // Turn off relay module
  } else if (option == 'S') {
    Seed.step(stepsPerRevolution);
    motor_role(LOW, LOW);
    delay(duration);
    stop_motors();
  } else {
    // Handle other cases, if any
    motor_role(LOW, LOW);
    delay(duration);
    stop_motors();
  }
}


void turn_right_manual(int duration) {
  turn_right();
  delay(duration);
  stop_motors();
}

void turn_left_manual(int duration) {
  turn_left();
  delay(duration);
  stop_motors();
}
void turn_right(){
    digitalWrite(RightMotor_1_pin, LOW);
    digitalWrite(RightMotor_2_pin, HIGH);
    digitalWrite(LeftMotor_3_pin, LOW);
    digitalWrite(LeftMotor_4_pin, LOW);
    analogWrite(RightMotor_E_pin, R_MotorSpeed);  
    analogWrite(LeftMotor_E_pin, L_MotorSpeed);
}


void turn_left(){
    digitalWrite(RightMotor_1_pin, LOW);
    digitalWrite(RightMotor_2_pin, LOW);
    digitalWrite(LeftMotor_3_pin, LOW);
    digitalWrite(LeftMotor_4_pin, HIGH);
    analogWrite(RightMotor_E_pin, R_MotorSpeed);  
    analogWrite(LeftMotor_E_pin, L_MotorSpeed);
}


void motor_role(int R_motor, int L_motor) {
  digitalWrite(RightMotor_1_pin, R_motor);
  digitalWrite(RightMotor_2_pin, !R_motor);
  digitalWrite(LeftMotor_3_pin, L_motor);
  digitalWrite(LeftMotor_4_pin, !L_motor);

  analogWrite(RightMotor_E_pin, R_MotorSpeed);
  analogWrite(LeftMotor_E_pin, L_MotorSpeed);
}

void stop_motors() {
  analogWrite(RightMotor_E_pin, 0);
  analogWrite(LeftMotor_E_pin, 0);
}
