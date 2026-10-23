# IR blaster Wi-Fi para ar-condicionado Gree

Controle de um ar-condicionado Gree de qualquer lugar, usando um ESP32 que imita o controle
remoto infravermelho e um app web próprio.

## Arquitetura

```
Celular (de qualquer lugar)
   │  HTTPS
   ▼
App web/PWA (Vercel Hobby, grátis)      ← login, tela, botões
   │  MQTT
   ▼
Broker MQTT (Adafruit IO, grátis)  ◄── MQTT ── Módulo na barra do Linux (Waybar)
   ▲  MQTT (conexão de saída, sem abrir porta no roteador)
   │
ESP32 em casa ──IR──► Ar Gree
```

### Tópicos MQTT (feeds do Adafruit IO)

Broker `io.adafruit.com:8883` (TLS), usuário `saulostorel`, senha = Active Key do Adafruit IO.

| Tópico | Direção | Conteúdo |
|---|---|---|
| `saulostorel/feeds/ar-quarto-set` | app → ESP32 | comando parcial, ex.: `{"power": true, "temp": 22}` |
| `saulostorel/feeds/ar-quarto-state` | ESP32 → app | `{"power", "mode", "temp", "fan", "swing"}` |
| `saulostorel/feeds/ar-quarto-online` | ESP32 → app | `online` / `offline` (last will) |

O Adafruit IO não usa retain: para receber o último valor de um feed, publique qualquer coisa em
`<feed>/get`. O plano grátis aceita até 30 mensagens por minuto e 10 feeds.

Valores: `mode` = `auto`, `cool`, `dry`, `fan`, `heat`; `fan` = `auto`, `low`, `medium`, `high`;
`temp` = 16 a 30.

- O protocolo do Gree é decodificado pela biblioteca
  [IRremoteESP8266](https://github.com/crankyoldgit/IRremoteESP8266) (classe `IRGreeAC`).
  Cada comando envia o estado completo: liga/desliga, modo, temperatura, ventilação e swing.
- O IR é de mão única (o ar não confirma o recebimento). O sensor de temperatura mostra no
  app a temperatura real do cômodo.
- Os agendamentos rodam no próprio ESP32, com o relógio sincronizado via NTP.
- O ESP32 guarda o último estado na flash, para não perder o estado numa queda de energia.
- Custo mensal: R$ 0.

## Peças

| Peça | Status |
|---|---|
| ESP32 30 pinos USB-C + placa de expansão (terminal adapter) | comprar |
| LED IR emissor 940 nm 5 mm | comprar |
| Jumpers macho-macho | comprar |
| Kit de resistores 1/4 W (1 kΩ e 33–47 Ω) | comprar |
| Sensor de temperatura AHT20 (opcional) | decidir |
| Transistor NPN (2N2222, BC337, BC547, S8050...) | confirmar se tem em casa |
| Receptor IR KY-022 | tem (2) |
| Protoboard | tem |
| Placa Arduino (testes de IR antes do ESP32 chegar) | tem |
| Cabo USB-C de dados e carregador USB 5 V | tem |

## Ligações

| Componente | Pino | ESP32 |
|---|---|---|
| Receptor KY-022 | S (sinal) | GPIO 14 |
| Receptor KY-022 | meio (VCC) | 3V3 (nunca 5 V) |
| Receptor KY-022 | – (GND) | GND |

O emissor (LED IR + transistor, no GPIO 4) será detalhado na montagem.

## Firmware

Em `firmware/`, compilado com `arduino-cli` (versões fixadas em `sketch.yaml`):

```sh
cd firmware
cp secrets.example.h secrets.h   # preencher Wi-Fi e a chave do Adafruit IO
arduino-cli compile --profile esp32 .
```

| Arquivo | Responsabilidade |
|---|---|
| `firmware.ino` | liga as peças: comando recebido → IR → publica o estado |
| `ac_state` | estado do ar e conversão de/para JSON |
| `gree_remote` | monta e envia o sinal IR do Gree |
| `state_store` | guarda o último estado na flash |
| `connection` | Wi-Fi, MQTT com TLS, reconexão e last will |
| `config.h` | pinos, modelo Gree, broker e tópicos |
| `ca_cert.h` | certificado raiz do TLS (DigiCert Global Root G2) |

## Onde paramos

- [x] Firmware escrito (IR + Wi-Fi + MQTT).
- [x] Firmware compilando (69% da flash, 13% da RAM).
- [x] Broker: o HiveMQ acabou com o plano grátis; adotado o Adafruit IO. Login, TLS e publicação
      testados do computador.
- [ ] Módulo na barra do Waybar: ícone e temperatura; clique liga/desliga; rolagem muda a
      temperatura; clique direito abre o menu de modo/ventilação. Usa `mosquitto_pub`/`mosquitto_sub`.
- [ ] App web/PWA com login.
- [ ] Fechar o pedido das peças e confirmar o transistor que tem em casa.
- [ ] Quando o ESP32 chegar: ler o controle com o receptor para confirmar o modelo Gree (`kGreeModel`).
