// Sem janela de console no Windows.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod credentials;
mod panel;
#[cfg(not(target_os = "linux"))]
mod startup;
#[cfg(not(target_os = "linux"))]
mod tray;

fn main() {
    let builder = tauri::Builder::default()
        // Abrir o app de novo (ex.: pelo ícone da barra do Linux) mostra ou esconde o painel já aberto.
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| panel::toggle(app)))
        // Ao iniciar com o sistema, abre escondido.
        .plugin(tauri_plugin_autostart::Builder::new().args(["--hidden"]).build())
        .invoke_handler(tauri::generate_handler![
            credentials::load_credentials,
            credentials::save_credentials
        ])
        .setup(panel::setup);

    builder
        .run(tauri::generate_context!())
        .expect("erro ao iniciar o painel");
}
