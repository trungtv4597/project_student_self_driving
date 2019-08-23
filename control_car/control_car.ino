/* LED CONTROLLING WITH PYTHON
   Written by Junicchi
   https://github.com/Kebablord

   It's a ESP management through Python example
   It simply fetches the path from the request
   Path is: https://example.com/this -> "/this"
   You can command your esp through python with request paths
   You can read the path with getPath() function
*/


#include "ESP_MICRO.h"

//motorA
#define A_en  5 // d2 pwm
#define A_dir 0 // d3 chiều quay
//motorB
#define B_en  4 // d1 pwm
#define B_dir 2 // d4 chiều quay

char ssid[] = "DucTrung";
char pass[] = "mangnhabihu";


void setup() {
  Serial.begin(9600);
  pinMode(A_en,  OUTPUT);
  pinMode(A_dir, OUTPUT);
  pinMode(B_en,  OUTPUT);
  pinMode(B_dir, OUTPUT);
  digitalWrite(A_en, LOW);
  digitalWrite(B_en, LOW);
}

void forward() {
  digitalWrite(A_en, LOW);
  digitalWrite(B_en, HIGH);
  //digitalWrite(A_dir, HIGH);
  //digitalWrite(B_dir, HIGH);
}

void forward_right() {
  digitalWrite(A_en, HIGH);
  digitalWrite(B_en, HIGH);
  digitalWrite(A_dir, LOW);
  digitalWrite(B_dir, HIGH);
}

void forward_left() {
  digitalWrite(A_en, HIGH);
  digitalWrite(B_en, HIGH);
  digitalWrite(A_dir, HIGH);
  digitalWrite(B_dir, HIGH);
}

void stop() {
  digitalWrite(A_en, LOW);
  digitalWrite(B_en, LOW);
}

void loop() {
  waitUntilNewReq();  //Waits until a new request from python come

  if (getPath() == "//0") {
    forward();
    returnThisInt('g'); //Returns the data to python
  }
  else if (getPath() == "//1") {
    forward_right();
    returnThisInt('r'); //Returns the data to python
  }
  else if (getPath() == "//2") {
    forward_left();
    returnThisInt('l'); //Returns the data to python
  }
  else if (getPath() == "//3") {
    stop();
    returnThisInt('s'); //Returns the data to python
  }
}
