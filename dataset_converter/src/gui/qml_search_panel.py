"""
QML风格数据搜索面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QFrame,
    QGridLayout, QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QCheckBox, QSlider, QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor

from .qml_style_window import Card


class SearchWorker(QThread):
    """搜索工作线程"""
    progress_updated = pyqtSignal(int, str)
    result_found = pyqtSignal(dict)
    finished = pyqtSignal(bool, str, list)
    
    def __init__(self, input_path, search_params):
        super().__init__()
        self.input_path = Path(input_path)
        self.search_params = search_params
    
    def run(self):
        try:
            self.progress_updated.emit(10, "正在扫描数据集...")
            
            # 模拟搜索过程
            import time
            results = []
            
            for i in range(10, 101, 15):
                time.sleep(0.2)
                if i == 25:
                    self.progress_updated.emit(i, "正在分析图片...")
                elif i == 40:
                    self.progress_updated.emit(i, "正在匹配条件...")
                    # 模拟找到结果
                    result = {
                        'filename': f'image_{i}.jpg',
                        'class': 'person',
                        'confidence': 0.95,
                        'bbox_count': 3
                    }
                    results.append(result)
                    self.result_found.emit(result)
                elif i == 55:
                    self.progress_updated.emit(i, "正在筛选结果...")
                elif i == 70:
                    self.progress_updated.emit(i, "正在排序结果...")
                elif i == 85:
                    self.progress_updated.emit(i, "正在整理输出...")
                else:
                    self.progress_updated.emit(i, f"搜索进度 {i}%")
                
                # 模拟更多结果
                if i % 20 == 0 and i > 20:
                    result = {
                        'filename': f'sample_{i}.jpg',
                        'class': self.search_params.get('class', 'car'),
                        'confidence': 0.8 + (i % 20) * 0.01,
                        'bbox_count': (i % 5) + 1
                    }
                    results.append(result)
                    self.result_found.emit(result)
            
            self.progress_updated.emit(100, "搜索完成")
            self.finished.emit(True, f"搜索完成，找到 {len(results)} 个结果", results)
            
        except Exception as e:
            self.finished.emit(False, f"搜索失败: {str(e)}", [])


class SearchFilter(QFrame):
    """搜索过滤器组件"""
    
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.title = title
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 标题
        title_label = QLabel(self.title)
        title_label.setObjectName("filterTitle")
        layout.addWidget(title_label)
        
        # 过滤器内容将由子类实现
        self.content_layout = QVBoxLayout()
        layout.addLayout(self.content_layout)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            SearchFilter {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            
            SearchFilter:hover {
                border-color: #cbd5e1;
            }
            
            #filterTitle {
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }
        """)


class ClassFilter(SearchFilter):
    """类别过滤器"""
    
    def __init__(self, parent=None):
        super().__init__("类别筛选", parent)
        self.setup_content()
    
    def setup_content(self):
        """设置内容"""
        # 类别选择
        self.class_combo = QComboBox()
        self.class_combo.addItems(["全部", "person", "car", "bicycle", "dog", "cat", "truck", "bus"])
        self.content_layout.addWidget(self.class_combo)
        
        # 启用复选框
        self.enabled_checkbox = QCheckBox("启用类别筛选")
        self.enabled_checkbox.setChecked(True)
        self.content_layout.addWidget(self.enabled_checkbox)
    
    def get_filter_value(self):
        """获取过滤值"""
        if not self.enabled_checkbox.isChecked():
            return None
        return self.class_combo.currentText() if self.class_combo.currentText() != "全部" else None


class ConfidenceFilter(SearchFilter):
    """置信度过滤器"""
    
    def __init__(self, parent=None):
        super().__init__("置信度筛选", parent)
        self.setup_content()
    
    def setup_content(self):
        """设置内容"""
        # 最小置信度
        min_layout = QHBoxLayout()
        min_layout.addWidget(QLabel("最小值:"))
        
        self.min_slider = QSlider(Qt.Horizontal)
        self.min_slider.setRange(0, 100)
        self.min_slider.setValue(50)
        self.min_slider.valueChanged.connect(self.update_labels)
        min_layout.addWidget(self.min_slider)
        
        self.min_label = QLabel("0.50")
        self.min_label.setMinimumWidth(40)
        min_layout.addWidget(self.min_label)
        
        self.content_layout.addLayout(min_layout)
        
        # 最大置信度
        max_layout = QHBoxLayout()
        max_layout.addWidget(QLabel("最大值:"))
        
        self.max_slider = QSlider(Qt.Horizontal)
        self.max_slider.setRange(0, 100)
        self.max_slider.setValue(100)
        self.max_slider.valueChanged.connect(self.update_labels)
        max_layout.addWidget(self.max_slider)
        
        self.max_label = QLabel("1.00")
        self.max_label.setMinimumWidth(40)
        max_layout.addWidget(self.max_label)
        
        self.content_layout.addLayout(max_layout)
        
        # 启用复选框
        self.enabled_checkbox = QCheckBox("启用置信度筛选")
        self.enabled_checkbox.setChecked(False)
        self.content_layout.addWidget(self.enabled_checkbox)
        
        self.update_labels()
    
    def update_labels(self):
        """更新标签"""
        self.min_label.setText(f"{self.min_slider.value()/100:.2f}")
        self.max_label.setText(f"{self.max_slider.value()/100:.2f}")
    
    def get_filter_value(self):
        """获取过滤值"""
        if not self.enabled_checkbox.isChecked():
            return None
        return (self.min_slider.value()/100, self.max_slider.value()/100)


