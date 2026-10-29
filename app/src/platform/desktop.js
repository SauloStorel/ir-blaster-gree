import { invoke } from "@tauri-apps/api/core"
import { getCurrentWindow } from "@tauri-apps/api/window"
import { disable, enable, isEnabled } from "@tauri-apps/plugin-autostart"

// Painel do computador (Tauri): credenciais no mesmo arquivo do script xfria.
export const loadCredentials = () => invoke("load_credentials")
export const saveCredentials = (credentials) => invoke("save_credentials", { credentials })
export const hide = () => getCurrentWindow().hide()

// Opção "Iniciar com o sistema" do menu "•••".
export async function setupStartupToggle(input) {
  input.checked = await isEnabled()
  input.addEventListener("change", () => (input.checked ? enable() : disable()))
}
