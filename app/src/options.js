import { AirVent, Droplet, Fan, Flame, Leaf, Moon, Snowflake, Zap } from "lucide"

export const MIN_TEMP = 16
export const MAX_TEMP = 30

// Escolhas com menu. O ícone da opção, quando existe, substitui o da escolha
// (o modo muda de ícone; a ventilação não).
export const CHOICES = {
  mode: {
    label: "Modo",
    options: [
      { value: "cool", name: "Frio", icon: Snowflake },
      { value: "dry", name: "Seco", icon: Droplet },
      { value: "fan", name: "Ventilar", icon: Fan },
      { value: "heat", name: "Quente", icon: Flame },
      { value: "auto", name: "Automático", icon: AirVent },
    ],
  },
  fan: {
    label: "Ventilação",
    icon: Fan,
    options: [
      { value: "auto", name: "Auto" },
      { value: "low", name: "Baixa" },
      { value: "medium", name: "Média" },
      { value: "high", name: "Alta" },
    ],
  },
  airflow: {
    label: "Aleta",
    options: [
      { value: "swing", name: "Oscilar" },
      { value: "up", name: "Cima" },
      { value: "middle", name: "Meio" },
      { value: "down", name: "Baixo" },
    ],
  },
}

// Posições fixas da aleta, usadas quando o oscilar está desligado.
export const FIXED_AIRFLOWS = CHOICES.airflow.options.filter((option) => option.value !== "swing")

// Extras liga/desliga: ficam no menu "•••" (um <input id> com o nome do campo) e,
// quando ativos, aparecem como etiquetas embaixo da temperatura.
export const EXTRAS = [
  { field: "turbo", name: "Turbo", icon: Zap },
  { field: "sleep", name: "Sono", icon: Moon },
  { field: "eco", name: "Eco", icon: Leaf },
]
