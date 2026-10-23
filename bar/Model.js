.pragma library

var MIN_TEMP = 16
var MAX_TEMP = 30

var MODES = ["cool", "dry", "fan", "heat", "auto"]

var MODE_ICONS = {
  cool: String.fromCodePoint(0xF0717),  // floco de neve
  dry: String.fromCodePoint(0xF058C),   // gota
  fan: String.fromCodePoint(0xF0210),   // ventilador
  heat: String.fromCodePoint(0xF0238),  // fogo
  auto: String.fromCodePoint(0xF001B)   // ar-condicionado
}

var AC_ICON = MODE_ICONS.auto

var MODE_NAMES = { cool: "Frio", dry: "Seco", fan: "Ventilar", heat: "Quente", auto: "Automático" }
var FAN_NAMES = { auto: "automática", low: "baixa", medium: "média", high: "alta" }

var HINT = "Clique: liga/desliga · Rolar: temperatura · Botão direito: modo"

function clampTemp(temp) {
  return Math.max(MIN_TEMP, Math.min(MAX_TEMP, temp))
}

function nextMode(mode) {
  return MODES[(MODES.indexOf(mode) + 1) % MODES.length]
}

// O estado vem da rede: só aceita os campos e valores conhecidos.
function parseState(raw) {
  try {
    var data = JSON.parse(String(raw || ""))
    var valid = typeof data.power === "boolean"
      && MODES.indexOf(data.mode) !== -1
      && Number.isInteger(data.temp)
      && FAN_NAMES.hasOwnProperty(data.fan)
    return valid
      ? { power: data.power, mode: data.mode, temp: clampTemp(data.temp), fan: data.fan }
      : null
  } catch (e) {
    return null
  }
}

function label(state, online, temp) {
  if (!online || !state || !state.power) return AC_ICON
  return MODE_ICONS[state.mode] + " " + temp + "°"
}

function tooltip(state, online) {
  if (!online || !state) return "Ar-condicionado offline"
  if (!state.power) return "Ar-condicionado desligado\n" + HINT
  return MODE_NAMES[state.mode] + " · " + state.temp + " °C · ventilação " + FAN_NAMES[state.fan] + "\n" + HINT
}
