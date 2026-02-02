import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication

from src.gui.qml_style_window import QMLStyleWindow


def ensure_data_dirs():
    base = Path(__file__).parent / "data"
    (base / "input").mkdir(parents=True, exist_ok=True)
    (base / "output").mkdir(parents=True, exist_ok=True)


def main():
    ensure_data_dirs()
    app = QApplication(sys.argv)
    
    # 设置应用程序属性
    app.setApplicationName("DataForge")
    app.setApplicationVersion("2.2.0")
    app.setOrganizationName("DataForge Team")
    
    # 创建并显示主窗口
    window = QMLStyleWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
