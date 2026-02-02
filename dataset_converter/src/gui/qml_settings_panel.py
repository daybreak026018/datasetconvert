"""
QML风格系统设置面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QFrame, QGridLayout, QComboBox,
    QCheckBox, QSpinBox, QSlider, QLineEdit, QTextEdit,
    QGroupBox, QTabWidget, QColorDialog, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QFont, QColor

from .qml_style_window import Card


class SettingItem(QFrame):
    """设置项组件"""
    
    value_changed = pyqtSignal(str, object)
    
    def __init__(self, title="", description="", setting_type="text", options=None, default_value=None, parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.setting_type = setting_type
        self.options = options or []
        self.default_value = default_value
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # 设置最小高度
        self.setMinimumHeight(80)
        
        # 标题和描述
        title_label = QLabel(self.title)
        title_label.setObjectName("settingTitle")
        layout.addWidget(title_label)
        
        if self.description:
            desc_label = QLabel(self.description)
            desc_label.setObjectName("settingDesc")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # 控件区域
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)
        
        # 根据类型创建控件
        if self.setting_type == "text":
            self.control = QLineEdit()
            if self.default_value:
                self.control.setText(str(self.default_value))
            self.control.textChanged.connect(lambda v: self.value_changed.emit(self.title, v))
            
        elif self.setting_type == "number":
            self.control = QSpinBox()
            self.control.setRange(0, 9999)
            if self.default_value:
                self.control.setValue(int(self.default_value))
            self.control.valueChanged.connect(lambda v: self.value_changed.emit(self.title, v))
            
        elif self.setting_type == "combo":
            self.control = QComboBox()
            self.control.addItems(self.options)
            if self.default_value and self.default_value in self.options:
                self.control.setCurrentText(self.default_value)
            self.control.currentTextChanged.connect(lambda v: self.value_changed.emit(self.title, v))
            
        elif self.setting_type == "checkbox":
            self.control = QCheckBox("启用")
            if self.default_value:
                self.control.setChecked(bool(self.default_value))
            self.control.toggled.connect(lambda v: self.value_changed.emit(self.title, v))
            
        elif self.setting_type == "slider":
            self.control = QSlider(Qt.Horizontal)
            self.control.setRange(0, 100)
            if self.default_value:
                self.control.setValue(int(self.default_value))
            
            self.value_label = QLabel(str(self.default_value or 0))
            self.value_label.setMinimumWidth(30)
            self.control.valueChanged.connect(self.update_slider_value)
            
            control_layout.addWidget(self.value_label)
            
        elif self.setting_type == "color":
            self.control = QPushButton("选择颜色")
            self.current_color = QColor(self.default_value or "#3b82f6")
            self.update_color_button()
            self.control.clicked.connect(self.select_color)
            
        elif self.setting_type == "path":
            self.control = QLineEdit()
            if self.default_value:
                self.control.setText(str(self.default_value))
            self.control.textChanged.connect(lambda v: self.value_changed.emit(self.title, v))
            
            browse_btn = QPushButton("浏览")
            browse_btn.setFixedWidth(60)
            browse_btn.clicked.connect(self.browse_path)
            control_layout.addWidget(browse_btn)
        
        control_layout.addWidget(self.control, 1)
        layout.addLayout(control_layout)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            SettingItem {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin: 2px 0;
            }
            
            SettingItem:hover {
                border-color: #cbd5e1;
                background-color: #f8fafc;
            }
            
            #settingTitle {
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }
            
            #settingDesc {
                font-size: 12px;
                color: #6b7280;
                line-height: 1.4;
            }
        """)
    
    def update_slider_value(self, value):
        """更新滑块值"""
        self.value_label.setText(str(value))
        self.value_changed.emit(self.title, value)
    
    def select_color(self):
        """选择颜色"""
        color = QColorDialog.getColor(self.current_color, self, "选择颜色")
        if color.isValid():
            self.current_color = color
            self.update_color_button()
            self.value_changed.emit(self.title, color.name())
    
    def update_color_button(self):
        """更新颜色按钮"""
        self.control.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_color.name()};
                border: 1px solid #d1d5db;
                border-radius: 6px;
                color: {"white" if self.current_color.lightness() < 128 else "black"};
                font-weight: 500;
                padding: 8px 16px;
            }}
        """)
    
    def browse_path(self):
        """浏览路径"""
        path = QFileDialog.getExistingDirectory(self, "选择目录")
        if path:
            self.control.setText(path)
    
    def get_value(self):
        """获取值"""
        if self.setting_type == "text" or self.setting_type == "path":
            return self.control.text()
        elif self.setting_type == "number" or self.setting_type == "slider":
            return self.control.value()
        elif self.setting_type == "combo":
            return self.control.currentText()
        elif self.setting_type == "checkbox":
            return self.control.isChecked()
        elif self.setting_type == "color":
            return self.current_color.name()
        return None


class QMLSettingsPanel(QWidget):
    """QML风格系统设置面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("DataForge", "DatasetConverter")
        self.setting_items = {}
        
        # 设置大小策略
        from PyQt5.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background-color: white;
            }
            
            QTabBar::tab {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-bottom: none;
                border-radius: 8px 8px 0 0;
                padding: 12px 20px;
                margin-right: 2px;
                font-weight: 500;
                color: #6b7280;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                color: #3b82f6;
                border-color: #3b82f6;
            }
            
            QTabBar::tab:hover {
                background-color: #f1f5f9;
                color: #374151;
            }
        """)
        
        # 通用设置标签页
        general_tab = self.create_general_tab()
        self.tab_widget.addTab(general_tab, "通用设置")
        
        # 界面设置标签页
        ui_tab = self.create_ui_tab()
        self.tab_widget.addTab(ui_tab, "界面设置")
        
        # 性能设置标签页
        performance_tab = self.create_performance_tab()
        self.tab_widget.addTab(performance_tab, "性能设置")
        
        # 高级设置标签页
        advanced_tab = self.create_advanced_tab()
        self.tab_widget.addTab(advanced_tab, "高级设置")
        
        layout.addWidget(self.tab_widget)
        
        # 操作按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.save_btn = QPushButton("保存设置")
        self.save_btn.setProperty("buttonType", "primary")
        self.save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_btn)
        
        self.reset_btn = QPushButton("恢复默认")
        self.reset_btn.setProperty("buttonType", "warning")
        self.reset_btn.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_btn)
        
        self.export_btn = QPushButton("导出配置")
        self.export_btn.setProperty("buttonType", "success")
        self.export_btn.clicked.connect(self.export_settings)
        button_layout.addWidget(self.export_btn)
        
        self.import_btn = QPushButton("导入配置")
        self.import_btn.clicked.connect(self.import_settings)
        button_layout.addWidget(self.import_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
    
    def create_general_tab(self):
        """创建通用设置标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        # 创建内容控件
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)  # 添加边距
        
        # 基本设置
        basic_card = Card("🔧 基本设置")
        basic_layout = QVBoxLayout()
        basic_layout.setSpacing(8)
        
        # 默认输入路径
        input_path_item = SettingItem(
            "默认输入路径",
            "设置默认的数据集输入目录",
            "path",
            default_value=""
        )
        input_path_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["default_input_path"] = input_path_item
        basic_layout.addWidget(input_path_item)
        
        # 默认输出路径
        output_path_item = SettingItem(
            "默认输出路径",
            "设置默认的结果输出目录",
            "path",
            default_value=""
        )
        output_path_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["default_output_path"] = output_path_item
        basic_layout.addWidget(output_path_item)
        
        # 自动保存
        auto_save_item = SettingItem(
            "自动保存",
            "启用后会自动保存工作进度",
            "checkbox",
            default_value=True
        )
        auto_save_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["auto_save"] = auto_save_item
        basic_layout.addWidget(auto_save_item)
        
        # 保存间隔
        save_interval_item = SettingItem(
            "保存间隔",
            "自动保存的时间间隔（分钟）",
            "number",
            default_value=5
        )
        save_interval_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["save_interval"] = save_interval_item
        basic_layout.addWidget(save_interval_item)
        
        basic_card.add_layout(basic_layout)
        layout.addWidget(basic_card)
        
        # 语言设置
        language_card = Card("🌐 语言设置")
        language_layout = QVBoxLayout()
        language_layout.setSpacing(8)
        
        # 界面语言
        language_item = SettingItem(
            "界面语言",
            "选择应用程序的显示语言",
            "combo",
            options=["简体中文", "English", "日本語"],
            default_value="简体中文"
        )
        language_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["language"] = language_item
        language_layout.addWidget(language_item)
        
        language_card.add_layout(language_layout)
        layout.addWidget(language_card)
        
        layout.addStretch()
        
        # 设置滚动区域
        scroll_area.setWidget(tab)
        return scroll_area
    
    def create_ui_tab(self):
        """创建界面设置标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        # 创建内容控件
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)  # 添加边距
        
        # 主题设置
        theme_card = Card("🎨 主题设置")
        theme_layout = QVBoxLayout()
        theme_layout.setSpacing(8)
        
        # 主题模式
        theme_mode_item = SettingItem(
            "主题模式",
            "选择应用程序的主题模式",
            "combo",
            options=["浅色模式", "深色模式", "跟随系统"],
            default_value="浅色模式"
        )
        theme_mode_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["theme_mode"] = theme_mode_item
        theme_layout.addWidget(theme_mode_item)
        
        # 主色调
        primary_color_item = SettingItem(
            "主色调",
            "设置应用程序的主要颜色",
            "color",
            default_value="#3b82f6"
        )
        primary_color_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["primary_color"] = primary_color_item
        theme_layout.addWidget(primary_color_item)
        
        # 字体大小
        font_size_item = SettingItem(
            "字体大小",
            "调整界面字体的大小",
            "slider",
            default_value=14
        )
        font_size_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["font_size"] = font_size_item
        theme_layout.addWidget(font_size_item)
        
        theme_card.add_layout(theme_layout)
        layout.addWidget(theme_card)
        
        # 窗口设置
        window_card = Card("🪟 窗口设置")
        window_layout = QVBoxLayout()
        window_layout.setSpacing(8)
        
        # 启动时最大化
        maximize_item = SettingItem(
            "启动时最大化",
            "程序启动时自动最大化窗口",
            "checkbox",
            default_value=False
        )
        maximize_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["start_maximized"] = maximize_item
        window_layout.addWidget(maximize_item)
        
        # 记住窗口位置
        remember_position_item = SettingItem(
            "记住窗口位置",
            "记住上次关闭时的窗口位置和大小",
            "checkbox",
            default_value=True
        )
        remember_position_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["remember_position"] = remember_position_item
        window_layout.addWidget(remember_position_item)
        
        window_card.add_layout(window_layout)
        layout.addWidget(window_card)
        
        layout.addStretch()
        
        # 设置滚动区域
        scroll_area.setWidget(tab)
        return scroll_area
    
    def create_performance_tab(self):
        """创建性能设置标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        # 创建内容控件
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)  # 添加边距
        
        # 处理设置
        processing_card = Card("⚡ 处理设置")
        processing_layout = QVBoxLayout()
        processing_layout.setSpacing(8)
        
        # 线程数
        thread_count_item = SettingItem(
            "处理线程数",
            "设置并行处理时使用的线程数量",
            "number",
            default_value=4
        )
        thread_count_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["thread_count"] = thread_count_item
        processing_layout.addWidget(thread_count_item)
        
        # 批处理大小
        batch_size_item = SettingItem(
            "批处理大小",
            "每批处理的文件数量",
            "number",
            default_value=32
        )
        batch_size_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["batch_size"] = batch_size_item
        processing_layout.addWidget(batch_size_item)
        
        # 内存限制
        memory_limit_item = SettingItem(
            "内存限制 (MB)",
            "设置程序使用的最大内存",
            "number",
            default_value=4096
        )
        memory_limit_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["memory_limit"] = memory_limit_item
        processing_layout.addWidget(memory_limit_item)
        
        processing_card.add_layout(processing_layout)
        layout.addWidget(processing_card)
        
        # 缓存设置
        cache_card = Card("💾 缓存设置")
        cache_layout = QVBoxLayout()
        cache_layout.setSpacing(8)
        
        # 启用缓存
        enable_cache_item = SettingItem(
            "启用缓存",
            "启用后可以提高重复操作的速度",
            "checkbox",
            default_value=True
        )
        enable_cache_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["enable_cache"] = enable_cache_item
        cache_layout.addWidget(enable_cache_item)
        
        # 缓存大小
        cache_size_item = SettingItem(
            "缓存大小 (MB)",
            "设置缓存使用的最大磁盘空间",
            "number",
            default_value=1024
        )
        cache_size_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["cache_size"] = cache_size_item
        cache_layout.addWidget(cache_size_item)
        
        cache_card.add_layout(cache_layout)
        layout.addWidget(cache_card)
        
        layout.addStretch()
        
        # 设置滚动区域
        scroll_area.setWidget(tab)
        return scroll_area
    
    def create_advanced_tab(self):
        """创建高级设置标签页"""
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        # 创建内容控件
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)  # 添加边距
        
        # 调试设置
        debug_card = Card("🐛 调试设置")
        debug_layout = QVBoxLayout()
        debug_layout.setSpacing(8)
        
        # 启用调试模式
        debug_mode_item = SettingItem(
            "调试模式",
            "启用后会显示详细的调试信息",
            "checkbox",
            default_value=False
        )
        debug_mode_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["debug_mode"] = debug_mode_item
        debug_layout.addWidget(debug_mode_item)
        
        # 日志级别
        log_level_item = SettingItem(
            "日志级别",
            "设置日志记录的详细程度",
            "combo",
            options=["ERROR", "WARNING", "INFO", "DEBUG"],
            default_value="INFO"
        )
        log_level_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["log_level"] = log_level_item
        debug_layout.addWidget(log_level_item)
        
        debug_card.add_layout(debug_layout)
        layout.addWidget(debug_card)
        
        # 实验性功能
        experimental_card = Card("🧪 实验性功能")
        experimental_layout = QVBoxLayout()
        experimental_layout.setSpacing(8)
        
        # GPU加速
        gpu_acceleration_item = SettingItem(
            "GPU加速",
            "启用GPU加速处理（需要支持的硬件）",
            "checkbox",
            default_value=False
        )
        gpu_acceleration_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["gpu_acceleration"] = gpu_acceleration_item
        experimental_layout.addWidget(gpu_acceleration_item)
        
        # AI辅助功能
        ai_assistance_item = SettingItem(
            "AI辅助功能",
            "启用AI辅助的智能功能（实验性）",
            "checkbox",
            default_value=False
        )
        ai_assistance_item.value_changed.connect(self.on_setting_changed)
        self.setting_items["ai_assistance"] = ai_assistance_item
        experimental_layout.addWidget(ai_assistance_item)
        
        experimental_card.add_layout(experimental_layout)
        layout.addWidget(experimental_card)
        
        # 配置信息
        info_card = Card("ℹ️ 配置信息")
        info_layout = QVBoxLayout()
        info_layout.setSpacing(8)
        
        # 配置文件路径
        config_path = self.settings.fileName()
        config_info = QLabel(f"配置文件位置:\n{config_path}")
        config_info.setStyleSheet("""
            QLabel {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                color: #6b7280;
            }
        """)
        config_info.setWordWrap(True)
        info_layout.addWidget(config_info)
        
        info_card.add_layout(info_layout)
        layout.addWidget(info_card)
        
        layout.addStretch()
        
        # 设置滚动区域
        scroll_area.setWidget(tab)
        return scroll_area
    
    def on_setting_changed(self, key, value):
        """设置值改变"""
        # 实时保存设置
        self.settings.setValue(key, value)
        
        # 应用某些设置的即时效果
        if key == "theme_mode":
            self.apply_theme_change(value)
        elif key == "font_size":
            self.apply_font_size_change(value)
        elif key == "primary_color":
            self.apply_color_change(value)
    
    def apply_theme_change(self, theme):
        """应用主题更改"""
        # 这里可以实现主题切换逻辑
        pass
    
    def apply_font_size_change(self, size):
        """应用字体大小更改"""
        # 这里可以实现字体大小调整逻辑
        pass
    
    def apply_color_change(self, color):
        """应用颜色更改"""
        # 这里可以实现主色调更改逻辑
        pass
    
    def load_settings(self):
        """加载设置"""
        for key, item in self.setting_items.items():
            value = self.settings.value(key)
            if value is not None:
                # 根据控件类型设置值
                if item.setting_type == "text" or item.setting_type == "path":
                    item.control.setText(str(value))
                elif item.setting_type == "number" or item.setting_type == "slider":
                    item.control.setValue(int(value))
                elif item.setting_type == "combo":
                    if str(value) in item.options:
                        item.control.setCurrentText(str(value))
                elif item.setting_type == "checkbox":
                    item.control.setChecked(bool(value))
                elif item.setting_type == "color":
                    item.current_color = QColor(str(value))
                    item.update_color_button()
    
    def save_settings(self):
        """保存设置"""
        for key, item in self.setting_items.items():
            value = item.get_value()
            self.settings.setValue(key, value)
        
        self.settings.sync()
        QMessageBox.information(self, "成功", "设置已保存")
    
    def reset_settings(self):
        """重置设置"""
        reply = QMessageBox.question(
            self, "确认", 
            "确定要恢复所有设置到默认值吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.settings.clear()
            
            # 重新设置默认值
            for key, item in self.setting_items.items():
                if item.default_value is not None:
                    if item.setting_type == "text" or item.setting_type == "path":
                        item.control.setText(str(item.default_value))
                    elif item.setting_type == "number" or item.setting_type == "slider":
                        item.control.setValue(int(item.default_value))
                    elif item.setting_type == "combo":
                        item.control.setCurrentText(str(item.default_value))
                    elif item.setting_type == "checkbox":
                        item.control.setChecked(bool(item.default_value))
                    elif item.setting_type == "color":
                        item.current_color = QColor(str(item.default_value))
                        item.update_color_button()
            
            QMessageBox.information(self, "成功", "设置已重置为默认值")
    
    def export_settings(self):
        """导出设置"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出配置文件", 
            "dataforge_config.ini",
            "配置文件 (*.ini);;所有文件 (*)"
        )
        
        if file_path:
            try:
                # 创建临时设置对象来导出
                export_settings = QSettings(file_path, QSettings.IniFormat)
                
                for key in self.settings.allKeys():
                    export_settings.setValue(key, self.settings.value(key))
                
                export_settings.sync()
                QMessageBox.information(self, "成功", f"配置已导出到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")
    
    def import_settings(self):
        """导入设置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入配置文件", 
            "",
            "配置文件 (*.ini);;所有文件 (*)"
        )
        
        if file_path:
            try:
                # 从文件导入设置
                import_settings = QSettings(file_path, QSettings.IniFormat)
                
                for key in import_settings.allKeys():
                    self.settings.setValue(key, import_settings.value(key))
                
                self.settings.sync()
                self.load_settings()  # 重新加载界面
                QMessageBox.information(self, "成功", "配置导入成功")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导入失败: {str(e)}")