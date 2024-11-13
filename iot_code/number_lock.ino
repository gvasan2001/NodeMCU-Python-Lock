#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "mi";
const char* password = "v@s@n2001";
const char* mqtt_server = "public-mqtt-broker.bevywise.com";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);
const int ledPin = D1;
String receivedOtp; // Variable to store the OTP

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  Serial.println("hello");
}

void setup_wifi() {
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      client.subscribe("led/control");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void callback(char* topic, byte* message, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) {
    msg += (char)message[i];
  }

  // Check if the message is an OTP or a control message
  if (msg == "on") {
    receivedOtp = msg;
    Serial.print("Received OTP: ");
    Serial.println(receivedOtp);
    digitalWrite(ledPin, HIGH);
    Serial.println("LED ON");
  } else if (msg == "off") {
    digitalWrite(ledPin, LOW);
    Serial.println("LED OFF");
  } else {
    // Assume any other message is an OTP, store it, and print it
    receivedOtp = msg;
    Serial.print("Received OTP: ");
    Serial.println(receivedOtp);
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
