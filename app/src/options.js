import { AirVent, Droplet, Fan, Flame, Snowflake } from "lucide"

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
