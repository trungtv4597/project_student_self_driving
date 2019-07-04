#include <Wire.h>
#include <AFMotor.h>

AF_DCMotor motor1(1);
AF_DCMotor motor2(2);
AF_DCMotor motor3(3);
AF_DCMotor motor4(4);
char command;

void setup() {
 Wire.begin(8);                /* join i2c bus with address 8 */
 Wire.onReceive(receiveEvent); /* register receive event */
 Wire.onRequest(requestEvent); /* register request event */
 Serial.begin(9600);           /* start serial for debug */
 /*pinMode(led, OUTPUT);
 digitalWrite(led, LOW);*/
}

void loop() {
 delay(100);
}

// function that executes whenever data is received from master
void receiveEvent(int howMany) {
 while (0 <Wire.available()) {
    int c = Wire.read();      /* receive byte as a character */
         
    if (c == 1){
      Serial.print(c); /* print the character */
      stop();
    }
    else if (c == 0){
      Serial.print(c);
      forward();
    }
    else{
      stop();
    }
  }
 Serial.println();             /* to newline */
}

// function that executes whenever data is requested from master
void requestEvent() {
 Wire.write("Hello NodeMCU");  /*send string on request */
}

void right()

{

    motor1.setSpeed(100);
    motor1.run(BACKWARD);

    motor2.setSpeed(100);
    motor2.run(FORWARD);

    motor3.setSpeed(100);
    motor3.run(FORWARD);

    motor4.setSpeed(100);
    motor4.run(BACKWARD);
    
}

void left()

{
    motor1.setSpeed(100);
    motor1.run(FORWARD);

    motor2.setSpeed(100);
    motor2.run(BACKWARD);

    motor3.setSpeed(100);
    motor3.run(BACKWARD);

    motor4.setSpeed(100);
    motor4.run(FORWARD);
}

void forward()

{
    motor4.setSpeed(100);
    motor4.run(FORWARD);

    motor2.setSpeed(100);
    motor2.run(FORWARD);

    motor3.setSpeed(100);
    motor3.run(FORWARD);

    motor1.setSpeed(100);
    motor1.run(FORWARD);
}

void back()

{
    motor3.setSpeed(100);
    motor3.run(BACKWARD);

    motor1.setSpeed(100);
    motor1.run(BACKWARD);

    motor4.setSpeed(100);
    motor4.run(BACKWARD);

    motor2.setSpeed(150);
    motor2.run(BACKWARD);
}

void stop()

{
    motor1.setSpeed(0);
    motor1.run(RELEASE);

    motor2.setSpeed(0);
    motor2.run(RELEASE);

    motor3.setSpeed(0);
    motor3.run(RELEASE);

    motor4.setSpeed(0);
    motor4.run(RELEASE);
}
