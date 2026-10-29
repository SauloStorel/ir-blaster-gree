use std::fs;
use std::path::PathBuf;

use serde::{Deserialize, Serialize};
use tauri::{AppHandle, Manager};

#[derive(Serialize, Deserialize)]
pub struct Credentials {
    username: String,
    key: String,
}

// O mesmo arquivo do script xfria: ~/.config/xfria/credentials no Linux,
// %APPDATA%\xfria\credentials no Windows.
fn path(app: &AppHandle) -> tauri::Result<PathBuf> {
    Ok(app.path().config_dir()?.join("xfria").join("credentials"))
}

#[tauri::command]
pub fn load_credentials(app: AppHandle) -> Option<Credentials> {
    let text = fs::read_to_string(path(&app).ok()?).ok()?;
    let value = |name: &str| {
        text.lines()
            .find_map(|line| line.strip_prefix(name)?.strip_prefix('='))
            .map(str::to_owned)
    };

    Some(Credentials { username: value("AIO_USERNAME")?, key: value("AIO_KEY")? })
}

#[tauri::command]
pub fn save_credentials(app: AppHandle, credentials: Credentials) -> Result<(), String> {
    let Credentials { username, key } = &credentials;
    if username.contains('\n') || key.contains('\n') {
        return Err("usuário e chave não podem ter quebra de linha".into());
    }

    let path = path(&app).map_err(|error| error.to_string())?;
    let write = || -> std::io::Result<()> {
        fs::create_dir_all(path.parent().expect("pasta do arquivo"))?;
        fs::write(&path, format!("AIO_USERNAME={username}\nAIO_KEY={key}\n"))?;
        restrict_to_owner(&path)
    };
    write().map_err(|error| error.to_string())
}

#[cfg(unix)]
fn restrict_to_owner(path: &PathBuf) -> std::io::Result<()> {
    use std::os::unix::fs::PermissionsExt;
    fs::set_permissions(path, fs::Permissions::from_mode(0o600))
}

// No Windows, %APPDATA% já é visível só para o próprio usuário.
#[cfg(not(unix))]
fn restrict_to_owner(_path: &PathBuf) -> std::io::Result<()> {
    Ok(())
}
