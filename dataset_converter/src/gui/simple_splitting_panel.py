"""
简洁版数据划分面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QMessageBox, QProgressBar, QGroupBox,
    QGridLayout, QSpinBox, QDoubleSpinBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal


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
            
            # 这里应该调用实际的划分逻辑
            from ..core.dataset_splitter import DatasetSplitter
            
            splitter = DatasetSplitter()
            
            self.progress_updated.emit(30, "正在划分数据集...")
            
            result = splitter.split_dataset(
                self.input_path,
                self.output_path,
                train_ratio=self.train_ratio,
                val_ratio=self.val_ratio,
                test_ratio=self.test_ratio
            )
            
            self.progress_updated.emit(100, "划分完成")
            self.finished.emit(True, "数据集划分成功完成！", result)
            
        except Exception as e:
            self.finished.emit(False, f"划分失败: {str(e)}", {})


class SimpleSplittingPanel(QWidget):
    """简洁版数据划分面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 数据集设置卡片
        dataset_card = self.create_dataset_card()
        layout.addWidget(dataset_card)
        
        # 划分设置卡片
        split_card = self.create_split_card()
        layout.addWidget(split_card)
        
        # 预览卡片
        preview_card = self.create_preview_card()
        layout.addWidget(preview_card)
        
        # 操作按钮
        button_layout = self.create_button_layout()
        layout.addLayout(button_layout)
        
        # 进度显示
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
    
    def create_dataset_card(self):
        """创建数据集设置卡片"""
        card = QGroupBox("数据集设置")
        layout = QGridLayout(card)
        layout.setSpacing(15)
        
        # 输入目录
        layout.addWidget(QLabel("数据集目录:"), 0, 0)
        
        input_layout = QHBoxLayout()
        self.input_path_label = QLabel("未选择")
        self.input_path_label.setStyleSheet("color: #6c757d; font-style: italic;")
        
        btn_select_input = QPushButton("选择目录")
        btn_select_input.clicked.connect(self.select_input_path)
        
        input_layout.addWidget(self.input_path_label, 1)
        input_layout.addWidget(btn_select_input)
        layout.addLayout(input_layout, 0, 1)
        
        # 输出目录
        layout.addWidget(QLabel("输出目录:"), 1, 0)
        
        output_layout = QHBoxLayout()
        self.output_path_label = QLabel("未选择")
        self.output_path_label.setStyleSheet("color: #6c757d; font-style: italic;")
        
        btn_select_output = QPushButton("选择目录")
        btn_select_output.clicked.connect(self.select_output_path)
        
        output_layout.addWidget(self.output_path_label, 1)
        output_layout.addWidget(btn_select_output)
        layout.addLayout(output_layout, 1, 1)
        
        return card
    
    def create_split_card(self):
        """创建划分设置卡片"""
        card = QGroupBox("划分比例")
        layout = QGridLayout(card)
        layout.setSpacing(15)
        
        # 训练集比例
        layout.addWidget(QLabel("训练集:"), 0, 0)
        self.train_ratio = QDoubleSpinBox()
        self.train_ratio.setRange(0.1, 0.9)
        self.train_ratio.setSingleStep(0.1)
        self.train_ratio.setValue(0.7)
        self.train_ratio.setSuffix(" (70%)")
        self.train_ratio.valueChanged.connect(self.update_ratios)
        layout.addWidget(self.train_ratio, 0, 1)
        
        # 验证集比例
        layout.addWidget(QLabel("验证集:"), 1, 0)
        self.val_ratio = QDoubleSpinBox()
        self.val_ratio.setRange(0.0, 0.5)
        self.val_ratio.setSingleStep(0.1)
        self.val_ratio.setValue(0.2)
        self.val_ratio.setSuffix(" (20%)")
        self.val_ratio.valueChanged.connect(self.update_ratios)
        layout.addWidget(self.val_ratio, 1, 1)
        
        # 测试集比例
        layout.addWidget(QLabel("测试集:"), 2, 0)
        self.test_ratio = QDoubleSpinBox()
        self.test_ratio.setRange(0.0, 0.5)
        self.test_ratio.setSingleStep(0.1)
        self.test_ratio.setValue(0.1)
        self.test_ratio.setSuffix(" (10%)")
        self.test_ratio.valueChanged.connect(self.update_ratios)
        layout.addWidget(self.test_ratio, 2, 1)
        
        # 总和显示
        layout.addWidget(QLabel("总和:"), 3, 0)
        self.total_label = QLabel("1.0 (100%)")
        self.total_label.setStyleSheet("font-weight: bold; color: #28a745;")
        layout.addWidget(self.total_label, 3, 1)
        
        return card
    
    def create_preview_card(self):
        """创建预览卡片"""
        card = QGroupBox("划分预览")
        layout = QVBoxLayout(card)
        
        # 预览表格
        self.preview_table = QTableWidget()
        self.preview_table.setColumnCount(3)
        self.preview_table.setHorizontalHeaderLabels(["数据集", "文件数量", "占比"])
        self.preview_table.setRowCount(3)
        
        # 设置表格内容
        datasets = ["训练集", "验证集", "测试集"]
        for i, name in enumerate(datasets):
            self.preview_table.setItem(i, 0, QTableWidgetItem(name))
            self.preview_table.setItem(i, 1, QTableWidgetItem("0"))
            self.preview_table.setItem(i, 2, QTableWidgetItem("0%"))
        
        # 调整表格样式
        self.preview_table.setAlternatingRowColors(True)
        self.preview_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.preview_table.resizeColumnsToContents()
        
        layout.addWidget(self.preview_table)
        
        return card
    
    def create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        
        # 预设按钮
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("快速设置:"))
        
        btn_preset_1 = QPushButton("7:2:1")
        btn_preset_1.clicked.connect(lambda: self.set_preset(0.7, 0.2, 0.1))
        
        btn_preset_2 = QPushButton("8:1:1")
        btn_preset_2.clicked.connect(lambda: self.set_preset(0.8, 0.1, 0.1))
        
        btn_preset_3 = QPushButton("6:2:2")
        btn_preset_3.clicked.connect(lambda: self.set_preset(0.6, 0.2, 0.2))
        
        preset_layout.addWidget(btn_preset_1)
        preset_layout.addWidget(btn_preset_2)
        preset_layout.addWidget(btn_preset_3)
        preset_layout.addStretch()
        
        # 主要操作按钮
        self.split_btn = QPushButton("开始划分")
        self.split_btn.setProperty("buttonType", "primary")
        self.split_btn.clicked.connect(self.start_split)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setProperty("buttonType", "danger")
        self.cancel_btn.clicked.connect(self.cancel_split)
        self.cancel_btn.setEnabled(False)
        
        layout.addLayout(preset_layout)
        layout.addWidget(self.split_btn)
        layout.addWidget(self.cancel_btn)
        
        return layout
    
    def select_input_path(self):
        """选择输入路径"""
        path = QFileDialog.getExistingDirectory(self, "选择数据集目录")
        if path:
            self.input_path_label.setText(path)
            self.input_path_label.setStyleSheet("color: #495057;")
            self.update_preview()
    
    def select_output_path(self):
        """选择输出路径"""
        path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if path:
            self.output_path_label.setText(path)
            self.output_path_label.setStyleSheet("color: #495057;")
    
    def update_ratios(self):
        """更新比例显示"""
        train = self.train_ratio.value()
        val = self.val_ratio.value()
        test = self.test_ratio.value()
        total = train + val + test
        
        # 更新后缀显示
        self.train_ratio.setSuffix(f" ({train*100:.0f}%)")
        self.val_ratio.setSuffix(f" ({val*100:.0f}%)")
        self.test_ratio.setSuffix(f" ({test*100:.0f}%)")
        
        # 更新总和显示
        self.total_label.setText(f"{total:.1f} ({total*100:.0f}%)")
        
        # 根据总和设置颜色
        if abs(total - 1.0) < 0.01:
            self.total_label.setStyleSheet("font-weight: bold; color: #28a745;")
        else:
            self.total_label.setStyleSheet("font-weight: bold; color: #dc3545;")
        
        self.update_preview()
    
    def update_preview(self):
        """更新预览"""
        input_path = self.input_path_label.text()
        if input_path == "未选择":
            return
        
        try:
            # 简单计算文件数量（实际应该扫描目录）
            total_files = 1000  # 示例数据
            
            train_files = int(total_files * self.train_ratio.value())
            val_files = int(total_files * self.val_ratio.value())
            test_files = total_files - train_files - val_files
            
            files = [train_files, val_files, test_files]
            ratios = [self.train_ratio.value(), self.val_ratio.value(), self.test_ratio.value()]
            
            for i, (file_count, ratio) in enumerate(zip(files, ratios)):
                self.preview_table.setItem(i, 1, QTableWidgetItem(str(file_count)))
                self.preview_table.setItem(i, 2, QTableWidgetItem(f"{ratio*100:.1f}%"))
        
        except Exception:
            pass
    
    def set_preset(self, train, val, test):
        """设置预设比例"""
        self.train_ratio.setValue(train)
        self.val_ratio.setValue(val)
        self.test_ratio.setValue(test)
    
    def start_split(self):
        """开始划分"""
        # 验证输入
        input_path = self.input_path_label.text()
        output_path = self.output_path_label.text()
        
        if input_path == "未选择":
            QMessageBox.warning(self, "警告", "请选择数据集目录")
            return
        
        if output_path == "未选择":
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
        
        # 验证比例
        total = self.train_ratio.value() + self.val_ratio.value() + self.test_ratio.value()
        if abs(total - 1.0) > 0.01:
            QMessageBox.warning(self, "警告", "比例总和必须等于1.0")
            return
        
        # 启动划分
        self.worker = SplitWorker(
            input_path, output_path,
            self.train_ratio.value(),
            self.val_ratio.value(),
            self.test_ratio.value()
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