#include "ac_state.h"

#include <string.h>

namespace {

struct Option {
  const char* name;
  uint8_t code;
};

constexpr Option kModes[] = {
    {"auto", kGreeAuto}, {"cool", kGreeCool}, {"dry", kGreeDry}, {"fan", kGreeFan}, {"heat", kGreeHeat},
};

constexpr Option kFans[] = {
    {"auto", kGreeFanAuto}, {"low", kGreeFanMin}, {"medium", kGreeFanMed}, {"high", kGreeFanMax},
};

constexpr Option kAirflows[] = {
    {"swing", kGreeSwingAuto}, {"up", kGreeSwingUp}, {"middle", kGreeSwingMiddle}, {"down", kGreeSwingDown},
};

template <size_t N>
uint8_t codeOf(const Option (&options)[N], const char* name, uint8_t fallback) {
  for (const Option& option : options) {
    if (strcmp(option.name, name) == 0) return option.code;
  }
  return fallback;
}

template <size_t N>
const char* nameOf(const Option (&options)[N], uint8_t code) {
  for (const Option& option : options) {
    if (option.code == code) return option.name;
  }
  return options[0].name;
}

}  // namespace

void applyCommand(AcState& state, const JsonDocument& command) {
  state.power = command["power"] | state.power;
  state.mode = codeOf(kModes, command["mode"] | "", state.mode);
  state.temp = constrain(command["temp"] | state.temp, kGreeMinTempC, kGreeMaxTempC);
  state.fan = codeOf(kFans, command["fan"] | "", state.fan);
  state.airflow = codeOf(kAirflows, command["airflow"] | "", state.airflow);
  state.sleep = command["sleep"] | state.sleep;
  state.eco = command["eco"] | state.eco;
}

void writeJson(const AcState& state, JsonDocument& doc) {
  doc["power"] = state.power;
  doc["mode"] = nameOf(kModes, state.mode);
  doc["temp"] = state.temp;
  doc["fan"] = nameOf(kFans, state.fan);
  doc["airflow"] = nameOf(kAirflows, state.airflow);
  doc["sleep"] = state.sleep;
  doc["eco"] = state.eco;
}
