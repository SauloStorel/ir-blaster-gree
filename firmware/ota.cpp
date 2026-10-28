#include "ota.h"

#include <ArduinoOTA.h>
#include <WiFi.h>

#include "config.h"
#include "secrets.h"

void Ota::loop() {
  if (started_) {
    ArduinoOTA.handle();
    return;
  }
  if (WiFi.status() != WL_CONNECTED) return;

  // Só começa a escutar com IP; o mDNS anuncia o ESP32 como <DEVICE_ID>.local.
  ArduinoOTA.setHostname(kDeviceId);
  ArduinoOTA.setPassword(kOtaPassword);
  ArduinoOTA.onStart([] { Serial.println("Atualizando o firmware pelo Wi-Fi..."); });
  ArduinoOTA.onEnd([] { Serial.println("Firmware atualizado, reiniciando"); });
  ArduinoOTA.onError([](ota_error_t error) { Serial.printf("Falha na atualização (erro %u)\n", error); });
  ArduinoOTA.begin();
  started_ = true;
}
