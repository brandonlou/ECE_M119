#include <WiFiNINA.h>

#include "secret.h"

#define BAUD_RATE 9600
#define CONNECTION_TIMEOUT 10000 /* Milliseconds */
#define UPDATE_INTERVAL 5000     /* Milliseconds */

unsigned long prevTime = 0; /* Last time WiFi info was updated */
unsigned long prevLED  = 0; /* Last time LED was updated */
int ledState = LOW;

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial);
  
  pinMode(LED_BUILTIN, OUTPUT);

  /* Attempt to connect to a WiFi network */
  int status = WL_IDLE_STATUS;
  while (1) {
    Serial.print(F("Attempting to connect to SSID: "));
    Serial.println(SSID);
    status = WiFi.beginEnterprise(SSID, USER, PASS);
    if (status == WL_CONNECTED) {
      break;
    }
    delay(CONNECTION_TIMEOUT);
  }

  Serial.println(F("Connected!\n"));
}

void loop() {
  unsigned long currTime = millis();
  if (currTime - prevTime >= UPDATE_INTERVAL) {
    prevTime = currTime;

    Serial.print(F("Connected to SSID: "));
    Serial.println(WiFi.SSID());

    Serial.print(F("Arduino's IP address: "));
    Serial.println(WiFi.localIP());

    Serial.print(F("Signal strength (RSSI): "));
    Serial.println(WiFi.RSSI());

    Serial.println();
  }

  unsigned long currLED = millis();
  int intervalLED = WiFi.RSSI() * -10; /* Convert the signal strengh into a time interval */
  if (currLED - prevLED >= intervalLED) {
    prevLED = currLED;
    ledState = (ledState == LOW) ? HIGH : LOW;
    digitalWrite(LED_BUILTIN, ledState);
  }
}
