"""
QML风格数据分析面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QFrame,
    QGridLayout, QTextEdit, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor

from .qml_style_window import Card


class AnalysisWorker(QThread):
    """分析工作线程"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str, dict)
    
    def __init__(self, input_path):
        super().__init__()
        self.input_path = Path(input_path)
    
    def run(self):
        try:
            self.progress_updated.emit(10, "正在扫描数据集...")
            
            # 模拟分析过程
            import time
            for i in range(10, 101, 20):
                time.sleep(0.4)
                if i == 30:
                    self.progress_updated.emit(i, "正在统计文件信息...")
                elif i == 50:
                    self.progress_updated.emit(i, "正在分析标注质量...")
                elif i == 70:
                    self.progress_updated.emit(i, "正在计算统计指标...")
                elif i == 90:
                    self.progress_updated.emit(i, "正在生成报告...")
                else:
                    self.progress_updated.emit(i, f"分析进度 {i}%")
            
            # 模拟分析结果
            result = {
                'total_images': 1000,
                'total_annotations': 5000,
                'classes': ['person', 'car', 'bicycle', 'dog', 'cat'],
                'class_counts': [2000, 1500, 800, 400, 300],
                'avg_objects_per_image': 5.0,
                'image_sizes': [(640, 480), (1920, 1080), (800, 600)],
                'quality_score': 85.5
            }
            
            self.progress_updated.emit(100, "分析完成")
            self.finished.emit(True, "数据集分析成功完成！", result)
            
        except Exception as e:
            self.finished.emit(False, f"分析失败: {str(e)}", {})


class StatCard(QFrame):
    """统计卡片组件"""
    
    def __init__(self, title="", value="", icon="📊", color="#3b82f6", parent=None):
        super().__init__(parent)
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        # 图标和值
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_label.setObjectName("statIcon")
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(icon_label)
        
        top_layout.addStretch()
        
        self.value_label = QLabel(self.value)
        self.value_label.setObjectName("statValue")
        top_layout.addWidget(self.value_label)
        
        layout.addLayout(top_layout)
        
        # 标题
        self.title_label = QLabel(self.title)
        self.title_label.setObjectName("statTitle")
        layout.addWidget(self.title_label)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet(f"""
            StatCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 white, stop:1 #f8fafc);
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                min-height: 100px;
                max-height: 120px;
            }}
            
            StatCard:hover {{
                border-color: {self.color};
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 white, stop:1 #f1f5f9);
            }}
            
            #statIcon {{
                font-size: 24px;
                color: {self.color};
            }}
            
            #statValue {{
                font-size: 24px;
                font-weight: 700;
                color: {self.color};
            }}
            
            #statTitle {{
                font-size: 12px;
                color: #6b7280;
                font-weight: 500;
            }}
        """)
    
    def update_value(self, value):
        """更新值"""
        self.value = value
        self.value_label.setText(str(value))


