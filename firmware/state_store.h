#pragma once

#include "ac_state.h"

// Guarda o último estado na flash, para o ESP32 voltar de uma queda de energia
// sabendo como o ar estava (o IR sempre envia o estado completo).
AcState loadState();
void saveState(const AcState& state);
