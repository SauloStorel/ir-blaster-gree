// Sem janela de console no Windows.
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod credentials;
mod panel;
#[cfg(not(target_os = "linux"))]
mod tray;

fn main() {
    let builder = tauri::Builder::default()
        // Abrir o app de novo (ex.: pelo ícone da barra do Linux) mostra ou esconde o painel já aberto.
        .plugin(tauri_plugin_single_instance::init(|app, _args, _cwd| panel::toggle(app)))
        .invoke_handler(tauri::generate_handler![
            credentials::load_credentials,
            credentials::save_credentials
        ])
        .setup(panel::setup);

    #[cfg(not(target_os = "linux"))]
    let builder = builder.plugin(tauri_plugin_positioner::init());

    builder
        .run(tauri::generate_context!())
        .expect("erro ao iniciar o painel");
}
