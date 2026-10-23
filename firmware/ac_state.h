#pragma once

#include <ArduinoJson.h>
#include <ir_Gree.h>

struct AcState {
  bool power = false;
  uint8_t mode = kGreeCool;
  uint8_t temp = 24;
  uint8_t fan = kGreeFanAuto;
  bool swing = false;
};

// Aplica um comando parcial, ex.: {"power": true, "temp": 22}.
// Campos ausentes ou inválidos mantêm o valor atual.
void applyCommand(AcState& state, const JsonDocument& command);

void writeJson(const AcState& state, JsonDocument& doc);
