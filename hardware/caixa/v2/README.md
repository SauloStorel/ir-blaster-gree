# Caixa v2 — carmesim

A segunda versão mantém 120 × 90 × 40,4 mm e muda a construção: a carcaça
superior incorpora o teto e se prende a uma bandeja inferior. Os quatro
parafusos ficam escondidos na parte de baixo.

- Cantos de raio 12 mm e borda superior arredondada em 2 mm.
- Junta inferior de 0,35 mm, com saia de encaixe e folga lateral de 0,3 mm.
- Faixa de onze fendas de ventilação, com comprimentos graduais.
- Símbolo de infravermelho gravado no topo, com profundidade de 0,45 mm.
- Rebaixo frontal que agrupa a janela do receptor e o furo do LED.
- Quatro apoios internos, passagens de abraçadeiras e rebaixos inferiores
  para pés autoadesivos opcionais de 8 mm.

## Arquivos

Abra `caixa_ir_gree_v2.FCStd` para ver a montagem fechada no FreeCAD. Oculte
`Carcaça superior` na árvore com a barra de espaço para inspecionar o interior.
`base.stl` e `tampa.stl` estão separados e orientados para a impressão.
O STEP mostra a montagem fechada. O gerador Python contém as dimensões;
a planilha no documento é apenas uma referência, não dirige a geometria.

## Impressão e montagem

Ponto de partida: bico 0,4 mm, camada 0,20 mm, quatro perímetros, cinco
camadas de topo/fundo e 15–20% de preenchimento. Use o perfil de temperatura
do fabricante do PLA. A textura da mesa ficará no topo externo da carcaça.

A bandeja imprime com o fundo na mesa. A carcaça imprime com o topo externo
para baixo; o STL já foi invertido. Confira as pequenas pontes dos furos e
o primeiro contato da borda arredondada no fatiador. O projeto busca dispensar
suportes, mas isso ainda não foi testado em uma impressão física.

Use quatro parafusos autoatarraxantes de aproximadamente 2,9 × 10 mm com
cabeça escareada de 90°. Piloto de 2,4 mm, passante de 3,3 mm e escareado de
6,2 mm. Os parafusos entram por baixo da bandeja. Faça um teste de tolerância
antes de apertar e não force o PLA. Pés autoadesivos são opcionais.

**O tamanho real da eletrônica ainda não foi informado.** Confirme placa,
adaptador, jumpers, conectores e eventual protoboard antes de imprimir.
A região central de 92 × 62 mm evita as torres; acima dos apoios há cerca de
34,6 mm livres até o teto. Isso é um envelope de referência, não uma
confirmação de que a montagem cabe. O Arduino de testes e uma protoboard
grande não foram previstos.

A janela do receptor mede aproximadamente 16 × 8 mm, com cantos arredondados;
o LED tem furo de 5,4 mm. Não há berços específicos: fixe as peças pelo
interior e isole os terminais. O cabo sai pela abertura traseira, que não
pressupõe a posição do conector na placa. Prenda a eletrônica à bandeja com
abraçadeiras e confira se ela não impede a montagem da carcaça.

## Verificação

Os dois sólidos são válidos e únicos; as malhas STL estão fechadas.
Interferência entre bandeja e carcaça montadas: zero. Os resultados estão em
`validacao.json`. A impressão, a montagem física e o alcance IR ainda não
foram testados.
