#pragma once

#include <ArduinoJson.h>
#include <ir_Gree.h>

struct AcState {
  bool power = false;
  uint8_t mode = kGreeCool;
  uint8_t temp = 24;
  uint8_t fan = kGreeFanAuto;
  uint8_t airflow = kGreeSwingAuto;  // posição da aleta vertical; kGreeSwingAuto = oscilar
  bool sleep = false;
  bool eco = false;
};

// Aplica um comando parcial, ex.: {"power": true, "temp": 22}.
// Campos ausentes ou inválidos mantêm o valor atual.
void applyCommand(AcState& state, const JsonDocument& command);

void writeJson(const AcState& state, JsonDocument& doc);
