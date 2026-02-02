"""
QML风格数据可视化面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QFrame,
    QGridLayout, QComboBox, QCheckBox, QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPixmap

from .qml_style_window import Card


class VisualizationWorker(QThread):
    """可视化工作线程"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, str)
    
    def __init__(self, input_path, output_path, chart_types, sample_count):
        super().__init__()
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.chart_types = chart_types
        self.sample_count = sample_count
    
    def run(self):
        try:
            self.progress_updated.emit(10, "正在加载数据集...")
            
            # 模拟可视化过程
            import time
            for i in range(10, 101, 18):
                time.sleep(0.3)
                if i == 28:
                    self.progress_updated.emit(i, "正在生成统计图表...")
                elif i == 46:
                    self.progress_updated.emit(i, "正在创建样本展示...")
                elif i == 64:
                    self.progress_updated.emit(i, "正在生成分布图...")
                elif i == 82:
                    self.progress_updated.emit(i, "正在保存结果...")
                else:
                    self.progress_updated.emit(i, f"可视化进度 {i}%")
            
            self.progress_updated.emit(100, "可视化完成")
            self.finished.emit(True, "数据可视化成功完成！", str(self.output_path))
            
        except Exception as e:
            self.finished.emit(False, f"可视化失败: {str(e)}", "")


