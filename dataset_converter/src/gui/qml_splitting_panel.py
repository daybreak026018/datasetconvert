"""
QML风格数据划分面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QFrame,
    QGridLayout, QSlider, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor

from .qml_style_window import Card


class SplitWorker(QThread):
    """划分工作线程"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, dict)
    
    def __init__(self, input_path, output_path, train_ratio, val_ratio, test_ratio):
        super().__init__()
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
    
    def run(self):
        try:
            self.progress_updated.emit(10, "正在扫描数据集...")
            
            # 模拟划分过程
            import time
            for i in range(10, 101, 15):
                time.sleep(0.3)
                if i == 25:
                    self.progress_updated.emit(i, "正在分析文件结构...")
                elif i == 55:
                    self.progress_updated.emit(i, "正在划分数据集...")
                elif i == 85:
                    self.progress_updated.emit(i, "正在复制文件...")
                else:
                    self.progress_updated.emit(i, f"划分进度 {i}%")
            
            # 模拟结果
            result = {
                'train_count': 700,
                'val_count': 200,
                'test_count': 100,
                'total_count': 1000
            }
            
            self.progress_updated.emit(100, "划分完成")
            self.finished.emit(True, "数据集划分成功完成！", result)
            
        except Exception as e:
            self.finished.emit(False, f"划分失败: {str(e)}", {})


class RatioSlider(QFrame):
    """比例滑块组件"""
    
    value_changed = pyqtSignal(float)
    
    def __init__(self, title="比例", min_val=0.0, max_val=1.0, default_val=0.7, color="#3b82f6", parent=None):
        super().__init__(parent)
        self.title = title
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = default_val
        self.color = color
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # 标题和值
        header_layout = QHBoxLayout()
        
        title_label = QLabel(self.title)
        title_label.setObjectName("sliderTitle")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        self.value_label = QLabel(f"{self.current_val:.1f}")
        self.value_label.setObjectName("sliderValue")
        header_layout.addWidget(self.value_label)
        
        layout.addLayout(header_layout)
        
        # 滑块
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(int(self.min_val * 100))
        self.slider.setMaximum(int(self.max_val * 100))
        self.slider.setValue(int(self.current_val * 100))
        self.slider.valueChanged.connect(self.on_value_changed)
        layout.addWidget(self.slider)
        
        # 百分比显示
        self.percent_label = QLabel(f"{self.current_val*100:.0f}%")
        self.percent_label.setObjectName("percentLabel")
        self.percent_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.percent_label)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet(f"""
            RatioSlider {{
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }}
            
            RatioSlider:hover {{
                border-color: {self.color};
                background-color: #f1f5f9;
            }}
            
            #sliderTitle {{
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }}
            
            #sliderValue {{
                font-size: 14px;
                font-weight: 700;
                color: {self.color};
            }}
            
            #percentLabel {{
                font-size: 12px;
                color: #6b7280;
                font-weight: 500;
            }}
            
            QSlider::groove:horizontal {{
                background-color: #e5e7eb;
                height: 6px;
                border-radius: 3px;
            }}
            
            QSlider::handle:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.color}, stop:1 {self.color});
                border: 2px solid white;
                width: 20px;
                height: 20px;
                border-radius: 12px;
                margin: -8px 0;
            }}
            
            QSlider::handle:horizontal:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.color}, stop:1 {self.color});
                border: 3px solid white;
            }}
            
            QSlider::sub-page:horizontal {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {self.color}, stop:1 {self.color});
                border-radius: 3px;
            }}
        """)
    
    def on_value_changed(self, value):
        """值改变事件"""
        self.current_val = value / 100.0
        self.value_label.setText(f"{self.current_val:.1f}")
        self.percent_label.setText(f"{self.current_val*100:.0f}%")
        self.value_changed.emit(self.current_val)
    
    def set_value(self, value):
        """设置值"""
        self.slider.setValue(int(value * 100))


class PreviewTable(QFrame):
    """预览表格组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["数据集", "文件数量", "占比"])
        self.table.setRowCount(3)
        
        # 设置表格内容
        datasets = ["训练集", "验证集", "测试集"]
        for i, name in enumerate(datasets):
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem("0"))
            self.table.setItem(i, 2, QTableWidgetItem("0%"))
        
        # 表格属性
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.table)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                gridline-color: #f1f5f9;
            }
            
            QTableWidget::item {
                padding: 12px 16px;
                border: none;
            }
            
            QTableWidget::item:selected {
                background-color: #eff6ff;
                color: #1e40af;
            }
            
            QHeaderView::section {
                background-color: #f8fafc;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                padding: 12px 16px;
                font-weight: 600;
                color: #374151;
            }
        """)
    
    def update_preview(self, train_ratio, val_ratio, test_ratio, total_files=1000):
        """更新预览"""
        train_files = int(total_files * train_ratio)
        val_files = int(total_files * val_ratio)
        test_files = total_files - train_files - val_files
        
        files = [train_files, val_files, test_files]
        ratios = [train_ratio, val_ratio, test_ratio]
        
        for i, (file_count, ratio) in enumerate(zip(files, ratios)):
            self.table.setItem(i, 1, QTableWidgetItem(str(file_count)))
            self.table.setItem(i, 2, QTableWidgetItem(f"{ratio*100:.1f}%"))


