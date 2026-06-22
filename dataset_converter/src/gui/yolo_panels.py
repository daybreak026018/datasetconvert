"""
Compact blue-white YOLO Studio panels.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from PyQt5.QtCore import QUrl

from ..core.yolo_services import (
    EnvironmentChecker,
    RunsManager,
    YOLOCommandBuilder,
    YOLODatasetInspector,
    YOLOPredictConfig,
    YOLOTrainConfig,
)


def _button(text: str, handler=None, button_type: str = "", height: int = 36) -> QPushButton:
    btn = QPushButton(text)
    btn.setMinimumHeight(height)
    if button_type:
        btn.setProperty("buttonType", button_type)
    if handler:
        btn.clicked.connect(handler)
    return btn


def _path_row(label_text: str, line_edit: QLineEdit, button: QPushButton) -> QHBoxLayout:
    row = QHBoxLayout()
    row.setSpacing(8)
    label = QLabel(label_text)
    label.setMinimumWidth(82)
    row.addWidget(label)
    row.addWidget(line_edit, 1)
    row.addWidget(button)
    return row


class YOLOBasePanel(QWidget):
    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#banner {
                background-color: #edf5ff;
                border: 1px solid #c8dcf8;
                border-radius: 10px;
                padding: 9px 12px;
                color: #20456d;
            }

            QFrame#metricCard {
                background-color: #f7fbff;
                border: 1px solid #dbe7f6;
                border-radius: 10px;
            }

            QLabel#metricTitle {
                color: #6d8198;
                font-size: 11px;
                background-color: transparent;
            }

            QLabel#metricValue {
                color: #20456d;
                font-size: 20px;
                font-weight: bold;
                background-color: transparent;
            }

            QGroupBox {
                margin-top: 14px;
                padding-top: 12px;
            }

            QTabWidget::pane {
                border: 1px solid #dbe7f6;
                border-radius: 8px;
                background-color: #ffffff;
                top: -1px;
            }

            QTabBar::tab {
                background-color: #f6faff;
                border: 1px solid #dbe7f6;
                border-bottom: none;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: #5f7895;
                padding: 7px 12px;
                margin-right: 3px;
            }

            QTabBar::tab:selected {
                background-color: #ffffff;
                color: #20456d;
                font-weight: bold;
                border-top: 2px solid #2f7fe8;
            }

            QLineEdit, QPlainTextEdit, QListWidget {
                border: 1px solid #dbe7f6;
                border-radius: 8px;
                background-color: #fbfdff;
                padding: 6px 8px;
            }
            """
        )

    def _metric_card(self, title: str, value: str = "0"):
        card = QFrame()
        card.setObjectName("metricCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        title_label = QLabel(title)
        title_label.setObjectName("metricTitle")
        value_label = QLabel(value)
        value_label.setObjectName("metricValue")
        value_label.setWordWrap(True)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return card, value_label

    def _open_path(self, path_text: str):
        if not path_text:
            return
        path = Path(path_text)
        if path.exists():
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))