class QMLAnalysisPanel(QWidget):
    """QML风格数据分析面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.input_path = ""
        self.analysis_result = {}
        
        # 设置大小策略
        from PyQt5.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 路径选择卡片
        path_card = Card("📁 数据集路径")
        path_layout = QHBoxLayout()
        path_layout.setSpacing(12)
        
        self.path_label = QLabel("未选择数据集")
        self.path_label.setObjectName("pathLabel")
        self.path_label.setStyleSheet("""
            #pathLabel {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 12px 16px;
                color: #6b7280;
                font-style: italic;
            }
        """)
        path_layout.addWidget(self.path_label, 1)
        
        select_btn = QPushButton("选择数据集")
        select_btn.setProperty("buttonType", "primary")
        select_btn.clicked.connect(self.select_dataset)
        path_layout.addWidget(select_btn)
        
        path_card.add_layout(path_layout)
        layout.addWidget(path_card)
        
        # 统计概览卡片
        stats_card = Card("📊 统计概览")
        stats_layout = QGridLayout()
        stats_layout.setSpacing(16)
        
        # 创建统计卡片
        self.total_images_card = StatCard("总图片数", "0", "🖼️", "#3b82f6")
        stats_layout.addWidget(self.total_images_card, 0, 0)
        
        self.total_annotations_card = StatCard("总标注数", "0", "🏷️", "#10b981")
        stats_layout.addWidget(self.total_annotations_card, 0, 1)
        
        self.avg_objects_card = StatCard("平均对象数", "0", "📈", "#f59e0b")
        stats_layout.addWidget(self.avg_objects_card, 0, 2)
        
        self.quality_score_card = StatCard("质量评分", "0", "⭐", "#ef4444")
        stats_layout.addWidget(self.quality_score_card, 0, 3)
        
        stats_card.add_layout(stats_layout)
        layout.addWidget(stats_card)
        
        # 类别分布卡片
        class_card = Card("🏷️ 类别分布")
        self.class_table = QTableWidget()
        self.class_table.setColumnCount(3)
        self.class_table.setHorizontalHeaderLabels(["类别", "数量", "占比"])
        self.class_table.setAlternatingRowColors(True)
        self.class_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.class_table.horizontalHeader().setStretchLastSection(True)
        self.class_table.verticalHeader().setVisible(False)
        self.class_table.setMinimumHeight(200)  # 设置最小高度
        self.class_table.setMaximumHeight(300)  # 设置最大高度
        self.class_table.setStyleSheet("""
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
        class_card.add_widget(self.class_table)
        layout.addWidget(class_card)
        
        # 详细报告卡片
        report_card = Card("📋 详细报告")
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setMinimumHeight(150)  # 设置最小高度
        self.report_text.setMaximumHeight(250)  # 增加最大高度
        self.report_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 16px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 13px;
                color: #374151;
            }
        """)
        report_card.add_widget(self.report_text)
        layout.addWidget(report_card)
        
        # 操作卡片
        action_card = Card("⚡ 执行操作")
        action_layout = QVBoxLayout()
        action_layout.setSpacing(16)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.analyze_btn = QPushButton("开始分析")
        self.analyze_btn.setProperty("buttonType", "primary")
        self.analyze_btn.clicked.connect(self.start_analysis)
        self.analyze_btn.setEnabled(False)
        button_layout.addWidget(self.analyze_btn)
        
        self.export_btn = QPushButton("导出报告")
        self.export_btn.setProperty("buttonType", "success")
        self.export_btn.clicked.connect(self.export_report)
        self.export_btn.setEnabled(False)
        button_layout.addWidget(self.export_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setProperty("buttonType", "danger")
        self.cancel_btn.clicked.connect(self.cancel_analysis)
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
    
    def select_dataset(self):
        """选择数据集"""
        path = QFileDialog.getExistingDirectory(self, "选择数据集目录")
        if path:
            self.input_path = path
            display_path = str(Path(path).name) if len(path) > 50 else path
            self.path_label.setText(display_path)
            self.path_label.setToolTip(path)
            self.path_label.setStyleSheet("""
                #pathLabel {
                    background-color: white;
                    border: 1px solid #10b981;
                    border-radius: 6px;
                    padding: 12px 16px;
                    color: #374151;
                    font-weight: 500;
                }
            """)
            self.analyze_btn.setEnabled(True)
    
    def start_analysis(self):
        """开始分析"""
        if not self.input_path:
            QMessageBox.warning(self, "警告", "请先选择数据集目录")
            return
        
        # 启动分析
        self.worker = AnalysisWorker(self.input_path)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.analysis_finished)
        
        # 更新界面状态
        self.analyze_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker.start()
    
    def cancel_analysis(self):
        """取消分析"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        self.reset_ui_state()
        self.status_label.setText("分析已取消")
    
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def analysis_finished(self, success, message, result):
        """分析完成"""
        self.reset_ui_state()
        
        if success:
            self.analysis_result = result
            self.update_results(result)
            self.export_btn.setEnabled(True)
            QMessageBox.information(self, "成功", message)
            self.status_label.setText("分析成功完成")
        else:
            QMessageBox.critical(self, "错误", message)
            self.status_label.setText("分析失败")
    
    def update_results(self, result):
        """更新结果显示"""
        # 更新统计卡片
        self.total_images_card.update_value(result.get('total_images', 0))
        self.total_annotations_card.update_value(result.get('total_annotations', 0))
        self.avg_objects_card.update_value(f"{result.get('avg_objects_per_image', 0):.1f}")
        self.quality_score_card.update_value(f"{result.get('quality_score', 0):.1f}")
        
        # 更新类别表格
        classes = result.get('classes', [])
        class_counts = result.get('class_counts', [])
        total_annotations = result.get('total_annotations', 1)
        
        self.class_table.setRowCount(len(classes))
        for i, (cls, count) in enumerate(zip(classes, class_counts)):
            self.class_table.setItem(i, 0, QTableWidgetItem(cls))
            self.class_table.setItem(i, 1, QTableWidgetItem(str(count)))
            self.class_table.setItem(i, 2, QTableWidgetItem(f"{count/total_annotations*100:.1f}%"))
        
        # 更新详细报告
        report = self.generate_report(result)
        self.report_text.setPlainText(report)
    
    def generate_report(self, result):
        """生成详细报告"""
        report = f"""数据集分析报告
{'='*50}

基本信息:
- 总图片数: {result.get('total_images', 0)}
- 总标注数: {result.get('total_annotations', 0)}
- 平均每张图片对象数: {result.get('avg_objects_per_image', 0):.2f}
- 质量评分: {result.get('quality_score', 0):.1f}/100

类别分布:"""
        
        classes = result.get('classes', [])
        class_counts = result.get('class_counts', [])
        total_annotations = result.get('total_annotations', 1)
        
        for cls, count in zip(classes, class_counts):
            percentage = count / total_annotations * 100
            report += f"\n- {cls}: {count} ({percentage:.1f}%)"
        
        report += f"""

图片尺寸分布:"""
        image_sizes = result.get('image_sizes', [])
        for size in image_sizes:
            report += f"\n- {size[0]}x{size[1]}"
        
        return report
    
    def export_report(self):
        """导出报告"""
        if not self.analysis_result:
            QMessageBox.warning(self, "警告", "没有可导出的分析结果")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存分析报告", 
            "dataset_analysis_report.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.report_text.toPlainText())
                QMessageBox.information(self, "成功", f"报告已保存到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
    
    def reset_ui_state(self):
        """重置界面状态"""
        self.analyze_btn.setEnabled(bool(self.input_path))
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)