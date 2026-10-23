import "@fontsource-variable/inter"
import "./style.css"

import { invoke } from "@tauri-apps/api/core"
import { getCurrentWindow } from "@tauri-apps/api/window"
import { Ellipsis, Minus, Plus, Power, RotateCcwSquare, createElement } from "lucide"

import { connect } from "./connection.js"
import { createPanel } from "./panel.js"
import { createSettings } from "./settings.js"
import { setupStartupToggle } from "./startup.js"

const STATIC_ICONS = { power: Power, minus: Minus, plus: Plus, swing: RotateCcwSquare, more: Ellipsis }

document.querySelectorAll("[data-icon]").forEach((slot) => slot.append(createElement(STATIC_ICONS[slot.dataset.icon])))

const views = { panel: document.querySelector("#panel"), settings: document.querySelector("#settings") }
const show = (name) => Object.entries(views).forEach(([view, node]) => (node.hidden = view !== name))

let credentials = null
let connection = null

function start() {
  connection?.end()
  connection = connect(credentials, panel)
  panel.setSender(connection.send)
  show("panel")
}

function openSettings() {
  settings.fill(credentials, { canCancel: credentials !== null })
  show("settings")
}

const panel = createPanel(views.panel, { onOpenSettings: openSettings })

const settings = createSettings(views.settings, {
  async onSave(next) {
    await invoke("save_credentials", { credentials: next })
    credentials = next
    start()
  },
  onCancel: () => show("panel"),
})

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return
  panel.closeMenus()
  getCurrentWindow().hide()
})

async function main() {
  setupStartupToggle(document.querySelector("#autostart"))
  credentials = await invoke("load_credentials")
  if (credentials) start()
  else openSettings()
}

main()
