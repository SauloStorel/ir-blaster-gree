const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)")

function directionOf(from, to) {
  if (typeof from !== "number" || typeof to !== "number") return null
  return to > from ? "up" : "down"
}

// Troca o número rolando: o novo entra por baixo quando sobe e por cima quando desce.
export function createRollingNumber(container) {
  let current = null

  return function show(value) {
    if (value === current) return
    const direction = reducedMotion.matches ? null : directionOf(current, value)
    current = value

    const next = document.createElement("span")
    next.textContent = value
    if (!direction) {
      container.replaceChildren(next)
      return
    }

    const previous = container.lastElementChild
    previous?.classList.add(`leave-${direction}`)
    previous?.addEventListener("animationend", () => previous.remove(), { once: true })
    next.classList.add(`enter-${direction}`)
    container.append(next)
  }
}
