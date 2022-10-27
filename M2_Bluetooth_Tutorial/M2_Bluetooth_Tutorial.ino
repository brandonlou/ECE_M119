#include <ArduinoBLE.h>

#define BLE_UUID_LED_SERVICE "180A"
#define BLE_UUID_SWITCH "2A57"
#define LOCAL_NAME "Brandon's Arduino"
#define BAUD_RATE 9600

BLEService ledService(BLE_UUID_LED_SERVICE);

BLEByteCharacteristic switchCharacteristic(BLE_UUID_SWITCH, BLERead | BLEWrite);

void setup() {
  Serial.begin(BAUD_RATE);
  while (!Serial);

  pinMode(LED_BUILTIN, OUTPUT);

  /* Initialize BLE */
  if (!BLE.begin()) {
    Serial.println(F("Error: Starting BLE module failed!"));
    while (1);
  }

  /* Set advertised local name and service UUID */
  BLE.setLocalName(LOCAL_NAME);
  BLE.setAdvertisedService(ledService);

  /* Add characteristic to the service */
  ledService.addCharacteristic(switchCharacteristic);

  /* Add service */
  BLE.addService(ledService);

  /* Set the initial value of the characeristic */
  switchCharacteristic.writeValue(0);

  /* Start advertising */
  BLE.advertise();

  Serial.print(F("BLE advertising as "));
  Serial.println(LOCAL_NAME);
}

void loop() {
  /* Listen for BLE peripherals to connect */
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print(F("Connected to central: "));
    Serial.println(central.address()); /* Central's MAC address */

    while (central.connected()) {
      /* Remote device wrote to the characteristic */
      if (switchCharacteristic.written()) {
        switch (switchCharacteristic.value()) {
          case 1:
            Serial.println(F("LED on"));
            digitalWrite(LED_BUILTIN, HIGH);
            break;
          case 2:
            Serial.println(F("LED fast blink"));
            digitalWrite(LED_BUILTIN, HIGH);
            delay(500);
            digitalWrite(LED_BUILTIN, LOW);
            delay(500);
            digitalWrite(LED_BUILTIN, HIGH);
            delay(500);
            digitalWrite(LED_BUILTIN, LOW);
            break;
          case 3:
            Serial.println(F("LED slow blink"));
            digitalWrite(LED_BUILTIN, HIGH);
            delay(1000);
            digitalWrite(LED_BUILTIN, LOW);
            delay(1000);
            digitalWrite(LED_BUILTIN, HIGH);
            delay(1000);
            digitalWrite(LED_BUILTIN, LOW);
            break;
          default:
            Serial.println(F("LED off"));
            digitalWrite(LED_BUILTIN, LOW);
            break;
        }
      }
    }

    /* Turn off the LED when the central disconnects */
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
    digitalWrite(LED_BUILTIN, LOW);
  }
}
