#include "ac_state.h"
#include "config.h"
#include "connection.h"
#include "gree_remote.h"
#include "ota.h"
#include "state_store.h"
#include "soc/rtc_cntl_reg.h"

GreeRemote remote(kIrLedPin, kGreeModel);
Connection connection;
Ota ota;
AcState state;

void handleCommand(const JsonDocument& command) {
  applyCommand(state, command);
  remote.send(state);
  saveState(state);
  connection.publishState(state);
}

void setup() {
  if (!kBrownoutDetector) WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0);
  Serial.begin(115200);
  state = loadState();
  remote.begin();
  connection.begin(handleCommand, [] { connection.publishState(state); });
}

void loop() {
  connection.loop();
  ota.loop();
}
