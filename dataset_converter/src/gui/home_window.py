from pathlib import Path

from PyQt5.QtCore import QSize, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFrame

from .main_window import MainWindow


class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DataForge v2.0")
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))

        # 设置窗口尺寸，适应更多内容
        # 计算需要的最小宽度以容纳所有选项卡
        min_width = 1200  # 基础宽度
        
        # 根据菜单项数量调整宽度
        menu_items_count = len([
            "数据集格式转换", "数据集划分", "数据集分析", "数据可视化",
            "数据搜索", "协作标注", "高级功能", "设置"
        ])
        
        # 确保有足够宽度显示所有功能
        if menu_items_count > 6:
            min_width = max(min_width, menu_items_count * 150 + 400)
        
        self.setMinimumSize(min_width, 800)
        self.resize(min_width, 800)

        central = QWidget(self)
        self.setCentralWidget(central)

        outer = QHBoxLayout(central)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # 左侧功能列表
        self.menu = QListWidget()
        self.menu.setFixedWidth(260)
        self.menu.setIconSize(QSize(24, 24))
        
        menu_icon = QIcon(str(icon_path)) if icon_path.exists() else None
        
        # 添加功能菜单项
        menu_items = [
            "数据集格式转换",
            "数据集划分", 
            "数据集分析",
            "数据可视化",
            "数据搜索",
            "协作标注",
            "高级功能",
            "设置"
        ]
        
        for item_text in menu_items:
            item = QListWidgetItem(item_text)
            if menu_icon:
                item.setIcon(menu_icon)
            self.menu.addItem(item)
            
        outer.addWidget(self.menu)

        # 分隔线
        sep = QFrame()
        sep.setFrameShape(QFrame.VLine)
        sep.setFrameShadow(QFrame.Sunken)
        outer.addWidget(sep)

        # 右侧内容区
        from .converter_panel import ConverterPanel
        from .splitting_panel import SplittingPanel
        from .analysis_panel import AnalysisPanel
        from .settings_panel import SettingsPanel
        from .search_panel import SearchPanel
        # from .collaboration_panel import CollaborationPanel
        from .advanced_panel import AdvancedPanel
        from .custom_tab_bar import CustomTabWidget
        
        self.content = QWidget()
        content_layout = QVBoxLayout(self.content)
        content_layout.setContentsMargins(16, 16, 16, 16)
        
        # 初始化所有面板
        self.converter_panel = ConverterPanel(self)
        self.splitting_panel = SplittingPanel(self)
        self.analysis_panel = AnalysisPanel(self)
        self.settings_panel = SettingsPanel(self)
        self.search_panel = SearchPanel(self)
        # self.collaboration_panel = CollaborationPanel(self)
        self.collaboration_panel = self.create_collaboration_panel()
        self.advanced_panel = AdvancedPanel(self)
        self.visualization_panel = self.create_visualization_panel()
        
        content_layout.addWidget(self.converter_panel)
        outer.addWidget(self.content)
        
        # 连接主题管理器信号
        from .theme_manager import theme_manager
        theme_manager.theme_changed.connect(self.apply_theme)
        self.settings_panel.settings_changed.connect(self.apply_theme)

        # 切换逻辑
        self.menu.currentRowChanged.connect(self.on_menu_change)
        self.menu.setCurrentRow(0)
        
        # 在所有组件初始化完成后应用主题
        self.apply_theme()

    def on_menu_change(self, idx: int):
        # 在切换面板前，确保当前面板的任务已完成或取消
        current_widgets = []
        for i in range(self.content.layout().count()):
            item = self.content.layout().itemAt(i)
            if item and item.widget():
                current_widgets.append(item.widget())
        
        # 检查搜索面板是否有正在运行的任务
        for widget in current_widgets:
            if hasattr(widget, 'progress_manager') and widget.progress_manager:
                # 如果有正在运行的任务，取消它
                widget.progress_manager.cleanup()
        
        # 清空右侧内容
        for widget in current_widgets:
            widget.setParent(None)
        
        # 根据选择显示对应面板
        if idx == 0:  # 数据集格式转换
            self.content.layout().addWidget(self.converter_panel)
        elif idx == 1:  # 数据集划分
            self.content.layout().addWidget(self.splitting_panel)
        elif idx == 2:  # 数据集分析
            self.content.layout().addWidget(self.analysis_panel)
        elif idx == 3:  # 数据可视化
            self.content.layout().addWidget(self.visualization_panel)
        elif idx == 4:  # 数据搜索
            self.content.layout().addWidget(self.search_panel)
        elif idx == 5:  # 协作标注
            self.content.layout().addWidget(self.collaboration_panel)
        elif idx == 6:  # 高级功能
            self.content.layout().addWidget(self.advanced_panel)
        elif idx == 7:  # 设置
            self.content.layout().addWidget(self.settings_panel)
        else:
            placeholder = QWidget()
            ph_layout = QVBoxLayout(placeholder)
            from PyQt5.QtWidgets import QLabel
            ph_layout.addWidget(QLabel("功能暂未实现，敬请期待"))
            self.content.layout().addWidget(placeholder)
    
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
                
                # 进度显示
                self.progress_bar = QProgressBar()
                self.progress_bar.setVisible(False)
                layout.addWidget(self.progress_bar)
                
                self.status_label = QLabel("")
                layout.addWidget(self.status_label)
                
                return widget
            
            def select_input_dataset(self):
                directory = QFileDialog.getExistingDirectory(self, "选择数据集目录")
                if directory:
                    self.input_label.setText(f"输入数据集: {directory}")
                    self.update_preview()
            
            def select_output_dir(self):
                directory = QFileDialog.getExistingDirectory(self, "选择输出目录")
                if directory:
                    self.output_label.setText(f"输出目录: {directory}")
            
            def on_naming_changed(self, text):
                is_custom = "自定义" in text
                self.custom_names_text.setVisible(is_custom)
            
            def update_preview(self):
                input_dir = self.input_label.text().replace("输入数据集: ", "")
                if input_dir == "未选择":
                    return
                
                try:
                    # 统计图片文件数量
                    input_path = Path(input_dir)
                    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
                    image_files = []
                    
                    for ext in image_extensions:
                        image_files.extend(input_path.rglob(f"*{ext}"))
                        image_files.extend(input_path.rglob(f"*{ext.upper()}"))
                    
                    total_files = len(image_files)
                    if total_files == 0:
                        QMessageBox.warning(self, "警告", "未找到图片文件")
                        return
                    
                    # 生成文件夹名称
                    num_people = self.num_people_spin.value()
                    folder_names = self._get_folder_names()
                    
                    # 计算每人分配的文件数
                    files_per_person = total_files // num_people
                    remainder = total_files % num_people
                    
                    # 更新预览表格
                    self.preview_table.setRowCount(num_people)
                    
                    for i, folder_name in enumerate(folder_names):
                        files_count = files_per_person
                        if i < remainder:
                            files_count += 1
                        
                        percentage = (files_count / total_files) * 100
                        
                        self.preview_table.setItem(i, 0, QTableWidgetItem(folder_name))
                        self.preview_table.setItem(i, 1, QTableWidgetItem(str(files_count)))
                        self.preview_table.setItem(i, 2, QTableWidgetItem(f"{percentage:.1f}%"))
                    
                    self.status_label.setText(f"总计 {total_files} 个图片文件，将分配给 {num_people} 个标注员")
                    
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"预览失败: {str(e)}")
            
            def _get_folder_names(self):
                num_people = self.num_people_spin.value()
                naming_text = self.naming_combo.currentText()
                
                if "自定义" in naming_text:
                    custom_names = [
                        line.strip() for line in self.custom_names_text.toPlainText().split('\n') 
                        if line.strip()
                    ]
                    if len(custom_names) >= num_people:
                        return custom_names[:num_people]
                    else:
                        for i in range(len(custom_names), num_people):
                            custom_names.append(f"标注员{i+1}")
                        return custom_names
                elif "annotator" in naming_text:
                    return [f"annotator_{i+1}" for i in range(num_people)]
                else:
                    return [f"person_{i+1}" for i in range(num_people)]
            
            def start_dataset_split(self):
                # 验证输入
                input_dir = self.input_label.text().replace("输入数据集: ", "")
                output_dir = self.output_label.text().replace("输出目录: ", "")
                
                if input_dir == "未选择":
                    QMessageBox.warning(self, "警告", "请选择输入数据集")
                    return
                
                if output_dir == "未选择":
                    QMessageBox.warning(self, "警告", "请选择输出目录")
                    return
                
                # 确认操作
                reply = QMessageBox.question(
                    self, "确认划分", 
                    f"确定要将数据集划分给 {self.num_people_spin.value()} 个标注员吗？",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply != QMessageBox.Yes:
                    return
                
                # 准备参数
                split_method_map = {
                    "按序号顺序分配": "sequential",
                    "随机分配": "random",
                    "按文件夹名称分配": "folder_name"
                }
                
                naming_pattern_map = {
                    "person_1, person_2, ...": "person_{i}",
                    "annotator_1, annotator_2, ...": "annotator_{i}",
                    "自定义名称": "custom"
                }
                
                split_method = split_method_map[self.split_method_combo.currentText()]
                naming_pattern = naming_pattern_map[self.naming_combo.currentText()]
                
                custom_names = None
                if naming_pattern == "custom":
                    custom_names = [
                        line.strip() for line in self.custom_names_text.toPlainText().split('\n') 
                        if line.strip()
                    ]
                
                # 启动工作线程
                self.split_worker = DatasetSplitWorker(
                    input_dir, output_dir, self.num_people_spin.value(),
                    split_method, naming_pattern, custom_names
                )
                
                self.split_worker.progress_updated.connect(self.update_progress)
                self.split_worker.finished.connect(self.on_split_finished)
                self.split_worker.error_occurred.connect(self.on_split_error)
                
                # 显示进度
                self.progress_bar.setVisible(True)
                self.progress_bar.setRange(0, 100)
                self.btn_cancel.setEnabled(True)
                
                self.split_worker.start()
            
            def cancel_split(self):
                if self.split_worker and self.split_worker.isRunning():
                    self.split_worker.cancel()
                    self.split_worker.wait(3000)
                    if self.split_worker.isRunning():
                        self.split_worker.terminate()
                    
                    self.progress_bar.setVisible(False)
                    self.btn_cancel.setEnabled(False)
                    self.status_label.setText("操作已取消")
            
            def update_progress(self, current, total, description):
                if total > 0:
                    progress = int((current / total) * 100)
                    self.progress_bar.setValue(progress)
                
                self.status_label.setText(description)
            
            def on_split_finished(self, result):
                self.progress_bar.setVisible(False)
                self.btn_cancel.setEnabled(False)
                
                if result['success']:
                    stats = result['assignment_stats']
                    total_files = result['total_files']
                    
                    message = f"数据集划分完成！\n\n"
                    message += f"总文件数: {total_files}\n"
                    message += f"输出目录: {result['output_dir']}\n\n"
                    message += "分配详情:\n"
                    
                    for folder_name, count in stats.items():
                        percentage = (count / total_files) * 100
                        message += f"• {folder_name}: {count} 个文件 ({percentage:.1f}%)\n"
                    
                    QMessageBox.information(self, "完成", message)
                    
                    # 询问是否打开输出目录
                    reply = QMessageBox.question(
                        self, "打开目录", "是否打开输出目录查看结果？",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    
                    if reply == QMessageBox.Yes:
                        import os
                        os.startfile(result['output_dir'])
                    
                    self.status_label.setText("数据集划分完成")
                else:
                    QMessageBox.critical(self, "错误", "数据集划分失败")
            
            def on_split_error(self, error_message):
                self.progress_bar.setVisible(False)
                self.btn_cancel.setEnabled(False)
                self.status_label.setText("操作失败")
                
                QMessageBox.critical(self, "错误", error_message)
        
        return CollaborationPanel(self)
    
    def create_visualization_panel(self) -> QWidget:
        """创建可视化面板"""
        from PyQt5.QtWidgets import QLabel, QPushButton, QFileDialog, QMessageBox
        
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 标题
        title = QLabel("数据可视化")
        title.setProperty("labelType", "title")
        layout.addWidget(title)
        
        # 数据集选择
        dataset_layout = QHBoxLayout()
        self.viz_dataset_label = QLabel("数据集: 未选择")
        self.viz_dataset_label.setProperty("labelType", "status")
        
        btn_select_dataset = QPushButton("选择数据集")
        btn_select_dataset.setProperty("buttonType", "default")
        btn_select_dataset.clicked.connect(self.select_visualization_dataset)
        
        dataset_layout.addWidget(self.viz_dataset_label, 1)
        dataset_layout.addWidget(btn_select_dataset)
        layout.addLayout(dataset_layout)
        
        # 可视化选项
        from PyQt5.QtWidgets import QGroupBox, QGridLayout
        
        viz_group = QGroupBox("可视化选项")
        viz_layout = QGridLayout(viz_group)
        
        # 统计仪表板按钮
        btn_dashboard = QPushButton("生成统计仪表板")
        btn_dashboard.setProperty("buttonType", "primary")
        btn_dashboard.clicked.connect(self.create_dashboard)
        viz_layout.addWidget(btn_dashboard, 0, 0)
        
        # 交互式可视化按钮
        btn_interactive = QPushButton("生成交互式图表")
        btn_interactive.setProperty("buttonType", "success")
        btn_interactive.clicked.connect(self.create_interactive_viz)
        viz_layout.addWidget(btn_interactive, 0, 1)
        
        # 主题选择
        from PyQt5.QtWidgets import QComboBox
        viz_layout.addWidget(QLabel("图表主题:"), 1, 0)
        self.viz_theme_combo = QComboBox()
        self.viz_theme_combo.addItems(["light", "dark"])
        viz_layout.addWidget(self.viz_theme_combo, 1, 1)
        
        layout.addWidget(viz_group)
        
        # 结果显示
        self.viz_result_label = QLabel("请选择数据集并生成可视化")
        self.viz_result_label.setProperty("labelType", "subtitle")
        layout.addWidget(self.viz_result_label)
        
        layout.addStretch()
        
        # 存储数据
        self.viz_annotations = []
        self.viz_dataset_dir = None
        self.visualizer = None  # 延迟初始化
        
        return panel
    
    def select_visualization_dataset(self):
        """选择可视化数据集"""
        from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog
        
        try:
            directory = QFileDialog.getExistingDirectory(self, "选择数据集目录")
            if not directory:
                return
            
            # 显示验证状态
            self.viz_result_label.setText("正在验证数据集格式...")
            
            # 验证数据集结构
            from ..core.dataset_validator import DatasetValidator
            dataset_info = DatasetValidator.get_dataset_info(Path(directory))
            
            if not dataset_info["is_valid"]:
                QMessageBox.critical(self, "数据集格式错误", 
                    f"数据集格式不符合要求:\n{dataset_info['message']}\n\n"
                    f"请确保数据集采用以下结构:\n"
                    f"数据集名称/\n"
                    f"├── images/\n"
                    f"│   ├── train/\n"
                    f"│   ├── test/\n"
                    f"│   └── val/\n"
                    f"└── labels/\n"
                    f"    ├── train/\n"
                    f"    ├── test/\n"
                    f"    └── val/")
                self.viz_result_label.setText("数据集格式验证失败")
                return
            
            # 自动检测格式或让用户选择
            detected_format = dataset_info["detected_format"]
            if detected_format:
                # 询问用户是否使用检测到的格式
                reply = QMessageBox.question(self, "格式检测", 
                    f"检测到数据集格式为: {detected_format.upper()}\n是否使用此格式？",
                    QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    format_name = detected_format
                else:
                    # 让用户手动选择
                    from ..core.converter import PARSERS
                    formats = list(PARSERS.keys())
                    format_name, ok = QInputDialog.getItem(self, "选择格式", "数据集格式:", formats, 0, False)
                    if not ok:
                        return
            else:
                # 无法自动检测，让用户选择
                from ..core.converter import PARSERS
                formats = list(PARSERS.keys())
                format_name, ok = QInputDialog.getItem(self, "选择格式", "数据集格式:", formats, 0, False)
                if not ok:
                    return
            
            # 显示加载状态
            self.viz_result_label.setText("正在加载数据集...")
            
            # 解析数据集
            self.viz_dataset_dir = Path(directory)
            self.viz_dataset_label.setText(f"数据集: {directory}")
            
            from ..core.converter import PARSERS
            parser = PARSERS[format_name]
            
            # 如果解析器支持标签映射，设置空映射避免错误
            if hasattr(parser, "set_label_map"):
                parser.set_label_map({})
            
            self.viz_annotations = parser.parse(self.viz_dataset_dir)
            
            if self.viz_annotations:
                stats = dataset_info["statistics"]
                self.viz_result_label.setText(
                    f"数据集加载成功！\n"
                    f"格式: {format_name.upper()}\n"
                    f"图片总数: {stats['total_images']}\n"
                    f"标签总数: {stats['total_labels']}\n"
                    f"子集: {', '.join(stats['subsets'].keys())}\n"
                    f"解析到 {len(self.viz_annotations)} 个有效标注"
                )
            else:
                self.viz_result_label.setText("数据集结构正确，但未找到有效的标注数据")
                QMessageBox.warning(self, "警告", "数据集结构正确，但未找到有效的标注数据，请检查标签文件内容")
            
        except ImportError as e:
            QMessageBox.critical(self, "导入错误", f"模块导入失败: {e}")
            self.viz_result_label.setText("模块导入失败")
        except FileNotFoundError as e:
            QMessageBox.critical(self, "文件错误", f"找不到文件: {e}")
            self.viz_result_label.setText("文件未找到")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据集失败: {str(e)}")
            self.viz_result_label.setText("数据集加载失败")
            print(f"详细错误信息: {e}")  # 调试用
    
    def create_dashboard(self):
        """创建统计仪表板"""
        if not self.viz_annotations:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "提示", "请先选择数据集")
            return
        
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        
        output_dir = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if not output_dir:
            return
        
        try:
            # 显示处理状态
            self.viz_result_label.setText("正在生成统计仪表板...")
            
            # 延迟初始化可视化器
            if self.visualizer is None:
                from ..core.enhanced_visualizer import EnhancedVisualizer
                self.visualizer = EnhancedVisualizer()
            
            theme = self.viz_theme_combo.currentText()
            self.visualizer.create_statistics_dashboard(
                self.viz_annotations, Path(output_dir), theme
            )
            
            self.viz_result_label.setText(f"统计仪表板已生成到: {output_dir}")
            QMessageBox.information(self, "完成", "统计仪表板生成完成！")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成失败: {str(e)}")
            self.viz_result_label.setText("仪表板生成失败")
            print(f"仪表板生成错误: {e}")  # 调试用
    
    def create_interactive_viz(self):
        """创建交互式可视化"""
        if not self.viz_annotations:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "提示", "请先选择数据集")
            return
        
        from PyQt5.QtWidgets import QFileDialog, QMessageBox
        
        output_dir = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if not output_dir:
            return
        
        try:
            # 显示处理状态
            self.viz_result_label.setText("正在生成交互式图表...")
            
            # 延迟初始化可视化器
            if self.visualizer is None:
                from ..core.enhanced_visualizer import EnhancedVisualizer
                self.visualizer = EnhancedVisualizer()
            
            self.visualizer.create_interactive_visualization(
                self.viz_annotations, Path(output_dir)
            )
            
            self.viz_result_label.setText(f"交互式图表已生成到: {output_dir}")
            QMessageBox.information(self, "完成", "交互式可视化生成完成！")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成失败: {str(e)}")
            self.viz_result_label.setText("交互式图表生成失败")
            print(f"交互式图表生成错误: {e}")  # 调试用
    
    def apply_theme(self, theme_name: str = None):
        """应用主题"""
        from .theme_manager import theme_manager
        
        if theme_name is None:
            theme_name = theme_manager.get_current_theme()
        
        # 生成并应用样式表
        stylesheet = theme_manager.generate_stylesheet(theme_name)
        
        # 使用setUpdatesEnabled来减少闪烁
        self.setUpdatesEnabled(False)
        try:
            self.setStyleSheet(stylesheet)
            
            # 更新转换面板的按钮样式
            if hasattr(self, 'converter_panel') and hasattr(self.converter_panel, 'apply_theme'):
                self.converter_panel.apply_theme()
                
            # 确保所有选项卡控件重新配置显示
            self._ensure_tab_display()
                
        finally:
            self.setUpdatesEnabled(True)
            self.update()  # 强制重绘
    
    def _ensure_tab_display(self):
        """确保所有选项卡正确显示"""
        # 查找所有CustomTabWidget并重新配置
        from .custom_tab_bar import CustomTabWidget
        
        def configure_tab_widgets(widget):
            for child in widget.findChildren(CustomTabWidget):
                if hasattr(child, '_configure_display'):
                    QTimer.singleShot(10, child._configure_display)
            
            # 递归处理子控件
            for child in widget.children():
                if hasattr(child, 'findChildren'):
                    configure_tab_widgets(child)
        
        configure_tab_widgets(self)
    
    def resizeEvent(self, event):
        """重写窗口大小调整事件"""
        super().resizeEvent(event)
        # 窗口大小变化时，确保选项卡正确显示
        QTimer.singleShot(50, self._ensure_tab_display)
    
    def closeEvent(self, event):
        """窗口关闭事件 - 确保所有任务被正确清理"""
        try:
            # 清理所有面板的进度管理器
            panels_with_progress = [
                self.search_panel,
                self.converter_panel,
                self.splitting_panel,
                self.analysis_panel,
                self.collaboration_panel
            ]
            
            for panel in panels_with_progress:
                if hasattr(panel, 'progress_manager') and panel.progress_manager:
                    panel.progress_manager.cleanup()
            
        except Exception as e:
            print(f"清理资源时发生错误: {e}")
        
        super().closeEvent(event)
