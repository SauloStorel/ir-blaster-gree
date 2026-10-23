use std::error::Error;
use std::fs;

use tauri::{App, Manager};
use tauri_plugin_autostart::ManagerExt;

// Na primeira vez que o app abre, ele passa a iniciar com o sistema (escondido, só no
// ícone da bandeja). Depois disso vale a opção "Iniciar com o sistema" do menu "•••".
pub fn enable_on_first_run(app: &App) -> Result<(), Box<dyn Error>> {
    let marker = app.path().app_config_dir()?.join("autostart-configured");
    if marker.exists() {
        return Ok(());
    }

    app.autolaunch().enable()?;
    fs::create_dir_all(marker.parent().expect("pasta de configuração"))?;
    fs::write(marker, "")?;
    Ok(())
}
