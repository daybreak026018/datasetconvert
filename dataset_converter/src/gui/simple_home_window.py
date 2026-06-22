"""
Responsive blue-and-white main window shell for DataForge.
"""

from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from .styles import AppStyles
from .theme_manager import theme_manager


class NavCard(QFrame):
    """Clickable navigation card used in the rebuilt sidebar."""

    clicked = pyqtSignal(int)

    def __init__(self, index: int, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self.index = index
        self.setObjectName("navCard")
        self.setProperty("selected", "false")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFixedHeight(64)

        self.layout_ref = QVBoxLayout(self)
        self.layout_ref.setContentsMargins(12, 8, 12, 8)
        self.layout_ref.setSpacing(2)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("navTitle")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("navSubtitle")
        self.subtitle_label.setWordWrap(True)

        self.layout_ref.addWidget(self.title_label)
        self.layout_ref.addWidget(self.subtitle_label)

    def set_selected(self, selected: bool):
        self.setProperty("selected", "true" if selected else "false")
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(event)


class SimpleHomeWindow(QMainWindow):
    """Single-palette blue shell around the tool panels."""

    NAV_ITEMS = [
        ("格式转换", "数据集格式转换与标签映射"),
        ("数据划分", "训练、验证、测试集划分"),
        ("数据分析", "快速统计与质量概览"),
        ("数据可视化", "图表预览与汇总方案"),
        ("数据搜索", "按名称、类型和子集检索"),
        ("协作标注", "任务看板与成员协作"),
        ("高级功能", "批量质检与修复建议"),
        ("设置", "蓝色固定主题与偏好设置"),
    ]

    def __init__(self):
        super().__init__()
        theme_manager.set_theme("light")
        self._sync_app_styles()
        self.nav_cards = []
        self.panels = []
        self.current_index = 0
        self._build_ui()
        self._build_panels()
        self._apply_shell_style()
        self.switch_panel(0)

    def _sync_app_styles(self):
        """Mirror the blue palette into shared style constants."""
        colors = theme_manager.get_theme_config("light")["colors"]
        AppStyles.PRIMARY_COLOR = colors["primary"]
        AppStyles.SUCCESS_COLOR = colors["success"]
        AppStyles.WARNING_COLOR = colors["warning"]
        AppStyles.DANGER_COLOR = colors["danger"]
        AppStyles.BACKGROUND_COLOR = colors["background"]
        AppStyles.CARD_COLOR = colors["card"]
        AppStyles.TEXT_COLOR = colors["text"]
        AppStyles.SECONDARY_TEXT = colors["secondary_text"]
        AppStyles.BORDER_COLOR = colors["border"]
        AppStyles.SIDEBAR_BG = colors["sidebar_bg"]
        AppStyles.SIDEBAR_TEXT = colors["sidebar_text"]
        AppStyles.SIDEBAR_HOVER = colors["sidebar_hover"]
        AppStyles.NAV_SELECTED_BG = colors["nav_selected"]
        AppStyles.NAV_SELECTED_BORDER = colors["nav_selected_border"]
        AppStyles.HEADER_BG = colors["header_bg"]
        AppStyles.HEADER_TEXT = colors["header_text"]

    def _build_ui(self):
        self.setWindowTitle("DataForge - 数据集工具箱")
        self.setMinimumSize(720, 480)
        self.resize(920, 560)

        icon_path = Path(__file__).parent.parent.parent / "resources" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        root = QWidget()
        root.setObjectName("shellRoot")
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setFixedWidth(190)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(14, 18, 14, 14)
        self.sidebar_layout.setSpacing(10)

        nav_container = QWidget()
        self.nav_layout = QVBoxLayout(nav_container)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(8)

        for index, (title, subtitle) in enumerate(self.NAV_ITEMS):
            card = NavCard(index, title, subtitle, self)
            card.clicked.connect(self.switch_panel)
            self.nav_cards.append(card)
            self.nav_layout.addWidget(card)

        self.nav_layout.addStretch()
        self.sidebar_layout.addWidget(nav_container, 1)

        root_layout.addWidget(self.sidebar)

        self.content_wrap = QFrame()
        self.content_wrap.setObjectName("contentWrap")
        self.content_layout = QVBoxLayout(self.content_wrap)
        self.content_layout.setContentsMargins(18, 18, 18, 18)
        self.content_layout.setSpacing(12)

        self.header_card = QFrame()
        self.header_card.setObjectName("headerCard")
        self.header_layout = QVBoxLayout(self.header_card)
        self.header_layout.setContentsMargins(18, 14, 18, 14)
        self.header_layout.setSpacing(4)

        self.page_title = QLabel("格式转换")
        self.page_title.setObjectName("pageTitle")
        self.page_desc = QLabel("数据集格式转换与标签映射")
        self.page_desc.setObjectName("pageDesc")
        self.page_desc.setWordWrap(True)

        self.header_layout.addWidget(self.page_title)
        self.header_layout.addWidget(self.page_desc)
        self.content_layout.addWidget(self.header_card)

        self.stack_card = QFrame()
        self.stack_card.setObjectName("stackCard")
        self.stack_layout = QVBoxLayout(self.stack_card)
        self.stack_layout.setContentsMargins(14, 14, 14, 14)
        self.stack_layout.setSpacing(0)

        self.stack_scroll = QScrollArea()
        self.stack_scroll.setObjectName("contentScroll")
        self.stack_scroll.setWidgetResizable(True)
        self.stack_scroll.setFrameShape(QFrame.NoFrame)
        self.stack_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.stack = QStackedWidget()
        self.stack.setObjectName("contentStack")
        self.stack_scroll.setWidget(self.stack)
        self.stack_layout.addWidget(self.stack_scroll)

        self.content_layout.addWidget(self.stack_card, 1)
        root_layout.addWidget(self.content_wrap, 1)

    def _build_panels(self):
        from .converter_panel import ConverterPanel
        from .simple_advanced_panel import SimpleAdvancedPanel
        from .simple_analysis_panel import SimpleAnalysisPanel
        from .simple_collaboration_panel import SimpleCollaborationPanel
        from .simple_search_panel import SimpleSearchPanel
        from .simple_settings_panel import SimpleSettingsPanel
        from .simple_splitting_panel import SimpleSplittingPanel
        from .simple_visualization_panel import SimpleVisualizationPanel

        self.panels = [
            ConverterPanel(self),
            SimpleSplittingPanel(self),
            SimpleAnalysisPanel(self),
            SimpleVisualizationPanel(self),
            SimpleSearchPanel(self),
            SimpleCollaborationPanel(self),
            SimpleAdvancedPanel(self),
            SimpleSettingsPanel(self),
        ]

        for panel in self.panels:
            if hasattr(panel, "apply_theme"):
                panel.apply_theme()
            self.stack.addWidget(panel)

    def switch_panel(self, index: int):
        if index < 0 or index >= len(self.NAV_ITEMS):
            return

        self.current_index = index
        self.stack.setCurrentIndex(index)

        title, subtitle = self.NAV_ITEMS[index]
        self.page_title.setText(title)
        self.page_desc.setText(subtitle)

        for card_index, card in enumerate(self.nav_cards):
            card.set_selected(card_index == index)

        current_panel = self.panels[index]
        if hasattr(current_panel, "apply_theme"):
            current_panel.apply_theme()

    def _apply_shell_style(self):
        green_base = theme_manager.generate_stylesheet("light")
        shell_style = """
        QWidget#shellRoot {
            background-color: #f4f8fc;
        }

        QFrame#sidebar {
            background-color: #ffffff;
            border-right: 1px solid #dbe6f2;
        }

        QFrame#headerCard,
        QFrame#stackCard {
            background-color: #ffffff;
            border: 1px solid #dbe6f2;
            border-radius: 8px;
        }

        QFrame#stackCard {
            background-color: #ffffff;
        }

        QLabel#pageDesc {
            color: #6c7f97;
            font-size: 11px;
            background-color: transparent;
        }

        QLabel#pageTitle {
            color: #1f3b63;
            font-size: 18px;
            font-weight: 700;
            background-color: transparent;
        }

        QFrame#navCard {
            background-color: #ffffff;
            border: 1px solid #e1eaf5;
            border-radius: 8px;
        }

        QFrame#navCard:hover {
            background-color: #f5f9ff;
            border-color: #bfd4ef;
        }

        QFrame#navCard[selected="true"] {
            background-color: #edf5ff;
            border: 1px solid #9fc2ef;
            border-left: 3px solid #2f7fe8;
        }

        QFrame#navCard QLabel#navTitle {
            color: #24466f;
            font-size: 12px;
            font-weight: 700;
            background-color: transparent;
        }

        QFrame#navCard QLabel#navSubtitle {
            color: #7a8ea8;
            font-size: 10px;
            background-color: transparent;
        }

        QStackedWidget#contentStack {
            background-color: transparent;
            border: none;
        }

        QScrollArea#contentScroll {
            background-color: transparent;
            border: none;
        }

        QScrollArea#contentScroll > QWidget > QWidget {
            background-color: transparent;
        }
        """
        self.setStyleSheet(green_base + shell_style)
