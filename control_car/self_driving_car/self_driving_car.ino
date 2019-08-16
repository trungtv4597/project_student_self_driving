#include "ESP_MICRO.h"

//motorA
#define A_en  4 // d2 pwm
#define A_dir 0 // d3 chiều quay
//motorB
#define B_en  5 // d1 pwm
#define B_dir 2 // d4 chiều quay

int Speed = 450;
//int maxSpeed = 1023;
int noSpeed = 0;

void setup() {
  // set up wifi
  //Serial.begin(9600);
  //start("DucTrung", "mangnhabihu"); // Wifi details connec to

  // initial settings for motors off and direction forward
  pinMode(A_en,  OUTPUT);
  pinMode(A_dir, OUTPUT);
  pinMode(B_en,  OUTPUT);
  pinMode(B_dir, OUTPUT);
  digitalWrite(A_en, LOW);
  digitalWrite(B_en, LOW);
  //digitalWrite(RightMotorDir, HIGH);
  //digitalWrite(LeftMotorDir, HIGH);
}

void forward() {
  digitalWrite(A_en, HIGH);
  digitalWrite(B_en, LOW);
  digitalWrite(A_dir, HIGH);
  analogWrite(B_dir, noSpeed);
}

void forward_right() {
  digitalWrite(A_en, HIGH);
  digitalWrite(B_en, HIGH);
  digitalWrite(A_dir, HIGH);
  digitalWrite(B_dir, HIGH);
}

void forward_left() {
  digitalWrite(A_en, HIGH);
  digitalWrite(B_en, HIGH);
  digitalWrite(A_dir, HIGH);
  digitalWrite(B_dir, LOW);
}

void stop() {
  digitalWrite(A_en, LOW);
  digitalWrite(B_en, LOW);
}

void loop() {
  // wait until a new request from Python
  //waitUntilNewReq();

  digitalWrite(A_en, HIGH);
  digitalWrite(A_dir, HIGH);
  
  digitalWrite(B_en, HIGH);
  digitalWrite(B_dir, HIGH);
  /*forward();
    delay(2000);

    stop();
    delay(2000);

    forward_right();
    delay(2000);

    stop();
    delay(2000);

    forward_left();
    delay(2000);

    stop();
    delay(2000);*/
}
