// Tela para informar o usuário e a Active Key do Adafruit IO.
export function createSettings(root, { onSave, onCancel }) {
  const form = root.querySelector("form")

  form.addEventListener("submit", (event) => {
    event.preventDefault()
    onSave({ username: form.username.value.trim(), key: form.key.value.trim() })
  })
  root.querySelector("#cancel").addEventListener("click", onCancel)

  return {
    fill(credentials, { canCancel }) {
      form.username.value = credentials?.username ?? ""
      form.key.value = credentials?.key ?? ""
      root.querySelector("#cancel").hidden = !canCancel
    },
  }
}
