#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

#define DHTPIN 15       // GPIO15
#define DHTTYPE DHT11
#define SOIL_PIN 33
DHT dht(DHTPIN, DHTTYPE);

const char* ssid       = "3Tan";
const char* password   = "3Sin/Cos";
const char* serverName = "http://192.168.250.11:8000/api/data";

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Connected!");
}

void loop() {                                                                                                                                                                                                                
  delay(2000);
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();
  int soil_analog = analogRead(SOIL_PIN);
  int soil_moisture = map(soil_analog, 0 ,4095,100,0);
  if (isnan(temp) || isnan(hum)) {
    Serial.println("DHT read failed");
    return;
  }
  if (isnan(soil_analog)){
    Serial.println("Soil_moisture read failed");
    return;
  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);
    http.addHeader("DHT11-Data", "application/json");
    String payload = "{\"temperature\": " + String(temp) + ", \"humidity\": " + String(hum) + ",\"soilMoisture\": "+ String(soil_moisture)+"}";
    int code = http.POST(payload);
    Serial.printf("HTTP %d\n", code);
    http.end();
  } else {
    Serial.println("WiFi lost");
  }
}
