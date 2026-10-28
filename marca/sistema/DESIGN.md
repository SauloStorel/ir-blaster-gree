# Xfria — decisões de identidade

Kit visual para uma marca de controle de climatização por desktop. A direção combina tecnologia doméstica premium, calma e conforto: superfícies planas, contraste amplo, bastante espaço livre e formas suaves, sem gradientes ou efeitos 3D.

## Marca e linguagem

O símbolo é um X abstrato formado por fluxos de ar cruzados e suaves. A assinatura reúne o símbolo, o nome Xfria em peso forte e um ponto vermelho. Foram entregues versões horizontais, verticais, isoladas e monocromáticas, com alternativas para fundos claros e escuros. Escolher a versão com contraste adequado e preservar proporções, desenho e cores; usar o símbolo isolado em ícones e como elemento gráfico de maior escala. Os textos dos SVGs estão convertidos em contornos.

A mensagem central é “Seu clima. Seu controle.”. As peças usam frases curtas, diretas e acolhedoras, com ênfase em conforto e autonomia.

## Tokens entregues

`tokens.json` é a referência exata, acompanhada de `tokens.css`.

| Cor | Valor | Papel visual |
| --- | --- | --- |
| Grafite | `#151517` | Fundos escuros e texto sobre superfícies claras |
| Branco suave | `#f5f5f7` | Fundos claros e texto principal sobre grafite |
| Vermelho | `#ff4d5a` | Ponto da assinatura e ação de desligar no conceito |
| Azul gelo | `#d4ebff` | Fluxo de ar, destaques e informações secundárias |

Tipografia: Inter, com peso 900 para destaques, 700 para títulos e 400 para corpo. O tracking de destaque é `-0.03em`. A fonte variável e sua licença acompanham o kit.

Escala de espaçamento: `4, 8, 12, 16, 24, 32, 48, 64, 96`. Raios: `control: 12` e `appIcon: 112`, nas unidades das respectivas artes. Os tokens de movimento são duração de `240 ms`, curva `cubic-bezier(0.16,1,0.3,1)` e movimento reduzido `disable`.

## Ícones e movimento

Seis ícones próprios de contorno: energia, temperatura, fluxo, conexão, mais e menos. Traços simples acompanham a linguagem da interface. O SVG `xfria-movimento.svg` apresenta uma flutuação vertical suave do símbolo em ciclo de 3 segundos e desativa a animação com `prefers-reduced-motion: reduce`; esse ciclo demonstrativo é distinto do token de transição de 240 ms.

## Conceito desktop e revisão

O conceito de 1440 × 900 usa navegação lateral clara e uma área principal grafite. A temperatura recebe a maior ênfase, com controles circulares de ajuste, modo de operação abaixo e ação vermelha de desligar. Sala, conexão, temperatura de 22 °C e estados são valores ilustrativos em uma arte estática. Funcionalidade de aplicativo e conexão com aparelhos não foram implementadas.

A revisão visual da visão geral e do conceito desktop teve disposição de entrega, sem problemas materiais identificados. Este registro documenta as decisões presentes nas peças entregues; não constitui validação de um aplicativo funcional.
