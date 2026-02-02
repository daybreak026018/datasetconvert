"""
QML风格格式转换面板
采用声明式UI设计和现代化交互
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QFileDialog, QMessageBox, QProgressBar, QFrame,
    QGridLayout, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QFont, QColor

from .qml_style_window import Card


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
            
            # 模拟转换过程
            import time
            for i in range(10, 101, 10):
                time.sleep(0.2)
                if i == 30:
                    self.progress_updated.emit(i, "正在解析数据集...")
                elif i == 60:
                    self.progress_updated.emit(i, "正在转换格式...")
                elif i == 90:
                    self.progress_updated.emit(i, "正在保存结果...")
                else:
                    self.progress_updated.emit(i, f"转换进度 {i}%")
            
            self.progress_updated.emit(100, "转换完成")
            self.finished.emit(True, "转换成功完成！")
            
        except Exception as e:
            self.finished.emit(False, f"转换失败: {str(e)}")


class FormatPreview(QFrame):
    """格式预览组件"""
    
    def __init__(self, format_name="YOLO", is_input=True, parent=None):
        super().__init__(parent)
        self.format_name = format_name
        self.is_input = is_input
        self.setup_ui()
        self.setup_style()
        self.setup_animation()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)
        
        # 格式标签
        self.format_label = QLabel(self.format_name)
        self.format_label.setObjectName("formatLabel")
        self.format_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.format_label)
        
        # 类型标签
        type_text = "输入格式" if self.is_input else "输出格式"
        type_label = QLabel(type_text)
        type_label.setObjectName("typeLabel")
        type_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(type_label)
    
    def setup_style(self):
        """设置样式"""
        if self.is_input:
            self.setStyleSheet("""
                FormatPreview {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #dbeafe, stop:1 #bfdbfe);
                    border: 2px solid #3b82f6;
                    border-radius: 16px;
                }
                
                #formatLabel {
                    font-size: 24px;
                    font-weight: 700;
                    color: #1e40af;
                }
                
                #typeLabel {
                    font-size: 12px;
                    color: #3730a3;
                    font-weight: 500;
                }
            """)
        else:
            self.setStyleSheet("""
                FormatPreview {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #dcfce7, stop:1 #bbf7d0);
                    border: 2px solid #10b981;
                    border-radius: 16px;
                }
                
                #formatLabel {
                    font-size: 24px;
                    font-weight: 700;
                    color: #047857;
                }
                
                #typeLabel {
                    font-size: 12px;
                    color: #065f46;
                    font-weight: 500;
                }
            """)
    
    def setup_animation(self):
        """设置动画"""
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(300)
        self.scale_animation.setEasingCurve(QEasingCurve.OutBack)
    
    def update_format(self, format_name):
        """更新格式"""
        self.format_name = format_name
        self.format_label.setText(format_name)
        self.animate_update()
    
    def animate_update(self):
        """更新动画"""
        current_rect = self.geometry()
        small_rect = QRect(
            current_rect.x() + 5,
            current_rect.y() + 5,
            current_rect.width() - 10,
            current_rect.height() - 10
        )
        
        self.scale_animation.setStartValue(current_rect)
        self.scale_animation.setEndValue(small_rect)
        self.scale_animation.finished.connect(lambda: self.setGeometry(current_rect))
        self.scale_animation.start()


class PathSelector(QFrame):
    """路径选择组件"""
    
    path_changed = pyqtSignal(str)
    
    def __init__(self, title="选择路径", is_input=True, parent=None):
        super().__init__(parent)
        self.title = title
        self.is_input = is_input
        self.current_path = ""
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # 标题
        title_label = QLabel(self.title)
        title_label.setObjectName("pathTitle")
        layout.addWidget(title_label)
        
        # 路径显示和选择
        path_layout = QHBoxLayout()
        path_layout.setSpacing(12)
        
        self.path_label = QLabel("未选择")
        self.path_label.setObjectName("pathLabel")
        path_layout.addWidget(self.path_label, 1)
        
        select_btn = QPushButton("浏览")
        select_btn.setObjectName("selectBtn")
        select_btn.clicked.connect(self.select_path)
        path_layout.addWidget(select_btn)
        
        layout.addLayout(path_layout)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            PathSelector {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            
            PathSelector:hover {
                border-color: #cbd5e1;
                background-color: #f1f5f9;
            }
            
            #pathTitle {
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }
            
            #pathLabel {
                font-size: 13px;
                color: #6b7280;
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 8px 12px;
            }
            
            #selectBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                border: 1px solid #2563eb;
                color: white;
                font-weight: 600;
                min-width: 80px;
            }
            
            #selectBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)
    
    def select_path(self):
        """选择路径"""
        if self.is_input:
            path = QFileDialog.getExistingDirectory(self, f"选择{self.title}")
        else:
            path = QFileDialog.getExistingDirectory(self, f"选择{self.title}")
        
        if path:
            self.current_path = path
            # 显示简化路径
            display_path = str(Path(path).name) if len(path) > 50 else path
            self.path_label.setText(display_path)
            self.path_label.setToolTip(path)
            self.path_label.setStyleSheet("""
                #pathLabel {
                    color: #374151;
                    font-weight: 500;
                }
            """)
            self.path_changed.emit(path)


class QMLConverterPanel(QWidget):
    """QML风格格式转换面板"""
    
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
        self.input_selector = PathSelector("输入数据集目录", True)
        self.input_selector.path_changed.connect(self.on_input_path_changed)
        path_layout.addWidget(self.input_selector, 0, 0)
        
        # 输出路径
        self.output_selector = PathSelector("输出目录", False)
        self.output_selector.path_changed.connect(self.on_output_path_changed)
        path_layout.addWidget(self.output_selector, 0, 1)
        
        path_card.add_layout(path_layout)
        layout.addWidget(path_card)
        
        # 格式设置卡片
        format_card = Card("🔄 格式转换")
        format_layout = QVBoxLayout()
        format_layout.setSpacing(20)
        
        # 格式选择
        format_select_layout = QHBoxLayout()
        format_select_layout.setSpacing(16)
        
        # 输入格式
        input_format_layout = QVBoxLayout()
        input_format_layout.setSpacing(8)
        
        input_label = QLabel("输入格式")
        input_label.setStyleSheet("font-weight: 600; color: #374151;")
        input_format_layout.addWidget(input_label)
        
        self.input_format_combo = QComboBox()
        self.input_format_combo.addItems(["YOLO", "VOC", "COCO", "JSON"])
        self.input_format_combo.currentTextChanged.connect(self.update_preview)
        input_format_layout.addWidget(self.input_format_combo)
        
        format_select_layout.addLayout(input_format_layout)
        
        # 输出格式
        output_format_layout = QVBoxLayout()
        output_format_layout.setSpacing(8)
        
        output_label = QLabel("输出格式")
        output_label.setStyleSheet("font-weight: 600; color: #374151;")
        output_format_layout.addWidget(output_label)
        
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(["YOLO", "VOC", "COCO", "JSON"])
        self.output_format_combo.setCurrentIndex(1)
        self.output_format_combo.currentTextChanged.connect(self.update_preview)
        output_format_layout.addWidget(self.output_format_combo)
        
        format_select_layout.addLayout(output_format_layout)
        format_layout.addLayout(format_select_layout)
        
        # 格式预览
        preview_layout = QHBoxLayout()
        preview_layout.setSpacing(24)
        
        self.input_preview = FormatPreview("YOLO", True)
        preview_layout.addWidget(self.input_preview)
        
        # 箭头
        arrow_label = QLabel("→")
        arrow_label.setAlignment(Qt.AlignCenter)
        arrow_label.setStyleSheet("""
            font-size: 32px;
            color: #6b7280;
            font-weight: bold;
        """)
        preview_layout.addWidget(arrow_label)
        
        self.output_preview = FormatPreview("VOC", False)
        preview_layout.addWidget(self.output_preview)
        
        format_layout.addLayout(preview_layout)
        format_card.add_layout(format_layout)
        layout.addWidget(format_card)
        
        # 操作卡片
        action_card = Card("⚡ 执行操作")
        action_layout = QVBoxLayout()
        action_layout.setSpacing(16)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.convert_btn = QPushButton("开始转换")
        self.convert_btn.setProperty("buttonType", "primary")
        self.convert_btn.clicked.connect(self.start_convert)
        button_layout.addWidget(self.convert_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setProperty("buttonType", "danger")
        self.cancel_btn.clicked.connect(self.cancel_convert)
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
    
    def on_input_path_changed(self, path):
        """输入路径改变"""
        self.input_path = path
    
    def on_output_path_changed(self, path):
        """输出路径改变"""
        self.output_path = path
    
    def update_preview(self):
        """更新预览"""
        input_format = self.input_format_combo.currentText()
        output_format = self.output_format_combo.currentText()
        
        self.input_preview.update_format(input_format)
        self.output_preview.update_format(output_format)
    
    def start_convert(self):
        """开始转换"""
        # 验证输入
        if not self.input_path:
            QMessageBox.warning(self, "警告", "请选择输入数据集目录")
            return
        
        if not self.output_path:
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
        self.worker = ConvertWorker(self.input_path, self.output_path, input_format, output_format)
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