class CountFilter(SearchFilter):
    """对象数量过滤器"""
    
    def __init__(self, parent=None):
        super().__init__("对象数量筛选", parent)
        self.setup_content()
    
    def setup_content(self):
        """设置内容"""
        # 最小数量
        min_layout = QHBoxLayout()
        min_layout.addWidget(QLabel("最小数量:"))
        
        self.min_spin = QSpinBox()
        self.min_spin.setRange(0, 100)
        self.min_spin.setValue(1)
        min_layout.addWidget(self.min_spin)
        
        self.content_layout.addLayout(min_layout)
        
        # 最大数量
        max_layout = QHBoxLayout()
        max_layout.addWidget(QLabel("最大数量:"))
        
        self.max_spin = QSpinBox()
        self.max_spin.setRange(0, 100)
        self.max_spin.setValue(10)
        max_layout.addWidget(self.max_spin)
        
        self.content_layout.addLayout(max_layout)
        
        # 启用复选框
        self.enabled_checkbox = QCheckBox("启用数量筛选")
        self.enabled_checkbox.setChecked(False)
        self.content_layout.addWidget(self.enabled_checkbox)
    
    def get_filter_value(self):
        """获取过滤值"""
        if not self.enabled_checkbox.isChecked():
            return None
        return (self.min_spin.value(), self.max_spin.value())


class ResultItem(QFrame):
    """结果项组件"""
    
    def __init__(self, result_data, parent=None):
        super().__init__(parent)
        self.result_data = result_data
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 文件图标
        icon_label = QLabel("🖼️")
        icon_label.setFixedSize(32, 32)
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # 文件信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        # 文件名
        filename_label = QLabel(self.result_data['filename'])
        filename_label.setObjectName("filename")
        info_layout.addWidget(filename_label)
        
        # 详细信息
        details = f"类别: {self.result_data['class']} | 置信度: {self.result_data['confidence']:.2f} | 对象数: {self.result_data['bbox_count']}"
        details_label = QLabel(details)
        details_label.setObjectName("details")
        info_layout.addWidget(details_label)
        
        layout.addLayout(info_layout, 1)
        
        # 操作按钮
        view_btn = QPushButton("查看")
        view_btn.setObjectName("viewBtn")
        view_btn.setFixedSize(60, 30)
        layout.addWidget(view_btn)
    
    def setup_style(self):
        """设置样式"""
        self.setStyleSheet("""
            ResultItem {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin: 2px 0;
            }
            
            ResultItem:hover {
                border-color: #3b82f6;
                background-color: #f8fafc;
            }
            
            #filename {
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }
            
            #details {
                font-size: 12px;
                color: #6b7280;
            }
            
            #viewBtn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3b82f6, stop:1 #2563eb);
                border: 1px solid #2563eb;
                color: white;
                border-radius: 4px;
                font-size: 12px;
                font-weight: 500;
            }
            
            #viewBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2563eb, stop:1 #1d4ed8);
            }
        """)


