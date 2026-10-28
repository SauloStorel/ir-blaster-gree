# Caixa compacta para ESP32 de 52 × 29 mm

Dimensões externas: **82 × 58 × 30,4 mm**. A caixa anterior media
120 × 90 × 40,4 mm. Esta versão mantém os parafusos inferiores ocultos,
as bordas arredondadas, a junta inferior discreta e o rebaixo frontal IR.
O topo tem nove fendas graduais e um símbolo IR gravado.

Abra `caixa_ir_gree_compacta.FCStd` no FreeCAD. `base.stl` e `tampa.stl`
estão em milímetros e orientados para impressão. O STEP contém somente as
duas peças imprimíveis. A referência verde do ESP32 fica oculta no FreeCAD;
é apenas uma representação de 52 × 29 mm, não um modelo detalhado da placa.
Sua espessura ilustrativa de 1,6 mm não é uma medida informada pelo usuário.

## Encaixe

O comprimento de 52 mm e a largura de 29 mm foram informados pelo usuário.
O envelope retangular da placa foi verificado sem colisões com paredes,
torres, saia ou apoios, a partir do topo dos apoios. A altura livre acima
dos apoios é de aproximadamente 24,6 mm. A altura real do ESP32, dos pinos,
dos conectores e dos fios ainda precisa ser conferida.

Esta caixa considera o ESP32 sem placa de expansão e sem protoboard.
Há espaço ao redor da placa para um pequeno circuito IR e cabos, mas os
volumes e a montagem dessas peças ainda não foram medidos nem validados.
A passagem traseira é para o cabo; ela não garante alinhamento direto com
o conector USB da placa. Confira o percurso do cabo antes de imprimir.

Prenda o ESP32 sobre os quatro apoios com abraçadeiras pelas passagens no
fundo. A janela IR tem 16 × 8 mm e o furo do LED tem diâmetro de 5,4 mm;
fixe ambos pelo interior. Os quatro parafusos entram pelo fundo: use como
referência autoatarraxantes de 2,9 × 10 mm, cabeça escareada de 90°.
Pilotos de 2,4 mm; passantes de 3,3 mm; escareados de 6,2 mm.
Teste um piloto e aperte à mão sem forçar o PLA.

## Impressão

Ponto de partida para PLA: bico de 0,4 mm, camada de 0,20 mm, quatro
perímetros, cinco camadas de topo/fundo e 15–20% de preenchimento. Use as
temperaturas e o perfil do fabricante do filamento.

A bandeja imprime com o fundo na mesa. A carcaça imprime com o topo externo
sobre a mesa — o STL já está invertido. A textura da mesa ficará no topo
externo. Confira a primeira camada da borda arredondada e as pequenas pontes
na prévia do fatiador. Não foi feita uma impressão física de teste.

## Verificação executada

- Dois sólidos únicos e válidos; duas malhas STL fechadas.
- Interferência entre base e carcaça: zero.
- Interferência do envelope de 52 × 29 mm acima dos apoios: zero.
- Resultados em `validacao.json`.

Para mudar dimensões, edite as constantes de `gerar_caixa.py` e regenere
com `python hardware/caixa/compacta/gerar_caixa.py` na raiz do projeto.
A planilha do FreeCAD é uma referência e não controla a geometria.
