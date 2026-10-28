#pragma once

// Atualização do firmware pelo Wi-Fi, protegida por senha (firmware/ota-upload).
class Ota {
 public:
  void loop();

 private:
  bool started_ = false;
};
