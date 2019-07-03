/* LED CONTROLLING WITH PYTHON
 * Written by Junicchi
 * https://github.com/Kebablord 
 *
 * It's a ESP management through Python example
 * It simply fetches the path from the request
 * Path is: https://example.com/this -> "/this"
 * You can command your esp through python with request paths
 * You can read the path with getPath() function
 */


#include "ESP_MICRO.h"

void setup(){
  Serial.begin(9600);
  start("DucTrung","mangnhabihu"); // Wifi details connec to

  pinMode(16,OUTPUT);
}

void loop(){
  waitUntilNewReq();  //Waits until a new request from python come

  if (getPath()=="//red"){
    digitalWrite(16,HIGH);
    returnThisInt(' '); //Returns the data to python
  }
  if (getPath()=="//pass"){
    digitalWrite(16,LOW);
    returnThisInt(' '); //Returns the data to python

  }
}
