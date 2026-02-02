"""
QML风格高级功能面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QFrame,
    QGridLayout, QComboBox, QCheckBox, QSpinBox, QSlider,
    QTextEdit, QTabWidget, QGroupBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from .qml_style_window import Card


class AdvancedWorker(QThread):
    """高级功能工作线程"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, operation, params):
        super().__init__()
        self.operation = operation
        self.params = params
    
    def run(self):
        try:
            self.progress_updated.emit(10, f"正在初始化{self.operation}...")
            
            # 模拟高级操作
            import time
            for i in range(10, 101, 15):
                time.sleep(0.4)
                if i == 25:
                    self.progress_updated.emit(i, "正在加载AI模型...")
                elif i == 40:
                    self.progress_updated.emit(i, "正在处理数据...")
                elif i == 55:
                    self.progress_updated.emit(i, "正在应用算法...")
                elif i == 70:
                    self.progress_updated.emit(i, "正在优化结果...")
                elif i == 85:
                    self.progress_updated.emit(i, "正在保存输出...")
                else:
                    self.progress_updated.emit(i, f"{self.operation}进度 {i}%")
            
            self.progress_updated.emit(100, f"{self.operation}完成")
            self.finished.emit(True, f"{self.operation}成功完成！")
            
        except Exception as e:
            self.finished.emit(False, f"{self.operation}失败: {str(e)}")


class FeatureCard(QFrame):
    """功能卡片组件"""
    
    feature_clicked = pyqtSignal(str)
    
    def __init__(self, title="", description="", icon="⚡", enabled=True, parent=None):
        super().__init__(parent)
        self.title = title
        self.description = description
        self.icon = icon
        self.enabled = enabled
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # 图标和标题
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_label.setObjectName("featureIcon")
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(self.title)
        title_label.setObjectName("featureTitle")
        header_layout.addWidget(title_label, 1)
        
        layout.addLayout(header_layout)
        
        # 描述
        desc_label = QLabel(self.description)
        desc_label.setObjectName("featureDesc")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # 启用按钮
        self.enable_btn = QPushButton("启用功能" if self.enabled else "功能未开放")
        self.enable_btn.setObjectName("enableBtn")
        self.enable_btn.setEnabled(self.enabled)
        self.enable_btn.clicked.connect(lambda: self.feature_clicked.emit(self.title))
        layout.addWidget(self.enable_btn)
    
    def setup_style(self):
        """设置样式"""
        border_color = "#3b82f6" if self.enabled else "#e5e7eb"
        
        self.setStyleSheet(f"""
            FeatureCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 white, stop:1 #f8fafc);
                border: 1px solid {border_color};
                border-radius: 12px;
            }}
            
            FeatureCard:hover {{
                border-color: {"#2563eb" if self.enabled else "#d1d5db"};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 white, stop:1 #f1f5f9);
            }}
            
            #featureIcon {{
                font-size: 24px;
                color: {"#3b82f6" if self.enabled else "#9ca3af"};
            }}
            
            #featureTitle {{
                font-size: 16px;
                font-weight: 600;
                color: {"#374151" if self.enabled else "#9ca3af"};
            }}
            
            #featureDesc {{
                font-size: 13px;
                color: {"#6b7280" if self.enabled else "#9ca3af"};
                line-height: 1.4;
            }}
            
            #enableBtn {{
                background: {"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3b82f6, stop:1 #2563eb)" if self.enabled else "#f3f4f6"};
                border: 1px solid {"#2563eb" if self.enabled else "#d1d5db"};
                color: {"white" if self.enabled else "#9ca3af"};
                font-weight: 600;
                padding: 8px 16px;
                border-radius: 6px;
            }}
            
            #enableBtn:hover {{
                background: {"qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2563eb, stop:1 #1d4ed8)" if self.enabled else "#f3f4f6"};
            }}
        """)


