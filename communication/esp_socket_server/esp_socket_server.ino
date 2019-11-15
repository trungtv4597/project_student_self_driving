#include <Arduino.h>
#include <WebSocketsServer.h>
#include <ESP8266WiFi.h>
#include <Servo.h>

#define USE_SERIAL Serial

//wifi identify
const char* ssid = "WCOMMLAB_LINKSYS";
const char* password = "labthongtinvotuyen@@";

//web_socket
WebSocketsServer webSocket = WebSocketsServer(81); // creating an object that will contain the Websocket server

//servo
Servo servo;

//motor
#define motor_en 4 //d2 enable
#define motor_dir 2 //d4 direction

//ultrasonic
#define trig 12 //d6
#define echo 13 //d7

//light
#define led 14 //d5

void setup() {
  //initial Serial
  USE_SERIAL.begin(115200);

  //Serial.setDebugOutput(true);
  USE_SERIAL.setDebugOutput(true);

  //initial WiFi accepting
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(200);
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  delay(500);

  //initial web_socket
  Serial.println("Start Websocket Server");
  webSocket.begin();
  webSocket.onEvent(webSocketEvent);

  //initial servo
  servo.attach(15);
  servo.write(150);

  //intital motor
  pinMode(motor_en, OUTPUT);
  pinMode(motor_dir, OUTPUT);
  digitalWrite(motor_en, LOW);

  //ultrasonic
  pinMode(trig, OUTPUT);
  pinMode(echo, INPUT);

  //led
  pinMode(led, OUTPUT);
  digitalWrite(led, LOW);
}

void loop() {
  float duration, distance;
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(5);
  digitalWrite(trig, LOW);
  duration = pulseIn(echo, HIGH);
  distance = (duration / 2) * 0.0344;
  USE_SERIAL.print("Distance: ");
  USE_SERIAL.println(distance);

  if (distance > 20) {
    webSocket.loop();
    digitalWrite(led, LOW);
  }
  else {
    stop();
    digitalWrite(led, HIGH);
  }

  delay(20);
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) {

  switch (type) {
    case WStype_DISCONNECTED:
      USE_SERIAL.printf("[%u] Disconnected!\n", num);
      break;

    case WStype_CONNECTED:
      {
        IPAddress ip = webSocket.remoteIP(num);
        USE_SERIAL.printf("[%u] Connected from %d.%d.%d.%d url: %s\n", num, ip[0], ip[1], ip[2], ip[3], payload);

        // send message to client
        webSocket.sendTXT(num, "Connected");
      }
      break;

    case WStype_TEXT: {
        USE_SERIAL.printf("[%u] get Text: %s\n", num, payload);
        String command = String((char *) &payload[0]);
        //USE_SERIAL.print("commnand: ");
        //USE_SERIAL.println(command);

        // send message to client
        // webSocket.sendTXT(num, "message here");

        // send data to all connected clients
        // webSocket.broadcastTXT("message here");

        if (command == "3") {
          stop();
        }
        else if (command == "0") {
          forward();
        }
        else if (command == "1") {
          forward_left();
        }
        else if (command == "2") {
          forward_right();
        }
      }
      break;

    case WStype_BIN:
      USE_SERIAL.printf("[%u] get binary length: %u\n", num, length);
      hexdump(payload, length);

      // send message to client
      // webSocket.sendBIN(num, payload, length);
      break;
  }

}



void stop(void) {
  digitalWrite(motor_en, LOW);
  servo.write(150);
}

void forward(void) {
  analogWrite(motor_en, 800);
  //digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, HIGH);
  servo.write(150);
}

void forward_left(void) {
  analogWrite(motor_en, 800);
  digitalWrite(motor_en, HIGH);
  digitalWrite(motor_dir, HIGH);
  servo.write(180);
}

void forward_right(void) {
  analogWrite(motor_en, 800);
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
