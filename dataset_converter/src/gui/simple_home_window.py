"""
简洁版主窗口 - DataForge v2.2.0
采用现代简约设计风格
"""

from pathlib import Path
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QListWidget, QListWidgetItem, QFrame, QLabel, QSplitter
)


class SimpleHomeWindow(QMainWindow):
    """简洁版主窗口"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_panels()
        self.apply_simple_style()
    
    def init_ui(self):
        """初始化界面"""
        self.setWindowTitle("DataForge v2.2.0 - 数据集工具箱")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # 设置窗口图标
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # 创建中央控件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局 - 水平分割
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧导航面板
        self.nav_panel = self.create_nav_panel()
        splitter.addWidget(self.nav_panel)
        
        # 右侧内容面板
        self.content_panel = self.create_content_panel()
        splitter.addWidget(self.content_panel)
        
        # 设置分割比例
        splitter.setSizes([250, 950])
        splitter.setCollapsible(0, False)  # 导航面板不可折叠
        
        main_layout.addWidget(splitter)
    
    def create_nav_panel(self):
        """创建导航面板"""
        nav_widget = QWidget()
        nav_widget.setObjectName("navPanel")
        nav_layout = QVBoxLayout(nav_widget)
        nav_layout.setContentsMargins(0, 0, 0, 0)
        nav_layout.setSpacing(0)
        
        # 标题区域
        title_widget = QWidget()
        title_widget.setObjectName("titleWidget")
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(20, 20, 20, 10)
        
        # 应用标题
        app_title = QLabel("DataForge")
        app_title.setObjectName("appTitle")
        
        # 版本信息
        version_label = QLabel("v2.2.0")
        version_label.setObjectName("versionLabel")
        
        title_layout.addWidget(app_title)
        title_layout.addWidget(version_label)
        
        nav_layout.addWidget(title_widget)
        
        # 导航菜单
        self.nav_menu = QListWidget()
        self.nav_menu.setObjectName("navMenu")
        
        # 菜单项
        menu_items = [
            ("🔄", "格式转换", "数据集格式转换"),
            ("✂️", "数据划分", "数据集划分"),
            ("📊", "数据分析", "数据集分析"),
            ("📈", "数据可视化", "数据可视化"),
            ("🔍", "数据搜索", "数据搜索"),
            ("👥", "协作标注", "协作标注"),
            ("⚡", "高级功能", "高级功能"),
            ("⚙️", "设置", "系统设置")
        ]
        
        for icon, title, desc in menu_items:
            item = QListWidgetItem()
            item_widget = self.create_nav_item(icon, title, desc)
            item.setSizeHint(item_widget.sizeHint())
            self.nav_menu.addItem(item)
            self.nav_menu.setItemWidget(item, item_widget)
        
        nav_layout.addWidget(self.nav_menu)
        
        # 底部信息
        footer_widget = QWidget()
        footer_widget.setObjectName("footerWidget")
        footer_layout = QVBoxLayout(footer_widget)
        footer_layout.setContentsMargins(20, 10, 20, 20)
        
        status_label = QLabel("就绪")
        status_label.setObjectName("statusLabel")
        footer_layout.addWidget(status_label)
        
        nav_layout.addWidget(footer_widget)
        
        return nav_widget
    
    def create_nav_item(self, icon, title, desc):
        """创建导航项"""
        item_widget = QWidget()
        item_widget.setObjectName("navItem")
        
        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)
        
        # 图标
        icon_label = QLabel(icon)
        icon_label.setObjectName("navIcon")
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(Qt.AlignCenter)
        
        # 文本区域
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        
        title_label = QLabel(title)
        title_label.setObjectName("navTitle")
        
        desc_label = QLabel(desc)
        desc_label.setObjectName("navDesc")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(desc_label)
        
        layout.addWidget(icon_label)
        layout.addWidget(text_widget, 1)
        
        return item_widget
    
    def create_content_panel(self):
        """创建内容面板"""
        content_widget = QWidget()
        content_widget.setObjectName("contentPanel")
        
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # 内容头部
        header_widget = QWidget()
        header_widget.setObjectName("contentHeader")
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(30, 20, 30, 20)
        
        # 页面标题
        self.page_title = QLabel("数据集格式转换")
        self.page_title.setObjectName("pageTitle")
        
        header_layout.addWidget(self.page_title)
        header_layout.addStretch()
        
        content_layout.addWidget(header_widget)
        
        # 分隔线
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setObjectName("separator")
        content_layout.addWidget(separator)
        
        # 内容区域
        self.content_area = QWidget()
        self.content_area.setObjectName("contentArea")
        
        # 为内容区域设置初始布局
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(30, 20, 30, 30)
        
        content_layout.addWidget(self.content_area, 1)
        
        return content_widget
    
    def init_panels(self):
        """初始化面板"""
        # 导入面板
        from .simple_converter_panel import SimpleConverterPanel
        from .simple_splitting_panel import SimpleSplittingPanel
        from .simple_analysis_panel import SimpleAnalysisPanel
        from .simple_visualization_panel import SimpleVisualizationPanel
        from .simple_search_panel import SimpleSearchPanel
        from .simple_collaboration_panel import SimpleCollaborationPanel
        from .simple_advanced_panel import SimpleAdvancedPanel
        from .simple_settings_panel import SimpleSettingsPanel
        
        # 创建面板实例
        self.panels = {
            0: SimpleConverterPanel(self),
            1: SimpleSplittingPanel(self),
            2: SimpleAnalysisPanel(self),
            3: SimpleVisualizationPanel(self),
            4: SimpleSearchPanel(self),
            5: SimpleCollaborationPanel(self),
            6: SimpleAdvancedPanel(self),
            7: SimpleSettingsPanel(self)
        }
        
        # 设置默认面板
        self.current_panel = None
        self.switch_panel(0)
        
        # 连接导航菜单
        self.nav_menu.currentRowChanged.connect(self.switch_panel)
    
    def switch_panel(self, index):
        """切换面板"""
        if index == -1 or index not in self.panels:
            return
        
        # 清除当前内容
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
        
        # 设置新面板
        self.current_panel = self.panels[index]
        self.content_layout.addWidget(self.current_panel)
        
        # 更新页面标题
        titles = [
            "数据集格式转换", "数据集划分", "数据集分析", "数据可视化",
            "数据搜索", "协作标注", "高级功能", "系统设置"
        ]
        if 0 <= index < len(titles):
            self.page_title.setText(titles[index])
    
    def apply_simple_style(self):
        """应用简洁样式"""
        style = """
        /* 主窗口 */
        QMainWindow {
            background-color: #f8f9fa;
            color: #212529;
        }
        
        /* 导航面板 */
        #navPanel {
            background-color: #ffffff;
            border-right: 1px solid #e9ecef;
        }
        
        /* 标题区域 */
        #titleWidget {
            background-color: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }
        
        #appTitle {
            font-size: 24px;
            font-weight: bold;
            color: #495057;
            margin: 0;
        }
        
        #versionLabel {
            font-size: 12px;
            color: #6c757d;
            margin: 0;
        }
        
        /* 导航菜单 */
        #navMenu {
            background-color: transparent;
            border: none;
            outline: none;
        }
        
        #navMenu::item {
            border: none;
            outline: none;
        }
        
        #navMenu::item:selected {
            background-color: #e3f2fd;
        }
        
        /* 导航项 */
        #navItem {
            background-color: transparent;
            border-radius: 8px;
            margin: 2px 10px;
        }
        
        #navItem:hover {
            background-color: #f1f3f4;
        }
        
        #navIcon {
            font-size: 18px;
            color: #495057;
        }
        
        #navTitle {
            font-size: 14px;
            font-weight: 600;
            color: #212529;
            margin: 0;
        }
        
        #navDesc {
            font-size: 12px;
            color: #6c757d;
            margin: 0;
        }
        
        /* 底部区域 */
        #footerWidget {
            border-top: 1px solid #e9ecef;
        }
        
        #statusLabel {
            font-size: 12px;
            color: #6c757d;
        }
        
        /* 内容面板 */
        #contentPanel {
            background-color: #ffffff;
        }
        
        /* 内容头部 */
        #contentHeader {
            background-color: #ffffff;
        }
        
        #pageTitle {
            font-size: 20px;
            font-weight: 600;
            color: #212529;
            margin: 0;
        }
        
        /* 分隔线 */
        #separator {
            background-color: #e9ecef;
            border: none;
            height: 1px;
        }
        
        /* 内容区域 */
        #contentArea {
            background-color: #f8f9fa;
        }
        
        /* 通用卡片样式 */
        .card {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        /* 通用按钮样式 */
        QPushButton {
            background-color: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 14px;
            color: #495057;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #f8f9fa;
            border-color: #adb5bd;
        }
        
        QPushButton:pressed {
            background-color: #e9ecef;
        }
        
        /* 主要按钮 */
        QPushButton[buttonType="primary"] {
            background-color: #007bff;
            border-color: #007bff;
            color: white;
        }
        
        QPushButton[buttonType="primary"]:hover {
            background-color: #0056b3;
            border-color: #0056b3;
        }
        
        /* 成功按钮 */
        QPushButton[buttonType="success"] {
            background-color: #28a745;
            border-color: #28a745;
            color: white;
        }
        
        QPushButton[buttonType="success"]:hover {
            background-color: #1e7e34;
            border-color: #1e7e34;
        }
        
        /* 警告按钮 */
        QPushButton[buttonType="warning"] {
            background-color: #ffc107;
            border-color: #ffc107;
            color: #212529;
        }
        
        QPushButton[buttonType="warning"]:hover {
            background-color: #e0a800;
            border-color: #e0a800;
        }
        
        /* 危险按钮 */
        QPushButton[buttonType="danger"] {
            background-color: #dc3545;
            border-color: #dc3545;
            color: white;
        }
        
        QPushButton[buttonType="danger"]:hover {
            background-color: #c82333;
            border-color: #c82333;
        }
        
        /* 输入框 */
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 14px;
            color: #495057;
        }
        
        QLineEdit:focus {
            border-color: #80bdff;
            outline: none;
        }
        
        /* 文本区域 */
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 14px;
            color: #495057;
        }
        
        QTextEdit:focus {
            border-color: #80bdff;
            outline: none;
        }
        
        /* 下拉框 */
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #ced4da;
            border-radius: 4px;
            padding: 8px 12px;
            font-size: 14px;
            color: #495057;
        }
        
        QComboBox:hover {
            border-color: #adb5bd;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #6c757d;
        }
        
        /* 标签 */
        QLabel {
            color: #495057;
            font-size: 14px;
        }
        
        /* 组框 */
        QGroupBox {
            background-color: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: 600;
            font-size: 14px;
            color: #495057;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px;
            background-color: #ffffff;
        }
        
        /* 进度条 */
        QProgressBar {
            background-color: #e9ecef;
            border: none;
            border-radius: 4px;
            text-align: center;
            font-size: 12px;
            color: #495057;
        }
        
        QProgressBar::chunk {
            background-color: #007bff;
            border-radius: 4px;
        }
        """
        
        self.setStyleSheet(style)