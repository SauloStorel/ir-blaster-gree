#include "gree_remote.h"

GreeRemote::GreeRemote(uint16_t pin, gree_ac_remote_model_t model) : ac_(pin, model) {}

void GreeRemote::begin() { ac_.begin(); }

void GreeRemote::send(const AcState& state) {
  ac_.setPower(state.power);
  ac_.setMode(state.mode);
  ac_.setTemp(state.temp);
  ac_.setFan(state.fan);
  ac_.setSwingVertical(state.swing, kGreeSwingLastPos);
  ac_.send();
}