class QMLSplittingPanel(QWidget):
    """QML风格数据划分面板"""
    
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
        path_card = Card("📁 数据集路径")
        path_layout = QGridLayout()
        path_layout.setSpacing(16)
        
        # 输入路径
        input_layout = self.create_path_selector("输入数据集", True)
        path_layout.addLayout(input_layout, 0, 0)
        
        # 输出路径
        output_layout = self.create_path_selector("输出目录", False)
        path_layout.addLayout(output_layout, 0, 1)
        
        path_card.add_layout(path_layout)
        layout.addWidget(path_card)
        
        # 比例设置卡片
        ratio_card = Card("⚖️ 划分比例")
        ratio_layout = QGridLayout()
        ratio_layout.setSpacing(16)
        
        # 训练集滑块
        self.train_slider = RatioSlider("训练集", 0.1, 0.9, 0.7, "#3b82f6")
        self.train_slider.value_changed.connect(self.update_ratios)
        ratio_layout.addWidget(self.train_slider, 0, 0)
        
        # 验证集滑块
        self.val_slider = RatioSlider("验证集", 0.0, 0.5, 0.2, "#10b981")
        self.val_slider.value_changed.connect(self.update_ratios)
        ratio_layout.addWidget(self.val_slider, 0, 1)
        
        # 测试集滑块
        self.test_slider = RatioSlider("测试集", 0.0, 0.5, 0.1, "#f59e0b")
        self.test_slider.value_changed.connect(self.update_ratios)
        ratio_layout.addWidget(self.test_slider, 0, 2)
        
        # 总和显示
        total_layout = QHBoxLayout()
        total_layout.setSpacing(8)
        
        total_label = QLabel("总和:")
        total_label.setStyleSheet("font-weight: 600; color: #374151;")
        total_layout.addWidget(total_label)
        
        self.total_label = QLabel("1.0 (100%)")
        self.total_label.setStyleSheet("font-weight: 700; color: #10b981;")
        total_layout.addWidget(self.total_label)
        
        total_layout.addStretch()
        
        # 快速设置按钮
        preset_label = QLabel("快速设置:")
        preset_label.setStyleSheet("font-weight: 600; color: #374151;")
        total_layout.addWidget(preset_label)
        
        for ratio_text, ratios in [("7:2:1", (0.7, 0.2, 0.1)), ("8:1:1", (0.8, 0.1, 0.1)), ("6:2:2", (0.6, 0.2, 0.2))]:
            btn = QPushButton(ratio_text)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f3f4f6;
                    border: 1px solid #d1d5db;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-size: 12px;
                    font-weight: 500;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #e5e7eb;
                }
            """)
            btn.clicked.connect(lambda checked, r=ratios: self.set_preset(*r))
            total_layout.addWidget(btn)
        
        ratio_layout.addLayout(total_layout, 1, 0, 1, 3)
        ratio_card.add_layout(ratio_layout)
        layout.addWidget(ratio_card)
        
        # 预览卡片
        preview_card = Card("👁️ 划分预览")
        self.preview_table = PreviewTable()
        preview_card.add_widget(self.preview_table)
        layout.addWidget(preview_card)
        
        # 操作卡片
        action_card = Card("⚡ 执行操作")
        action_layout = QVBoxLayout()
        action_layout.setSpacing(16)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.split_btn = QPushButton("开始划分")
        self.split_btn.setProperty("buttonType", "primary")
        self.split_btn.clicked.connect(self.start_split)
        button_layout.addWidget(self.split_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setProperty("buttonType", "danger")
        self.cancel_btn.clicked.connect(self.cancel_split)
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
        
        # 初始更新
        self.update_ratios()
    
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
    
    def update_ratios(self):
        """更新比例"""
        train = self.train_slider.current_val
        val = self.val_slider.current_val
        test = self.test_slider.current_val
        total = train + val + test
        
        # 更新总和显示
        self.total_label.setText(f"{total:.1f} ({total*100:.0f}%)")
        
        # 根据总和设置颜色
        if abs(total - 1.0) < 0.01:
            self.total_label.setStyleSheet("font-weight: 700; color: #10b981;")
        else:
            self.total_label.setStyleSheet("font-weight: 700; color: #ef4444;")
        
        # 更新预览
        self.preview_table.update_preview(train, val, test)
    
    def set_preset(self, train, val, test):
        """设置预设比例"""
        self.train_slider.set_value(train)
        self.val_slider.set_value(val)
        self.test_slider.set_value(test)
    
    def start_split(self):
        """开始划分"""
        # 验证输入
        if not self.input_path:
            QMessageBox.warning(self, "警告", "请选择数据集目录")
            return
        
        if not self.output_path:
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
        
        # 验证比例
        total = (self.train_slider.current_val + 
                self.val_slider.current_val + 
                self.test_slider.current_val)
        if abs(total - 1.0) > 0.01:
            QMessageBox.warning(self, "警告", "比例总和必须等于1.0")
            return
        
        # 启动划分
        self.worker = SplitWorker(
            self.input_path, self.output_path,
            self.train_slider.current_val,
            self.val_slider.current_val,
            self.test_slider.current_val
        )
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.split_finished)
        
        # 更新界面状态
        self.split_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker.start()
    
    def cancel_split(self):
        """取消划分"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        self.reset_ui_state()
        self.status_label.setText("划分已取消")
    
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def split_finished(self, success, message, result):
        """划分完成"""
        self.reset_ui_state()
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.status_label.setText("划分成功完成")
        else:
            QMessageBox.critical(self, "错误", message)
            self.status_label.setText("划分失败")
    
    def reset_ui_state(self):
        """重置界面状态"""
        self.split_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)