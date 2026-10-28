const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)")
// Mesma duração das animações enter-*/leave-* do style.css (--duration).
const ROLL_MS = 240

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

    // Sobras de uma troca anterior ainda em andamento saem já, para não empilhar números.
    const previous = container.lastElementChild
    for (const stale of [...container.children].slice(0, -1)) stale.remove()
    previous?.classList.add(`leave-${direction}`)
    // Timer em vez de animationend: com a janela oculta ou minimizada o evento pode nunca chegar.
    setTimeout(() => previous?.remove(), ROLL_MS)
    next.classList.add(`enter-${direction}`)
    container.append(next)
  }
}