class ParameterGroup(QGroupBox):
    """参数组组件"""
    
    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setup_style()
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(12)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: 600;
                color: #374151;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin-top: 8px;
                padding-top: 8px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                background-color: #f8fafc;
            }
        """)
    
    def add_parameter(self, label_text, widget):
        """添加参数"""
        param_layout = QHBoxLayout()
        param_layout.setSpacing(8)
        
        label = QLabel(label_text)
        label.setStyleSheet("color: #6b7280; font-weight: 500; min-width: 100px;")
        param_layout.addWidget(label)
        
        param_layout.addWidget(widget, 1)
        
        self.layout.addLayout(param_layout)


class QMLAdvancedPanel(QWidget):
    """QML风格高级功能面板"""
    
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
        input_layout = self.create_path_selector("输入数据集", True)
        path_layout.addLayout(input_layout, 0, 0)
        
        # 输出路径
        output_layout = self.create_path_selector("输出目录", False)
        path_layout.addLayout(output_layout, 0, 1)
        
        path_card.add_layout(path_layout)
        layout.addWidget(path_card)
        
        # AI功能卡片
        ai_card = Card("🤖 AI辅助功能")
        ai_layout = QGridLayout()
        ai_layout.setSpacing(16)
        
        # AI功能列表
        ai_features = [
            ("智能标注", "使用AI模型自动生成标注", "🎯", True),
            ("质量检测", "AI检测标注质量问题", "🔍", True),
            ("数据增强", "智能生成更多训练数据", "📈", True),
            ("异常检测", "识别数据集中的异常样本", "⚠️", False)
        ]
        
        self.ai_feature_cards = []
        for i, (title, desc, icon, enabled) in enumerate(ai_features):
            feature_card = FeatureCard(title, desc, icon, enabled)
            feature_card.feature_clicked.connect(self.start_ai_feature)
            self.ai_feature_cards.append(feature_card)
            ai_layout.addWidget(feature_card, i // 2, i % 2)
        
        ai_card.add_layout(ai_layout)
        layout.addWidget(ai_card)
        
        # 批处理功能卡片
        batch_card = Card("⚡ 批处理功能")
        batch_layout = QVBoxLayout()
        batch_layout.setSpacing(16)
        
        # 批处理选项
        batch_options_layout = QGridLayout()
        batch_options_layout.setSpacing(12)
        
        # 并行处理
        parallel_group = ParameterGroup("并行处理设置")
        
        self.thread_spin = QSpinBox()
        self.thread_spin.setRange(1, 16)
        self.thread_spin.setValue(4)
        self.thread_spin.setSuffix(" 线程")
        parallel_group.add_parameter("线程数:", self.thread_spin)
        
        self.batch_size_spin = QSpinBox()
        self.batch_size_spin.setRange(1, 1000)
        self.batch_size_spin.setValue(32)
        self.batch_size_spin.setSuffix(" 个/批")
        parallel_group.add_parameter("批大小:", self.batch_size_spin)
        
        batch_options_layout.addWidget(parallel_group, 0, 0)
        
        # 内存优化
        memory_group = ParameterGroup("内存优化设置")
        
        self.memory_limit_spin = QSpinBox()
        self.memory_limit_spin.setRange(512, 32768)
        self.memory_limit_spin.setValue(4096)
        self.memory_limit_spin.setSuffix(" MB")
        memory_group.add_parameter("内存限制:", self.memory_limit_spin)
        
        self.cache_checkbox = QCheckBox("启用缓存")
        self.cache_checkbox.setChecked(True)
        memory_group.layout.addWidget(self.cache_checkbox)
        
        batch_options_layout.addWidget(memory_group, 0, 1)
        
        batch_layout.addLayout(batch_options_layout)
        
        # 批处理操作
        batch_ops_layout = QHBoxLayout()
        batch_ops_layout.setSpacing(12)
        
        self.batch_convert_btn = QPushButton("批量转换")
        self.batch_convert_btn.setProperty("buttonType", "primary")
        self.batch_convert_btn.clicked.connect(lambda: self.start_batch_operation("批量转换"))
        batch_ops_layout.addWidget(self.batch_convert_btn)
        
        self.batch_resize_btn = QPushButton("批量调整")
        self.batch_resize_btn.setProperty("buttonType", "success")
        self.batch_resize_btn.clicked.connect(lambda: self.start_batch_operation("批量调整"))
        batch_ops_layout.addWidget(self.batch_resize_btn)
        
        self.batch_validate_btn = QPushButton("批量验证")
        self.batch_validate_btn.setProperty("buttonType", "warning")
        self.batch_validate_btn.clicked.connect(lambda: self.start_batch_operation("批量验证"))
        batch_ops_layout.addWidget(self.batch_validate_btn)
        
        batch_ops_layout.addStretch()
        batch_layout.addLayout(batch_ops_layout)
        
        batch_card.add_layout(batch_layout)
        layout.addWidget(batch_card)
        
        # 自动化工具卡片
        automation_card = Card("🔧 自动化工具")
        automation_layout = QVBoxLayout()
        automation_layout.setSpacing(16)
        
        # 脚本编辑器
        script_layout = QVBoxLayout()
        script_layout.setSpacing(8)
        
        script_label = QLabel("自定义脚本:")
        script_label.setStyleSheet("font-weight: 600; color: #374151;")
        script_layout.addWidget(script_label)
        
        self.script_editor = QTextEdit()
        self.script_editor.setMaximumHeight(120)
        self.script_editor.setPlaceholderText("输入Python脚本代码...")
        self.script_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1f2937;
                color: #f9fafb;
                border: 1px solid #374151;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
            }
        """)
        script_layout.addWidget(self.script_editor)
        
        # 预设脚本
        preset_layout = QHBoxLayout()
        preset_layout.setSpacing(8)
        
        preset_label = QLabel("预设脚本:")
        preset_label.setStyleSheet("font-weight: 600; color: #374151;")
        preset_layout.addWidget(preset_label)
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "选择预设脚本...",
            "图片重命名",
            "标注格式检查",
            "数据集统计",
            "重复文件清理"
        ])
        self.preset_combo.currentTextChanged.connect(self.load_preset_script)
        preset_layout.addWidget(self.preset_combo, 1)
        
        run_script_btn = QPushButton("运行脚本")
        run_script_btn.setProperty("buttonType", "primary")
        run_script_btn.clicked.connect(lambda: self.start_batch_operation("运行脚本"))
        preset_layout.addWidget(run_script_btn)
        
        script_layout.addLayout(preset_layout)
        automation_layout.addLayout(script_layout)
        
        automation_card.add_layout(automation_layout)
        layout.addWidget(automation_card)
        
        # 操作状态卡片
        status_card = Card("📊 操作状态")
        status_layout = QVBoxLayout()
        status_layout.setSpacing(16)
        
        # 进度显示
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #6b7280; font-style: italic;")
        status_layout.addWidget(self.status_label)
        
        # 日志显示
        log_label = QLabel("操作日志:")
        log_label.setStyleSheet("font-weight: 600; color: #374151;")
        status_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                color: #374151;
            }
        """)
        status_layout.addWidget(self.log_text)
        
        status_card.add_layout(status_layout)
        layout.addWidget(status_card)
        
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
    
    def start_ai_feature(self, feature_name):
        """启动AI功能"""
        if not self.input_path:
            QMessageBox.warning(self, "警告", "请先选择输入数据集")
            return
        
        self.add_log(f"启动AI功能: {feature_name}")
        self.start_operation(f"AI{feature_name}")
    
    def start_batch_operation(self, operation):
        """启动批处理操作"""
        if not self.input_path and operation != "运行脚本":
            QMessageBox.warning(self, "警告", "请先选择输入数据集")
            return
        
        if operation == "运行脚本":
            script_content = self.script_editor.toPlainText().strip()
            if not script_content:
                QMessageBox.warning(self, "警告", "请输入脚本内容")
                return
        
        self.add_log(f"启动批处理操作: {operation}")
        self.start_operation(operation)
    
    def start_operation(self, operation):
        """启动操作"""
        # 收集参数
        params = {
            'threads': self.thread_spin.value(),
            'batch_size': self.batch_size_spin.value(),
            'memory_limit': self.memory_limit_spin.value(),
            'use_cache': self.cache_checkbox.isChecked()
        }
        
        # 启动工作线程
        self.worker = AdvancedWorker(operation, params)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.operation_finished)
        
        # 更新界面状态
        self.set_buttons_enabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker.start()
    
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        self.add_log(message)
    
    def operation_finished(self, success, message):
        """操作完成"""
        self.set_buttons_enabled(True)
        self.progress_bar.setVisible(False)
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.status_label.setText("操作成功完成")
            self.add_log(f"✓ {message}")
        else:
            QMessageBox.critical(self, "错误", message)
            self.status_label.setText("操作失败")
            self.add_log(f"✗ {message}")
    
    def load_preset_script(self, preset_name):
        """加载预设脚本"""
        scripts = {
            "图片重命名": """# 批量重命名图片文件
