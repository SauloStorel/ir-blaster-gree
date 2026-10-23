import { AirVent, Droplet, Fan, Flame, Moon, Snowflake, Wind } from "lucide"

export const MIN_TEMP = 16
export const MAX_TEMP = 30

// Escolhas com menu, na ordem em que aparecem. O ícone da opção, quando existe,
// substitui o do bloco (o modo muda de ícone; ventilação e aleta não).
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
    icon: Wind,
    options: [
      { value: "swing", name: "Oscilar" },
      { value: "up", name: "Cima" },
      { value: "middle", name: "Meio" },
      { value: "down", name: "Baixo" },
    ],
  },
}

export const SLEEP = { label: "Sono", icon: Moon }

export const TILE_ORDER = ["mode", "fan", "sleep", "airflow"]
