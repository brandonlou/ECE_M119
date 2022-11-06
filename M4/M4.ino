#include <Arduino_LSM6DS3.h>
#include <ArduinoBLE.h>

#define BLE_UUID_ACCELEROMETER_SERVICE "1101"
#define BLE_UUID_ACCELEROMETER_X "2101"
#define BLE_NAME "Barduino"
#define BAUD_RATE 9600

BLEService accelerometerService(BLE_UUID_ACCELEROMETER_SERVICE);

BLEFloatCharacteristic accelerometerCharacteristicX(BLE_UUID_ACCELEROMETER_X, BLERead | BLENotify);

float ax, ay, az;

void setup() {
  /* Initialize serial */
  Serial.begin(BAUD_RATE);
  while (!Serial);

  /* Initialize IMU */
  if (!IMU.begin()) {
    Serial.println(F("Error: Failed to initialize IMU!"));
    while (1);
  }
  Serial.print(F("Accelerometer sample rate: "));
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(F(" Hz"));

  /* Initialize BLE */
  if (!BLE.begin()) {
    Serial.println(F("Error: Failed to initialize BLE module!"));
    while (1);
  }

  /* Set advertised local name and service UUID */
  BLE.setLocalName(BLE_NAME);
  BLE.setDeviceName(BLE_NAME);
  // BLE.setDeviceName(BLE_DEVICE_NAME); // May not be necessary
  BLE.setAdvertisedService(accelerometerService);

  /* Add characteristics to the service */
  accelerometerService.addCharacteristic(accelerometerCharacteristicX);

  /* Add service */
  BLE.addService(accelerometerService);

  /* Set initial values for characteristics */
  accelerometerCharacteristicX.writeValue(0.0);

  /* Start advertising */
  BLE.advertise();
  Serial.print(F("BLE advertising as "));
  Serial.println(BLE_NAME);
}

void loop() {
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print(F("Connected to central: "));
    Serial.println(central.address());

    while (central.connected()) {
      if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(ax, ay, az);
        accelerometerCharacteristicX.writeValue(ax);
      }
    }

    Serial.print(F("Disconnected from central: "));
    Serial.println(central.address());
  }
}