class ChartOption(QFrame):
    """图表选项组件"""
    
    def __init__(self, title="", description="", icon="📊", parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.icon = icon
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 复选框
        self.checkbox = QCheckBox()
        self.checkbox.setChecked(True)
        layout.addWidget(self.checkbox)
        
        # 图标
        icon_label = QLabel(self.icon)
        icon_label.setObjectName("chartIcon")
        icon_label.setFixedSize(24, 24)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # 文本信息
        text_layout = QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_label = QLabel(self.title)
        title_label.setObjectName("chartTitle")
        text_layout.addWidget(title_label)
        
        desc_label = QLabel(self.description)
        desc_label.setObjectName("chartDesc")
        text_layout.addWidget(desc_label)
        
        layout.addLayout(text_layout, 1)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            ChartOption {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            
            ChartOption:hover {
                border-color: #cbd5e1;
                background-color: #f1f5f9;
            }
            
            #chartIcon {
                font-size: 20px;
                color: #3b82f6;
            }
            
            #chartTitle {
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }
            
            #chartDesc {
                font-size: 12px;
                color: #6b7280;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #d1d5db;
                border-radius: 4px;
                background-color: white;
            }
            
            QCheckBox::indicator:checked {
                background-color: #3b82f6;
                border-color: #3b82f6;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xMC42IDEuNEw0LjIgNy44TDEuNCA1IiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            QCheckBox::indicator:hover {
                border-color: #9ca3af;
            }
        """)
    
    def is_checked(self):
        """是否选中"""
        return self.checkbox.isChecked()


class PreviewArea(QFrame):
    """预览区域组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        # 标题
        title_label = QLabel("预览区域")
        title_label.setObjectName("previewTitle")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 预览内容
        self.preview_label = QLabel("选择数据集后将显示预览")
        self.preview_label.setObjectName("previewContent")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setMinimumHeight(200)
        layout.addWidget(self.preview_label, 1)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            PreviewArea {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8fafc, stop:1 #e2e8f0);
                border: 2px dashed #cbd5e1;
                border-radius: 12px;
            }
            
            #previewTitle {
                font-size: 16px;
                font-weight: 600;
                color: #374151;
            }
            
            #previewContent {
                font-size: 14px;
                color: #6b7280;
                font-style: italic;
            }
        """)
    
    def update_preview(self, text):
        """更新预览"""
        self.preview_label.setText(text)


class QMLVisualizationPanel(QWidget):
    """QML风格数据可视化面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.input_path = ""
        self.output_path = ""
        
        # 设置大小策略
        from PyQt5.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 路径设置卡片
        path_card = Card("📁 路径设置")
        path_layout = QGridLayout()
        path_layout.setSpacing(16)
        
        # 输入路径
        input_layout = self.create_path_selector("数据集目录", True)
        path_layout.addLayout(input_layout, 0, 0)
        
        # 输出路径
        output_layout = self.create_path_selector("输出目录", False)
        path_layout.addLayout(output_layout, 0, 1)
        
        path_card.add_layout(path_layout)
        layout.addWidget(path_card)
        
        # 可视化选项卡片
        options_card = Card("📊 可视化选项")
        options_layout = QVBoxLayout()
        options_layout.setSpacing(16)
        
        # 图表类型选择
        chart_layout = QGridLayout()
        chart_layout.setSpacing(12)
        
        # 创建图表选项
        self.chart_options = []
        
        chart_data = [
            ("类别分布图", "显示各类别的数量分布", "📊"),
            ("样本展示", "随机展示标注样本", "🖼️"),
            ("尺寸分布图", "图片尺寸统计分布", "📏"),
            ("质量报告", "数据质量分析报告", "📋")
        ]
        
        for i, (title, desc, icon) in enumerate(chart_data):
            option = ChartOption(title, desc, icon)
            self.chart_options.append(option)
            chart_layout.addWidget(option, i // 2, i % 2)
        
        options_layout.addLayout(chart_layout)
        
        # 高级选项
        advanced_layout = QHBoxLayout()
        advanced_layout.setSpacing(16)
        
        # 样本数量
        sample_layout = QVBoxLayout()
        sample_layout.setSpacing(4)
        
        sample_label = QLabel("样本数量")
        sample_label.setStyleSheet("font-weight: 600; color: #374151;")
        sample_layout.addWidget(sample_label)
        
        self.sample_spin = QSpinBox()
        self.sample_spin.setRange(10, 1000)
        self.sample_spin.setValue(50)
        self.sample_spin.setSuffix(" 张")
        sample_layout.addWidget(self.sample_spin)
        
        advanced_layout.addLayout(sample_layout)
        
        # 图表风格
        style_layout = QVBoxLayout()
        style_layout.setSpacing(4)
        
        style_label = QLabel("图表风格")
        style_label.setStyleSheet("font-weight: 600; color: #374151;")
        style_layout.addWidget(style_label)
        
        self.style_combo = QComboBox()
        self.style_combo.addItems(["现代风格", "经典风格", "简约风格", "科技风格"])
        style_layout.addWidget(self.style_combo)
        
        advanced_layout.addLayout(style_layout)
        
        advanced_layout.addStretch()
        options_layout.addLayout(advanced_layout)
        
        options_card.add_layout(options_layout)
        layout.addWidget(options_card)
        
        # 预览卡片
        preview_card = Card("👁️ 预览")
        self.preview_area = PreviewArea()
        preview_card.add_widget(self.preview_area)
        layout.addWidget(preview_card)
        
        # 操作卡片
        action_card = Card("⚡ 执行操作")
        action_layout = QVBoxLayout()
        action_layout.setSpacing(16)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.generate_btn = QPushButton("生成可视化")
        self.generate_btn.setProperty("buttonType", "primary")
        self.generate_btn.clicked.connect(self.start_visualization)
        self.generate_btn.setEnabled(False)
        button_layout.addWidget(self.generate_btn)
        
        self.preview_btn = QPushButton("预览")
        self.preview_btn.setProperty("buttonType", "success")
        self.preview_btn.clicked.connect(self.preview_visualization)
        self.preview_btn.setEnabled(False)
        button_layout.addWidget(self.preview_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setProperty("buttonType", "danger")
        self.cancel_btn.clicked.connect(self.cancel_visualization)
        self.cancel_btn.setEnabled(False)
        button_layout.addWidget(self.cancel_btn)
        
        button_layout.addStretch()
        action_layout.addLayout(button_layout)
        
        # 进度显示
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        action_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #6b7280; font-style: italic;")
        action_layout.addWidget(self.status_label)
        
        action_card.add_layout(action_layout)
        layout.addWidget(action_card)
        
        layout.addStretch()
    
    def create_path_selector(self, title, is_input):
        """创建路径选择器"""
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: 600; color: #374151;")
        layout.addWidget(title_label)
        
        # 路径选择
        path_layout = QHBoxLayout()
        path_layout.setSpacing(8)
        
        path_label = QLabel("未选择")
        path_label.setObjectName("pathLabel")
        path_label.setStyleSheet("""
            #pathLabel {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
                color: #6b7280;
                font-style: italic;
            }
        """)
        path_layout.addWidget(path_label, 1)
        
        select_btn = QPushButton("浏览")
        select_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                border: 1px solid #2563eb;
                color: white;
                font-weight: 600;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)
        
        def select_path():
            path = QFileDialog.getExistingDirectory(self, f"选择{title}")
            if path:
                if is_input:
                    self.input_path = path
                    self.generate_btn.setEnabled(True)
                    self.preview_btn.setEnabled(True)
                    self.preview_area.update_preview(f"已选择数据集: {Path(path).name}")
                else:
                    self.output_path = path
                
                display_path = str(Path(path).name) if len(path) > 40 else path
                path_label.setText(display_path)
                path_label.setToolTip(path)
                path_label.setStyleSheet("""
                    #pathLabel {
                        background-color: white;
                        border: 1px solid #10b981;
                        border-radius: 6px;
                        padding: 8px 12px;
                        color: #374151;
                        font-weight: 500;
                    }
                """)
        
        select_btn.clicked.connect(select_path)
        path_layout.addWidget(select_btn)
        
        layout.addLayout(path_layout)
        return layout
    
    def preview_visualization(self):
        """预览可视化"""
        if not self.input_path:
            QMessageBox.warning(self, "警告", "请先选择数据集目录")
            return
        
        # 获取选中的图表类型
        selected_charts = []
        for i, option in enumerate(self.chart_options):
            if option.is_checked():
                chart_names = ["类别分布图", "样本展示", "尺寸分布图", "质量报告"]
                selected_charts.append(chart_names[i])
        
        if not selected_charts:
            QMessageBox.warning(self, "警告", "请至少选择一种图表类型")
            return
        
        preview_text = f"""预览信息:
数据集: {Path(self.input_path).name}
样本数量: {self.sample_spin.value()}
图表风格: {self.style_combo.currentText()}
选中图表: {', '.join(selected_charts)}

点击"生成可视化"开始处理..."""
        
        self.preview_area.update_preview(preview_text)
    
    def start_visualization(self):
        """开始可视化"""
        # 验证输入
        if not self.input_path:
            QMessageBox.warning(self, "警告", "请选择数据集目录")
            return
        
        if not self.output_path:
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
        
        # 获取选中的图表类型
        selected_charts = []
        for i, option in enumerate(self.chart_options):
            if option.is_checked():
                chart_names = ["class_distribution", "sample_display", "size_distribution", "quality_report"]
                selected_charts.append(chart_names[i])
        
        if not selected_charts:
            QMessageBox.warning(self, "警告", "请至少选择一种图表类型")
            return
        
        # 启动可视化
        self.worker = VisualizationWorker(
            self.input_path, self.output_path,
            selected_charts, self.sample_spin.value()
        )
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.visualization_finished)
        
        # 更新界面状态
        self.generate_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker.start()
    
    def cancel_visualization(self):
        """取消可视化"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        self.reset_ui_state()
        self.status_label.setText("可视化已取消")
    
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def visualization_finished(self, success, message, output_path):
        """可视化完成"""
        self.reset_ui_state()
        
        if success:
            QMessageBox.information(self, "成功", f"{message}\n输出路径: {output_path}")
            self.status_label.setText("可视化成功完成")
        else:
            QMessageBox.critical(self, "错误", message)
            self.status_label.setText("可视化失败")
    
    def reset_ui_state(self):
        """重置界面状态"""
        self.generate_btn.setEnabled(bool(self.input_path))
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)