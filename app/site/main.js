import "@fontsource-variable/inter"
import "./site.css"

import {
  ArrowRight,
  Check,
  Cloud,
  Cpu,
  Fan,
  Globe,
  History,
  Moon,
  RotateCcwSquare,
  SlidersHorizontal,
  Snowflake,
  Thermometer,
  createElement,
} from "lucide"

import { parallax } from "./parallax.js"

const ICONS = {
  arrow: ArrowRight,
  check: Check,
  cloud: Cloud,
  remote: Cpu,
  fan: Fan,
  globe: Globe,
  history: History,
  moon: Moon,
  swing: RotateCcwSquare,
  sliders: SlidersHorizontal,
  snowflake: Snowflake,
  thermometer: Thermometer,
}

document.querySelectorAll("[data-icon]").forEach((slot) => slot.append(createElement(ICONS[slot.dataset.icon])))

// A barra do topo ganha uma linha quando a página sai do início.
const topbar = document.querySelector(".topbar")
const markScrolled = () => topbar.toggleAttribute("data-scrolled", scrollY > 8)
addEventListener("scroll", markScrolled, { passive: true })
markScrolled()

// Movimento é extra: some para quem pediu menos movimento, e o que segue o mouse só vale com mouse.
const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches
const finePointer = matchMedia("(pointer: fine)").matches

if (!reduceMotion && finePointer) parallax(document.querySelector(".hero"))
