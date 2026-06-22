"""
Light-green dataset analysis panel.
"""

from pathlib import Path

from PyQt5.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SimpleAnalysisPanel(QWidget):
    """Dataset analysis page with lightweight local scanning."""

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dataset_path = None
        self.metric_labels = {}
        self._build_ui()

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(6, 6, 6, 6)
        root_layout.setSpacing(22)

        intro = QLabel("快速扫描数据集目录，查看图像、标注和完整度概览，适合正式处理前先做健康检查。")
        intro.setObjectName("analysisIntro")
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        path_group = QGroupBox("数据源")
        path_layout = QVBoxLayout(path_group)
        path_layout.setContentsMargins(20, 24, 20, 20)
        path_layout.setSpacing(14)

        self.path_label = QLabel("未选择分析目录")
        self.path_label.setWordWrap(True)
        select_button = QPushButton("选择分析目录")
        select_button.setMinimumHeight(42)
        select_button.clicked.connect(self.select_dataset)

        path_row = QHBoxLayout()
        path_row.setSpacing(16)
        path_row.addWidget(self.path_label, 1)
        path_row.addWidget(select_button)
        path_layout.addLayout(path_row)
        root_layout.addWidget(path_group)

        metrics_group = QGroupBox("核心指标")
        metrics_layout = QGridLayout(metrics_group)
        metrics_layout.setContentsMargins(20, 24, 20, 20)
        metrics_layout.setHorizontalSpacing(18)
        metrics_layout.setVerticalSpacing(18)

        metric_specs = [
            ("图像文件", "images"),
            ("标注文件", "labels"),
            ("目录层级", "folders"),
            ("完整配对", "paired"),
        ]
        for index, (title, key) in enumerate(metric_specs):
            card, value_label = self._create_metric_card(title)
            self.metric_labels[key] = value_label
            metrics_layout.addWidget(card, index // 2, index % 2)

        root_layout.addWidget(metrics_group)

        action_group = QGroupBox("分析动作")
        action_layout = QHBoxLayout(action_group)
        action_layout.setContentsMargins(20, 22, 20, 20)
        action_layout.setSpacing(12)

        scan_button = QPushButton("扫描概览")
        scan_button.setProperty("buttonType", "success")
        scan_button.setMinimumHeight(46)
        scan_button.clicked.connect(self.refresh_stats)

        quality_button = QPushButton("质量提醒")
        quality_button.setProperty("buttonType", "warning")
        quality_button.setMinimumHeight(46)
        quality_button.clicked.connect(self.show_quality_tips)

        summary_button = QPushButton("生成摘要")
        summary_button.setMinimumHeight(46)
        summary_button.clicked.connect(self.generate_summary)

        action_layout.addWidget(scan_button)
        action_layout.addWidget(quality_button)
        action_layout.addWidget(summary_button)
        action_layout.addStretch()
        root_layout.addWidget(action_group)

        self.status_label = QLabel("等待目录扫描。")
        self.status_label.setObjectName("analysisBanner")
        self.status_label.setWordWrap(True)
        root_layout.addWidget(self.status_label)

        report_group = QGroupBox("分析记录")
        report_layout = QVBoxLayout(report_group)
        report_layout.setContentsMargins(20, 24, 20, 20)
        report_layout.setSpacing(12)

        self.report_view = QPlainTextEdit()
        self.report_view.setReadOnly(True)
        self.report_view.setMinimumHeight(210)
        report_layout.addWidget(self.report_view)
        root_layout.addWidget(report_group)
        root_layout.addStretch()

    def _create_metric_card(self, title: str):
        card = QFrame()
        card.setObjectName("summaryCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("metricTitle")
        value_label = QLabel("0")
        value_label.setObjectName("metricValue")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return card, value_label

    def select_dataset(self):
        path = QFileDialog.getExistingDirectory(self, "选择分析目录")
        if not path:
            return
        self.dataset_path = Path(path)
        self.path_label.setText(str(self.dataset_path))
        self.refresh_stats()

    def refresh_stats(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "提示", "请先选择分析目录。")
            return

        stats = self._scan_dataset(self.dataset_path)
        self.metric_labels["images"].setText(str(stats["images"]))
        self.metric_labels["labels"].setText(str(stats["labels"]))
        self.metric_labels["folders"].setText(str(stats["folders"]))
        self.metric_labels["paired"].setText(f"{stats['paired_images']} / {stats['images']}")

        self.status_label.setText(
            f"扫描完成，共发现 {stats['images']} 张图像、{stats['labels']} 个标注文件，"
            f"其中 {stats['paired_images']} 张图像存在同名标注。"
        )
        self.report_view.setPlainText(self._format_stats_report(stats))

    def show_quality_tips(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "提示", "请先选择分析目录。")
            return

        stats = self._scan_dataset(self.dataset_path)
        tips = []
        if stats["images"] == 0:
            tips.append("当前目录没有识别到图像文件。")
        if stats["labels"] == 0:
            tips.append("当前目录没有识别到标注文件。")
        if stats["orphan_images"] > 0:
            tips.append(f"有 {stats['orphan_images']} 张图像缺少同名标注。")
        if stats["orphan_labels"] > 0:
            tips.append(f"有 {stats['orphan_labels']} 个标注文件找不到对应图像。")
        if not tips:
            tips.append("未发现明显的配对问题，可以继续进入下一步处理。")

        self.report_view.appendPlainText("\n质量提醒")
        for item in tips:
            self.report_view.appendPlainText(f"- {item}")
        self.status_label.setText("质量提醒已更新到分析记录。")

    def generate_summary(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "提示", "请先选择分析目录。")
            return

        stats = self._scan_dataset(self.dataset_path)
        summary = [
            "数据集摘要",
            f"目录: {self.dataset_path}",
            f"图像文件: {stats['images']}",
            f"标注文件: {stats['labels']}",
            f"目录层级: {stats['folders']}",
            f"完整配对图像: {stats['paired_images']}",
        ]
        self.report_view.setPlainText("\n".join(summary))
        self.status_label.setText("摘要已生成，可直接作为后续处理前的概览。")

    def _scan_dataset(self, root: Path):
        image_files = [item for item in root.rglob("*") if item.is_file() and item.suffix.lower() in self.IMAGE_EXTENSIONS]
        label_files = [
            item
            for item in root.rglob("*")
            if item.is_file() and item.suffix.lower() in {".txt", ".json", ".xml"}
        ]

        image_stems = {item.stem for item in image_files}
        label_stems = {item.stem for item in label_files}
        paired_images = len(image_stems & label_stems)

        return {
            "images": len(image_files),
            "labels": len(label_files),
            "folders": sum(1 for item in root.rglob("*") if item.is_dir()),
            "paired_images": paired_images,
            "orphan_images": len(image_stems - label_stems),
            "orphan_labels": len(label_stems - image_stems),
        }

    def _format_stats_report(self, stats):
        lines = [
            "数据集扫描结果",
            f"目录: {self.dataset_path}",
            f"图像文件: {stats['images']}",
            f"标注文件: {stats['labels']}",
            f"目录层级: {stats['folders']}",
            f"完整配对图像: {stats['paired_images']}",
            f"缺少标注的图像: {stats['orphan_images']}",
            f"缺少图像的标注: {stats['orphan_labels']}",
        ]
        return "\n".join(lines)

    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#analysisIntro {
                color: #6d8198;
                font-size: 13px;
                line-height: 1.6;
                padding: 0 4px 2px 4px;
            }

            QLabel#analysisBanner {
                background-color: #edf5ff;
                border: 1px solid #c8dcf8;
                border-radius: 14px;
                padding: 12px 16px;
                color: #20456d;
            }

            QFrame#summaryCard {
                background-color: #f7fbff;
                border: 1px solid #dbe7f6;
                border-radius: 18px;
            }

            QLabel#metricTitle {
                color: #6d8198;
                font-size: 12px;
            }

            QLabel#metricValue {
                color: #20456d;
                font-size: 28px;
                font-weight: bold;
            }

            QGroupBox {
                margin-top: 16px;
                padding-top: 18px;
            }

            QPlainTextEdit {
                border: 1px solid #dbe7f6;
                border-radius: 14px;
                background-color: #fbfdff;
            }
            """
        )
