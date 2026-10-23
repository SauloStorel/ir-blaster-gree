import { ChevronDown, ShieldCheck, WifiOff, createElement } from "lucide"

import { CHOICES, MAX_TEMP, MIN_TEMP, SLEEP, TILE_ORDER } from "./options.js"
import { clampTemp } from "./state.js"

// Espera a pessoa parar de ajustar antes de enviar: o plano grátis aceita 30 mensagens por minuto.
const TEMP_SEND_DELAY_MS = 600

const STATUS = {
  connecting: { text: "Conectando…", icon: WifiOff },
  disconnected: { text: "Sem conexão com a internet", icon: WifiOff },
  unauthorized: { text: "Usuário ou chave do Adafruit inválidos", icon: WifiOff },
  offline: { text: "ESP32 offline", icon: WifiOff },
  ready: { text: "Conectado", icon: ShieldCheck },
}

function element(tag, className, children = []) {
  const node = document.createElement(tag)
  node.className = className
  node.append(...children)
  return node
}

function controlButton(className) {
  const button = element("button", className)
  button.type = "button"
  button.dataset.control = ""
  return button
}

export function createPanel(root, { onOpenSettings }) {
  let acState = null
  let online = false
  let connection = "connecting"
  let send = () => {}
  let pendingTemp = null
  let tempTimer = null

  const $ = (selector) => root.querySelector(selector)
  const ready = () => connection === "connected" && online && acState !== null
  const shownTemp = () => pendingTemp ?? acState?.temp

  function statusKey() {
    if (connection !== "connected") return connection
    return online ? "ready" : "offline"
  }

  function change(patch) {
    if (!ready()) return
    acState = { ...acState, ...patch } // otimista: o estado confirmado pelo ESP32 chega em seguida
    send(patch)
    render()
  }

  function stepTemp(temp) {
    if (!ready()) return
    pendingTemp = clampTemp(temp)
    render()
    clearTimeout(tempTimer)
    tempTimer = setTimeout(() => {
      change({ temp: pendingTemp })
      pendingTemp = null
    }, TEMP_SEND_DELAY_MS)
  }

  function closeMenus() {
    root.querySelectorAll(".menu").forEach((menu) => (menu.hidden = true))
  }

  function choiceTile(field) {
    const choice = CHOICES[field]
    const button = controlButton("tile")
    const items = choice.options.map((option) => {
      const item = controlButton("menu-item")
      item.append(option.name)
      item.setAttribute("role", "menuitemradio")
      item.addEventListener("click", () => {
        closeMenus()
        change({ [field]: option.value })
      })
      return { item, option }
    })
    const menu = element("div", "menu", items.map(({ item }) => item))
    menu.setAttribute("role", "menu")
    menu.hidden = true

    button.setAttribute("aria-haspopup", "menu")
    button.addEventListener("click", (event) => {
      event.stopPropagation()
      const opening = menu.hidden
      closeMenus()
      menu.hidden = !opening
    })

    return {
      node: element("div", "tile-wrap", [button, menu]),
      render() {
        const selected = choice.options.find((option) => option.value === acState?.[field])
        button.replaceChildren(
          element("span", "tile-icon", [createElement(selected?.icon ?? choice.icon ?? choice.options[0].icon)]),
          element("span", "tile-corner", [createElement(ChevronDown)]),
          element("span", "tile-label", [choice.label]),
          element("span", "tile-value", [selected?.name ?? "—"]),
        )
        items.forEach(({ item, option }) => item.setAttribute("aria-checked", option === selected))
      },
    }
  }

  function sleepTile() {
    const button = controlButton("tile")
    button.addEventListener("click", () => change({ sleep: !acState.sleep }))

    return {
      node: button,
      render() {
        const on = Boolean(acState?.sleep)
        button.setAttribute("aria-pressed", on)
        button.replaceChildren(
          element("span", "tile-icon", [createElement(SLEEP.icon)]),
          element("span", "tile-corner dot"),
          element("span", "tile-label", [SLEEP.label]),
          element("span", "tile-value", [on ? "Ativo" : "Inativo"]),
        )
      },
    }
  }

  const TILE_BUILDERS = { sleep: sleepTile }
  const tiles = TILE_ORDER.map((field) => (TILE_BUILDERS[field] ?? choiceTile)(field))
  $(".tiles").append(...tiles.map((tile) => tile.node))

  $("#power").addEventListener("click", () => change({ power: !acState.power }))
  $("#eco").addEventListener("change", (event) => change({ eco: event.target.checked }))
  $("#minus").addEventListener("click", () => stepTemp(shownTemp() - 1))
  $("#plus").addEventListener("click", () => stepTemp(shownTemp() + 1))
  $("#slider").addEventListener("input", (event) => stepTemp(Number(event.target.value)))
  $("#open-settings").addEventListener("click", onOpenSettings)
  document.addEventListener("click", closeMenus)

  function render() {
    const temp = shownTemp() ?? MIN_TEMP
    const status = STATUS[statusKey()]

    root.dataset.power = acState?.power ? "on" : "off"
    root.dataset.mode = acState?.mode ?? "cool"
    root.dataset.ready = ready()
    root.querySelectorAll("[data-control]").forEach((control) => (control.disabled = !ready()))

    $("#temp").textContent = acState ? temp : "--"
    $("#slider").value = temp
    $("#slider").style.setProperty("--fill", `${((temp - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)) * 100}%`)
    $("#eco").checked = Boolean(acState?.eco)
    $("#status").replaceChildren(createElement(status.icon), status.text)
    tiles.forEach((tile) => tile.render())
  }

  render()

  return {
    setSender(sender) {
      send = sender
    },
    closeMenus,
    onState(next) {
      acState = next ?? acState
      render()
    },
    onOnline(value) {
      online = value
      render()
    },
    onConnection(status) {
      connection = status
      render()
    },
  }
}
