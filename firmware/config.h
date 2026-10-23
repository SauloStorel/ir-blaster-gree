#pragma once

#include <ir_Gree.h>

// Pino que aciona o transistor do LED IR.
constexpr uint16_t kIrLedPin = 4;

// Variante do protocolo Gree. Confirmar lendo o controle original com o receptor.
constexpr gree_ac_remote_model_t kGreeModel = gree_ac_remote_model_t::YAW1F;

#define DEVICE_ID "ar-quarto"

constexpr char kDeviceId[] = DEVICE_ID;
constexpr char kTopicSet[] = "ir-blaster/" DEVICE_ID "/set";
constexpr char kTopicState[] = "ir-blaster/" DEVICE_ID "/state";
constexpr char kTopicOnline[] = "ir-blaster/" DEVICE_ID "/online";
