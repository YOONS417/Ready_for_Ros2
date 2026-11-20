#include <Arduino.h>

namespace {
constexpr uint8_t MQ3_PIN = A0;
constexpr unsigned long SAMPLE_PERIOD_MS = 400;

unsigned long last_sample_ms = 0;
uint32_t sample_sequence = 0;
}  // namespace

void setup() {
  Serial.begin(9600);
}

void loop() {
  const unsigned long now = millis();
  if (now - last_sample_ms < SAMPLE_PERIOD_MS) {
    return;
  }
  last_sample_ms = now;

  const int adc_value = analogRead(MQ3_PIN);
  Serial.print("MQ3,");
  Serial.print(sample_sequence++);
  Serial.print(',');
  Serial.println(adc_value);

  delay(200);
}
