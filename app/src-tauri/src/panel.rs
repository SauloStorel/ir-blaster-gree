use std::error::Error;
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Mutex;
use std::time::{Duration, Instant};

use tauri::{App, AppHandle, Manager, WebviewWindow, WindowEvent};

const LABEL: &str = "panel";

// Clicar no ícone com o painel aberto tira o foco da janela, que some antes do clique
// chegar. Esse intervalo evita que o mesmo clique abra o painel de novo.
const REOPEN_GUARD: Duration = Duration::from_millis(300);

#[derive(Default)]
struct Visibility {
    hidden_at: Mutex<Option<Instant>>,
    // Ao aparecer, a janela pode avisar "sem foco" antes de ganhar foco; só esconde
    // quando ela perde um foco que de fato teve.
    focused_since_show: AtomicBool,
}

pub fn setup(app: &mut App) -> Result<(), Box<dyn Error>> {
    app.manage(Visibility::default());

    let handle = app.handle().clone();
    window(app.handle()).on_window_event(move |event| {
        if let WindowEvent::Focused(focused) = event {
            on_focus_changed(&handle, *focused);
        }
    });

    #[cfg(not(target_os = "linux"))]
    {
        crate::tray::setup(app)?;
        crate::startup::enable_on_first_run(app)?;
    }

    // Com --hidden (ex.: iniciado junto com o sistema), começa só no ícone.
    if !std::env::args().any(|arg| arg == "--hidden") {
        show(app.handle());
    }
    Ok(())
}

pub fn window(app: &AppHandle) -> WebviewWindow {
    app.get_webview_window(LABEL)
        .expect("janela \"panel\" definida no tauri.conf.json")
}

pub fn toggle(app: &AppHandle) {
    if window(app).is_visible().unwrap_or(false) {
        hide(app);
        return;
    }

    let hidden_at = *visibility(app).hidden_at.lock().unwrap();
    let just_hidden = hidden_at.is_some_and(|at| at.elapsed() < REOPEN_GUARD);
    if !just_hidden {
        show(app);
    }
}

fn visibility(app: &AppHandle) -> tauri::State<'_, Visibility> {
    app.state::<Visibility>()
}

fn on_focus_changed(app: &AppHandle, focused: bool) {
    let had_focus = visibility(app).focused_since_show.swap(focused, Ordering::SeqCst);
    if had_focus && !focused {
        hide(app);
    }
}

fn show(app: &AppHandle) {
    visibility(app).focused_since_show.store(false, Ordering::SeqCst);
    let window = window(app);
    let _ = window.show();
    let _ = window.set_focus();
}

fn hide(app: &AppHandle) {
    let _ = window(app).hide();
    *visibility(app).hidden_at.lock().unwrap() = Some(Instant::now());
}
