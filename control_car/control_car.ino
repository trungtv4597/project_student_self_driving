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
#include <Wire.h>

void setup() {
  Serial.begin(9600);
  start("Viva Star Nguyễn Ảnh Thủ", "0123456789"); // Wifi details connec to
  Wire.begin(D1, D2);
}

void loop() {
  waitUntilNewReq();  //Waits until a new request from python come

  if (getPath() == "//red") {
    Wire.beginTransmission(8); /* begin with device address 8 */
    Wire.write(2);
    Wire.endTransmission();    /* stop transmitting */
    returnThisInt('r'); //Returns the data to python
  }
  else if (getPath() == "//pass") {
    Wire.beginTransmission(8); /* begin with device address 8 */
    Wire.write(1);
    Wire.endTransmission();    /* stop transmitting */
    returnThisInt('p'); //Returns the data to python
  }
  else if (getPath() == "//exit") {
    Wire.beginTransmission(8); /* begin with device address 8 */
    Wire.write(0);
    Wire.endTransmission();    /* stop transmitting */
    returnThisInt('e'); //Returns the data to python
  }
}
