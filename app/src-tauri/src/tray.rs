use tauri::menu::{Menu, MenuItem};
use tauri::tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent};
use tauri::App;
use tauri_plugin_positioner::{Position, WindowExt};

use crate::panel;

// Ícone na bandeja (Windows e macOS): clique abre o painel colado nele; o menu tem "Sair".
pub fn setup(app: &App) -> tauri::Result<()> {
    let quit = MenuItem::with_id(app, "quit", "Sair", true, None::<&str>)?;

    TrayIconBuilder::new()
        .icon(app.default_window_icon().cloned().expect("ícone do app"))
        .tooltip("Ar Gree")
        .menu(&Menu::with_items(app, &[&quit])?)
        .show_menu_on_left_click(false)
        .on_menu_event(|app, event| {
            if event.id == "quit" {
                app.exit(0);
            }
        })
        .on_tray_icon_event(|tray, event| {
            let app = tray.app_handle();
            tauri_plugin_positioner::on_tray_event(app, &event);

            if let TrayIconEvent::Click { button: MouseButton::Left, button_state: MouseButtonState::Up, .. } = event {
                let _ = panel::window(app).move_window(Position::TrayBottomCenter);
                panel::toggle(app);
            }
        })
        .build(app)?;

    Ok(())
}
