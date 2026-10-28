import { fileURLToPath } from "node:url"
import { defineConfig } from "vite"

// O modo "web" gera a versão para o celular (PWA), sem o Tauri; os outros, o painel do computador.
export default defineConfig(({ mode }) => {
  const platform = mode === "web" ? "web" : "desktop"

  return {
    clearScreen: false,
    // Porta fixa: o Tauri abre a janela apontando para ela no modo de desenvolvimento.
    server: { port: 1420, strictPort: true },
    resolve: {
      alias: { "#platform": fileURLToPath(new URL(`src/platform/${platform}.js`, import.meta.url)) },
    },
    build: { outDir: platform === "web" ? "dist-web" : "dist" },
  }
})
