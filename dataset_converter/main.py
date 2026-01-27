import sys
from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from src.gui.home_window import HomeWindow


def ensure_data_dirs():
    base = Path(__file__).parent / "data"
    (base / "input").mkdir(parents=True, exist_ok=True)
    (base / "output").mkdir(parents=True, exist_ok=True)


from PyQt5.QtGui import QFont

def main():
    ensure_data_dirs()
    
    # 启用 High DPI Scaling 支持
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
    app = QApplication(sys.argv)
    
    # 设置默认字体，防止初始化时字体过大导致布局错乱
    font = QFont("SimSun", 12)
    font.setStyleStrategy(QFont.PreferAntialias)
    app.setFont(font)
    
    window = HomeWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
8