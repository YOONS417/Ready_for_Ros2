#include <Arduino.h>
#include <SensirionI2cScd4x.h>
#include <Wire.h>

SensirionI2cScd4x scd4x;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  scd4x.begin(Wire, SCD41_I2C_ADDR_62);

  scd4x.wakeUp();
  scd4x.stopPeriodicMeasurement();
  delay(500);
  scd4x.reinit();
  delay(30);
  if (scd4x.startPeriodicMeasurement() != 0) {
    Serial.println("SCD41_START_ERROR");
  }
}

void loop() {
  bool data_ready = false;
  if (scd4x.getDataReadyStatus(data_ready) != 0 || !data_ready) {
    delay(100);
    return;
  }

  uint16_t co2_ppm = 0;
  float temperature_c = 0.0f;
  float humidity_percent = 0.0f;
  if (scd4x.readMeasurement(co2_ppm, temperature_c, humidity_percent) == 0
      && co2_ppm > 0) {
    Serial.println(co2_ppm);
  }
}