#include "ac_state.h"
#include "config.h"
#include "connection.h"
#include "gree_remote.h"
#include "state_store.h"

GreeRemote remote(kIrLedPin, kGreeModel);
Connection connection;
AcState state;

void handleCommand(const JsonDocument& command) {
  applyCommand(state, command);
  remote.send(state);
  saveState(state);
  connection.publishState(state);
}

void setup() {
  Serial.begin(115200);
  state = loadState();
  remote.begin();
  connection.begin(handleCommand, [] { connection.publishState(state); });
}

void loop() { connection.loop(); }
