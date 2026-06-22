"""
Light-green dataset splitting panel.
"""

from pathlib import Path

from PyQt5.QtCore import QThread, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class SplitWorker(QThread):
    """Worker thread for dataset splitting."""

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

            from ..core.dataset_splitter import DatasetSplitter

            splitter = DatasetSplitter()

            self.progress_updated.emit(30, "正在执行划分...")

            result = splitter.split_dataset(
                self.input_path,
                self.output_path,
                train_ratio=self.train_ratio,
                val_ratio=self.val_ratio,
                test_ratio=self.test_ratio,
            )

            self.progress_updated.emit(100, "数据划分完成")
            self.finished.emit(True, "数据集划分成功完成。", result)
        except Exception as exc:
            self.finished.emit(False, f"划分失败: {exc}", {})


class SimpleSplittingPanel(QWidget):
    """Spacious dataset splitting page."""

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self._input_path = None
        self._output_path = None
        self._build_ui()
        self.update_ratios()

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(6, 6, 6, 6)
        root_layout.setSpacing(22)

        intro = QLabel("为数据集设置训练、验证和测试比例，并在执行前先查看样本预估数量。")
        intro.setObjectName("splitIntro")
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        dataset_group = QGroupBox("路径设置")
        dataset_layout = QVBoxLayout(dataset_group)
        dataset_layout.setContentsMargins(20, 24, 20, 20)
        dataset_layout.setSpacing(16)

        self.input_path_label = QLabel("未选择输入目录")
        self.input_path_label.setWordWrap(True)
        input_button = QPushButton("选择输入目录")
        input_button.setMinimumHeight(42)
        input_button.clicked.connect(self.select_input_path)
        dataset_layout.addLayout(self._build_path_row(self.input_path_label, input_button))

        self.output_path_label = QLabel("未选择输出目录")
        self.output_path_label.setWordWrap(True)
        output_button = QPushButton("选择输出目录")
        output_button.setMinimumHeight(42)
        output_button.clicked.connect(self.select_output_path)
        dataset_layout.addLayout(self._build_path_row(self.output_path_label, output_button))

        root_layout.addWidget(dataset_group)

        ratio_group = QGroupBox("划分比例")
        ratio_layout = QGridLayout(ratio_group)
        ratio_layout.setContentsMargins(20, 24, 20, 20)
        ratio_layout.setHorizontalSpacing(18)
        ratio_layout.setVerticalSpacing(16)

        ratio_layout.addWidget(QLabel("训练集"), 0, 0)
        self.train_ratio = self._create_ratio_spin(0.7)
        ratio_layout.addWidget(self.train_ratio, 0, 1)

        ratio_layout.addWidget(QLabel("验证集"), 1, 0)
        self.val_ratio = self._create_ratio_spin(0.2)
        ratio_layout.addWidget(self.val_ratio, 1, 1)

        ratio_layout.addWidget(QLabel("测试集"), 2, 0)
        self.test_ratio = self._create_ratio_spin(0.1)
        ratio_layout.addWidget(self.test_ratio, 2, 1)

        ratio_layout.addWidget(QLabel("比例合计"), 3, 0)
        self.total_label = QLabel("1.0 (100%)")
        self.total_label.setObjectName("splitTotal")
        ratio_layout.addWidget(self.total_label, 3, 1)

        preset_wrap = QHBoxLayout()
        preset_wrap.setSpacing(10)
        preset_wrap.addWidget(QLabel("常用预设"))

        for text, values in (
            ("7:2:1", (0.7, 0.2, 0.1)),
            ("8:1:1", (0.8, 0.1, 0.1)),
            ("6:2:2", (0.6, 0.2, 0.2)),
        ):
            button = QPushButton(text)
            button.setProperty("buttonRole", "chip")
            button.setMinimumHeight(38)
            button.clicked.connect(lambda _, pair=values: self.set_preset(*pair))
            preset_wrap.addWidget(button)

        preset_wrap.addStretch()
        ratio_layout.addLayout(preset_wrap, 4, 0, 1, 2)
        root_layout.addWidget(ratio_group)

        self.summary_banner = QLabel("预览会根据当前目录中的图像数量自动更新。")
        self.summary_banner.setObjectName("splitBanner")
        self.summary_banner.setWordWrap(True)
        root_layout.addWidget(self.summary_banner)

        preview_group = QGroupBox("划分预览")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(20, 24, 20, 20)
        preview_layout.setSpacing(12)

        self.preview_table = QTableWidget(3, 3)
        self.preview_table.setHorizontalHeaderLabels(["子集", "预计文件数", "比例"])
        self.preview_table.verticalHeader().setVisible(False)
        self.preview_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.preview_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.preview_table.setSelectionMode(QTableWidget.NoSelection)
        self.preview_table.setAlternatingRowColors(True)

        for row, name in enumerate(["训练集", "验证集", "测试集"]):
            self.preview_table.setItem(row, 0, QTableWidgetItem(name))
            self.preview_table.setItem(row, 1, QTableWidgetItem("0"))
            self.preview_table.setItem(row, 2, QTableWidgetItem("0%"))

        preview_layout.addWidget(self.preview_table)
        root_layout.addWidget(preview_group)

        action_group = QGroupBox("执行")
        action_layout = QVBoxLayout(action_group)
        action_layout.setContentsMargins(20, 22, 20, 20)
        action_layout.setSpacing(14)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        self.split_btn = QPushButton("开始划分")
        self.split_btn.setProperty("buttonType", "success")
        self.split_btn.setMinimumHeight(46)
        self.split_btn.clicked.connect(self.start_split)

        self.cancel_btn = QPushButton("取消任务")
        self.cancel_btn.setProperty("buttonType", "warning")
        self.cancel_btn.setMinimumHeight(46)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_split)

        button_row.addWidget(self.split_btn)
        button_row.addWidget(self.cancel_btn)
        button_row.addStretch()

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        self.status_label = QLabel("等待开始")
        self.status_label.setObjectName("splitStatus")

        action_layout.addLayout(button_row)
        action_layout.addWidget(self.progress_bar)
        action_layout.addWidget(self.status_label)
        root_layout.addWidget(action_group)
        root_layout.addStretch()

    def _build_path_row(self, label: QLabel, button: QPushButton):
        layout = QHBoxLayout()
        layout.setSpacing(16)
        label.setMinimumHeight(42)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(label, 1)
        layout.addWidget(button)
        return layout

    def _create_ratio_spin(self, value: float):
        spin = QDoubleSpinBox()
        spin.setRange(0.0, 1.0)
        spin.setSingleStep(0.1)
        spin.setDecimals(1)
        spin.setValue(value)
        spin.setMinimumHeight(40)
        spin.valueChanged.connect(self.update_ratios)
        return spin

    def select_input_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择输入目录")
        if not path:
            return
        self._input_path = Path(path)
        self.input_path_label.setText(str(self._input_path))
        self.update_preview()

    def select_output_path(self):
        path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if not path:
            return
        self._output_path = Path(path)
        self.output_path_label.setText(str(self._output_path))

    def update_ratios(self):
        train = self.train_ratio.value()
        val = self.val_ratio.value()
        test = self.test_ratio.value()
        total = train + val + test

        self.total_label.setText(f"{total:.1f} ({total * 100:.0f}%)")
        if abs(total - 1.0) < 0.01:
            self.total_label.setProperty("state", "ok")
            self.summary_banner.setText("比例已平衡，可以直接执行划分。")
        else:
            self.total_label.setProperty("state", "warn")
            self.summary_banner.setText("比例合计需要等于 1.0，当前仅更新为预览状态。")

        self.total_label.style().unpolish(self.total_label)
        self.total_label.style().polish(self.total_label)
        self.update_preview()

    def update_preview(self):
        total_files = self._count_images(self._input_path) if self._input_path else 0
        train_files = int(total_files * self.train_ratio.value())
        val_files = int(total_files * self.val_ratio.value())
        test_files = max(total_files - train_files - val_files, 0)

        preview_data = [
            (train_files, self.train_ratio.value()),
            (val_files, self.val_ratio.value()),
            (test_files, self.test_ratio.value()),
        ]

        for row, (file_count, ratio) in enumerate(preview_data):
            self.preview_table.setItem(row, 1, QTableWidgetItem(str(file_count)))
            self.preview_table.setItem(row, 2, QTableWidgetItem(f"{ratio * 100:.1f}%"))

        if self._input_path:
            self.summary_banner.setText(f"当前目录共识别到 {total_files} 个图像文件，预估结果已同步刷新。")

    def _count_images(self, root: Path):
        if not root or not root.exists():
            return 0
        return sum(1 for item in root.rglob("*") if item.is_file() and item.suffix.lower() in self.IMAGE_EXTENSIONS)

    def set_preset(self, train, val, test):
        self.train_ratio.setValue(train)
        self.val_ratio.setValue(val)
        self.test_ratio.setValue(test)

    def start_split(self):
        if not self._input_path:
            QMessageBox.warning(self, "提示", "请先选择输入目录。")
            return
        if not self._output_path:
            QMessageBox.warning(self, "提示", "请先选择输出目录。")
            return

        total = self.train_ratio.value() + self.val_ratio.value() + self.test_ratio.value()
        if abs(total - 1.0) > 0.01:
            QMessageBox.warning(self, "提示", "训练、验证、测试比例合计必须等于 1.0。")
            return

        self.worker = SplitWorker(
            self._input_path,
            self._output_path,
            self.train_ratio.value(),
            self.val_ratio.value(),
            self.test_ratio.value(),
        )
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.split_finished)

        self.split_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_label.setText("任务已启动，正在准备划分...")
        self.worker.start()

    def cancel_split(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()

        self.reset_ui_state()
        self.status_label.setText("任务已取消。")

    def update_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.status_label.setText(message)

    def split_finished(self, success, message, result):
        self.reset_ui_state()
        if success:
            self.status_label.setText("数据划分完成。")
            if result:
                self.summary_banner.setText(f"任务完成，输出摘要: {result}")
            QMessageBox.information(self, "完成", message)
        else:
            self.status_label.setText("数据划分失败。")
            QMessageBox.critical(self, "错误", message)

    def reset_ui_state(self):
        self.split_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setVisible(False)

    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#splitIntro {
                color: #6d8198;
                font-size: 13px;
                line-height: 1.6;
                padding: 0 4px 2px 4px;
            }

            QLabel#splitBanner,
            QLabel#splitStatus {
                background-color: #edf5ff;
                border: 1px solid #c8dcf8;
                border-radius: 14px;
                padding: 12px 16px;
                color: #20456d;
            }

            QLabel#splitTotal[state="ok"] {
                color: #2f7fe8;
                font-weight: bold;
            }

            QLabel#splitTotal[state="warn"] {
                color: #d97706;
                font-weight: bold;
            }

            QGroupBox {
                margin-top: 16px;
                padding-top: 18px;
            }

            QFrame#summaryCard {
                background-color: #f7fbff;
                border: 1px solid #dbe7f6;
                border-radius: 18px;
            }

            QPushButton[buttonRole="chip"] {
                border-radius: 12px;
                padding: 8px 14px;
            }

            QTableWidget {
                border: 1px solid #dbe7f6;
                border-radius: 14px;
                background-color: #fbfdff;
                gridline-color: #e7eef8;
            }

            QHeaderView::section {
                background-color: #eef5ff;
                color: #20456d;
                border: none;
                padding: 10px;
            }
            """
        )
