import { fileURLToPath } from "node:url"
import { defineConfig } from "vite"

const path = (file) => fileURLToPath(new URL(file, import.meta.url))

// O modo "web" gera o site: a apresentação (index.html) e o painel para o celular (PWA), sem o Tauri.
// Os outros modos geram só o painel do computador.
export default defineConfig(({ mode }) => {
  const platform = mode === "web" ? "web" : "desktop"
  const pages = { web: { site: path("index.html"), painel: path("painel.html") }, desktop: { painel: path("painel.html") } }

  return {
    clearScreen: false,
    // Porta fixa: o Tauri abre a janela apontando para ela no modo de desenvolvimento.
    server: { port: 1420, strictPort: true },
    resolve: { alias: { "#platform": path(`src/platform/${platform}.js`) } },
    build: { outDir: platform === "web" ? "dist-web" : "dist", rollupOptions: { input: pages[platform] } },
  }
})
