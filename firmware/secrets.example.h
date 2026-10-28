#pragma once

// Copie este arquivo para secrets.h e preencha. O secrets.h não vai para o git.

constexpr char kWifiSsid[] = "nome-da-rede";  // o ESP32 só conecta em redes 2,4 GHz
constexpr char kWifiPassword[] = "senha-da-rede";

// Active Key do Adafruit IO (ícone de chave em io.adafruit.com).
constexpr char kAioKey[] = "aio_xxxxxxxxxxxxxxxxxxxxxxxxxxxx";

// Senha da atualização pelo Wi-Fi (firmware/ota-upload). Qualquer texto difícil de adivinhar.
constexpr char kOtaPassword[] = "troque-esta-senha";
