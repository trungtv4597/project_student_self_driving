#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>
#include <ArduinoJson.h>


//server
ESP8266WebServer server;
//light
//#define pin_led  5;
//servo
Servo servo;
//motor
#define motor_en 4 //d2 enable
#define motor_dir 2 //d4 direction


char* ssid = "DucTrung";
char* password = "mangnhabihu";


void setup() {
  //initial settings for connecting to the network
  WiFi.begin(ssid, password);
  Serial.begin(115200);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("");
  Serial.print("IP Address: ");
  Serial.print(WiFi.localIP());

  //initial settings for light
  //pinMode(pin_led, OUTPUT);

  //initial settings for servo
  servo.attach(15);
  servo.write(150);

  //initial settings for motor
  pinMode(motor_en, OUTPUT);
  pinMode(motor_dir, OUTPUT);
  digitalWrite(motor_en, LOW);

  //initial settings for making ESP to be a Access Point
  server.on("/", []() {
    server.send(200, "text/plain", "you, motherfucker you");
  });
  server.on("/self_driving", self_driving); //page for receiving data from clients
  server.begin();
}

void loop() {
  server.handleClient();
}

void self_driving() {
  String data_string = server.arg("plain"); //.arg method receives a parameter and returns the value of that parameter
  //allocate the memory for the document
  const size_t capacity = JSON_OBJECT_SIZE(10);
  /*Calculate the capacity of JsonDocument
    JSON_OBJECT_SIZE: returnS the number of bytes required to store a JSON object that contains n key-value pairs
  */
  StaticJsonDocument<capacity> jDoc;
  /*JsonDocument stores a JSON document in memory with serialization function,
    StaticJsonDocument: stores in the stack with smaller than 1KB data,
    DynamiccJsonDocument: stores in the stack with larger than 1KB data.
  */
  //deserialize the object
  DeserializationError err = deserializeJson(jDoc, data_string);
  //extract the data
  JsonObject object = jDoc.as<JsonObject>();
  String c = object["command"];
  char d = c.charAt(1);
  Serial.println(c);
  //server.send(204, "");

  if (c == "w") {
    forward();
    server.send(204, "");
  }
  else if (c == "q") {
    forward_left();
    server.send(204, "");
  }
  else if (c == "e") {
    forward_right();
    server.send(204, "");
  }
  /*else if (c == "s") {
    backward();
    server.send(204, "");
  }
  else if (c == "a") {
    backward_left();
    server.send(204, "");
  }
  else if (c == "d") {
    backward_right();
    server.send(204, "");
  }*/
  else if (c == "x") {
    stop();
    server.send(204, "");
  }
  /*
    switch (d) { //switch(var): var is a variable whose value to compare, allowed data types: int, char
      case 'w':
        forward();
        server.send(204, "");
      case 'q':
        forward_left();
        server.send(204, "");
      case 'e':
        forward_right();
        server.send(204, "");
      case 's':
        backward();
        server.send(204, "");
      case 'a':
        backward_left();
        server.send(204, "");
      case 'd':
        backward_right();
        server.send(204, "");
      case 'x':
        stop();
        server.send(204, "");
    }*/
}


void stop(void) {
  digitalWrite(motor_en, LOW);
  servo.write(150);
}

void forward(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, HIGH);
  servo.write(150);
}

void forward_left(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, HIGH);
  servo.write(180);
}

void forward_right(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, HIGH);
  servo.write(130);
}

void backward(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, LOW);
  servo.write(150);
}

void backward_left(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, LOW);
  servo.write(180);
}

void backward_right(void) {
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, LOW);
  servo.write(130);
}
