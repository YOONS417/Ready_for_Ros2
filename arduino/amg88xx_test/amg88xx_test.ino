/***************************************************************************
  This is a library for the AMG88xx GridEYE 8x8 IR camera

  This sketch tries to read the onboard thermistor.
  This is useful for ensuring your wiring is correct.
  Expect a reading of ~25 degrees C (room temperature)

  Designed specifically to work with the Adafruit AMG88 breakout
  ----> http://www.adafruit.com/products/3538

  These sensors use I2C to communicate. The device's I2C address is 0x69

  Adafruit invests time and resources providing this open source code,
  please support Adafruit andopen-source hardware by purchasing products
  from Adafruit!

  Written by Dean Miller for Adafruit Industries.
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/
#include <Wire.h>
#include <Adafruit_AMG88xx.h>

Adafruit_AMG88xx amg; 
float pixels[AMG88xx_PIXEL_ARRAY_SIZE];
bool sensor_ready = false;
unsigned long last_init_attempt_ms = 0;

bool initialize_sensor() {
  Serial.println("Initializing AMG88xx...");
  sensor_ready = amg.begin();
  if (sensor_ready) {
    Serial.println("AMG88xx initialized.");
  } else {
    Serial.println("ERROR: AMG88xx not found. Check I2C wiring and address 0x69.");
  }
  last_init_attempt_ms = millis();
  return sensor_ready;
}

void setup() {
  Serial.begin(115200);
  initialize_sensor();
}

void loop() {
  if (!sensor_ready) {
    if (millis() - last_init_attempt_ms >= 1000) {
      initialize_sensor();
    }
    return;
  }

  amg.readPixels(pixels);
  for(int i = 0; i < AMG88xx_PIXEL_ARRAY_SIZE; i++){
    Serial.print(pixels[i]);
    if (i < AMG88xx_PIXEL_ARRAY_SIZE - 1) {
      Serial.print(",");
    }
  }
  Serial.println();
  delay(100);
}
