# FreeCAD MCP instalado neste notebook

Integração: https://github.com/neka-nat/freecad-mcp
Commit instalado: `8babe9927ce8e6e8fe7dd6ae2ffa2c93776e845a` (0.1.28).

- Complemento: `~/.local/share/FreeCAD/v1-1/Mod/FreeCADMCP`.
- Servidor e ambiente Python: `~/.local/share/freecad-mcp`.
- Registro no Codex: servidor `freecad` em `~/.codex/config.toml`.
- Comunicação com o aplicativo: somente `127.0.0.1:9875`.
- Inicialização automática do complemento habilitada ao abrir o FreeCAD.

O FreeCAD deve permanecer aberto. O MCP permite consultar e alterar o
modelo aberto; isso não é sincronização automática de arquivos alterados
externamente. As alterações são enviadas por comandos do assistente.

A conexão foi verificada por um cliente MCP: inicialização, descoberta de
17 ferramentas, listagem de documentos e execução de alterações no documento
V2 dentro da interface do FreeCAD. A sessão Codex que já estava aberta pode
precisar ser reiniciada para expor as novas ferramentas diretamente. O teste
foi realizado pelo cliente MCP via terminal nesta mesma sessão.

No FreeCAD, a bancada `MCP Addon` oferece os comandos de iniciar e parar o
servidor. Para desregistrar do Codex: `codex mcp remove freecad`.

Documentação do Codex: https://developers.openai.com/codex/mcp
