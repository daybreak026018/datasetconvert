"""
Theme management for the desktop UI.
"""

from typing import Any, Dict

from PyQt5.QtCore import QObject, QSettings, pyqtSignal


class ThemeManager(QObject):
    """Centralized theme manager."""

    theme_changed = pyqtSignal(str)
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if ThemeManager._initialized:
            return

        super().__init__()
        self.settings = QSettings("DataForge", "Theme")
        self.themes = self._load_themes()
        stored_theme = self.settings.value("current_theme", "light")
        self.current_theme = self._normalize_theme_name(stored_theme)
        ThemeManager._initialized = True

    def _load_themes(self) -> Dict[str, Dict[str, Any]]:
        base_fonts = {
            "family": "Microsoft YaHei, Segoe UI, sans-serif",
            "size_small": 10,
            "size_normal": 12,
            "size_large": 14,
            "size_title": 16,
        }
        base_spacing = {
            "small": 4,
            "normal": 8,
            "large": 16,
            "xlarge": 24,
        }

        return {
            "light": {
                "name": "浅色白色主题",
                "colors": {
                    "primary": "#2563EB",
                    "success": "#16A34A",
                    "warning": "#F59E0B",
                    "danger": "#EF4444",
                    "background": "#F7F9FC",
                    "card": "#FFFFFF",
                    "text": "#111827",
                    "secondary_text": "#6B7280",
                    "border": "#D6DEEB",
                    "hover": "#EEF4FF",
                    "selected": "#DBEAFE",
                    "sidebar_bg": "#FFFFFF",
                    "sidebar_text": "#1F2937",
                    "sidebar_hover": "#F3F7FF",
                    "nav_selected": "#E8F0FF",
                    "nav_selected_border": "#2563EB",
                    "header_bg": "#FFFFFF",
                    "header_text": "#111827",
                },
                "fonts": dict(base_fonts),
                "spacing": dict(base_spacing),
                "border_radius": 10,
                "shadow": "0 2px 6px rgba(37,99,235,0.08)",
            },
            "dark": {
                "name": "深色蓝调主题",
                "colors": {
                    "primary": "#4DA3FF",
                    "success": "#34D399",
                    "warning": "#FBBF24",
                    "danger": "#F87171",
                    "background": "#0B1220",
                    "card": "#111C2E",
                    "text": "#E5EEF9",
                    "secondary_text": "#9FB3C8",
                    "border": "#22324A",
                    "hover": "#16243A",
                    "selected": "#1D4ED8",
                    "sidebar_bg": "#0F172A",
                    "sidebar_text": "#DCE8F8",
                    "sidebar_hover": "#16243A",
                    "nav_selected": "#17345C",
                    "nav_selected_border": "#4DA3FF",
                    "header_bg": "#10213B",
                    "header_text": "#EFF6FF",
                },
                "fonts": dict(base_fonts),
                "spacing": dict(base_spacing),
                "border_radius": 10,
                "shadow": "0 2px 10px rgba(5,10,20,0.35)",
            },
            "green": {
                "name": "护眼绿色主题",
                "colors": {
                    "primary": "#2F855A",
                    "success": "#38A169",
                    "warning": "#D69E2E",
                    "danger": "#E53E3E",
                    "background": "#EEF7EF",
                    "card": "#FFFFFF",
                    "text": "#1F3A2D",
                    "secondary_text": "#5F7A69",
                    "border": "#C8DEC8",
                    "hover": "#E3F2E5",
                    "selected": "#CFE8D2",
                    "sidebar_bg": "#F4FAF4",
                    "sidebar_text": "#274C3A",
                    "sidebar_hover": "#E5F2E7",
                    "nav_selected": "#D8EEDC",
                    "nav_selected_border": "#2F855A",
                    "header_bg": "#E6F4EA",
                    "header_text": "#1F3A2D",
                },
                "fonts": dict(base_fonts),
                "spacing": dict(base_spacing),
                "border_radius": 10,
                "shadow": "0 2px 8px rgba(47,133,90,0.12)",
            },
        }

    def _normalize_theme_name(self, theme_name: str) -> str:
        alias_map = {
            "blue": "dark",
        }
        normalized = alias_map.get(theme_name, theme_name)
        if normalized not in self.themes:
            return "light"
        return normalized

    def get_current_theme(self) -> str:
        return self.current_theme

    def get_theme_config(self, theme_name: str = None) -> Dict[str, Any]:
        theme_name = self.current_theme if theme_name is None else theme_name
        theme_name = self._normalize_theme_name(theme_name)
        return self.themes.get(theme_name, self.themes["light"])

    def set_theme(self, theme_name: str):
        theme_name = self._normalize_theme_name(theme_name)
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.settings.setValue("current_theme", theme_name)
            self.theme_changed.emit(theme_name)

    def get_available_themes(self) -> Dict[str, str]:
        return {name: config["name"] for name, config in self.themes.items()}

    def generate_stylesheet(self, theme_name: str = None) -> str:
        config = self.get_theme_config(theme_name)
        colors = config["colors"]
        fonts = config["fonts"]
        spacing = config["spacing"]
        radius = config["border_radius"]

        return f"""
        QWidget {{
            background-color: {colors['background']};
            color: {colors['text']};
            font-family: {fonts['family']};
            font-size: {fonts['size_normal']}px;
        }}

        QMainWindow {{
            background-color: {colors['background']};
        }}

        QGroupBox {{
            background-color: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: {radius + 4}px;
            margin-top: {spacing['large']}px;
            padding-top: {spacing['large']}px;
            font-weight: bold;
            font-size: {fonts['size_large']}px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: {spacing['large']}px;
            padding: 0 {spacing['normal']}px;
            background-color: {colors['card']};
            color: {colors['primary']};
        }}

        QPushButton {{
            background-color: {colors['card']};
            border: 2px solid {colors['border']};
            border-radius: {radius}px;
            padding: {spacing['normal']}px {spacing['large']}px;
            color: {colors['text']};
            min-height: 20px;
        }}

        QPushButton:hover {{
            background-color: {colors['hover']};
            border-color: {colors['primary']};
        }}

        QPushButton:pressed {{
            background-color: {colors['primary']};
            color: white;
        }}

        QPushButton:disabled {{
            background-color: {colors['border']};
            color: {colors['secondary_text']};
            border-color: {colors['border']};
        }}

        QPushButton[buttonType="primary"] {{
            background-color: {colors['primary']};
            border: none;
            color: white;
            font-weight: bold;
        }}

        QPushButton[buttonType="primary"]:hover {{
            background-color: {colors['selected']};
        }}

        QPushButton[buttonType="success"] {{
            background-color: {colors['success']};
            border: none;
            color: white;
            font-weight: bold;
        }}

        QPushButton[buttonType="warning"] {{
            background-color: {colors['warning']};
            border: none;
            color: white;
        }}

        QPushButton[buttonType="danger"] {{
            background-color: {colors['danger']};
            border: none;
            color: white;
        }}

        QLabel {{
            background-color: transparent;
            color: {colors['text']};
        }}

        QLabel[labelType="title"] {{
            color: {colors['primary']};
            font-size: {fonts['size_title']}px;
            font-weight: bold;
        }}

        QLabel[labelType="subtitle"] {{
            color: {colors['secondary_text']};
            font-size: {fonts['size_small']}px;
        }}

        QLabel[labelType="status"] {{
            background-color: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: {radius // 2}px;
            padding: {spacing['small']}px {spacing['normal']}px;
        }}

        QTextEdit, QLineEdit, QComboBox, QSpinBox, QListWidget, QScrollArea {{
            background-color: {colors['card']};
            border: 1px solid {colors['border']};
            border-radius: {radius}px;
        }}

        QTextEdit:focus, QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
            border: 2px solid {colors['primary']};
        }}

        QListWidget::item:selected {{
            background-color: {colors['primary']};
            color: white;
        }}

        QListWidget::item:hover {{
            background-color: {colors['hover']};
        }}

        QCheckBox {{
            color: {colors['text']};
            spacing: {spacing['normal']}px;
        }}

        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 2px solid {colors['border']};
            border-radius: 3px;
            background-color: {colors['card']};
        }}

        QCheckBox::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
        }}

        QProgressBar {{
            background-color: {colors['background']};
            border: 2px solid {colors['border']};
            border-radius: {radius}px;
            text-align: center;
        }}

        QProgressBar::chunk {{
            background-color: {colors['primary']};
            border-radius: {max(radius - 2, 1)}px;
        }}

        QTabWidget::pane {{
            background-color: {colors['card']};
            border: 2px solid {colors['border']};
            border-radius: {radius}px;
        }}

        QTabBar::tab {{
            background-color: {colors['background']};
            border: 1px solid {colors['border']};
            border-bottom: none;
            border-top-left-radius: {radius}px;
            border-top-right-radius: {radius}px;
            padding: {spacing['small']}px {spacing['normal']}px;
            color: {colors['text']};
        }}

        QTabBar::tab:selected {{
            background-color: {colors['card']};
            border-color: {colors['primary']};
            color: {colors['primary']};
            font-weight: bold;
        }}

        QTabBar::tab:hover {{
            background-color: {colors['hover']};
        }}

        QScrollBar:vertical {{
            background-color: transparent;
            width: 10px;
            margin: 4px 0px 4px 0px;
        }}

        QScrollBar::handle:vertical {{
            background-color: #cfe1d0;
            border-radius: 5px;
            min-height: 36px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: #b7d1bb;
        }}

        QScrollBar:horizontal {{
            background-color: transparent;
            height: 10px;
            margin: 0px 4px 0px 4px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: #cfe1d0;
            border-radius: 5px;
            min-width: 36px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: #b7d1bb;
        }}

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical,
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical,
        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal,
        QScrollBar::add-page:horizontal,
        QScrollBar::sub-page:horizontal {{
            background: transparent;
            border: none;
        }}
        """


def get_theme_manager():
    return ThemeManager()


theme_manager = get_theme_manager()
