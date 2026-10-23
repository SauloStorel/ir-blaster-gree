#pragma once

#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFiClientSecure.h>

#include <functional>

#include "ac_state.h"

// Mantém Wi-Fi e MQTT conectados e entrega os comandos recebidos.
class Connection {
 public:
  using CommandHandler = std::function<void(const JsonDocument&)>;
  using ConnectedHandler = std::function<void()>;

  void begin(CommandHandler onCommand, ConnectedHandler onConnected);
  void loop();
  void publishState(const AcState& state);

 private:
  void connect();
  void receive(const char* topic, const uint8_t* payload, unsigned int length);

  WiFiClientSecure tls_;
  PubSubClient mqtt_{tls_};
  CommandHandler onCommand_;
  ConnectedHandler onConnected_;
  unsigned long lastAttemptAt_ = 0;
};
