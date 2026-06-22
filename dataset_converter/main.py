import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from src.gui.simple_home_window import SimpleHomeWindow


def ensure_data_dirs():
    base = Path(__file__).parent / "data"
    (base / "input").mkdir(parents=True, exist_ok=True)
    (base / "output").mkdir(parents=True, exist_ok=True)


def main():
    ensure_data_dirs()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)

    window = SimpleHomeWindow()
    screen = app.primaryScreen()
    if screen is not None:
        available = screen.availableGeometry()
        target_width = int(available.width() * 0.5)
        target_height = int(available.height() * 0.5)
        window.resize(target_width, target_height)
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
