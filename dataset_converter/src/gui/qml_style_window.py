"""
QML风格主窗口 - DataForge v2.2.0
采用QML设计思想：声明式UI、组件化、动画效果
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame, QScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QFont, QPainter, QPen, QColor, QPixmap


class AnimatedButton(QPushButton):
    """QML风格的动画按钮"""
    
    def __init__(self, text="", icon_text="", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.icon_text = icon_text
        self.is_active = False
        self.hover_animation = None
        self.click_animation = None
        self.setup_animations()
        self.setup_style()
    
    def setup_animations(self):
        """设置动画效果"""
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        self.click_animation = QPropertyAnimation(self, b"geometry")
        self.click_animation.setDuration(100)
        self.click_animation.setEasingCurve(QEasingCurve.OutBack)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            AnimatedButton {
                background-color: transparent;
                border: none;
                border-radius: 12px;
                padding: 16px 20px;
                text-align: left;
                font-size: 14px;
                font-weight: 500;
                color: #64748b;
            }
            
            AnimatedButton:hover {
                background-color: #f1f5f9;
                color: #334155;
            }
            
            AnimatedButton[active="true"] {
                background-color: #3b82f6;
                color: white;
            }
            
            AnimatedButton[active="true"]:hover {
                background-color: #2563eb;
            }
        """)
    
    def set_active(self, active):
        """设置激活状态"""
        self.is_active = active
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        if not self.is_active:
            self.animate_hover(True)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        if not self.is_active:
            self.animate_hover(False)
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        """鼠标按下事件"""
        self.animate_click()
        super().mousePressEvent(event)
    
    def animate_hover(self, hover):
        """悬停动画"""
        if self.hover_animation.state() == QPropertyAnimation.Running:
            self.hover_animation.stop()
        
        current_rect = self.geometry()
        if hover:
            # 顶部品牌区域已移除，仅保留导航项以保持侧栏整洁
            # 保留少量上边距使导航项与窗口边缘有间距
            layout.setContentsMargins(0, 12, 0, 0)
        self.hover_animation.start()
    
    def animate_click(self):
        """点击动画"""
        if self.click_animation.state() == QPropertyAnimation.Running:
            return
        
        current_rect = self.geometry()
        small_rect = QRect(
            current_rect.x() + 1,
            current_rect.y() + 1,
            current_rect.width() - 2,
            current_rect.height() - 2
        )
        
        self.click_animation.setStartValue(current_rect)
        self.click_animation.setEndValue(small_rect)
        self.click_animation.finished.connect(lambda: self.setGeometry(current_rect))
        self.click_animation.start()


class Card(QFrame):
    """QML风格的卡片组件"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        
        # 设置大小策略
        from PyQt5.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.setup_ui()
        self.setup_style()
        self.setup_shadow()
    
    def setup_ui(self):
        """设置UI"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(24, 20, 24, 24)
        self.layout.setSpacing(16)
        
        if self.title:
            title_label = QLabel(self.title)
            title_label.setObjectName("cardTitle")
            self.layout.addWidget(title_label)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            Card {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 16px;
            }
            
            Card:hover {
                border-color: #cbd5e1;
            }
            
            #cardTitle {
                font-size: 18px;
                font-weight: 600;
                color: #1e293b;
                margin-bottom: 8px;
            }
        """)
    
    def setup_shadow(self):
        """设置阴影效果"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 8))
        self.setGraphicsEffect(shadow)
    
    def add_widget(self, widget):
        """添加控件"""
        self.layout.addWidget(widget)
    
    def add_layout(self, layout):
        """添加布局"""
        self.layout.addLayout(layout)


