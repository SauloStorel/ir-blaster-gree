import { ChevronDown, createElement } from "lucide"

import { CHOICES, EXTRAS, FIXED_AIRFLOWS, MAX_TEMP, MIN_TEMP } from "./options.js"
import { createRollingNumber } from "./rolling.js"
import { clampTemp } from "./state.js"

// Espera a pessoa parar de ajustar antes de enviar: o plano grátis aceita 30 mensagens por minuto.
const TEMP_SEND_DELAY_MS = 600
// Sem confirmação do ESP32 nesse tempo, o painel volta ao último estado confirmado.
const CONFIRM_TIMEOUT_MS = 5000
const NOTICE_MS = 3500
// Quanto de rolagem do mouse ou do trackpad vale um grau.
const WHEEL_STEP = 40

const KEY_STEPS = { ArrowUp: 1, ArrowRight: 1, ArrowDown: -1, ArrowLeft: -1 }

const STATUS_TAGLINES = {
  connecting: "Conectando…",
  disconnected: "Sem conexão com a internet",
  unauthorized: "Usuário ou chave do Adafruit inválidos",
  offline: "ESP32 offline",
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
  // O último estado publicado pelo ESP32 e o que o painel mostra (com as mudanças ainda não confirmadas).
  let confirmed = null
  let acState = null
  let waiting = false
  let online = false
  let connection = "connecting"
  let send = () => {}
  let pendingTemp = null
  let notice = null
  let wheelDelta = 0
  // Posição para onde a aleta volta quando o oscilar é desligado.
  let fixedAirflow = FIXED_AIRFLOWS[1].value
  const timers = {}

  const $ = (selector) => root.querySelector(selector)
  const ready = () => connection === "connected" && online && acState !== null
  const shownTemp = () => pendingTemp ?? acState?.temp
  const showTemp = createRollingNumber($("#temp"))

  function restartTimer(name, delay, callback) {
    clearTimeout(timers[name])
    timers[name] = setTimeout(callback, delay)
  }

  function statusKey() {
    if (connection !== "connected") return connection
    return online ? "ready" : "offline"
  }

  function tagline() {
    const status = statusKey()
    if (status !== "ready") return STATUS_TAGLINES[status]
    if (notice) return notice
    return acState?.power ? "Do jeito certo." : "Desligado"
  }

  function showNotice(text) {
    notice = text
    restartTimer("notice", NOTICE_MS, () => {
      notice = null
      render()
    })
  }

  function change(patch) {
    if (!ready()) return
    acState = { ...acState, ...patch } // otimista: o estado confirmado pelo ESP32 chega em seguida
    send(patch)
    waiting = true
    restartTimer("confirm", CONFIRM_TIMEOUT_MS, () => {
      acState = confirmed
      waiting = false
      showNotice("O ar não respondeu")
      render()
    })
    render()
  }

  function stepTemp(temp) {
    if (!ready()) return
    pendingTemp = clampTemp(temp)
    render()
    restartTimer("temp", TEMP_SEND_DELAY_MS, () => {
      change({ temp: pendingTemp })
      pendingTemp = null
    })
  }

  function togglePower() {
    change({ power: !acState?.power })
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

  // Etiquetas dos extras ativos; clicar numa delas desliga o extra.
  function extrasControl(container) {
    const chips = EXTRAS.map((extra) => {
      const chip = controlButton("chip", [createElement(extra.icon), extra.name])
      chip.title = `Desligar ${extra.name.toLowerCase()}`
      chip.addEventListener("click", () => change({ [extra.field]: false }))
      return { chip, extra }
    })
    container.append(...chips.map(({ chip }) => chip))

    return () => chips.forEach(({ chip, extra }) => (chip.hidden = !acState?.[extra.field]))
  }

  function onWheel(event) {
    event.preventDefault()
    wheelDelta += event.deltaY
    if (Math.abs(wheelDelta) < WHEEL_STEP) return
    stepTemp(shownTemp() + (wheelDelta < 0 ? 1 : -1))
    wheelDelta = 0
  }

  const renderers = [
    ...[...root.querySelectorAll(".choice")].map(choiceControl),
    airflowControl($("#airflow")),
    extrasControl($("#extras")),
  ]

  $("#power").addEventListener("click", togglePower)
  $(".unit").addEventListener("click", togglePower)
  $("#minus").addEventListener("click", () => stepTemp(shownTemp() - 1))
  $("#plus").addEventListener("click", () => stepTemp(shownTemp() + 1))
  $("#slider").addEventListener("input", (event) => stepTemp(Number(event.target.value)))
  for (const area of [$(".hero"), $(".adjust")]) area.addEventListener("wheel", onWheel, { passive: false })
  $("#swing").addEventListener("click", () => {
    const swinging = acState.airflow === "swing"
    change({ airflow: swinging ? fixedAirflow : "swing" })
  })
  for (const { field } of EXTRAS) {
    $(`#${field}`).addEventListener("change", (event) => change({ [field]: event.target.checked }))
  }
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
  document.addEventListener("keydown", (event) => {
    // Teclas sobre botões e campos mantêm o comportamento padrão.
    if (event.target !== document.body) return
    const step = KEY_STEPS[event.key]
    if (step) stepTemp(shownTemp() + step)
    if (event.key === " ") togglePower()
  })

  function render() {
    const temp = shownTemp() ?? MIN_TEMP
    const airflow = acState?.airflow
    const status = statusKey()

    if (airflow && airflow !== "swing") fixedAirflow = airflow

    Object.assign(root.dataset, {
      power: acState?.power ? "on" : "off",
      status,
      mode: acState?.mode ?? "cool",
      // O turbo sopra mais forte que qualquer velocidade.
      fan: acState?.turbo ? "turbo" : (acState?.fan ?? "auto"),
      airflow: airflow ?? "middle",
      waiting,
      alert: status !== "ready" || notice !== null,
    })
    root.querySelectorAll("[data-control]").forEach((control) => (control.disabled = !ready()))

    showTemp(acState ? temp : "--")
    $("#tagline").textContent = tagline()
    $("#slider").value = temp
    $("#slider").style.setProperty("--fill", `${((temp - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)) * 100}%`)
    $("#swing").setAttribute("aria-pressed", airflow === "swing")
    for (const { field } of EXTRAS) $(`#${field}`).checked = Boolean(acState?.[field])
    renderers.forEach((render) => render())
  }

  render()

  return {
    setSender(sender) {
      send = sender
    },
    closeMenus,
    onState(next) {
      if (!next) return
      confirmed = next
      acState = next
      waiting = false
      clearTimeout(timers.confirm)
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
