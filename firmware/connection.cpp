#include "connection.h"

#include <WiFi.h>

#include "ca_cert.h"
#include "config.h"
#include "secrets.h"

namespace {
constexpr unsigned long kRetryIntervalMs = 5000;
}

void Connection::begin(CommandHandler onCommand, ConnectedHandler onConnected) {
  onCommand_ = onCommand;
  onConnected_ = onConnected;

  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.begin(kWifiSsid, kWifiPassword);

  tls_.setCACert(kMqttRootCa);
  mqtt_.setServer(kMqttHost, kMqttPort);
  mqtt_.setBufferSize(512);
  mqtt_.setCallback([this](char* topic, uint8_t* payload, unsigned int length) { receive(topic, payload, length); });
}

void Connection::loop() {
  if (mqtt_.connected()) {
    mqtt_.loop();
    return;
  }

  const bool waiting = millis() - lastAttemptAt_ < kRetryIntervalMs;
  if (WiFi.status() != WL_CONNECTED || waiting) return;

  lastAttemptAt_ = millis();
  connect();
}

void Connection::publishState(const AcState& state) {
  JsonDocument doc;
  writeJson(state, doc);

  char payload[256];
  const size_t length = serializeJson(doc, payload);
  mqtt_.publish(kTopicState, reinterpret_cast<const uint8_t*>(payload), length, true);
}

void Connection::connect() {
  Serial.printf("Conectando ao MQTT em %s...\n", kMqttHost);

  // Se o ESP32 cair, o broker publica "offline" no lugar dele (last will).
  const bool connected = mqtt_.connect(kDeviceId, kMqttUser, kMqttPassword, kTopicOnline, 1, true, "offline");
  if (!connected) {
    Serial.printf("Falha no MQTT (código %d), tentando de novo em %lus\n", mqtt_.state(), kRetryIntervalMs / 1000);
    return;
  }

  Serial.println("MQTT conectado");
  mqtt_.publish(kTopicOnline, "online", true);
  mqtt_.subscribe(kTopicSet, 1);
  onConnected_();
}

void Connection::receive(const char* topic, const uint8_t* payload, unsigned int length) {
  JsonDocument command;
  const DeserializationError error = deserializeJson(command, payload, length);
  if (error) {
    Serial.printf("Comando inválido em %s: %s\n", topic, error.c_str());
    return;
  }

  onCommand_(command);
}
