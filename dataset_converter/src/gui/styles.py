"""
Shared application styles.
"""


class AppStyles:
    """Application style definitions."""

    PRIMARY_COLOR = "#2563EB"
    SUCCESS_COLOR = "#16A34A"
    WARNING_COLOR = "#F59E0B"
    DANGER_COLOR = "#EF4444"
    BACKGROUND_COLOR = "#F7F9FC"
    CARD_COLOR = "#FFFFFF"
    TEXT_COLOR = "#111827"
    SECONDARY_TEXT = "#6B7280"
    BORDER_COLOR = "#D6DEEB"

    SIDEBAR_BG = "#FFFFFF"
    SIDEBAR_TEXT = "#1F2937"
    SIDEBAR_HOVER = "#F3F7FF"
    HEADER_BG = "#FFFFFF"
    HEADER_TEXT = "#111827"
    NAV_SELECTED_BG = "#E8F0FF"
    NAV_SELECTED_BORDER = "#2563EB"

    @staticmethod
    def get_main_window_style():
        return f"""
        QMainWindow {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
        }}

        QFrame#sidebar {{
            background-color: {AppStyles.SIDEBAR_BG};
            border: none;
            border-right: 1px solid {AppStyles.BORDER_COLOR};
        }}

        QFrame#header {{
            background-color: {AppStyles.HEADER_BG};
            border: none;
            border-bottom: 1px solid {AppStyles.BORDER_COLOR};
        }}

        QLabel#headerTitle {{
            color: {AppStyles.HEADER_TEXT};
            font-size: 18px;
            font-weight: bold;
            padding-left: 20px;
        }}

        QLabel#headerUserInfo {{
            color: {AppStyles.HEADER_TEXT};
            font-weight: bold;
        }}

        QFrame#navButton {{
            background-color: transparent;
            border: none;
            border-radius: 0px;
            margin: 0px;
            padding: 0px;
        }}

        QFrame#navButton:hover {{
            background-color: {AppStyles.SIDEBAR_HOVER};
        }}

        QFrame#navButton[selected="true"] {{
            background-color: {AppStyles.NAV_SELECTED_BG};
            border-left: 4px solid {AppStyles.NAV_SELECTED_BORDER};
        }}

        QLabel[class="navIcon"] {{
            background-color: transparent;
            padding: 0px;
        }}

        QLabel[class="navText"] {{
            color: {AppStyles.SIDEBAR_TEXT};
            font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            font-size: 14px;
            font-weight: 500;
        }}

        QFrame#navButton[selected="true"] QLabel[class="navText"] {{
            color: {AppStyles.SIDEBAR_TEXT};
            font-weight: bold;
        }}

        QGroupBox, QScrollArea, QListWidget {{
            background-color: {AppStyles.CARD_COLOR};
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 4px;
        }}

        QFrame[class="navSeparator"] {{
            color: #D1D5DB;
            border: none;
            background-color: #E9ECEF;
            width: 1px;
            margin: 0px 5px;
        }}
        """

    @staticmethod
    def get_panel_style():
        return f"""
        QWidget {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            color: {AppStyles.TEXT_COLOR};
            font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            font-size: 12px;
        }}

        QGroupBox {{
            background-color: {AppStyles.CARD_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 10px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
            font-size: 13px;
        }}

        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px;
            color: {AppStyles.PRIMARY_COLOR};
        }}

        QScrollArea {{
            border: none;
            background-color: transparent;
        }}

        QScrollBar:vertical {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            width: 10px;
            border-radius: 5px;
            margin: 0px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {AppStyles.BORDER_COLOR};
            border-radius: 5px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {AppStyles.SECONDARY_TEXT};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            height: 10px;
            border-radius: 5px;
            margin: 0px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {AppStyles.BORDER_COLOR};
            border-radius: 5px;
            min-width: 20px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {AppStyles.SECONDARY_TEXT};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """

    @staticmethod
    def get_button_style(button_type="default"):
        styles = {
            "default": f"""
                QPushButton {{
                    background-color: {AppStyles.CARD_COLOR};
                    border: 2px solid {AppStyles.BORDER_COLOR};
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: 500;
                    color: {AppStyles.TEXT_COLOR};
                }}

                QPushButton:hover {{
                    background-color: #EEF4FF;
                    border-color: {AppStyles.PRIMARY_COLOR};
                }}

                QPushButton:pressed {{
                    background-color: {AppStyles.PRIMARY_COLOR};
                    color: white;
                }}
            """,
            "primary": f"""
                QPushButton {{
                    background-color: {AppStyles.PRIMARY_COLOR};
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    color: white;
                }}

                QPushButton:hover {{
                    background-color: #1D4ED8;
                }}

                QPushButton:pressed {{
                    background-color: #1E40AF;
                }}
            """,
            "success": f"""
                QPushButton {{
                    background-color: {AppStyles.SUCCESS_COLOR};
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    color: white;
                }}

                QPushButton:hover {{
                    background-color: #15803D;
                }}

                QPushButton:pressed {{
                    background-color: #166534;
                }}
            """,
            "warning": f"""
                QPushButton {{
                    background-color: {AppStyles.WARNING_COLOR};
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: bold;
                    color: white;
                }}

                QPushButton:hover {{
                    background-color: #D97706;
                }}

                QPushButton:pressed {{
                    background-color: #B45309;
                }}
            """,
            "danger": f"""
                QPushButton {{
                    background-color: {AppStyles.DANGER_COLOR};
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: bold;
                    color: white;
                }}

                QPushButton:hover {{
                    background-color: #DC2626;
                }}

                QPushButton:pressed {{
                    background-color: #B91C1C;
                }}
            """,
        }
        return styles.get(button_type, styles["default"])

    @staticmethod
    def get_label_style(label_type="default"):
        styles = {
            "default": f"color: {AppStyles.TEXT_COLOR}; font-size: 12px;",
            "title": f"color: {AppStyles.PRIMARY_COLOR}; font-size: 16px; font-weight: bold;",
            "subtitle": f"color: {AppStyles.SECONDARY_TEXT}; font-size: 11px;",
            "status": (
                f"background-color: {AppStyles.CARD_COLOR};"
                f"border: 1px solid {AppStyles.BORDER_COLOR};"
                "border-radius: 6px; padding: 4px 8px;"
                f"color: {AppStyles.TEXT_COLOR};"
            ),
        }
        return styles.get(label_type, styles["default"])

    @staticmethod
    def get_textedit_style():
        return f"""
        QTextEdit {{
            background-color: {AppStyles.CARD_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            padding: 8px;
            color: {AppStyles.TEXT_COLOR};
        }}

        QTextEdit:focus {{
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        """

    @staticmethod
    def get_progressbar_style():
        return f"""
        QProgressBar {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            text-align: center;
            color: {AppStyles.TEXT_COLOR};
        }}

        QProgressBar::chunk {{
            background-color: {AppStyles.PRIMARY_COLOR};
            border-radius: 6px;
        }}
        """

    @staticmethod
    def get_combobox_style():
        return f"""
        QComboBox {{
            background-color: {AppStyles.CARD_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            padding: 6px 10px;
            color: {AppStyles.TEXT_COLOR};
        }}

        QComboBox:hover, QComboBox:focus {{
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        """

    @staticmethod
    def get_checkbox_style():
        return f"""
        QCheckBox {{
            color: {AppStyles.TEXT_COLOR};
            spacing: 8px;
        }}

        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 3px;
            background-color: {AppStyles.CARD_COLOR};
        }}

        QCheckBox::indicator:checked {{
            background-color: {AppStyles.PRIMARY_COLOR};
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        """

    @staticmethod
    def get_spinbox_style():
        return f"""
        QSpinBox {{
            background-color: {AppStyles.CARD_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            padding: 6px 8px;
            color: {AppStyles.TEXT_COLOR};
        }}

        QSpinBox:focus {{
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        """
