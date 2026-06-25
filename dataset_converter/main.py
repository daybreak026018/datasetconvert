import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src.gui.simple_home_window import SimpleHomeWindow


def ensure_data_dirs():
    base = Path(__file__).parent / "data"
    (base / "input").mkdir(parents=True, exist_ok=True)
    (base / "output").mkdir(parents=True, exist_ok=True)


def _apply_windows_taskbar_icon(window, icon_path: Path):
    if not sys.platform.startswith("win") or not icon_path.exists():
        return

    try:
        import ctypes

        window.setWindowIcon(QIcon(str(icon_path)))

        hwnd = int(window.winId())
        user32 = ctypes.windll.user32

        WM_SETICON = 0x0080
        ICON_SMALL = 0
        ICON_BIG = 1
        GCLP_HICON = -14
        GCLP_HICONSM = -34
        IMAGE_ICON = 1
        LR_LOADFROMFILE = 0x00000010
        LR_DEFAULTSIZE = 0x00000040

        large_icon = user32.LoadImageW(
            None,
            str(icon_path),
            IMAGE_ICON,
            256,
            256,
            LR_LOADFROMFILE,
        )
        small_icon = user32.LoadImageW(
            None,
            str(icon_path),
            IMAGE_ICON,
            32,
            32,
            LR_LOADFROMFILE | LR_DEFAULTSIZE,
        )

        if large_icon:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_BIG, large_icon)
            ctypes.windll.user32.SetClassLongPtrW(hwnd, GCLP_HICON, large_icon)
        if small_icon:
            user32.SendMessageW(hwnd, WM_SETICON, ICON_SMALL, small_icon)
            ctypes.windll.user32.SetClassLongPtrW(hwnd, GCLP_HICONSM, small_icon)
    except Exception:
        pass


def main():
    ensure_data_dirs()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    if sys.platform.startswith("win"):
        try:
            import ctypes

            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("DataForge.YOLOStudio")
        except Exception:
            pass

    app = QApplication(sys.argv)

    icon_root = Path(__file__).resolve().parents[1] / "assets"
    icon_path = icon_root / "logo.ico"
    if not icon_path.exists():
        icon_path = icon_root / "logo.png"
    if not icon_path.exists():
        icon_path = Path(__file__).parent / "resources" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = SimpleHomeWindow()
    screen = app.primaryScreen()
    if screen is not None:
        available = screen.availableGeometry()
        target_width = int(available.width() * 0.5)
        target_height = int(available.height() * 0.5)
        window.resize(target_width, target_height)
    window.show()
    _apply_windows_taskbar_icon(window, icon_path)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
