import { AirVent, Droplet, Fan, Flame, Snowflake } from "lucide"

export const MIN_TEMP = 16
export const MAX_TEMP = 30

// Escolhas com menu. O ícone da opção, quando existe, substitui o da escolha
// (o modo muda de ícone; a ventilação não).
export const CHOICES = {
  mode: {
    label: "Modo",
    options: [
      { value: "cool", name: "frio", icon: Snowflake },
      { value: "dry", name: "seco", icon: Droplet },
      { value: "fan", name: "ventilar", icon: Fan },
      { value: "heat", name: "quente", icon: Flame },
      { value: "auto", name: "automático", icon: AirVent },
    ],
  },
  fan: {
    label: "Ventilação",
    icon: Fan,
    options: [
      { value: "auto", name: "auto" },
      { value: "low", name: "baixa" },
      { value: "medium", name: "média" },
      { value: "high", name: "alta" },
    ],
  },
  airflow: {
    label: "Aleta",
    options: [
      { value: "swing", name: "oscilar" },
      { value: "up", name: "cima" },
      { value: "middle", name: "meio" },
      { value: "down", name: "baixo" },
    ],
  },
}

// Posições fixas da aleta, usadas quando o oscilar está desligado.
export const FIXED_AIRFLOWS = CHOICES.airflow.options.filter((option) => option.value !== "swing")
