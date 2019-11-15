#include <SocketIOClient.h>
#include <ESP8266WiFi.h>

const char* ssid = "DucTrung";
const char* password = "mangnhabihu";

SocketIOClient client;

char host[] = "127.0.0.1";
int port = 4567;

extern String RID; // ten su kien
extern String Rname; //
extern String Rcontent;

void setup() {
  WiFi.begin(ssid, password);
  Serial.begin(115200);
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("");
  Serial.print("IP Address: ");
  Serial.print(WiFi.localIP());

  if (!client.connect(host, port)) {
    Serial.println("connection failed");
    return;
  }
  if (client.connected())
  {
    client.send("connection", "message", "Connected !!!!");
  }
}

void loop() {
  Serial.print("RID:");
  Serial.println(RID);
  Serial.print("Rname:");
  Serial.println(Rname);
  Serial.print("Rcontent:");
  Serial.println(Rcontent);

  if (!client.connected()) {
    client.reconnect(host, port);
  }
}
