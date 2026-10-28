import "../web.css"

// Versão para o celular (PWA): as credenciais ficam só neste navegador.
const STORAGE_KEY = "xfria:credentials"

export function loadCredentials() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY))
  } catch {
    return null
  }
}

export function saveCredentials(credentials) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(credentials))
}

// No navegador não há janela para esconder nem sistema para iniciar junto.
export const hide = () => {}

export function setupStartupToggle(input) {
  input.closest(".menu-row").hidden = true
}
