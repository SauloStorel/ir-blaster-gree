use tauri::menu::{Menu, MenuItem};
use tauri::tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent};
use tauri::{App, PhysicalPosition, Rect, WebviewWindow};

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
            if let TrayIconEvent::Click { rect, button: MouseButton::Left, button_state: MouseButtonState::Up, .. } = event {
                let app = tray.app_handle();
                let _ = place_by_icon(&panel::window(app), rect);
                panel::toggle(app);
            }
        })
        .build(app)?;

    Ok(())
}

// Acima do ícone e centralizado nele, sem sair da área útil do monitor: com a barra de tarefas
// em cima ou num canto, a janela encosta na borda em vez de ficar cortada.
fn place_by_icon(window: &WebviewWindow, icon: Rect) -> tauri::Result<()> {
    let scale = window.scale_factor()?;
    let icon_position = icon.position.to_physical::<i32>(scale);
    let icon_width = icon.size.to_physical::<i32>(scale).width;
    let Some(monitor) = window.monitor_from_point(icon_position.x.into(), icon_position.y.into())? else {
        return Ok(());
    };

    let area = monitor.work_area();
    let size = window.outer_size()?;
    let (width, height) = (size.width as i32, size.height as i32);
    let max_x = area.position.x + area.size.width as i32 - width;
    let max_y = area.position.y + area.size.height as i32 - height;

    let x = (icon_position.x + icon_width / 2 - width / 2).min(max_x).max(area.position.x);
    let y = (icon_position.y - height).min(max_y).max(area.position.y);
    window.set_position(PhysicalPosition::new(x, y))
}
