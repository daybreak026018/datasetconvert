"""
简洁版格式转换面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QMessageBox, QProgressBar, QGroupBox,
    QGridLayout, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal


class ConvertWorker(QThread):
    """转换工作线程"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, input_path, output_path, input_format, output_format):
        super().__init__()
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.input_format = input_format
        self.output_format = output_format
    
    def run(self):
        try:
            self.progress_updated.emit(10, "正在验证输入格式...")
            
            # 这里应该调用实际的转换逻辑
            from ..core.converter import convert
            
            self.progress_updated.emit(30, "正在解析数据集...")
            
            # 执行转换
            result = convert(
                self.input_path,
                self.output_path,
                self.input_format,
                self.output_format
            )
            
            self.progress_updated.emit(100, "转换完成")
            self.finished.emit(True, "转换成功完成！")
            
        except Exception as e:
            self.finished.emit(False, f"转换失败: {str(e)}")


class SimpleConverterPanel(QWidget):
    """简洁版格式转换面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 输入设置卡片
        input_card = self.create_input_card()
        layout.addWidget(input_card)
        
        # 输出设置卡片
        output_card = self.create_output_card()
        layout.addWidget(output_card)
        
        # 转换设置卡片
        convert_card = self.create_convert_card()
        layout.addWidget(convert_card)
        
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
    
    def create_input_card(self):
        """创建输入设置卡片"""
        card = QGroupBox("输入设置")
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
        
        # 输入格式
        layout.addWidget(QLabel("输入格式:"), 1, 0)
        self.input_format_combo = QComboBox()
        self.input_format_combo.addItems(["YOLO", "VOC", "COCO", "JSON"])
        layout.addWidget(self.input_format_combo, 1, 1)
        
        return card
    
    def create_output_card(self):
        """创建输出设置卡片"""
        card = QGroupBox("输出设置")
        layout = QGridLayout(card)
        layout.setSpacing(15)
        
        # 输出目录
        layout.addWidget(QLabel("输出目录:"), 0, 0)
        
        output_layout = QHBoxLayout()
        self.output_path_label = QLabel("未选择")
        self.output_path_label.setStyleSheet("color: #6c757d; font-style: italic;")
        
        btn_select_output = QPushButton("选择目录")
        btn_select_output.clicked.connect(self.select_output_path)
        
        output_layout.addWidget(self.output_path_label, 1)
        output_layout.addWidget(btn_select_output)
        layout.addLayout(output_layout, 0, 1)
        
        # 输出格式
        layout.addWidget(QLabel("输出格式:"), 1, 0)
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(["YOLO", "VOC", "COCO", "JSON"])
        layout.addWidget(self.output_format_combo, 1, 1)
        
        return card
    
    def create_convert_card(self):
        """创建转换设置卡片"""
        card = QGroupBox("转换选项")
        layout = QGridLayout(card)
        layout.setSpacing(15)
        
        # 转换预览
        preview_layout = QHBoxLayout()
        
        # 输入格式显示
        self.input_preview = QLabel("YOLO")
        self.input_preview.setAlignment(Qt.AlignCenter)
        self.input_preview.setStyleSheet("""
            background-color: #e3f2fd;
            border: 2px solid #2196f3;
            border-radius: 8px;
            padding: 15px;
            font-weight: bold;
            color: #1976d2;
        """)
        
        # 箭头
        arrow_label = QLabel("→")
        arrow_label.setAlignment(Qt.AlignCenter)
        arrow_label.setStyleSheet("font-size: 24px; color: #6c757d;")
        
        # 输出格式显示
        self.output_preview = QLabel("YOLO")
        self.output_preview.setAlignment(Qt.AlignCenter)
        self.output_preview.setStyleSheet("""
            background-color: #e8f5e8;
            border: 2px solid #4caf50;
            border-radius: 8px;
            padding: 15px;
            font-weight: bold;
            color: #388e3c;
        """)
        
        preview_layout.addWidget(self.input_preview, 1)
        preview_layout.addWidget(arrow_label)
        preview_layout.addWidget(self.output_preview, 1)
        
        layout.addLayout(preview_layout, 0, 0, 1, 2)
        
        # 连接信号更新预览
        self.input_format_combo.currentTextChanged.connect(self.update_preview)
        self.output_format_combo.currentTextChanged.connect(self.update_preview)
        
        return card
    
    def create_button_layout(self):
        """创建按钮布局"""
        layout = QHBoxLayout()
        
        # 开始转换按钮
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.setProperty("buttonType", "primary")
        self.convert_btn.clicked.connect(self.start_convert)
        
        # 取消按钮
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setProperty("buttonType", "danger")
        self.cancel_btn.clicked.connect(self.cancel_convert)
        self.cancel_btn.setEnabled(False)
        
        layout.addStretch()
        layout.addWidget(self.convert_btn)
        layout.addWidget(self.cancel_btn)
        
        return layout
    
    def select_input_path(self):
        """选择输入路径"""
        path = QFileDialog.getExistingDirectory(self, "选择输入数据集目录")
        if path:
            self.input_path_label.setText(path)
            self.input_path_label.setStyleSheet("color: #495057;")
    
    def select_output_path(self):
        """选择输出路径"""
        path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if path:
            self.output_path_label.setText(path)
            self.output_path_label.setStyleSheet("color: #495057;")
    
    def update_preview(self):
        """更新转换预览"""
        input_format = self.input_format_combo.currentText()
        output_format = self.output_format_combo.currentText()
        
        self.input_preview.setText(input_format)
        self.output_preview.setText(output_format)
        
        # 如果格式相同，显示警告
        if input_format == output_format:
            self.output_preview.setStyleSheet("""
                background-color: #fff3cd;
                border: 2px solid #ffc107;
                border-radius: 8px;
                padding: 15px;
                font-weight: bold;
                color: #856404;
            """)
        else:
            self.output_preview.setStyleSheet("""
                background-color: #e8f5e8;
                border: 2px solid #4caf50;
                border-radius: 8px;
                padding: 15px;
                font-weight: bold;
                color: #388e3c;
            """)
    
    def start_convert(self):
        """开始转换"""
        # 验证输入
        input_path = self.input_path_label.text()
        output_path = self.output_path_label.text()
        
        if input_path == "未选择":
            QMessageBox.warning(self, "警告", "请选择输入数据集目录")
            return
        
        if output_path == "未选择":
            QMessageBox.warning(self, "警告", "请选择输出目录")
            return
        
        input_format = self.input_format_combo.currentText().lower()
        output_format = self.output_format_combo.currentText().lower()
        
        if input_format == output_format:
            reply = QMessageBox.question(
                self, "确认", 
                "输入和输出格式相同，确定要继续吗？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return
        
        # 启动转换
        self.worker = ConvertWorker(input_path, output_path, input_format, output_format)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.convert_finished)
        
        # 更新界面状态
        self.convert_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker.start()
    
    def cancel_convert(self):
        """取消转换"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        self.reset_ui_state()
        self.status_label.setText("转换已取消")
    
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def convert_finished(self, success, message):
        """转换完成"""
        self.reset_ui_state()
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.status_label.setText("转换成功完成")
        else:
            QMessageBox.critical(self, "错误", message)
            self.status_label.setText("转换失败")
    
    def reset_ui_state(self):
        """重置界面状态"""
        self.convert_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)