import QtQuick
import Quickshell
import Quickshell.Io
import qs.Commons
import qs.Ui
import "Model.js" as Model

BarWidget {
  id: root
  moduleName: "storell.ar-gree"

  readonly property string cli: Qt.resolvedUrl("ar-gree").toString().replace(/^file:\/\//, "")
  // App do painel (~/ir-blaster-gree/app); abrir de novo mostra ou esconde a janela.
  readonly property string panelApp: Quickshell.env("HOME") + "/.local/bin/ar-gree-panel"

  property var acState: null
  property bool online: false
  // Temperatura escolhida na rolagem, ainda não enviada (null = nenhuma).
  property var pendingTemp: null

  readonly property bool controllable: online && acState !== null
  readonly property int shownTemp: pendingTemp !== null ? pendingTemp : (acState ? acState.temp : 0)

  function send(command) {
    Quickshell.execDetached([root.cli, "send", JSON.stringify(command)])
  }

  function handleLine(line) {
    var text = String(line)
    var space = text.indexOf(" ")
    var feed = text.slice(0, space)
    var payload = text.slice(space + 1)

    if (feed === "online") root.online = payload === "online"
    if (feed === "state") root.acState = Model.parseState(payload) || root.acState
  }

  function togglePower() {
    if (root.controllable) root.send({ power: !root.acState.power })
  }

  function togglePanel() {
    Quickshell.execDetached([root.panelApp])
  }

  function stepTemp(delta) {
    if (!root.controllable || !root.acState.power) return
    root.pendingTemp = Model.clampTemp(root.shownTemp + (delta > 0 ? 1 : -1))
    tempDebounce.restart()
  }

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  Process {
    id: watchProc
    command: [root.cli, "watch"]
    running: true
    stdout: SplitParser { onRead: function(line) { root.handleLine(line) } }
    onExited: {
      root.online = false
      reconnect.start()
    }
  }

  Timer {
    id: reconnect
    interval: 10000
    onTriggered: watchProc.running = true
  }

  // Junta vários passos da rolagem num só comando: o plano grátis aceita 30 mensagens por minuto.
  Timer {
    id: tempDebounce
    interval: 700
    onTriggered: {
      root.send({ temp: root.pendingTemp })
      root.pendingTemp = null
    }
  }

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: Model.label(root.acState, root.online, root.shownTemp)
    dimmed: !root.controllable
    tooltipText: Model.tooltip(root.acState, root.online)

    onPressed: function(b) {
      if (b === Qt.RightButton) root.togglePower()
      else root.togglePanel()
    }
    onWheelMoved: function(delta) { root.stepTemp(delta) }
  }
}
