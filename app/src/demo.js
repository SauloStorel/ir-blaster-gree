// Ar simulado para a demonstração da apresentação (/painel?demo): responde como o ESP32,
// sem rede e sem conta do Adafruit.
const RESPONSE_MS = 350

const INITIAL_STATE = {
  power: true,
  mode: "cool",
  temp: 22,
  fan: "auto",
  airflow: "swing",
  sleep: false,
  eco: false,
  turbo: false,
  light: false,
}

export const loadCredentials = async () => ({})

export function connect(_credentials, listener) {
  let state = INITIAL_STATE
  listener.onConnection("connected")
  listener.onOnline(true)
  listener.onState(state)

  return {
    send(command) {
      setTimeout(() => {
        state = { ...state, ...command }
        listener.onState(state)
      }, RESPONSE_MS)
    },
    end() {},
  }
}
