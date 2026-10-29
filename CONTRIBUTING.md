# Contribuindo

Obrigado por querer ajudar no Xfria. Issues e pull requests são bem-vindos.

## Antes de começar

- Para algo grande (um recurso novo, outro modelo de ar, uma mudança de comportamento), abra uma issue antes e conte a ideia. Assim a gente combina o caminho antes de você gastar tempo.
- Para correções pequenas (bug, texto, documentação), pode mandar a pull request direto.

## Como mandar uma mudança

1. Faça um fork do repositório e crie uma branch a partir da `main`.
2. Rode localmente seguindo a [Instalação](README.md#instalação) do README. Não precisa da placa: `bar/xfria simulate` finge ser o ESP32, e `/painel?demo` abre o painel com um ar simulado.
3. Antes de abrir a PR, rode `npm run build:web` em `app/` e, se mexeu no firmware, compile com `arduino-cli compile --profile esp32 .` em `firmware/`.
4. Abra a pull request explicando o que mudou e por quê. Se mexer na interface, coloque um print.

Toda PR passa pelo build automático e pela revisão do mantenedor antes de entrar na `main`.

## Estilo

- O código segue o que já existe ao redor: nomes claros, funções pequenas, comentários só onde o porquê não é óbvio.
- No firmware, cada arquivo tem uma responsabilidade (veja a tabela em [Estrutura](README.md#estrutura)).
- A interface é em português. Textos sem emojis.
- Nunca suba `firmware/secrets.h` nem credenciais do Adafruit IO.

## Licença

Ao contribuir, você concorda que sua contribuição fica sob a [licença MIT](LICENSE) do projeto.
