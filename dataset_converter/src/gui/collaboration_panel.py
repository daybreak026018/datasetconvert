# Collaboration Panel - Dataset Splitting
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, 
    QFileDialog, QSpinBox, QComboBox, QTextEdit, QFormLayout,
    QGroupBox, QTableWidget, QTableWidgetItem, QProgressBar,
    QMessageBox, QTabWidget
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, Qt
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
        
        # 定时刷新
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_current_view)
        self.refresh_timer.start(30000)
    
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
    
    def refresh_current_view(self):
        pass