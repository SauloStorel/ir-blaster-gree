import mqtt from "mqtt"

import { parseState } from "./state.js"

const BROKER_URL = "wss://io.adafruit.com:443/mqtt"
const DEVICE = "ar-quarto"

// Códigos de recusa do broker para usuário ou chave errados.
const AUTH_ERROR_CODES = [4, 5]

// Liga o painel ao Adafruit IO. `listener` recebe onState, onOnline e onConnection.
export function connect({ username, key }, listener) {
  const feed = (name) => `${username}/feeds/${DEVICE}-${name}`
  const client = mqtt.connect(BROKER_URL, { username, password: key, reconnectPeriod: 5000 })

  const routes = {
    [feed("state")]: (text) => listener.onState(parseState(text)),
    [feed("online")]: (text) => listener.onOnline(text === "online"),
  }

  listener.onConnection("connecting")

  client.on("connect", () => {
    listener.onConnection("connected")
    client.subscribe(Object.keys(routes), () => {
      // O Adafruit IO não tem retain: o /get devolve o último valor para esta conexão.
      Object.keys(routes).forEach((topic) => client.publish(`${topic}/get`, ""))
    })
  })

  client.on("message", (topic, payload) => routes[topic]?.(payload.toString()))
  client.on("offline", () => listener.onConnection("disconnected"))
  client.on("error", (error) => {
    if (!AUTH_ERROR_CODES.includes(error.code)) return
    listener.onConnection("unauthorized")
    client.end()
  })

  return {
    send: (command) => client.publish(feed("set"), JSON.stringify(command)),
    end: () => client.end(true),
  }
}
