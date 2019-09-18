#include "ESP_MICRO.h"
#include <Servo.h>



//motor
#define motor_en  4 // d2 pwm
#define motor_dir 2 // d4 chiều quay
//servoX
Servo servoX;


void setup() {
  Serial.begin(9600); // Starting serial port for seeing details
  start("DucTrung", "mangnhabihu");  // EnAIt will connect to your wifi with given details

  // initial settings for servo
  servoX.attach(15); // GPIO 15_D8
  servoX.write(150);

  // initial settings for motors Y off and direction forward
  pinMode(motor_en,  OUTPUT);
  pinMode(motor_dir, OUTPUT);
  digitalWrite(motor_en, LOW);
  //digitalWrite(motor_dir, HIGH);
}

//int Speed = 1000; //speed of wifi_car
void stop(void) {
  digitalWrite(motor_en, LOW);
  servoX.write(150);
}
void forward(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, HIGH);
  servoX.write(150);
}
void backward(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, LOW);
  servoX.write(150);
}
void left(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, HIGH);
  servoX.write(180);
}
void right(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, HIGH);
  servoX.write(130);
}

void loop() {
  waitUntilNewReq();  //Waits until a new request from python come

  if (getPath() == "//0") {
    Serial.print("forward");
    forward();
    returnThisInt(1); //Returns the data to python
  }
  else if (getPath() == "//2") {
    Serial.print("right");
    right();
    returnThisInt(1); //Returns the data to python
  }
  else if (getPath() == "//1") {
    Serial.print("left");
    left();
    returnThisInt(1); //Returns the data to python
  }
  else if (getPath() == "//stop") {
    Serial.print("stop");
    stop();
    returnThisInt(1); //Returns the data to python
  }
}
