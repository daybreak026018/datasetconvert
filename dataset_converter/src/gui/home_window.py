from pathlib import Path

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QGroupBox
from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap

from .main_window import MainWindow


class NavButton(QFrame):
    """自定义侧边栏导航按钮"""
    clicked = pyqtSignal(int)
    
    def __init__(self, text, icon_path, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("navButton")
        self.setProperty("class", "navButton")
        self.setFixedHeight(50)  # 高度固定
        
        # 允许样式表设置背景
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        layout = QHBoxLayout(self)  # 水平布局：图标左，文字右
        layout.setContentsMargins(20, 0, 10, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # 图标
        self.icon_label = QLabel()
        self.icon_label.setProperty("class", "navIcon")
        self.icon_label.setFixedSize(24, 24)
        if icon_path and Path(icon_path).exists():
            pixmap = QIcon(str(icon_path)).pixmap(20, 20)
            self.icon_label.setPixmap(pixmap)
            self.icon_label.setScaledContents(True)
        layout.addWidget(self.icon_label)
        
        # 文本
        self.text_label = QLabel(text)
        self.text_label.setProperty("class", "navText")
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout.addWidget(self.text_label)
        
        self.selected = False
        
    def set_selected(self, selected):
        self.selected = selected
        self.setProperty("selected", str(selected).lower())
        # 刷新样式
        self.style().unpolish(self)
        self.style().polish(self)
        self.text_label.style().unpolish(self.text_label)
        self.text_label.style().polish(self.text_label)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)


class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataForge v2.0")
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        self.setMinimumSize(1200, 800)
        self.resize(1200, 800)

        central = QWidget(self)
        self.setCentralWidget(central)

        # 主布局：水平 (左侧边栏 + 右侧内容)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- 左侧边栏 ---
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(280)  # 增加宽度以适应不同缩放比例
        main_layout.addWidget(sidebar)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # 侧边栏 Logo 区域
        logo_area = QFrame()
        logo_area.setFixedHeight(60)
        logo_area.setStyleSheet("background-color: #27ae60; border-bottom: 1px solid #2ecc71;") # 稍微深一点的绿色
        logo_layout = QHBoxLayout(logo_area)
        logo_layout.setContentsMargins(20, 0, 0, 0)
        
        logo_label = QLabel("DataForge")
        logo_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; font-family: 'Segoe UI', sans-serif;")
        logo_layout.addWidget(logo_label)
        
        sidebar_layout.addWidget(logo_area)
        
        # 导航按钮容器
        self.nav_buttons = []
        nav_container = QWidget()
        nav_layout = QVBoxLayout(nav_container)
        nav_layout.setContentsMargins(0, 10, 0, 0)
        nav_layout.setSpacing(2)
        nav_layout.setAlignment(Qt.AlignTop)
        
        menu_items = [
            "数据集格式转换", "数据集划分", "数据集分析", "数据可视化",
            "数据搜索", "协作标注", "高级功能", "设置"
        ]
        
        for idx, item_text in enumerate(menu_items):
            btn = NavButton(item_text, str(icon_path), idx)
            btn.clicked.connect(self.on_menu_change)
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)
            
        sidebar_layout.addWidget(nav_container)
        sidebar_layout.addStretch() # 底部留白

        # --- 右侧内容区域 ---
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        main_layout.addWidget(content_container)
        
        # 顶部 Header
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(60)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        header_title = QLabel("数据集处理中心")
        header_title.setObjectName("headerTitle")
        header_layout.addWidget(header_title)
        header_layout.addStretch()
        
        # 右上角用户信息占位
        user_info = QLabel("Admin")
        user_info.setStyleSheet("color: white; font-weight: bold;")
        header_layout.addWidget(user_info)
        
        content_layout.addWidget(header)
        
        # 内容区域
        from .converter_panel import ConverterPanel
        from .splitting_panel import SplittingPanel
        from .analysis_panel import AnalysisPanel
        from .settings_panel import SettingsPanel
        from .search_panel import SearchPanel
        from .advanced_panel import AdvancedPanel
        from .custom_tab_bar import CustomTabWidget
        
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(16, 16, 16, 16)
        
        # 初始化所有面板
        self.converter_panel = ConverterPanel(self)
        self.splitting_panel = SplittingPanel(self)
        self.analysis_panel = AnalysisPanel(self)
        self.settings_panel = SettingsPanel(self)
        self.search_panel = SearchPanel(self)
        self.collaboration_panel = self.create_collaboration_panel()
        self.advanced_panel = AdvancedPanel(self)
        self.visualization_panel = self.create_visualization_panel()
        
        self.content_layout.addWidget(self.converter_panel)
        content_layout.addWidget(self.content)

        # 连接主题管理器信号
        from .theme_manager import theme_manager
        theme_manager.theme_changed.connect(self.apply_theme)
        self.settings_panel.settings_changed.connect(self.apply_theme)

        # 初始化选中第一个
        self.current_index = 0
        self.nav_buttons[0].set_selected(True)
        
        # 应用样式
        from .styles import AppStyles
        self.setStyleSheet(AppStyles.get_main_window_style())
        
        # 初始应用主题
        self.apply_theme()

    def apply_theme(self):
        """应用当前主题"""
        from .styles import AppStyles
        from .theme_manager import theme_manager
        
        # 更新样式类属性
        theme_config = theme_manager.get_theme_config()
        colors = theme_config.get("colors", {})
        
        if "primary" in colors:
            AppStyles.PRIMARY_COLOR = colors["primary"]
        if "success" in colors:
            AppStyles.SUCCESS_COLOR = colors["success"]
        if "warning" in colors:
            AppStyles.WARNING_COLOR = colors["warning"]
        if "danger" in colors:
            AppStyles.DANGER_COLOR = colors["danger"]
        if "background" in colors:
            AppStyles.BACKGROUND_COLOR = colors["background"]
        if "card" in colors:
            AppStyles.CARD_COLOR = colors["card"]
        if "text" in colors:
            AppStyles.TEXT_COLOR = colors["text"]
        if "secondary_text" in colors:
            AppStyles.SECONDARY_TEXT = colors["secondary_text"]
        if "border" in colors:
            AppStyles.BORDER_COLOR = colors["border"]
            
        # 侧边栏和头部颜色 (如果没有定义则使用默认值)
        AppStyles.SIDEBAR_BG = colors.get("sidebar_bg", "#2c3e50")
        AppStyles.HEADER_BG = colors.get("header_bg", "#27ae60")
        
        # 重新应用样式表
        self.setStyleSheet(AppStyles.get_main_window_style())
        
        # 强制更新子组件样式
        for btn in self.nav_buttons:
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            
            # 更新选中的按钮样式
            if btn.selected:
                btn.text_label.style().unpolish(btn.text_label)
                btn.text_label.style().polish(btn.text_label)

    def on_menu_change(self, idx: int):
        if idx == self.current_index:
            return

        # 更新按钮状态
        self.nav_buttons[self.current_index].set_selected(False)
        self.nav_buttons[idx].set_selected(True)
        self.current_index = idx
        
        # 更新 Header 标题
        header_title = self.findChild(QLabel, "headerTitle")
        if header_title:
            header_title.setText(self.nav_buttons[idx].text_label.text())
            
        # 在切换面板前，确保当前面板的任务已完成或取消
        current_widgets = []
        for i in range(self.content_layout.count()):
            item = self.content_layout.itemAt(i)
            if item and item.widget():
                current_widgets.append(item.widget())
        
        # 检查搜索面板是否有正在运行的任务
        for widget in current_widgets:
            if hasattr(widget, 'progress_manager') and widget.progress_manager:
                widget.progress_manager.cleanup()
        
        # 清空右侧内容
        for widget in current_widgets:
            widget.setParent(None)
        
        # 根据选择显示对应面板
        if idx == 0:  # 数据集格式转换
            self.content_layout.addWidget(self.converter_panel)
        elif idx == 1:  # 数据集划分
            self.content_layout.addWidget(self.splitting_panel)
        elif idx == 2:  # 数据集分析
            self.content_layout.addWidget(self.analysis_panel)
        elif idx == 3:  # 数据可视化
            self.content_layout.addWidget(self.visualization_panel)
        elif idx == 4:  # 数据搜索
            self.content_layout.addWidget(self.search_panel)
        elif idx == 5:  # 协作标注
            self.content_layout.addWidget(self.collaboration_panel)
        elif idx == 6:  # 高级功能
            self.content_layout.addWidget(self.advanced_panel)
        elif idx == 7:  # 设置
            self.content_layout.addWidget(self.settings_panel)
        else:
            placeholder = QWidget()
            ph_layout = QVBoxLayout(placeholder)
            ph_layout.addWidget(QLabel("功能暂未实现，敬请期待"))
            self.content_layout.addWidget(placeholder)
    
    def create_visualization_panel(self):
        """创建可视化面板"""
        from .visualization_panel import VisualizationPanel
        return VisualizationPanel(self)

    def create_collaboration_panel(self) -> QWidget:
        """创建协作标注面板"""
        from PyQt5.QtWidgets import (
            QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, 
            QFileDialog, QSpinBox, QComboBox, QTextEdit, QFormLayout,
            QGroupBox, QTableWidget, QTableWidgetItem, QProgressBar,
            QMessageBox, QTabWidget
        )
        from PyQt5.QtCore import QThread, pyqtSignal, QTimer
        from pathlib import Path
        import shutil
        import random
        from .custom_tab_bar import CustomTabWidget
        
        class DatasetSplitWorker(QThread):
            progress_updated = pyqtSignal(int, int, str)
            finished = pyqtSignal(dict)
            error_occurred = pyqtSignal(str)
            
            def __init__(self, input_dir, output_dir, num_people, split_method, naming_pattern, custom_names=None):
                super().__init__()
                self.input_dir = Path(input_dir)
                self.output_dir = Path(output_dir)
                self.num_people = num_people
                self.split_method = split_method
                self.naming_pattern = naming_pattern
                self.custom_names = custom_names or []
                self.is_cancelled = False
            
            def cancel(self):
                self.is_cancelled = True
            
            def run(self):
                try:
                    # 获取图片文件
                    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
                    image_files = []
                    
                    for ext in image_extensions:
                        image_files.extend(self.input_dir.rglob(f"*{ext}"))
                        image_files.extend(self.input_dir.rglob(f"*{ext.upper()}"))
                    
                    if not image_files:
                        self.error_occurred.emit("未找到图片文件")
                        return
                    
                    total_files = len(image_files)
                    self.progress_updated.emit(0, total_files, f"找到 {total_files} 个图片文件")
                    
                    # 创建输出目录
                    self.output_dir.mkdir(parents=True, exist_ok=True)
                    
                    # 生成文件夹名称
                    if self.naming_pattern == 'custom' and self.custom_names:
                        folder_names = self.custom_names[:self.num_people]
                    elif self.naming_pattern == 'annotator_{i}':
                        folder_names = [f"annotator_{i+1}" for i in range(self.num_people)]
                    else:
                        folder_names = [f"person_{i+1}" for i in range(self.num_people)]
                    
                    # 创建子文件夹
                    for folder_name in folder_names:
                        (self.output_dir / folder_name).mkdir(exist_ok=True)
                        (self.output_dir / folder_name / "images").mkdir(exist_ok=True)
                        (self.output_dir / folder_name / "labels").mkdir(exist_ok=True)
                    
                    # 划分文件
                    if self.split_method == 'random':
                        random.shuffle(image_files)
                    elif self.split_method == 'folder_name':
                        image_files.sort(key=lambda x: x.parent.name)
                    else:  # sequential
                        image_files.sort(key=lambda x: x.name)
                    
                    # 分配文件
                    files_per_person = total_files // self.num_people
                    remainder = total_files % self.num_people
                    
                    current_index = 0
                    assignment_stats = {}
                    
                    for i, folder_name in enumerate(folder_names):
                        if self.is_cancelled:
                            return
                        
                        files_count = files_per_person
                        if i < remainder:
                            files_count += 1
                        
                        person_files = image_files[current_index:current_index + files_count]
                        current_index += files_count
                        assignment_stats[folder_name] = len(person_files)
                        
                        # 复制文件
                        for j, image_file in enumerate(person_files):
                            if self.is_cancelled:
                                return
                            
                            progress = (current_index - len(person_files) + j + 1)
                            self.progress_updated.emit(
                                progress, total_files, 
                                f"分配给 {folder_name}: {image_file.name}"
                            )
                            
                            # 复制图片文件
                            dest_image = self.output_dir / folder_name / "images" / image_file.name
                            shutil.copy2(image_file, dest_image)
                            
                            # 复制标签文件
                            for ext in ['.txt', '.xml', '.json']:
                                label_file = image_file.with_suffix(ext)
                                if label_file.exists():
                                    dest_label = self.output_dir / folder_name / "labels" / label_file.name
                                    shutil.copy2(label_file, dest_label)
                                    break
                    
                    result = {
                        'success': True,
                        'total_files': total_files,
                        'assignment_stats': assignment_stats,
                        'output_dir': str(self.output_dir)
                    }
                    
                    self.finished.emit(result)
                    
                except Exception as e:
                    self.error_occurred.emit(f"数据集划分失败: {str(e)}")
        
        class CollaborationPanel(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.split_worker = None
                self.init_ui()
            
            def init_ui(self):
                layout = QVBoxLayout(self)
                
                # 标题
                title = QLabel("协作标注管理")
                title.setProperty("labelType", "title")
                layout.addWidget(title)
                
                # 选项卡
                tab_widget = CustomTabWidget()
                
                # 数据集划分选项卡
                split_tab = self.create_split_tab()
                tab_widget.addTab(split_tab, "数据集划分")
                
                # 项目管理选项卡（占位）
                project_tab = QWidget()
                project_layout = QVBoxLayout(project_tab)
                project_layout.addWidget(QLabel("项目管理功能正在开发中"))
                tab_widget.addTab(project_tab, "项目管理")
                
                layout.addWidget(tab_widget)
            
            def create_split_tab(self):
                widget = QWidget()
                layout = QVBoxLayout(widget)
                
                # 输入输出设置
                io_group = QGroupBox("输入输出设置")
                io_layout = QVBoxLayout(io_group)
                
                # 输入目录
                input_layout = QHBoxLayout()
                self.input_label = QLabel("输入数据集: 未选择")
                btn_select_input = QPushButton("选择数据集")
                btn_select_input.clicked.connect(self.select_input_dataset)
                input_layout.addWidget(self.input_label, 1)
                input_layout.addWidget(btn_select_input)
                io_layout.addLayout(input_layout)
                
                # 输出目录
                output_layout = QHBoxLayout()
                self.output_label = QLabel("输出目录: 未选择")
                btn_select_output = QPushButton("选择输出目录")
                btn_select_output.clicked.connect(self.select_output_dir)
                output_layout.addWidget(self.output_label, 1)
                output_layout.addWidget(btn_select_output)
                io_layout.addLayout(output_layout)
                
                layout.addWidget(io_group)
                
                # 划分设置
                split_group = QGroupBox("划分设置")
                split_layout = QFormLayout(split_group)
                
                # 人数设置
                self.num_people_spin = QSpinBox()
                self.num_people_spin.setRange(2, 20)
                self.num_people_spin.setValue(3)
                self.num_people_spin.valueChanged.connect(self.update_preview)
                split_layout.addRow("划分人数:", self.num_people_spin)
                
                # 划分方法
                self.split_method_combo = QComboBox()
                self.split_method_combo.addItems([
                    "按序号顺序分配",
                    "随机分配", 
                    "按文件夹名称分配"
                ])
                split_layout.addRow("划分方法:", self.split_method_combo)
                
                # 命名模式
                self.naming_combo = QComboBox()
                self.naming_combo.addItems([
                    "person_1, person_2, ...",
                    "annotator_1, annotator_2, ...",
                    "自定义名称"
                ])
                self.naming_combo.currentTextChanged.connect(self.on_naming_changed)
                split_layout.addRow("文件夹命名:", self.naming_combo)
                
                # 自定义名称输入
                self.custom_names_text = QTextEdit()
                self.custom_names_text.setMaximumHeight(100)
                self.custom_names_text.setPlaceholderText("每行一个名称，例如:\n张三\n李四\n王五")
                self.custom_names_text.setVisible(False)
                split_layout.addRow("自定义名称:", self.custom_names_text)
                
                layout.addWidget(split_group)
                
                # 预览区域
                preview_group = QGroupBox("划分预览")
                preview_layout = QVBoxLayout(preview_group)
                
                self.preview_table = QTableWidget()
                self.preview_table.setColumnCount(3)
                self.preview_table.setHorizontalHeaderLabels(["文件夹名称", "预计文件数", "占比"])
                preview_layout.addWidget(self.preview_table)
                
                btn_update_preview = QPushButton("更新预览")
                btn_update_preview.clicked.connect(self.update_preview)
                preview_layout.addWidget(btn_update_preview)
                
                layout.addWidget(preview_group)
                
                # 操作按钮
                button_layout = QHBoxLayout()
                
                btn_start_split = QPushButton("开始划分")
                btn_start_split.setProperty("buttonType", "primary")
                btn_start_split.clicked.connect(self.start_dataset_split)
                
                btn_cancel = QPushButton("取消")
                btn_cancel.setProperty("buttonType", "danger")
                btn_cancel.clicked.connect(self.cancel_split)
                btn_cancel.setEnabled(False)
                self.btn_cancel = btn_cancel
                
                button_layout.addWidget(btn_start_split)
                button_layout.addWidget(btn_cancel)
                button_layout.addStretch()
                
                layout.addLayout(button_layout)
                
                # 进度条
                self.progress_bar = QProgressBar()
                self.progress_bar.setVisible(False)
                layout.addWidget(self.progress_bar)
                
                self.status_label = QLabel("")
                layout.addWidget(self.status_label)
                
                layout.addStretch()
                
                return widget
                
            def select_input_dataset(self):
                dir_path = QFileDialog.getExistingDirectory(self, "选择输入数据集")
                if dir_path:
                    self.input_label.setText(f"输入数据集: {dir_path}")
                    self.input_path = dir_path
                    self.update_preview()
            
            def select_output_dir(self):
                dir_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
                if dir_path:
                    self.output_label.setText(f"输出目录: {dir_path}")
                    self.output_path = dir_path
            
            def on_naming_changed(self, text):
                self.custom_names_text.setVisible(text == "自定义名称")
            
            def update_preview(self):
                # 简单的预览逻辑
                num_people = self.num_people_spin.value()
                
                self.preview_table.setRowCount(num_people)
                
                # 获取文件夹名称
                naming_pattern = self.naming_combo.currentText()
                if naming_pattern == "自定义名称":
                    custom_names = self.custom_names_text.toPlainText().strip().split('\n')
                    names = [name.strip() for name in custom_names if name.strip()][:num_people]
                    # 补齐
                    while len(names) < num_people:
                        names.append(f"未命名_{len(names)+1}")
                elif "annotator" in naming_pattern:
                    names = [f"annotator_{i+1}" for i in range(num_people)]
                else:
                    names = [f"person_{i+1}" for i in range(num_people)]
                
                for i in range(num_people):
                    self.preview_table.setItem(i, 0, QTableWidgetItem(names[i]))
                    self.preview_table.setItem(i, 1, QTableWidgetItem("待计算"))
                    self.preview_table.setItem(i, 2, QTableWidgetItem(f"{100/num_people:.1f}%"))
            
            def start_dataset_split(self):
                if not hasattr(self, 'input_path') or not hasattr(self, 'output_path'):
                    QMessageBox.warning(self, "提示", "请先选择输入和输出目录")
                    return
                
                num_people = self.num_people_spin.value()
                split_method_map = {
                    "按序号顺序分配": "sequential",
                    "随机分配": "random",
                    "按文件夹名称分配": "folder_name"
                }
                split_method = split_method_map.get(self.split_method_combo.currentText(), "sequential")
                
                naming_pattern_map = {
                    "person_1, person_2, ...": "person_{i}",
                    "annotator_1, annotator_2, ...": "annotator_{i}",
                    "自定义名称": "custom"
                }
                naming_pattern = naming_pattern_map.get(self.naming_combo.currentText(), "person_{i}")
                
                custom_names = None
                if naming_pattern == "custom":
                    custom_names = [name.strip() for name in self.custom_names_text.toPlainText().strip().split('\n') if name.strip()]
                
                self.split_worker = DatasetSplitWorker(
                    self.input_path, self.output_path, num_people, 
                    split_method, naming_pattern, custom_names
                )
                
                self.split_worker.progress_updated.connect(self.on_progress)
                self.split_worker.finished.connect(self.on_split_finished)
                self.split_worker.error_occurred.connect(self.on_split_error)
                
                self.progress_bar.setVisible(True)
                self.progress_bar.setValue(0)
                self.btn_cancel.setEnabled(True)
                self.status_label.setText("正在划分数据集...")
                
                self.split_worker.start()
            
            def cancel_split(self):
                if self.split_worker and self.split_worker.isRunning():
                    self.split_worker.cancel()
                    self.status_label.setText("正在取消...")
                    self.btn_cancel.setEnabled(False)
            
            def on_progress(self, current, total, message):
                self.progress_bar.setMaximum(total)
                self.progress_bar.setValue(current)
                self.status_label.setText(message)
            
            def on_split_finished(self, result):
                self.progress_bar.setVisible(False)
                self.btn_cancel.setEnabled(False)
                self.status_label.setText("划分完成")
                
                stats_msg = "划分统计:\n"
                for name, count in result['assignment_stats'].items():
                    stats_msg += f"{name}: {count} 张图片\n"
                
                QMessageBox.information(self, "完成", f"数据集划分成功！\n\n{stats_msg}")
            
            def on_split_error(self, error_msg):
                self.progress_bar.setVisible(False)
                self.btn_cancel.setEnabled(False)
                self.status_label.setText("发生错误")
                QMessageBox.critical(self, "错误", error_msg)

        return CollaborationPanel(self)
