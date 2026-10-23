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
Broker MQTT (Adafruit IO, grátis)  ◄── MQTT ── Plugin na barra do Omarchy
   ▲  MQTT (conexão de saída, sem abrir porta no roteador)
   │
ESP32 em casa ──IR──► Ar Gree
```

### Tópicos MQTT (feeds do Adafruit IO)

Broker `io.adafruit.com:8883` (TLS), usuário `saulostorel`, senha = Active Key do Adafruit IO.

| Tópico | Direção | Conteúdo |
|---|---|---|
| `saulostorel/feeds/ar-quarto-set` | app → ESP32 | comando parcial, ex.: `{"power": true, "temp": 22}` |
| `saulostorel/feeds/ar-quarto-state` | ESP32 → app | `{"power", "mode", "temp", "fan", "airflow", "sleep", "eco", "turbo"}` |
| `saulostorel/feeds/ar-quarto-online` | ESP32 → app | `online` / `offline` (last will) |

O Adafruit IO não usa retain: para receber o último valor de um feed, publique qualquer coisa em
`<feed>/get`. O plano grátis aceita até 30 mensagens por minuto e 10 feeds.

Valores: `mode` = `auto`, `cool`, `dry`, `fan`, `heat`; `fan` = `auto`, `low`, `medium`, `high`;
`airflow` = `swing`, `up`, `middle`, `down`; `sleep`, `eco` e `turbo` = `true`/`false`;
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

## Barra do Omarchy

Em `bar/`: um plugin da barra (`storell.ar-gree`) e o script `ar-gree`, que ele usa para falar com
o Adafruit IO. As credenciais ficam em `~/.config/ir-blaster-gree/credentials` (`AIO_USERNAME` e
`AIO_KEY`, modo 600).

| Na barra | Ação |
|---|---|
| ícone do modo + temperatura | ar ligado |
| ícone do ar | ar desligado |
| ícone apagado | ESP32 offline |
| clique | abre/fecha o painel |
| botão direito | liga/desliga |
| rolar | sobe/desce a temperatura (enviada 0,7 s depois da última rolagem) |

```sh
bar/install                               # instala ou atualiza o plugin e reinicia a barra
omarchy plugin enable storell.ar-gree --section right

bar/ar-gree simulate                      # finge ser o ESP32, para testar sem a placa
bar/ar-gree send '{"power": true}'        # manda um comando pelo terminal
bar/ar-gree watch                         # mostra o estado em tempo real
```

## Painel (Windows e Linux)

Em `app/`: um app [Tauri](https://tauri.app) com o painel "meu canto": liga/desliga, temperatura,
modo, ventilação e oscilar; no menu "•••", turbo, sono, eco, posição da aleta e a conta do Adafruit. O visual é HTML/CSS/JS em `app/src/`, e o MQTT vai direto do painel
para o Adafruit IO por WebSocket.

- **Linux:** clique no ícone da barra do Omarchy abre e fecha o painel no canto superior direito
  (regra de janela `ar-gree(-panel)?` em `~/.config/hypr/hyprland.lua`).
- **Windows:** ícone na bandeja; clique abre o painel colado nele, e o menu tem "Sair".
- As credenciais ficam no mesmo arquivo do script `ar-gree` (no Windows, em
  `%APPDATA%\ir-blaster-gree\credentials`). Sem esse arquivo, o painel abre na tela de configuração.

```sh
app/install                 # Linux: compila e instala em ~/.local/bin/ar-gree-panel
cd app && npm install && npx tauri build   # Windows: gera o instalador em src-tauri/target/release/bundle/
```

No Linux com NVIDIA, a janela é opaca de propósito: com transparência o WebKitGTK não desenha o conteúdo.
Os cantos arredondados vêm da regra do Hyprland.

## Onde paramos

- [x] Firmware escrito (IR + Wi-Fi + MQTT).
- [x] Firmware compilando (69% da flash, 13% da RAM).
- [x] Broker: o HiveMQ acabou com o plano grátis; adotado o Adafruit IO. Login, TLS e publicação
      testados do computador.
- [x] Plugin na barra do Omarchy, testado com o simulador.
- [x] Painel desktop (Tauri) para Windows e Linux, aberto pela barra no Linux.
- [ ] Gerar o instalador do Windows (compilar num PC com Windows ou via GitHub Actions).
- [ ] App web/PWA para o celular, reaproveitando o painel.
- [ ] Fechar o pedido das peças e confirmar o transistor que tem em casa.
- [ ] Quando o ESP32 chegar: ler o controle com o receptor para confirmar o modelo Gree (`kGreeModel`).
