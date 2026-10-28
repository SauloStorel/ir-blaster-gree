#pragma once

#include <ir_Gree.h>

// Pino que aciona o transistor do LED IR.
constexpr uint16_t kIrLedPin = 4;

// Paliativo: a placa atual tem uma queda rápida de tensão quando o rádio Wi-Fi liga, e o detector de
// brownout reiniciava o ESP32 em loop. Volte para true quando houver um capacitor de 470–1000 µF
// entre 3V3 e GND.
constexpr bool kBrownoutDetector = false;

// Variante do protocolo Gree, confirmada lendo o controle original com receptor_ir/.
constexpr gree_ac_remote_model_t kGreeModel = gree_ac_remote_model_t::YAW1F;

// Adafruit IO: cada tópico é um feed no formato <usuário>/feeds/<chave-do-feed>.
#define AIO_USERNAME "saulostorel"
#define DEVICE_ID "ar-quarto"
#define FEED_PREFIX AIO_USERNAME "/feeds/" DEVICE_ID "-"

constexpr char kMqttHost[] = "io.adafruit.com";
constexpr uint16_t kMqttPort = 8883;
constexpr char kMqttUser[] = AIO_USERNAME;

constexpr char kDeviceId[] = DEVICE_ID;
constexpr char kTopicSet[] = FEED_PREFIX "set";
constexpr char kTopicState[] = FEED_PREFIX "state";
constexpr char kTopicOnline[] = FEED_PREFIX "online";
