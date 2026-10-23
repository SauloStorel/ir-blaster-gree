import { defineConfig } from "vite"

// Porta fixa: o Tauri abre a janela apontando para ela no modo de desenvolvimento.
export default defineConfig({
  clearScreen: false,
  server: { port: 1420, strictPort: true },
})