class QMLSearchPanel(QWidget):
    """QML风格数据搜索面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.input_path = ""
        self.search_results = []
        
        # 设置大小策略
        from PyQt5.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 数据集选择卡片
        dataset_card = Card("📁 数据集选择")
        dataset_layout = QHBoxLayout()
        dataset_layout.setSpacing(12)
        
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
        dataset_layout.addWidget(self.path_label, 1)
        
        select_btn = QPushButton("选择数据集")
        select_btn.setProperty("buttonType", "primary")
        select_btn.clicked.connect(self.select_dataset)
        dataset_layout.addWidget(select_btn)
        
        dataset_card.add_layout(dataset_layout)
        layout.addWidget(dataset_card)
        
        # 搜索条件卡片
        search_card = Card("🔍 搜索条件")
        search_layout = QVBoxLayout()
        search_layout.setSpacing(16)
        
        # 关键词搜索
        keyword_layout = QHBoxLayout()
        keyword_layout.setSpacing(8)
        
        keyword_label = QLabel("关键词:")
        keyword_label.setStyleSheet("font-weight: 600; color: #374151; min-width: 60px;")
        keyword_layout.addWidget(keyword_label)
        
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("输入搜索关键词...")
        keyword_layout.addWidget(self.keyword_input, 1)
        
        search_layout.addLayout(keyword_layout)
        
        # 过滤器
        filters_layout = QGridLayout()
        filters_layout.setSpacing(12)
        
        # 类别过滤器
        self.class_filter = ClassFilter()
        filters_layout.addWidget(self.class_filter, 0, 0)
        
        # 置信度过滤器
        self.confidence_filter = ConfidenceFilter()
        filters_layout.addWidget(self.confidence_filter, 0, 1)
        
        # 数量过滤器
        self.count_filter = CountFilter()
        filters_layout.addWidget(self.count_filter, 0, 2)
        
        search_layout.addLayout(filters_layout)
        search_card.add_layout(search_layout)
        layout.addWidget(search_card)
        
        # 搜索结果卡片
        results_card = Card("📋 搜索结果")
        results_layout = QVBoxLayout()
        results_layout.setSpacing(12)
        
        # 结果统计
        self.result_stats = QLabel("等待搜索...")
        self.result_stats.setStyleSheet("color: #6b7280; font-style: italic;")
        results_layout.addWidget(self.result_stats)
        
        # 结果列表
        self.results_list = QListWidget()
        self.results_list.setMinimumHeight(250)  # 设置最小高度
        self.results_list.setStyleSheet("""
            QListWidget {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 2px;
            }
        """)
        results_layout.addWidget(self.results_list)
        
        results_card.add_layout(results_layout)
        layout.addWidget(results_card)
        
        # 操作卡片
        action_card = Card("⚡ 执行操作")
        action_layout = QVBoxLayout()
        action_layout.setSpacing(16)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.search_btn = QPushButton("开始搜索")
        self.search_btn.setProperty("buttonType", "primary")
        self.search_btn.clicked.connect(self.start_search)
        self.search_btn.setEnabled(False)
        button_layout.addWidget(self.search_btn)
        
        self.export_btn = QPushButton("导出结果")
        self.export_btn.setProperty("buttonType", "success")
        self.export_btn.clicked.connect(self.export_results)
        self.export_btn.setEnabled(False)
        button_layout.addWidget(self.export_btn)
        
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.setProperty("buttonType", "danger")
        self.cancel_btn.clicked.connect(self.cancel_search)
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
            self.search_btn.setEnabled(True)
    
    def start_search(self):
        """开始搜索"""
        if not self.input_path:
            QMessageBox.warning(self, "警告", "请先选择数据集目录")
            return
        
        # 收集搜索参数
        search_params = {
            'keyword': self.keyword_input.text(),
            'class': self.class_filter.get_filter_value(),
            'confidence': self.confidence_filter.get_filter_value(),
            'count': self.count_filter.get_filter_value()
        }
        
        # 清空之前的结果
        self.results_list.clear()
        self.search_results = []
        
        # 启动搜索
        self.worker = SearchWorker(self.input_path, search_params)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.result_found.connect(self.add_result)
        self.worker.finished.connect(self.search_finished)
        
        # 更新界面状态
        self.search_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.result_stats.setText("搜索中...")
        
        self.worker.start()
    
    def cancel_search(self):
        """取消搜索"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        self.reset_ui_state()
        self.status_label.setText("搜索已取消")
    
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def add_result(self, result_data):
        """添加搜索结果"""
        self.search_results.append(result_data)
        
        # 创建结果项
        result_item = ResultItem(result_data)
        
        # 添加到列表
        list_item = QListWidgetItem()
        list_item.setSizeHint(result_item.sizeHint())
        self.results_list.addItem(list_item)
        self.results_list.setItemWidget(list_item, result_item)
        
        # 更新统计
        self.result_stats.setText(f"已找到 {len(self.search_results)} 个结果")
    
    def search_finished(self, success, message, results):
        """搜索完成"""
        self.reset_ui_state()
        
        if success:
            self.export_btn.setEnabled(len(results) > 0)
            self.result_stats.setText(f"搜索完成，共找到 {len(results)} 个结果")
            self.status_label.setText("搜索成功完成")
        else:
            QMessageBox.critical(self, "错误", message)
            self.status_label.setText("搜索失败")
    
    def export_results(self):
        """导出结果"""
        if not self.search_results:
            QMessageBox.warning(self, "警告", "没有可导出的搜索结果")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存搜索结果", 
            "search_results.txt",
            "文本文件 (*.txt);;CSV文件 (*.csv);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("搜索结果报告\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i, result in enumerate(self.search_results, 1):
                        f.write(f"{i}. {result['filename']}\n")
                        f.write(f"   类别: {result['class']}\n")
                        f.write(f"   置信度: {result['confidence']:.2f}\n")
                        f.write(f"   对象数: {result['bbox_count']}\n\n")
                
                QMessageBox.information(self, "成功", f"结果已保存到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
    
    def reset_ui_state(self):
        """重置界面状态"""
        self.search_btn.setEnabled(bool(self.input_path))
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)