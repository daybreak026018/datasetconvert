"""
Blue-white dataset analysis panel.
"""

import json
from datetime import datetime
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

        export_button = QPushButton("导出报告")
        export_button.setMinimumHeight(46)
        export_button.clicked.connect(self.export_report)

        action_layout.addWidget(scan_button)
        action_layout.addWidget(quality_button)
        action_layout.addWidget(summary_button)
        action_layout.addWidget(export_button)
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
        if stats["empty_labels"] > 0:
            tips.append(f"有 {stats['empty_labels']} 个空标注文件，请确认是否为负样本。")
        if stats["duplicate_stems"] > 0:
            tips.append(f"发现 {stats['duplicate_stems']} 组同名文件，请确认多级目录下是否存在重复样本。")
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
            f"空标注文件: {stats['empty_labels']}",
            f"重复文件名: {stats['duplicate_stems']}",
        ]
        self.report_view.setPlainText("\n".join(summary))
        self.status_label.setText("摘要已生成，可直接作为后续处理前的概览。")

    def export_report(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "提示", "请先选择分析目录。")
            return

        stats = self._scan_dataset(self.dataset_path)
        default_name = f"dataset_health_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "导出数据体检报告",
            str(self.dataset_path / default_name),
            "JSON Files (*.json);;Text Files (*.txt)",
        )
        if not file_path:
            return

        target = Path(file_path)
        try:
            if target.suffix.lower() == ".txt":
                target.write_text(self._format_stats_report(stats), encoding="utf-8")
            else:
                payload = {
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "dataset_path": str(self.dataset_path),
                    "stats": stats,
                    "tips": self._build_quality_tips(stats),
                }
                target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as exc:
            QMessageBox.critical(self, "错误", f"报告导出失败：{exc}")
            return

        self.status_label.setText(f"体检报告已导出：{target}")
        self.report_view.setPlainText(self._format_stats_report(stats))
        QMessageBox.information(self, "完成", "体检报告已导出。")

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
        duplicate_stems = self._count_duplicate_stems(image_files) + self._count_duplicate_stems(label_files)

        return {
            "images": len(image_files),
            "labels": len(label_files),
            "folders": sum(1 for item in root.rglob("*") if item.is_dir()),
            "paired_images": paired_images,
            "orphan_images": len(image_stems - label_stems),
            "orphan_labels": len(label_stems - image_stems),
            "empty_labels": sum(1 for item in label_files if item.stat().st_size == 0),
            "duplicate_stems": duplicate_stems,
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
            f"空标注文件: {stats['empty_labels']}",
            f"重复文件名: {stats['duplicate_stems']}",
        ]
        tips = self._build_quality_tips(stats)
        if tips:
            lines.append("")
            lines.append("处理建议")
            lines.extend(f"- {item}" for item in tips)
        return "\n".join(lines)

    def _build_quality_tips(self, stats):
        tips = []
        if stats["images"] == 0:
            tips.append("当前目录没有识别到图像文件。")
        if stats["labels"] == 0:
            tips.append("当前目录没有识别到标注文件。")
        if stats["orphan_images"] > 0:
            tips.append(f"有 {stats['orphan_images']} 张图像缺少同名标注。")
        if stats["orphan_labels"] > 0:
            tips.append(f"有 {stats['orphan_labels']} 个标注文件找不到对应图像。")
        if stats["empty_labels"] > 0:
            tips.append(f"有 {stats['empty_labels']} 个空标注文件，请确认是否为负样本。")
        if stats["duplicate_stems"] > 0:
            tips.append(f"发现 {stats['duplicate_stems']} 组同名文件，请确认是否会覆盖或混淆。")
        if not tips:
            tips.append("未发现明显配对问题，可以继续进行格式转换或划分。")
        return tips

    def _count_duplicate_stems(self, files):
        seen = set()
        duplicates = set()
        for item in files:
            if item.stem in seen:
                duplicates.add(item.stem)
            seen.add(item.stem)
        return len(duplicates)

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