import os
from pathlib import Path

def rename_images(input_dir, prefix="img"):
    count = 1
    for file in Path(input_dir).glob("*.jpg"):
        new_name = f"{prefix}_{count:04d}.jpg"
        file.rename(file.parent / new_name)
        count += 1
    print(f"重命名完成，共处理 {count-1} 个文件")""",
            
            "标注格式检查": """# 检查标注文件格式
import json
from pathlib import Path

def check_annotations(input_dir):
    errors = []
    for file in Path(input_dir).glob("*.json"):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
            # 检查必要字段
            if 'annotations' not in data:
                errors.append(f"{file.name}: 缺少annotations字段")
        except Exception as e:
            errors.append(f"{file.name}: {str(e)}")
    
    if errors:
        print("发现错误:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("所有标注文件格式正确")""",
            
            "数据集统计": """# 统计数据集信息
from pathlib import Path
import json

def analyze_dataset(input_dir):
    image_count = len(list(Path(input_dir).glob("*.jpg")))
    annotation_count = len(list(Path(input_dir).glob("*.json")))
    
    print(f"图片数量: {image_count}")
    print(f"标注数量: {annotation_count}")
    print(f"匹配率: {annotation_count/image_count*100:.1f}%")""",
            
            "重复文件清理": """# 清理重复文件
import hashlib
from pathlib import Path

def remove_duplicates(input_dir):
    seen_hashes = set()
    removed_count = 0
    
    for file in Path(input_dir).glob("*"):
        if file.is_file():
            file_hash = hashlib.md5(file.read_bytes()).hexdigest()
            if file_hash in seen_hashes:
                file.unlink()
                removed_count += 1
            else:
                seen_hashes.add(file_hash)
    
    print(f"清理完成，删除 {removed_count} 个重复文件")"""
        }
        
        if preset_name in scripts:
            self.script_editor.setPlainText(scripts[preset_name])
    
    def add_log(self, message):
        """添加日志"""
        current_text = self.log_text.toPlainText()
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        new_message = f"[{timestamp}] {message}"
        
        if current_text:
            self.log_text.setPlainText(current_text + "\n" + new_message)
        else:
            self.log_text.setPlainText(new_message)
        
        # 滚动到底部
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def set_buttons_enabled(self, enabled):
        """设置按钮状态"""
        self.batch_convert_btn.setEnabled(enabled)
        self.batch_resize_btn.setEnabled(enabled)
        self.batch_validate_btn.setEnabled(enabled)
        
        for card in self.ai_feature_cards:
            card.enable_btn.setEnabled(enabled and card.enabled)