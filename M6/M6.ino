#include <Arduino_LSM6DS3.h>
#include <ArduinoBLE.h>

#define BLE_UUID_GESTURE_SERVICE "1101"
#define BLE_UUID_GESTURE_CHARACTERISTIC "2101"
#define BLE_NAME "Brandon's Arduino"
#define BAUD_RATE (9600)

enum Gesture {
  UP, DOWN, STOP  
};

BLEService gestureService(BLE_UUID_GESTURE_SERVICE);
BLEIntCharacteristic gestureCharacteristic(BLE_UUID_GESTURE_CHARACTERISTIC, BLERead | BLENotify);

float ax, ay, az;

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);

  /* Initialize serial */
  Serial.begin(BAUD_RATE);
  while (!Serial);

  /* Initialize IMU */
  if (!IMU.begin()) {
    Serial.println(F("Error: Failed to initialize IMU!"));
    while (1);
  }

  /* Initialize BLE */
  if (!BLE.begin()) {
    Serial.println(F("Error: Failed to initialize BLE module!"));
    while (1);
  }

  /* Set advertised local name and service UUID */
  BLE.setLocalName(BLE_NAME);
  BLE.setDeviceName(BLE_NAME);
  BLE.setAdvertisedService(gestureService);

  /* Add characteristic(s) to the service */
  gestureService.addCharacteristic(gestureCharacteristic);

  /* Add service */
  BLE.addService(gestureService);

  /* Set initial values for characteristics */
  gestureCharacteristic.writeValue(STOP);

  /* Start advertising */
  BLE.advertise();
  Serial.print(F("BLE advertising as "));
  Serial.println(BLE_NAME);
}

void loop()
{
  BLEDevice central = BLE.central();

  if (central) {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.print(F("Connected to central: "));
    Serial.println(central.address());

    while (central.connected()) {
      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(ax, ay, az);
        if (az >= 0.8) {
          gestureCharacteristic.writeValue(UP);
        } else if (az <= -0.8) {
          gestureCharacteristic.writeValue(DOWN);
        } else {
          gestureCharacteristic.writeValue(STOP);
        }
      }
    }

    digitalWrite(LED_BUILTIN, LOW);
    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}