class NavigationItem(QWidget):
    """QML风格的导航项"""
    
    clicked = pyqtSignal()
    
    def __init__(self, icon, title, subtitle="", parent=None):
        super().__init__(parent)
        self.icon = icon
        self.title = title
        self.subtitle = subtitle
        self.is_active = False
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        # 设置固定高度确保内容完整显示
        self.setFixedHeight(72)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 12, 20, 12)
        layout.setSpacing(16)
        
        # 图标
        self.icon_label = QLabel(self.icon)
        self.icon_label.setObjectName("navIcon")
        self.icon_label.setFixedSize(28, 28)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)
        
        # 文本区域
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("navTitle")
        self.title_label.setWordWrap(False)
        text_layout.addWidget(self.title_label)
        
        if self.subtitle:
            self.subtitle_label = QLabel(self.subtitle)
            self.subtitle_label.setObjectName("navSubtitle")
            self.subtitle_label.setWordWrap(True)
            text_layout.addWidget(self.subtitle_label)
        
        layout.addLayout(text_layout, 1)
        
        # 激活指示器
        self.indicator = QFrame()
        self.indicator.setObjectName("navIndicator")
        self.indicator.setFixedSize(4, 32)
        layout.addWidget(self.indicator)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            NavigationItem {
                background-color: transparent;
                border-radius: 12px;
                margin: 2px 8px;
                min-height: 72px;
                max-height: 72px;
            }
            
            NavigationItem:hover {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
            }
            
            NavigationItem[active="true"] {
                background-color: #eff6ff;
                border: 1px solid #bfdbfe;
            }
            
            #navIcon {
                font-size: 22px;
                color: #64748b;
                background-color: transparent;
            }
            
            NavigationItem[active="true"] #navIcon {
                color: #3b82f6;
            }
            
            #navTitle {
                font-size: 15px;
                font-weight: 600;
                color: #334155;
                margin: 0px;
                padding: 0px;
                background-color: transparent;
            }
            
            NavigationItem[active="true"] #navTitle {
                color: #1e40af;
            }
            
            #navSubtitle {
                font-size: 12px;
                color: #64748b;
                margin: 0px;
                padding: 0px;
                line-height: 1.3;
                background-color: transparent;
            }
            
            NavigationItem[active="true"] #navSubtitle {
                color: #3730a3;
            }
            
            #navIndicator {
                background-color: transparent;
                border-radius: 2px;
            }
            
            NavigationItem[active="true"] #navIndicator {
                background-color: #3b82f6;
            }
        """)
    
    def set_active(self, active):
        """设置激活状态"""
        self.is_active = active
        self.setProperty("active", active)
        self.style().unpolish(self)
        self.style().polish(self)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class QMLStyleWindow(QMainWindow):
    """QML风格主窗口"""
    
    def __init__(self):
        super().__init__()
        self.current_panel_index = 0
        self.navigation_items = []
        self.panels = {}
        self.init_ui()
        self.init_panels()
        self.apply_global_style()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("现代化数据集工具")
        self.setMinimumSize(1400, 900)  # 增加最小尺寸
        self.resize(1600, 1000)  # 增加默认尺寸
        
        # 设置窗口图标
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # 中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 左侧导航面板
        self.nav_panel = self.create_navigation_panel()
        main_layout.addWidget(self.nav_panel)
        
        # 右侧内容面板
        self.content_panel = self.create_content_panel()
        main_layout.addWidget(self.content_panel, 1)
    
    def create_navigation_panel(self):
        """创建导航面板"""
        nav_widget = QWidget()
        nav_widget.setObjectName("navigationPanel")
        nav_widget.setFixedWidth(300)  # 增加宽度从280到300
        
        layout = QVBoxLayout(nav_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 顶部品牌区域已移除，仅保留导航项以保持侧栏整洁
        layout.setContentsMargins(0, 12, 0, 0)
        
        # 导航菜单
        nav_scroll = QScrollArea()
        nav_scroll.setWidgetResizable(True)
        nav_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        nav_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        nav_scroll.setObjectName("navScroll")
        
        nav_content = QWidget()
        nav_content_layout = QVBoxLayout(nav_content)
        nav_content_layout.setContentsMargins(0, 12, 0, 12)
        nav_content_layout.setSpacing(6)
        
        # 导航项数据
        nav_data = [
            ("🔄", "格式转换", "数据集格式转换"),
            ("✂️", "数据划分", "训练/验证/测试集划分"),
            ("📊", "数据分析", "统计信息和质量分析"),
            ("📈", "数据可视化", "图表和报告生成"),
            ("🔍", "数据搜索", "智能搜索和筛选"),
            ("👥", "协作标注", "多人协作管理"),
            ("⚡", "高级功能", "AI辅助和批处理"),
            ("⚙️", "系统设置", "偏好设置和配置")
        ]
        
        # 创建导航项
        for i, (icon, title, subtitle) in enumerate(nav_data):
            nav_item = NavigationItem(icon, title, subtitle)
            nav_item.clicked.connect(lambda idx=i: self.switch_panel(idx))
            self.navigation_items.append(nav_item)
            nav_content_layout.addWidget(nav_item)
        
        nav_content_layout.addStretch()
        nav_scroll.setWidget(nav_content)
        layout.addWidget(nav_scroll, 1)
        
        # 底部状态区域
        status_widget = QWidget()
        status_widget.setObjectName("statusWidget")
        status_layout = QVBoxLayout(status_widget)
        status_layout.setContentsMargins(24, 16, 24, 24)
        
        self.status_label = QLabel("就绪")
        self.status_label.setObjectName("statusLabel")
        status_layout.addWidget(self.status_label)
        
        layout.addWidget(status_widget)
        
        return nav_widget
    
    def create_content_panel(self):
        """创建内容面板"""
        content_widget = QWidget()
        content_widget.setObjectName("contentPanel")
        
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(24, 24, 24, 24)  # 减少边距
        layout.setSpacing(20)  # 减少间距
        
        # 页面标题区域
        title_widget = QWidget()
        title_layout = QHBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        self.page_title = QLabel("数据集格式转换")
        self.page_title.setObjectName("pageTitle")
        title_layout.addWidget(self.page_title)
        title_layout.addStretch()
        
        layout.addWidget(title_widget)
        
        # 内容区域 - 使用滚动区域确保内容完全显示
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setObjectName("contentScroll")
        
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(24)
        
        scroll_area.setWidget(self.content_area)
        layout.addWidget(scroll_area, 1)
        
        return content_widget
    
    def init_panels(self):
        """初始化面板"""
        from .qml_converter_panel import QMLConverterPanel
        from .qml_splitting_panel import QMLSplittingPanel
        from .qml_analysis_panel import QMLAnalysisPanel
        from .qml_visualization_panel import QMLVisualizationPanel
        from .qml_search_panel import QMLSearchPanel
        from .qml_collaboration_panel import QMLCollaborationPanel
        from .qml_advanced_panel import QMLAdvancedPanel
        from .qml_settings_panel import QMLSettingsPanel
        
        # 创建面板实例
        self.panels = {
            0: QMLConverterPanel(self),
            1: QMLSplittingPanel(self),
            2: QMLAnalysisPanel(self),
            3: QMLVisualizationPanel(self),
            4: QMLSearchPanel(self),
            5: QMLCollaborationPanel(self),
            6: QMLAdvancedPanel(self),
            7: QMLSettingsPanel(self)
        }
        
        # 确保第一个导航项被激活
        if self.navigation_items:
            self.navigation_items[0].set_active(True)
        
        # 设置默认面板并确保显示
        self.switch_panel(0)
    
    def switch_panel(self, index):
        """切换面板"""
        # 更新导航状态
        for i, nav_item in enumerate(self.navigation_items):
            nav_item.set_active(i == index)
        
        # 清除当前内容
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
        
        # 添加新面板
        if index in self.panels:
            panel = self.panels[index]
            self.content_layout.addWidget(panel)
            panel.setVisible(True)  # 确保面板可见
            panel.update()  # 强制更新
            self.current_panel_index = index
            
            # 更新页面标题
            titles = [
                "数据集格式转换", "数据集划分", "数据集分析", "数据可视化",
                "数据搜索", "协作标注", "高级功能", "系统设置"
            ]
            if 0 <= index < len(titles):
                self.page_title.setText(titles[index])
        
        # 强制更新内容区域
        self.content_area.update()
    
    def apply_global_style(self):
        """应用全局样式"""
        style = """
        /* 主窗口 */
        QMainWindow {
            background-color: #f8fafc;
            color: #1e293b;
        }
        
        /* 导航面板 */
        #navigationPanel {
            background-color: #ffffff;
            border-right: 1px solid #e2e8f0;
        }
        
        /* 顶部品牌区域已移除，侧栏保持简洁，仅显示导航项 */
        
        /* 导航滚动区域 */
        #navScroll {
            background-color: transparent;
            border: none;
        }
        
        #navScroll QScrollBar:vertical {
            background-color: #f1f5f9;
            width: 6px;
            border-radius: 3px;
        }
        
        #navScroll QScrollBar::handle:vertical {
            background-color: #cbd5e1;
            border-radius: 3px;
            min-height: 20px;
        }
        
        #navScroll QScrollBar::handle:vertical:hover {
            background-color: #94a3b8;
        }
        
        /* 状态区域 */
        #statusWidget {
            background-color: #f8fafc;
            border-top: 1px solid #e2e8f0;
        }
        
        #statusLabel {
            font-size: 12px;
            color: #64748b;
        }
        
        /* 内容面板 */
        #contentPanel {
            background-color: #f8fafc;
        }
        
        #contentScroll {
            background-color: transparent;
            border: none;
        }
        
        #contentScroll QScrollBar:vertical {
            background-color: #f1f5f9;
            width: 8px;
            border-radius: 4px;
            margin: 0px;
        }
        
        #contentScroll QScrollBar::handle:vertical {
            background-color: #cbd5e1;
            border-radius: 4px;
            min-height: 20px;
        }
        
        #contentScroll QScrollBar::handle:vertical:hover {
            background-color: #94a3b8;
        }
        
        #contentScroll QScrollBar::add-line:vertical,
        #contentScroll QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        #pageTitle {
            font-size: 28px;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
        }
        
        #contentArea {
            background-color: transparent;
        }
        
        /* 通用按钮样式 */
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 500;
            color: #374151;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #f9fafb;
            border-color: #9ca3af;
        }
        
        QPushButton:pressed {
            background-color: #f3f4f6;
            border-color: #6b7280;
        }
        
        QPushButton:disabled {
            background-color: #f9fafb;
            border-color: #e5e7eb;
            color: #9ca3af;
        }
        
        /* 主要按钮 */
        QPushButton[buttonType="primary"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #3b82f6, stop:1 #2563eb);
            border: 1px solid #2563eb;
            color: white;
        }
        
        QPushButton[buttonType="primary"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2563eb, stop:1 #1d4ed8);
            border-color: #1d4ed8;
        }
        
        /* 成功按钮 */
        QPushButton[buttonType="success"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #10b981, stop:1 #059669);
            border: 1px solid #059669;
            color: white;
        }
        
        QPushButton[buttonType="success"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #059669, stop:1 #047857);
            border-color: #047857;
        }
        
        /* 警告按钮 */
        QPushButton[buttonType="warning"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f59e0b, stop:1 #d97706);
            border: 1px solid #d97706;
            color: white;
        }
        
        QPushButton[buttonType="warning"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #d97706, stop:1 #b45309);
            border-color: #b45309;
        }
        
        /* 危险按钮 */
        QPushButton[buttonType="danger"] {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ef4444, stop:1 #dc2626);
            border: 1px solid #dc2626;
            color: white;
        }
        
        QPushButton[buttonType="danger"]:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #dc2626, stop:1 #b91c1c);
            border-color: #b91c1c;
        }
        
        /* 输入框 */
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #111827;
        }
        
        QLineEdit:focus {
            border-color: #3b82f6;
            outline: none;
        }
        
        QLineEdit:disabled {
            background-color: #f9fafb;
            color: #9ca3af;
        }
        
        /* 文本区域 */
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #111827;
        }
        
        QTextEdit:focus {
            border-color: #3b82f6;
            outline: none;
        }
        
        /* 下拉框 */
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 14px;
            color: #111827;
        }
        
        QComboBox:hover {
            border-color: #9ca3af;
        }
        
        QComboBox:focus {
            border-color: #3b82f6;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 24px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #6b7280;
        }
        
        /* 标签 */
        QLabel {
            color: #374151;
            font-size: 14px;
        }
        
        /* 进度条 */
        QProgressBar {
            background-color: #e5e7eb;
            border: none;
            border-radius: 8px;
            text-align: center;
            font-size: 12px;
            color: #374151;
            height: 8px;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #3b82f6, stop:1 #1d4ed8);
            border-radius: 8px;
        }
        """
        
        self.setStyleSheet(style)
    
    def showEvent(self, event):
        """窗口显示事件"""
        super().showEvent(event)
        # 确保第一个面板正确显示
        if self.current_panel_index == 0 and 0 in self.panels:
            panel = self.panels[0]
            panel.setVisible(True)
            panel.update()
            self.content_area.update()