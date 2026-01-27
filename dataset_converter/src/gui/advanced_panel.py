"""
高级功能面板
集成AI质量检测、批量图片处理等高级功能
"""

from pathlib import Path
from typing import List, Dict, Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QTextEdit, QComboBox, QListWidget, QGroupBox,
    QTableWidget, QTableWidgetItem, QTabWidget, QSpinBox,
    QFileDialog, QMessageBox, QProgressBar, QCheckBox,
    QSlider, QDoubleSpinBox, QFormLayout, QScrollArea,
    QSplitter, QTreeWidget, QTreeWidgetItem, QInputDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from ..core.ai_quality_checker import AIQualityChecker, QualityIssueType
from ..core.batch_image_processor import BatchImageProcessor, ProcessingOperation, ProcessingConfig
from ..core.base_parser import ImageAnnotation
from ..core.converter import PARSERS
from .custom_tab_bar import CustomTabWidget


class QualityCheckTab(QWidget):
    """AI质量检测选项卡"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.quality_checker = AIQualityChecker()
        self.annotations = []
        self.quality_result = None
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 数据集选择
        dataset_group = QGroupBox("数据集选择")
        dataset_layout = QHBoxLayout(dataset_group)
        
        self.dataset_label = QLabel("数据集: 未选择")
        btn_select_dataset = QPushButton("选择数据集")
        btn_select_dataset.clicked.connect(self.select_dataset)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["yolo", "yolo_seg", "voc", "json"])
        
        dataset_layout.addWidget(self.dataset_label, 1)
        dataset_layout.addWidget(QLabel("格式:"))
        dataset_layout.addWidget(self.format_combo)
        dataset_layout.addWidget(btn_select_dataset)
        
        layout.addWidget(dataset_group)
        
        # 检测设置
        settings_group = QGroupBox("检测设置")
        settings_layout = QFormLayout(settings_group)
        
        self.check_image_quality = QCheckBox("检测图片质量")
        self.check_image_quality.setChecked(True)
        settings_layout.addRow("", self.check_image_quality)
        
        self.check_bbox_quality = QCheckBox("检测标注质量")
        self.check_bbox_quality.setChecked(True)
        settings_layout.addRow("", self.check_bbox_quality)
        
        self.check_class_balance = QCheckBox("检测类别平衡")
        self.check_class_balance.setChecked(True)
        settings_layout.addRow("", self.check_class_balance)
        
        # 质量阈值设置
        self.min_bbox_size = QSpinBox()
        self.min_bbox_size.setRange(1, 100)
        self.min_bbox_size.setValue(10)
        settings_layout.addRow("最小边界框尺寸:", self.min_bbox_size)
        
        self.max_overlap_ratio = QDoubleSpinBox()
        self.max_overlap_ratio.setRange(0.1, 1.0)
        self.max_overlap_ratio.setSingleStep(0.1)
        self.max_overlap_ratio.setValue(0.7)
        settings_layout.addRow("最大重叠比例:", self.max_overlap_ratio)
        
        layout.addWidget(settings_group)
        
        # 检测按钮
        btn_layout = QHBoxLayout()
        btn_start_check = QPushButton("开始质量检测")
        btn_start_check.setProperty("buttonType", "primary")
        btn_start_check.clicked.connect(self.start_quality_check)
        
        btn_export_report = QPushButton("导出报告")
        btn_export_report.setProperty("buttonType", "success")
        btn_export_report.clicked.connect(self.export_quality_report)
        
        btn_layout.addWidget(btn_start_check)
        btn_layout.addWidget(btn_export_report)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        
        # 结果显示
        result_group = QGroupBox("检测结果")
        result_layout = QVBoxLayout(result_group)
        
        # 总体评分
        score_layout = QHBoxLayout()
        self.score_label = QLabel("质量评分: --")
        self.score_label.setProperty("labelType", "title")
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        score_layout.addWidget(self.score_label)
        score_layout.addStretch()
        score_layout.addWidget(self.progress_bar)
        
        result_layout.addLayout(score_layout)
        
        # 问题列表
        self.issue_table = QTableWidget()
        self.issue_table.setColumnCount(4)
        self.issue_table.setHorizontalHeaderLabels([
            "问题类型", "严重程度", "描述", "建议"
        ])
        result_layout.addWidget(self.issue_table)
        
        layout.addWidget(result_group)
    
    def select_dataset(self):
        """选择数据集"""
        directory = QFileDialog.getExistingDirectory(self, "选择数据集目录")
        if not directory:
            return
        
        try:
            # 验证数据集结构
            from ..core.dataset_validator import DatasetValidator
            dataset_info = DatasetValidator.get_dataset_info(Path(directory))
            
            if not dataset_info["is_valid"]:
                QMessageBox.critical(self, "数据集格式错误", 
                    f"数据集格式不符合要求:\n{dataset_info['message']}")
                return
            
            self.dataset_label.setText(f"数据集: {directory}")
            
            # 自动检测格式
            if dataset_info["detected_format"]:
                format_index = self.format_combo.findText(dataset_info["detected_format"])
                if format_index >= 0:
                    self.format_combo.setCurrentIndex(format_index)
            
            QMessageBox.information(self, "成功", "数据集加载成功！")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据集失败: {e}")
    
    def start_quality_check(self):
        """开始质量检测"""
        dataset_path = self.dataset_label.text().replace("数据集: ", "")
        if dataset_path == "未选择":
            QMessageBox.warning(self, "警告", "请先选择数据集")
            return
        
        try:
            # 显示进度条
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # 不确定进度
            
            # 更新质量检测器阈值
            self.quality_checker.thresholds['min_bbox_size'] = self.min_bbox_size.value()
            self.quality_checker.thresholds['max_overlap_ratio'] = self.max_overlap_ratio.value()
            
            # 解析数据集
            format_name = self.format_combo.currentText()
            parser = PARSERS[format_name]
            
            if hasattr(parser, "set_label_map"):
                parser.set_label_map({})
            
            self.annotations = parser.parse(Path(dataset_path))
            
            if not self.annotations:
                QMessageBox.warning(self, "警告", "未找到有效的标注数据")
                return
            
            # 执行质量检测
            self.quality_result = self.quality_checker.check_dataset_quality(self.annotations)
            
            # 更新显示
            self.update_quality_display()
            
            # 隐藏进度条
            self.progress_bar.setVisible(False)
            
            QMessageBox.information(self, "完成", 
                f"质量检测完成！\n"
                f"检测了 {len(self.annotations)} 个标注\n"
                f"发现 {self.quality_result['total_issues']} 个问题\n"
                f"质量评分: {self.quality_result['quality_score']}/100")
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, "错误", f"质量检测失败: {e}")
    
    def update_quality_display(self):
        """更新质量显示"""
        if not self.quality_result:
            return
        
        # 更新评分
        score = self.quality_result['quality_score']
        self.score_label.setText(f"质量评分: {score}/100")
        
        # 根据评分设置颜色
        if score >= 80:
            color = "green"
        elif score >= 60:
            color = "orange"
        else:
            color = "red"
        
        self.score_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        
        # 更新问题表格
        issues = self.quality_result['issues']
        self.issue_table.setRowCount(len(issues))
        
        for row, issue in enumerate(issues):
            # 问题类型
            issue_type = issue.issue_type.value.replace('_', ' ').title()
            self.issue_table.setItem(row, 0, QTableWidgetItem(issue_type))
            
            # 严重程度
            severity_item = QTableWidgetItem(issue.severity)
            if issue.severity == "high":
                severity_item.setBackground(Qt.red)
            elif issue.severity == "medium":
                severity_item.setBackground(Qt.yellow)
            else:
                severity_item.setBackground(Qt.lightGray)
            self.issue_table.setItem(row, 1, severity_item)
            
            # 描述
            self.issue_table.setItem(row, 2, QTableWidgetItem(issue.description))
            
            # 建议
            self.issue_table.setItem(row, 3, QTableWidgetItem(issue.suggestion))
        
        # 调整列宽
        self.issue_table.resizeColumnsToContents()
    
    def export_quality_report(self):
        """导出质量报告"""
        if not self.quality_result:
            QMessageBox.warning(self, "警告", "请先进行质量检测")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存质量报告", "quality_report.md", 
            "Markdown文件 (*.md);;文本文件 (*.txt)"
        )
        
        if file_path:
            try:
                self.quality_checker.export_quality_report(self.quality_result, Path(file_path))
                QMessageBox.information(self, "成功", f"质量报告已保存到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出报告失败: {e}")


class BatchProcessingTab(QWidget):
    """批量图片处理选项卡"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.processor = BatchImageProcessor()
        self.processing_configs = []
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 输入输出目录
        io_group = QGroupBox("输入输出设置")
        io_layout = QVBoxLayout(io_group)
        
        # 输入目录
        input_layout = QHBoxLayout()
        self.input_label = QLabel("输入目录: 未选择")
        btn_select_input = QPushButton("选择输入目录")
        btn_select_input.clicked.connect(self.select_input_dir)
        
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
        
        # 处理配置
        config_splitter = QSplitter(Qt.Horizontal)
        
        # 左侧：可用操作
        operations_widget = QWidget()
        operations_layout = QVBoxLayout(operations_widget)
        
        operations_layout.addWidget(QLabel("可用操作:"))
        
        self.operations_list = QListWidget()
        operations = [
            "调整尺寸", "裁剪", "旋转", "翻转", 
            "调整亮度", "调整对比度", "调整饱和度",
            "模糊", "锐化", "转灰度", "格式转换", "标准化"
        ]
        for op in operations:
            self.operations_list.addItem(op)
        
        operations_layout.addWidget(self.operations_list)
        
        btn_add_operation = QPushButton("添加操作")
        btn_add_operation.clicked.connect(self.add_operation)
        operations_layout.addWidget(btn_add_operation)
        
        config_splitter.addWidget(operations_widget)
        
        # 右侧：已选操作和参数
        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        
        config_layout.addWidget(QLabel("处理流程:"))
        
        self.config_table = QTableWidget()
        self.config_table.setColumnCount(4)
        self.config_table.setHorizontalHeaderLabels([
            "操作", "参数", "启用", "操作"
        ])
        config_layout.addWidget(self.config_table)
        
        # 预设配置
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("预设:"))
        
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "自定义", "网页优化", "缩略图生成", "图像增强", "数据集准备"
        ])
        self.preset_combo.currentTextChanged.connect(self.load_preset)
        
        btn_save_preset = QPushButton("保存预设")
        btn_save_preset.clicked.connect(self.save_preset)
        
        preset_layout.addWidget(self.preset_combo)
        preset_layout.addWidget(btn_save_preset)
        preset_layout.addStretch()
        
        config_layout.addLayout(preset_layout)
        
        config_splitter.addWidget(config_widget)
        config_splitter.setSizes([300, 500])
        
        layout.addWidget(config_splitter)
        
        # 处理按钮
        process_layout = QHBoxLayout()
        
        btn_start_process = QPushButton("开始批量处理")
        btn_start_process.setProperty("buttonType", "primary")
        btn_start_process.clicked.connect(self.start_batch_processing)
        
        btn_preview = QPushButton("预览效果")
        btn_preview.clicked.connect(self.preview_processing)
        
        process_layout.addWidget(btn_start_process)
        process_layout.addWidget(btn_preview)
        process_layout.addStretch()
        
        layout.addLayout(process_layout)
        
        # 进度显示
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
    
    def select_input_dir(self):
        """选择输入目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择输入目录")
        if directory:
            self.input_label.setText(f"输入目录: {directory}")
    
    def select_output_dir(self):
        """选择输出目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if directory:
            self.output_label.setText(f"输出目录: {directory}")
    
    def add_operation(self):
        """添加处理操作"""
        current_item = self.operations_list.currentItem()
        if not current_item:
            return
        
        operation_name = current_item.text()
        
        # 根据操作类型创建默认配置
        config = self._create_default_config(operation_name)
        if config:
            self.processing_configs.append(config)
            self.update_config_table()
    
    def _create_default_config(self, operation_name: str) -> Optional[ProcessingConfig]:
        """创建默认配置"""
        operation_map = {
            "调整尺寸": (ProcessingOperation.RESIZE, {'width': 640, 'height': 640, 'mode': 'exact'}),
            "裁剪": (ProcessingOperation.CROP, {'x': 0, 'y': 0, 'width': 100, 'height': 100}),
            "旋转": (ProcessingOperation.ROTATE, {'angle': 90, 'expand': True}),
            "翻转": (ProcessingOperation.FLIP, {'direction': 'horizontal'}),
            "调整亮度": (ProcessingOperation.BRIGHTNESS, {'factor': 1.2}),
            "调整对比度": (ProcessingOperation.CONTRAST, {'factor': 1.2}),
            "调整饱和度": (ProcessingOperation.SATURATION, {'factor': 1.2}),
            "模糊": (ProcessingOperation.BLUR, {'radius': 1.0}),
            "锐化": (ProcessingOperation.SHARPEN, {'factor': 0.5}),
            "转灰度": (ProcessingOperation.GRAYSCALE, {}),
            "格式转换": (ProcessingOperation.FORMAT_CONVERT, {'format': 'JPEG'}),
            "标准化": (ProcessingOperation.NORMALIZE, {})
        }
        
        if operation_name in operation_map:
            operation, params = operation_map[operation_name]
            return ProcessingConfig(operation, params)
        
        return None
    
    def update_config_table(self):
        """更新配置表格"""
        self.config_table.setRowCount(len(self.processing_configs))
        
        for row, config in enumerate(self.processing_configs):
            # 操作名称
            op_name = config.operation.value.replace('_', ' ').title()
            self.config_table.setItem(row, 0, QTableWidgetItem(op_name))
            
            # 参数
            params_str = ", ".join([f"{k}={v}" for k, v in config.parameters.items()])
            self.config_table.setItem(row, 1, QTableWidgetItem(params_str))
            
            # 启用状态
            enabled_check = QCheckBox()
            enabled_check.setChecked(config.enabled)
            enabled_check.stateChanged.connect(
                lambda state, idx=row: self._update_config_enabled(idx, state == Qt.Checked)
            )
            self.config_table.setCellWidget(row, 2, enabled_check)
            
            # 删除按钮
            btn_delete = QPushButton("删除")
            btn_delete.clicked.connect(lambda checked, idx=row: self._delete_config(idx))
            self.config_table.setCellWidget(row, 3, btn_delete)
        
        self.config_table.resizeColumnsToContents()
    
    def _update_config_enabled(self, index: int, enabled: bool):
        """更新配置启用状态"""
        if 0 <= index < len(self.processing_configs):
            self.processing_configs[index].enabled = enabled
    
    def _delete_config(self, index: int):
        """删除配置"""
        if 0 <= index < len(self.processing_configs):
            del self.processing_configs[index]
            self.update_config_table()
    
    def load_preset(self, preset_name: str):
        """加载预设配置"""
        if preset_name == "自定义":
            return
        
        preset_map = {
            "网页优化": "web_optimization",
            "缩略图生成": "thumbnail_generation", 
            "图像增强": "image_enhancement",
            "数据集准备": "dataset_preparation"
        }
        
        if preset_name in preset_map:
            self.processing_configs = self.processor.create_preset_configs(preset_map[preset_name])
            self.update_config_table()
    
    def save_preset(self):
        """保存预设配置"""
        if not self.processing_configs:
            QMessageBox.warning(self, "警告", "没有配置可保存")
            return
        
        preset_name, ok = QInputDialog.getText(self, "保存预设", "预设名称:")
        if ok and preset_name:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "保存预设配置", f"{preset_name}.json",
                "JSON文件 (*.json)"
            )
            
            if file_path:
                try:
                    self.processor.save_config_preset(self.processing_configs, preset_name, Path(file_path))
                    QMessageBox.information(self, "成功", f"预设已保存到: {file_path}")
                except Exception as e:
                    QMessageBox.critical(self, "错误", f"保存预设失败: {e}")
    
    def start_batch_processing(self):
        """开始批量处理"""
        input_dir = self.input_label.text().replace("输入目录: ", "")
        output_dir = self.output_label.text().replace("输出目录: ", "")
        
        if input_dir == "未选择" or output_dir == "未选择":
            QMessageBox.warning(self, "警告", "请选择输入和输出目录")
            return
        
        if not self.processing_configs:
            QMessageBox.warning(self, "警告", "请添加至少一个处理操作")
            return
        
        try:
            # 显示进度
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 100)
            
            def progress_callback(current, total, description):
                progress = int((current / total) * 100) if total > 0 else 0
                self.progress_bar.setValue(progress)
                self.status_label.setText(description)
            
            def status_callback(status):
                self.status_label.setText(status)
            
            # 执行批量处理
            result = self.processor.process_images(
                Path(input_dir), Path(output_dir), self.processing_configs,
                progress_callback, status_callback
            )
            
            # 隐藏进度条
            self.progress_bar.setVisible(False)
            self.status_label.setText("处理完成")
            
            # 显示结果
            stats = result['stats']
            QMessageBox.information(self, "处理完成",
                f"批量处理完成！\n"
                f"总计: {stats['total_processed']} 个文件\n"
                f"成功: {stats['successful']} 个\n"
                f"失败: {stats['failed']} 个")
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, "错误", f"批量处理失败: {e}")
    
    def preview_processing(self):
        """预览处理效果"""
        QMessageBox.information(self, "提示", "预览功能正在开发中...")


class AdvancedPanel(QWidget):
    """高级功能面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.apply_styles()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title = QLabel("高级功能")
        title.setProperty("labelType", "title")
        layout.addWidget(title)
        
        # 选项卡控件
        self.tab_widget = CustomTabWidget()
        
        # AI质量检测选项卡
        self.quality_tab = QualityCheckTab(self)
        self.tab_widget.addTab(self.quality_tab, "AI质量检测")
        
        # 批量图片处理选项卡
        self.batch_tab = BatchProcessingTab(self)
        self.tab_widget.addTab(self.batch_tab, "批量处理")
        
        layout.addWidget(self.tab_widget)
    
    def apply_styles(self):
        """应用样式"""
        # 为按钮设置属性
        for btn in self.findChildren(QPushButton):
            if not btn.property("buttonType"):
                btn.setProperty("buttonType", "default")