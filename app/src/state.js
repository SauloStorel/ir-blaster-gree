import { CHOICES, MAX_TEMP, MIN_TEMP } from "./options.js"

export const clampTemp = (temp) => Math.min(MAX_TEMP, Math.max(MIN_TEMP, temp))

const isOption = (field, value) => CHOICES[field].options.some((option) => option.value === value)

// O estado vem da rede: só aceita os campos e valores conhecidos.
export function parseState(text) {
  try {
    const data = JSON.parse(text)
    const valid =
      typeof data.power === "boolean" &&
      Number.isInteger(data.temp) &&
      typeof data.sleep === "boolean" &&
      typeof data.eco === "boolean" &&
      Object.keys(CHOICES).every((field) => isOption(field, data[field]))

    const { power, mode, fan, airflow, sleep, eco } = data
    return valid ? { power, mode, fan, airflow, sleep, eco, temp: clampTemp(data.temp) } : null
  } catch {
    return null
  }
}