class YOLOHomePanel(YOLOBasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.metrics = {}
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(12)

        banner = QLabel("YOLO Studio：数据准备、环境检测、训练、检测和结果管理集中到一条工作流。")
        banner.setObjectName("banner")
        banner.setWordWrap(True)
        root.addWidget(banner)

        metrics = QGridLayout()
        metrics.setHorizontalSpacing(10)
        metrics.setVerticalSpacing(10)
        for index, key in enumerate(["环境状态", "最近训练", "最近检测", "可用权重"]):
            card, label = self._metric_card(key, "-")
            self.metrics[key] = label
            metrics.addWidget(card, index // 2, index % 2)
        root.addLayout(metrics)

        action_group = QGroupBox("快捷入口")
        actions = QHBoxLayout(action_group)
        actions.setContentsMargins(12, 16, 12, 12)
        actions.setSpacing(8)
        actions.addWidget(_button("刷新概览", self.refresh, "success"))
        actions.addWidget(_button("打开 runs", lambda: self._open_path(str(Path.cwd() / "runs"))))
        actions.addStretch()
        root.addWidget(action_group)

        self.summary = QPlainTextEdit()
        self.summary.setReadOnly(True)
        self.summary.setMinimumHeight(160)
        root.addWidget(self.summary)
        root.addStretch()

    def refresh(self):
        report = EnvironmentChecker.check()
        runs = RunsManager(Path.cwd() / "runs").list_runs()
        train_runs = [item for item in runs if item["type"] == "训练"]
        predict_runs = [item for item in runs if item["type"] == "检测"]
        weights = [item for item in runs if item.get("best") or item.get("last")]
        self.metrics["环境状态"].setText(report.status)
        self.metrics["最近训练"].setText(train_runs[0]["modified"] if train_runs else "暂无")
        self.metrics["最近检测"].setText(predict_runs[0]["modified"] if predict_runs else "暂无")
        self.metrics["可用权重"].setText(str(len(weights)))
        self.summary.setPlainText(
            "\n".join(
                [
                    f"Python: {report.python_version}",
                    f"PyTorch: {report.torch_version}",
                    f"CUDA: {report.cuda_version}",
                    f"GPU: {report.gpu_name}",
                    f"Ultralytics: {report.ultralytics_version}",
                    f"建议: {'可以开始训练' if report.ultralytics_installed else '请先到环境检测页安装依赖'}",
                ]
            )
        )


class YOLODataPanel(YOLOBasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.inspector = YOLODatasetInspector()
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(10)

        banner = QLabel("准备 YOLO 数据集：检测/分割使用 images 与 labels，分类使用 train/val/test/类别名目录。")
        banner.setObjectName("banner")
        banner.setWordWrap(True)
        root.addWidget(banner)

        self.tabs = QTabWidget()
        self.tabs.setObjectName("dataPrepTabs")
        root.addWidget(self.tabs, 1)

        self.tabs.addTab(self._build_yolo_check_tab(), "YOLO体检")
        self.tabs.addTab(self._wrap_legacy_panel("converter"), "格式转换")
        self.tabs.addTab(self._wrap_legacy_panel("split"), "数据划分")
        self.tabs.addTab(self._wrap_legacy_panel("analysis"), "分析报告")
        self.tabs.addTab(self._wrap_legacy_panel("visual"), "可视化预览")

    def _build_yolo_check_tab(self):
        tab = QWidget()
        root = QVBoxLayout(tab)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(10)

        group = QGroupBox("数据集")
        layout = QVBoxLayout(group)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(8)
        self.dataset_edit = QLineEdit()
        self.dataset_edit.setReadOnly(True)
        layout.addLayout(_path_row("数据目录", self.dataset_edit, _button("选择", self.choose_dataset)))
        task_row = QHBoxLayout()
        task_row.addWidget(QLabel("任务类型"))
        self.task_combo = QComboBox()
        self.task_combo.addItems(["detect", "segment", "classify"])
        task_row.addWidget(self.task_combo, 1)
        layout.addLayout(task_row)
        root.addWidget(group)

        actions = QHBoxLayout()
        actions.addWidget(_button("扫描数据集", self.scan_dataset, "success"))
        actions.addWidget(_button("生成/修复 data.yaml", self.generate_yaml))
        actions.addWidget(_button("打开目录", lambda: self._open_path(self.dataset_edit.text())))
        actions.addStretch()
        root.addLayout(actions)

        self.report = QPlainTextEdit()
        self.report.setReadOnly(True)
        self.report.setMinimumHeight(240)
        root.addWidget(self.report)
        root.addStretch()
        return tab

    def _wrap_legacy_panel(self, panel_name: str):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if panel_name == "converter":
            from .converter_panel import ConverterPanel

            panel = ConverterPanel(self)
        elif panel_name == "split":
            from .simple_splitting_panel import SimpleSplittingPanel

            panel = SimpleSplittingPanel(self)
        elif panel_name == "analysis":
            from .simple_analysis_panel import SimpleAnalysisPanel

            panel = SimpleAnalysisPanel(self)
        else:
            from .simple_visualization_panel import SimpleVisualizationPanel

            panel = SimpleVisualizationPanel(self)

        if hasattr(panel, "apply_theme"):
            panel.apply_theme()
        layout.addWidget(panel)
        return tab

    def choose_dataset(self):
        path = QFileDialog.getExistingDirectory(self, "选择 YOLO 数据集目录", str(Path.cwd()))
        if path:
            self.dataset_edit.setText(path)

    def scan_dataset(self):
        if not self.dataset_edit.text():
            QMessageBox.warning(self, "提示", "请先选择数据集目录。")
            return
        profile = self.inspector.inspect(Path(self.dataset_edit.text()), self.task_combo.currentText())
        self.report.setPlainText(self._format_profile(profile))

    def generate_yaml(self):
        if not self.dataset_edit.text():
            QMessageBox.warning(self, "提示", "请先选择数据集目录。")
            return
        if self.task_combo.currentText() == "classify":
            QMessageBox.information(self, "提示", "分类任务通常直接选择数据集根目录，不需要 data.yaml。")
            return
        path = self.inspector.generate_data_yaml(Path(self.dataset_edit.text()), self.task_combo.currentText())
        self.report.appendPlainText(f"\ndata.yaml 已生成：{path}")

    def _format_profile(self, profile):
        lines = [
            "YOLO 数据集体检",
            f"任务类型: {profile.task}",
            f"目录: {profile.dataset_path}",
            f"data.yaml: {profile.data_yaml or '缺失'}",
            f"类别数: {len(profile.classes) or profile.classification_classes}",
            f"类别: {', '.join(profile.classes[:20]) if profile.classes else '未读取到'}",
            f"train 图像: {profile.train_images}",
            f"val 图像: {profile.val_images}",
            f"test 图像: {profile.test_images}",
            f"标注文件: {profile.label_files}",
            f"空标注: {profile.empty_labels}",
            f"图像缺标注: {profile.orphan_images}",
            f"标注缺图像: {profile.orphan_labels}",
            f"异常标注行: {profile.invalid_yolo_rows}",
        ]
        if profile.warnings:
            lines.append("")
            lines.append("提醒")
            lines.extend(f"- {item}" for item in profile.warnings)
        return "\n".join(lines)


class YOLOEnvironmentPanel(YOLOBasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(12)
        banner = QLabel("环境检测只读执行，不自动安装或修改系统环境。")
        banner.setObjectName("banner")
        banner.setWordWrap(True)
        root.addWidget(banner)
        root.addWidget(_button("重新检测", self.refresh, "success"))
        self.report = QPlainTextEdit()
        self.report.setReadOnly(True)
        self.report.setMinimumHeight(300)
        root.addWidget(self.report)

    def refresh(self):
        report = EnvironmentChecker.check()
        self.report.setPlainText(
            "\n".join(
                [
                    f"状态: {report.status}",
                    f"系统: {report.platform}",
                    f"Python: {report.python_version}",
                    f"PyTorch: {report.torch_version}",
                    f"CUDA 可用: {'是' if report.cuda_available else '否'}",
                    f"CUDA 版本: {report.cuda_version}",
                    f"GPU: {report.gpu_name}",
                    f"Ultralytics: {report.ultralytics_version}",
                    f"OpenCV: {report.opencv_version}",
                    "",
                    "CPU 安装命令:",
                    report.cpu_install_command,
                    "",
                    "GPU 安装建议:",
                    report.gpu_install_command,
                ]
            )
        )


class YOLOProcessPanel(YOLOBasePanel):
    process_kind = "process"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.process = None

    def _start_process(self, command: list[str], cwd: Path):
        if self.process and self.process.state() != QProcess.NotRunning:
            QMessageBox.warning(self, "提示", "已有任务正在运行。")
            return
        self.log.clear()
        self.log.appendPlainText("执行命令:\n" + subprocess.list2cmdline(command) + "\n")
        self.process = QProcess(self)
        self.process.setProgram(command[0])
        self.process.setArguments(command[1:])
        self.process.setWorkingDirectory(str(cwd))
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self._read_output)
        self.process.finished.connect(self._finished)
        self.process.start()

    def _read_output(self):
        data = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="ignore")
        if data:
            self.log.appendPlainText(data.rstrip())

    def _finished(self, exit_code, exit_status):
        status = "完成" if exit_code == 0 else f"失败({exit_code})"
        self.log.appendPlainText(f"\n任务{status}。")

    def stop_process(self):
        if self.process and self.process.state() != QProcess.NotRunning:
            self.process.terminate()
            self.log.appendPlainText("\n已请求停止任务。")


class YOLOTrainingPanel(YOLOProcessPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(12)
        banner = QLabel("本机一键训练：选择任务、模型和数据后启动，日志会实时输出。")
        banner.setObjectName("banner")
        banner.setWordWrap(True)
        root.addWidget(banner)

        group = QGroupBox("训练配置")
        grid = QGridLayout(group)
        grid.setContentsMargins(12, 16, 12, 12)
        grid.setHorizontalSpacing(8)
        grid.setVerticalSpacing(8)

        self.task_combo = QComboBox()
        self.task_combo.addItems(["detect", "segment", "classify"])
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.addItems(["yolo26n.pt", "yolo26s.pt", "yolo26m.pt", "yolo11n.pt", "yolov8n.pt"])
        self.data_edit = QLineEdit()
        self.project_edit = QLineEdit(str(Path.cwd() / "runs" / "train"))
        self.name_edit = QLineEdit("exp")
        self.epochs_spin = self._spin(1, 1000, 100)
        self.imgsz_spin = self._spin(64, 2048, 640)
        self.batch_spin = self._spin(1, 512, 16)
        self.workers_spin = self._spin(0, 32, 4)
        self.patience_spin = self._spin(0, 300, 50)
        self.device_combo = QComboBox()
        self.device_combo.setEditable(True)
        self.device_combo.addItems(["auto", "cpu", "0"])
        self.resume_check = QCheckBox("恢复训练 resume=True")

        rows = [
            ("任务", self.task_combo),
            ("模型", self.model_combo),
            ("数据", self.data_edit),
            ("输出", self.project_edit),
            ("名称", self.name_edit),
            ("epochs", self.epochs_spin),
            ("imgsz", self.imgsz_spin),
            ("batch", self.batch_spin),
            ("device", self.device_combo),
            ("workers", self.workers_spin),
            ("patience", self.patience_spin),
        ]
        for index, (label, widget) in enumerate(rows):
            grid.addWidget(QLabel(label), index // 2, (index % 2) * 2)
            grid.addWidget(widget, index // 2, (index % 2) * 2 + 1)
        grid.addWidget(self.resume_check, 6, 0, 1, 2)
        grid.addWidget(_button("选择 data.yaml/分类目录", self.choose_data), 6, 2, 1, 2)
        root.addWidget(group)

        actions = QHBoxLayout()
        actions.addWidget(_button("开始训练", self.start_training, "success"))
        actions.addWidget(_button("停止", self.stop_process))
        actions.addWidget(_button("打开输出目录", lambda: self._open_path(self.project_edit.text())))
        actions.addStretch()
        root.addLayout(actions)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(220)
        root.addWidget(self.log)

    def _spin(self, min_value, max_value, value):
        spin = QSpinBox()
        spin.setRange(min_value, max_value)
        spin.setValue(value)
        return spin

    def choose_data(self):
        if self.task_combo.currentText() == "classify":
            path = QFileDialog.getExistingDirectory(self, "选择分类数据集根目录", str(Path.cwd()))
        else:
            path, _ = QFileDialog.getOpenFileName(self, "选择 data.yaml", str(Path.cwd()), "YAML Files (*.yaml *.yml)")
        if path:
            self.data_edit.setText(path)

    def start_training(self):
        if not self.data_edit.text():
            QMessageBox.warning(self, "提示", "请先选择训练数据。")
            return
        cfg = YOLOTrainConfig(
            task=self.task_combo.currentText(),
            model=self.model_combo.currentText(),
            data_yaml=self.data_edit.text(),
            epochs=self.epochs_spin.value(),
            imgsz=self.imgsz_spin.value(),
            batch=self.batch_spin.value(),
            device=self.device_combo.currentText(),
            project=self.project_edit.text(),
            name=self.name_edit.text() or "exp",
            workers=self.workers_spin.value(),
            patience=self.patience_spin.value(),
            resume=self.resume_check.isChecked(),
        )
        self._start_process(YOLOCommandBuilder.build_train(cfg), Path.cwd())


class YOLOPredictPanel(YOLOProcessPanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(12)
        banner = QLabel("模型检测：支持图片、文件夹、视频和摄像头编号，结果保存到指定目录。")
        banner.setObjectName("banner")
        banner.setWordWrap(True)
        root.addWidget(banner)

        group = QGroupBox("检测配置")
        grid = QGridLayout(group)
        grid.setContentsMargins(12, 16, 12, 12)
        self.task_combo = QComboBox()
        self.task_combo.addItems(["detect", "segment", "classify"])
        self.model_edit = QLineEdit()
        self.source_edit = QLineEdit()
        self.output_edit = QLineEdit(str(Path.cwd() / "runs" / "predict"))
        self.device_combo = QComboBox()
        self.device_combo.setEditable(True)
        self.device_combo.addItems(["auto", "cpu", "0"])
        self.conf_spin = self._double_spin(0.01, 1.0, 0.25)
        self.iou_spin = self._double_spin(0.01, 1.0, 0.7)
        self.imgsz_spin = QSpinBox()
        self.imgsz_spin.setRange(64, 2048)
        self.imgsz_spin.setValue(640)
        self.save_txt_check = QCheckBox("保存 txt")
        self.save_conf_check = QCheckBox("保存置信度")

        rows = [
            ("任务", self.task_combo),
            ("权重", self.model_edit),
            ("输入源", self.source_edit),
            ("输出", self.output_edit),
            ("conf", self.conf_spin),
            ("iou", self.iou_spin),
            ("imgsz", self.imgsz_spin),
            ("device", self.device_combo),
        ]
        for index, (label, widget) in enumerate(rows):
            grid.addWidget(QLabel(label), index // 2, (index % 2) * 2)
            grid.addWidget(widget, index // 2, (index % 2) * 2 + 1)
        grid.addWidget(self.save_txt_check, 4, 0)
        grid.addWidget(self.save_conf_check, 4, 1)
        grid.addWidget(_button("选择权重", self.choose_model), 4, 2)
        grid.addWidget(_button("选择输入", self.choose_source), 4, 3)
        root.addWidget(group)

        actions = QHBoxLayout()
        actions.addWidget(_button("开始检测", self.start_predict, "success"))
        actions.addWidget(_button("停止", self.stop_process))
        actions.addWidget(_button("打开输出目录", lambda: self._open_path(self.output_edit.text())))
        actions.addStretch()
        root.addLayout(actions)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMinimumHeight(220)
        root.addWidget(self.log)

    def _double_spin(self, min_value, max_value, value):
        spin = QDoubleSpinBox()
        spin.setRange(min_value, max_value)
        spin.setSingleStep(0.05)
        spin.setDecimals(2)
        spin.setValue(value)
        return spin

    def choose_model(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择 YOLO 权重", str(Path.cwd()), "Model Files (*.pt *.onnx *.engine);;All Files (*)")
        if path:
            self.model_edit.setText(path)

    def choose_source(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "选择图片或视频",
            str(Path.cwd()),
            "Media Files (*.jpg *.jpeg *.png *.bmp *.webp *.mp4 *.avi *.mov *.mkv);;All Files (*)",
        )
        if not path:
            path = QFileDialog.getExistingDirectory(self, "选择图片/视频目录", str(Path.cwd()))
        if path:
            self.source_edit.setText(path)

    def start_predict(self):
        if not self.model_edit.text() or not self.source_edit.text():
            QMessageBox.warning(self, "提示", "请先选择权重和输入源。")
            return
        cfg = YOLOPredictConfig(
            task=self.task_combo.currentText(),
            model_path=self.model_edit.text(),
            source=self.source_edit.text(),
            conf=self.conf_spin.value(),
            iou=self.iou_spin.value(),
            imgsz=self.imgsz_spin.value(),
            device=self.device_combo.currentText(),
            save_txt=self.save_txt_check.isChecked(),
            save_conf=self.save_conf_check.isChecked(),
            output_dir=self.output_edit.text(),
        )
        self._start_process(YOLOCommandBuilder.build_predict(cfg), Path.cwd())


class YOLORunsPanel(YOLOBasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.runs_root = Path.cwd() / "runs"
        self.runs = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(12)
        banner = QLabel("结果管理：扫描 runs 目录，快速找到训练权重和预测输出。")
        banner.setObjectName("banner")
        banner.setWordWrap(True)
        root.addWidget(banner)
        actions = QHBoxLayout()
        actions.addWidget(_button("刷新", self.refresh, "success"))
        actions.addWidget(_button("打开选中目录", self.open_selected))
        actions.addWidget(_button("复制 best.pt 路径", self.copy_best))
        actions.addStretch()
        root.addLayout(actions)
        self.list_widget = QListWidget()
        self.list_widget.currentRowChanged.connect(self.show_detail)
        root.addWidget(self.list_widget, 1)
        self.detail = QPlainTextEdit()
        self.detail.setReadOnly(True)
        self.detail.setMinimumHeight(120)
        root.addWidget(self.detail)

    def refresh(self):
        self.runs = RunsManager(self.runs_root).list_runs()
        self.list_widget.clear()
        for item in self.runs:
            self.list_widget.addItem(f"[{item['type']}] {item['modified']}  {item['path']}")
        self.detail.setPlainText(f"共发现 {len(self.runs)} 个结果。")

    def show_detail(self, index):
        if index < 0 or index >= len(self.runs):
            return
        item = self.runs[index]
        self.detail.setPlainText(
            "\n".join(
                [
                    f"类型: {item['type']}",
                    f"目录: {item['path']}",
                    f"best.pt: {item['best'] or '无'}",
                    f"last.pt: {item['last'] or '无'}",
                    f"更新时间: {item['modified']}",
                ]
            )
        )

    def open_selected(self):
        index = self.list_widget.currentRow()
        if 0 <= index < len(self.runs):
            self._open_path(self.runs[index]["path"])

    def copy_best(self):
        index = self.list_widget.currentRow()
        if 0 <= index < len(self.runs) and self.runs[index]["best"]:
            from PyQt5.QtWidgets import QApplication

            QApplication.clipboard().setText(self.runs[index]["best"])
            QMessageBox.information(self, "完成", "best.pt 路径已复制。")


class YOLOSettingsPanel(YOLOBasePanel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(12)
        banner = QLabel("YOLO Studio 设置：第一版保留蓝白固定主题，环境安装由用户按检测页命令执行。")
        banner.setObjectName("banner")
        banner.setWordWrap(True)
        root.addWidget(banner)
        info = QPlainTextEdit()
        info.setReadOnly(True)
        info.setPlainText(
            "默认输出目录:\n"
            f"{Path.cwd() / 'runs'}\n\n"
            "推荐流程:\n"
            "1. 环境检测确认 ultralytics 与 torch 可用\n"
            "2. 数据准备扫描并生成 data.yaml\n"
            "3. 模型训练启动本机训练\n"
            "4. 模型检测选择 best.pt 运行推理\n"
            "5. 结果管理查看输出"
        )
        root.addWidget(info)
        root.addStretch()
