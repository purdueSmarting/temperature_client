#include <Adafruit_Sensor.h>
#include <DHT22.h>
#include "DHT.h"
 
#define DHTPIN 2    //센서가 연결된 디지털핀
#define DHTTYPE DHT22   // DHT 22  (AM2302)
 
//DHT 센서 초기화
DHT dht(DHTPIN, DHTTYPE);
 
void setup() {
  Serial.begin(9600);
  dht.begin();
}
 
void loop() { 
  //측정하는 시간사이에 10초간의 딜레이를 줌
  delay(2000);

  int t= dht.readTemperature();
  int send_t = t;
  float h = dht.readHumidity();
  //에러 검사
  if ( isnan(h) || isnan(t) ) { 
    Serial.println("Failed to read from DHT sensor");
    return;
  }
  Serial.println(send_t);
}
