#pragma once

#include <ir_Gree.h>

#include "ac_state.h"

// Faz o papel do controle remoto: cada envio transmite o estado completo do ar.
class GreeRemote {
 public:
  GreeRemote(uint16_t pin, gree_ac_remote_model_t model);

  void begin();
  void send(const AcState& state);

 private:
  IRGreeAC ac_;
};
