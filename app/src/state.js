import { CHOICES, MAX_TEMP, MIN_TEMP } from "./options.js"

export const clampTemp = (temp) => Math.min(MAX_TEMP, Math.max(MIN_TEMP, temp))

const isOption = (field, value) => CHOICES[field].options.some((option) => option.value === value)

const BOOLEANS = ["power", "sleep", "eco", "turbo", "light"]
// Campos que um firmware mais antigo ainda não manda.
const DEFAULTS = { light: false }

// O estado vem da rede: só aceita os campos e valores conhecidos.
export function parseState(text) {
  try {
    const data = { ...DEFAULTS, ...JSON.parse(text) }
    const valid =
      Number.isInteger(data.temp) &&
      BOOLEANS.every((field) => typeof data[field] === "boolean") &&
      Object.keys(CHOICES).every((field) => isOption(field, data[field]))

    const { power, mode, fan, airflow, sleep, eco, turbo, light } = data
    return valid ? { power, mode, fan, airflow, sleep, eco, turbo, light, temp: clampTemp(data.temp) } : null
  } catch {
    return null
  }
}
