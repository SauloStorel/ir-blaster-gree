# Caixa mini — 64 × 50,4 × 35,4 mm

## Imprimir

Os STL já estão orientados e não precisam de suportes. PLA, bico 0,4 mm,
camada 0,2 mm, 4 perímetros, 15–20% de preenchimento e ventoinha ligada.

1. `teste_encaixe_base.stl` + `teste_encaixe_parede.stl` (minutos): encaixe
   a parede na base. Se a trava ficar dura demais ou frouxa, ajuste as
   constantes `SNAP_*` ou `GAP` e gere de novo.
2. `base.stl`: fundo na mesa.
3. `tampa.stl`: topo na mesa.

## O que vai dentro

ESP32 DevKit de 30 pinos (52 × 29 mm) e o emissor IR KY-005, ligados por
jumpers Dupont fêmea-fêmea, sem solda. Sem receptor IR: o KY-022 serviu só
para ler o controle original (`firmware/receptor_ir/`).

- **ESP32 de cabeça para baixo**, com os componentes para baixo e os pinos
  para cima. Apoia em quatro calços nos cantos, fora das fileiras de pinos,
  com guias em L que impedem a placa de escorregar. Sem travas.
- A **fileira de trás** é a que tem 3V3, GND e D4, perto do USB: é nela que
  entram os jumpers. Eles sobem e o fio dobra para trás, rente ao teto. Por
  isso o micro-USB fica na **lateral esquerda**, ao olhar a caixa pela frente.
- O micro-USB fica embaixo da placa: ela sobe 5,5 mm do fundo para a
  borracha do plugue entrar sem tocar o chão da caixa.
- **Emissor deitado nos trilhos do teto**, acima das pontas dos pinos do
  ESP32, com o LED no furo central da frente. A placa entra por trás até a
  aba do LED encostar no furo. Os jumpers dele saem para trás e o fio dobra
  para o lado antes da parede.

Veja `previa_interna.png`. Montagem: encaixe o ESP32 nos calços, ligue os
jumpers (sinal do emissor no D4, `–` no GND), deslize o emissor nos trilhos
da carcaça virada de cabeça para baixo, acomode as sobras de fio e feche
pressionando os quatro pontos das travas até assentarem.

## Construção

- Paredes e fundo de 2,4 mm; cantos externos de raio 6 mm, borda superior
  arredondada em 2 mm e inferior em 1,2 mm.
- Fechamento por quatro linguetas ocultas na saia da base, duas na frente e
  duas atrás, sem parafusos. Cada uma tem trecho flexível de 12 mm, 1 mm de
  espessura e dente de 0,6 mm com rampas de entrada e saída.
- Profundidade calculada pela fila do emissor: LED, PCB de 18,5 mm, capa
  Dupont de 14 mm e 7 mm para o fio dobrar 90° antes da parede de trás.
- Altura calculada pelos jumpers do ESP32: espaçador de 2,5 mm, capa de
  14 mm e 7 mm para o fio dobrar antes do teto.
- Frente com faixa rebaixada em 0,5 mm e um único furo de 5,2 mm para o
  LED, centralizado e a 24,6 mm do fundo.
- Micro-USB na lateral esquerda: janela de 12 × 9 mm, centralizada no
  conector, que atravessa a parede, a junta e a saia da base.
- Sete fendas de ventilação na traseira. Topo e fundo lisos e fechados.

## O que já foi confirmado

O gerador confere que base e carcaça são sólidos válidos e sem
interferência, com malhas fechadas, contorno do fundo sem furos, travas
livres nas cavidades e espaço de entrada dos dentes. Também confere, com
referências simplificadas, que nada encosta na caixa nem um no outro: PCB
do ESP32, componentes por baixo dela (até 3,5 mm), as duas barras de pinos,
os jumpers do ESP32 e a dobra dos fios, o emissor, o LED, os jumpers dele e
a dobra dos fios, além do plugue micro-USB. Deslocar o ESP32 ou o emissor
0,4 mm faz a placa encontrar uma guia ou o trilho. Resultados em
`validacao.json`. Nada disso substitui o teste físico.

**Antes de imprimir, meça com paquímetro:**

- o comprimento da capa dos seus jumpers Dupont: o projeto supõe 14 mm
  (`DUPONT_LENGTH`);
- se os cantos da face dos componentes do ESP32 estão livres (2,5 × 2,2 mm),
  onde ficam os calços, e a altura dos componentes: supõe até 3,5 mm;
- quanto os pinos do ESP32 saem da placa, contando o espaçador: supõe 8,5 mm;
- a placa do KY-005 (supõe 15 × 18,5 mm; os trilhos aceitam 14 a 16 mm de
  largura) e onde o LED fica em relação à borda;
- a borracha do cabo micro-USB: a passagem aceita até ~11,5 × 8,5 mm.

## Arquivos

- `gerar_caixa.py`: fonte; altere as constantes e execute
  `python hardware/caixa/mini/gerar_caixa.py`.
- `base.stl`, `tampa.stl` e as amostras de encaixe: peças de impressão.
- `caixa_ir_gree_mini.FCStd`: montagem no FreeCAD, com referências verdes
  ocultas do ESP32, do emissor e dos jumpers (não imprimir).
- `caixa_ir_gree_mini.step`: base e carcaça para outros programas CAD.
- `previa*.png`: renderizações das malhas reais por `render_vtk.py`.
- `historico_versoes.tar.xz`: versões anteriores, cada uma numa pasta
  `antes_*`. A mais recente é `antes_esp32_invertido` (ESP32 em pé,
  64 × 63 × 35,8 mm), descartada porque o fio do emissor não tinha espaço
  para dobrar antes da placa.

As imagens geradas por IA (`proposta_interna*.png`, `visualizacao_fisica.png`)
são de versões anteriores e não mostram este arranjo.
