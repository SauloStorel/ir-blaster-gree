import { ChevronDown, createElement } from "lucide"

import { CHOICES, FIXED_AIRFLOWS, MAX_TEMP, MIN_TEMP } from "./options.js"
import { clampTemp } from "./state.js"

// Espera a pessoa parar de ajustar antes de enviar: o plano grátis aceita 30 mensagens por minuto.
const TEMP_SEND_DELAY_MS = 600

// Opções liga/desliga do menu "•••"; cada uma tem um <input id> com o mesmo nome do campo.
const SWITCHES = ["turbo", "sleep", "eco"]

// Texto embaixo da temperatura: o slogan quando está tudo certo, o problema quando não está.
const TAGLINES = {
  connecting: "Conectando…",
  disconnected: "Sem conexão com a internet",
  unauthorized: "Usuário ou chave do Adafruit inválidos",
  offline: "ESP32 offline",
  ready: "Do jeito certo.",
}

function element(tag, className, children = []) {
  const node = document.createElement(tag)
  node.className = className
  node.append(...children)
  return node
}

function controlButton(className, children = []) {
  const button = element("button", className, children)
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
  // Posição para onde a aleta volta quando o oscilar é desligado.
  let fixedAirflow = FIXED_AIRFLOWS[1].value

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

  function toggleMenu(menu) {
    const opening = menu.hidden
    closeMenus()
    menu.hidden = !opening
  }

  function choiceControl(container) {
    const field = container.dataset.field
    const choice = CHOICES[field]
    const button = controlButton("choice-button")
    const items = choice.options.map((option) => {
      const item = controlButton("menu-item", [option.name])
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
    button.setAttribute("aria-label", choice.label)
    button.addEventListener("click", (event) => {
      event.stopPropagation()
      toggleMenu(menu)
    })
    container.append(button, menu)

    return () => {
      const selected = choice.options.find((option) => option.value === acState?.[field])
      button.replaceChildren(
        createElement(selected?.icon ?? choice.icon ?? choice.options[0].icon),
        element("span", "choice-value", [selected?.name ?? "—"]),
        element("span", "chevron", [createElement(ChevronDown)]),
      )
      items.forEach(({ item, option }) => item.setAttribute("aria-checked", option === selected))
    }
  }

  function airflowControl(container) {
    const buttons = FIXED_AIRFLOWS.map((option) => {
      const button = controlButton("segment", [option.name])
      button.addEventListener("click", () => change({ airflow: option.value }))
      return { button, option }
    })
    container.append(...buttons.map(({ button }) => button))

    return () =>
      buttons.forEach(({ button, option }) => button.setAttribute("aria-pressed", acState?.airflow === option.value))
  }

  const renderers = [
    ...[...root.querySelectorAll(".choice")].map(choiceControl),
    airflowControl($("#airflow")),
  ]

  $("#power").addEventListener("click", () => change({ power: !acState.power }))
  $("#minus").addEventListener("click", () => stepTemp(shownTemp() - 1))
  $("#plus").addEventListener("click", () => stepTemp(shownTemp() + 1))
  $("#slider").addEventListener("input", (event) => stepTemp(Number(event.target.value)))
  $("#swing").addEventListener("click", () => {
    const swinging = acState.airflow === "swing"
    change({ airflow: swinging ? fixedAirflow : "swing" })
  })
  SWITCHES.forEach((field) => $(`#${field}`).addEventListener("change", (event) => change({ [field]: event.target.checked })))
  $("#more").addEventListener("click", (event) => {
    event.stopPropagation()
    toggleMenu($("#more-menu"))
  })
  $("#more-menu").addEventListener("click", (event) => event.stopPropagation())
  $("#open-settings").addEventListener("click", () => {
    closeMenus()
    onOpenSettings()
  })
  document.addEventListener("click", closeMenus)

  function render() {
    const temp = shownTemp() ?? MIN_TEMP
    const airflow = acState?.airflow

    if (airflow && airflow !== "swing") fixedAirflow = airflow

    root.dataset.power = acState?.power ? "on" : "off"
    root.dataset.status = statusKey()
    root.dataset.airflow = airflow ?? "middle"
    root.querySelectorAll("[data-control]").forEach((control) => (control.disabled = !ready()))

    $("#temp").textContent = acState ? temp : "--"
    $("#tagline").textContent = TAGLINES[statusKey()]
    $("#slider").value = temp
    $("#slider").style.setProperty("--fill", `${((temp - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)) * 100}%`)
    $("#swing").setAttribute("aria-pressed", airflow === "swing")
    SWITCHES.forEach((field) => ($(`#${field}`).checked = Boolean(acState?.[field])))
    renderers.forEach((render) => render())
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
