import { disable, enable, isEnabled } from "@tauri-apps/plugin-autostart"

// Opção "Iniciar com o sistema" do menu "•••".
export async function setupStartupToggle(input) {
  input.checked = await isEnabled()
  input.addEventListener("change", () => (input.checked ? enable() : disable()))
}
