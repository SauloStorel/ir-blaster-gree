# Visualização interna ilustrativa

**As imagens geradas são anteriores às revisões da entrada USB e do topo.**
O modelo atual tem passagem para o micro-USB do ESP32 na lateral direita, topo liso e ventilação na parede
traseira. Veja `previa.png` e `previa_traseira.png` para as renderizações das
malhas STL atuais.
As imagens ilustrativas mantêm o percurso antigo do cabo e as fendas no topo;
não devem orientar a abertura na caixa.

As imagens `proposta_interna*.png` foram geradas com a ferramenta integrada
de geração de imagens, usando a captura CAD `previa.png` como referência.
Mostram uma sugestão de distribuição dos três elementos principais:
ESP32, receptor IR e conjunto emissor IR. Transistor e resistores fazem
parte do conjunto emissor.

O CAD contém somente a caixa e uma referência do tamanho da placa. A imagem
não é um render de uma montagem CAD validada dos componentes. Conectores,
cabos, fixações e módulos são representações aproximadas. As dimensões dos
módulos IR e a altura real da placa ainda precisam ser conferidas.
Não use a imagem como esquema elétrico.

As imagens geradas usam um conceito anterior de 70 × 45 × 25,4 mm, sem
expansão ou protoboard. O CAD atual mede 64 × 45 × 32,9 mm.
O teto removido é um recurso visual para mostrar o interior. A carcaça real
inclui teto e paredes, e se abre retirando a bandeja inferior.
