// Lê o controle original do Gree pelo receptor e mostra o protocolo, o modelo e o estado.
// Serve para confirmar o kGreeModel de config.h antes de ligar o emissor.

#include <IRac.h>
#include <IRrecv.h>
#include <IRutils.h>

constexpr uint16_t kIrRecvPin = 14;
constexpr uint16_t kCaptureBufferSize = 1024;
// Os protocolos de ar-condicionado mandam quadros longos com pausas no meio.
constexpr uint8_t kFrameTimeoutMs = 50;

IRrecv receiver(kIrRecvPin, kCaptureBufferSize, kFrameTimeoutMs, true);
decode_results results;

void setup() {
  Serial.begin(115200);
  receiver.enableIRIn();
  Serial.println("Aponte o controle do Gree para o receptor e aperte um botão.");
}

void loop() {
  if (!receiver.decode(&results)) return;

  Serial.print(resultToHumanReadableBasic(&results));
  Serial.println(IRAcUtils::resultAcToString(&results));
  Serial.println();
  receiver.resume();
}
