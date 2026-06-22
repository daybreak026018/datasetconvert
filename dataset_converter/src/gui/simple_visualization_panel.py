"""
Light-green dataset visualization panel.
"""

from pathlib import Path

from PyQt5.QtWidgets import (
    QComboBox,
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


class SimpleVisualizationPanel(QWidget):
    """Visualization planning page for dataset summaries."""

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

        intro = QLabel("先选择数据目录，再决定用什么方式做图表预览和汇总说明，让可视化输出更清晰。")
        intro.setObjectName("vizIntro")
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        source_group = QGroupBox("预览来源")
        source_layout = QVBoxLayout(source_group)
        source_layout.setContentsMargins(20, 24, 20, 20)
        source_layout.setSpacing(14)

        self.path_label = QLabel("未选择数据目录")
        self.path_label.setWordWrap(True)
        select_button = QPushButton("选择数据目录")
        select_button.setMinimumHeight(42)
        select_button.clicked.connect(self.select_dataset)

        path_row = QHBoxLayout()
        path_row.setSpacing(16)
        path_row.addWidget(self.path_label, 1)
        path_row.addWidget(select_button)
        source_layout.addLayout(path_row)

        option_row = QHBoxLayout()
        option_row.setSpacing(14)
        option_row.addWidget(QLabel("主图类型"))
        self.chart_combo = QComboBox()
        self.chart_combo.addItems(["类别分布", "子集占比", "标注格式分布", "目录结构概览"])
        self.chart_combo.setMinimumHeight(40)
        option_row.addWidget(self.chart_combo, 1)
        source_layout.addLayout(option_row)
        root_layout.addWidget(source_group)

        metrics_group = QGroupBox("预览指标")
        metrics_layout = QGridLayout(metrics_group)
        metrics_layout.setContentsMargins(20, 24, 20, 20)
        metrics_layout.setHorizontalSpacing(18)
        metrics_layout.setVerticalSpacing(18)

        for index, title in enumerate(["图像总量", "标注总量", "推荐主图", "输出说明"]):
            card, value_label = self._create_metric_card(title)
            self.metric_labels[title] = value_label
            metrics_layout.addWidget(card, index // 2, index % 2)

        root_layout.addWidget(metrics_group)

        action_group = QGroupBox("输出方案")
        action_layout = QHBoxLayout(action_group)
        action_layout.setContentsMargins(20, 22, 20, 20)
        action_layout.setSpacing(12)

        preview_button = QPushButton("刷新预览")
        preview_button.setProperty("buttonType", "success")
        preview_button.setMinimumHeight(46)
        preview_button.clicked.connect(self.refresh_preview)

        report_button = QPushButton("生成方案")
        report_button.setMinimumHeight(46)
        report_button.clicked.connect(self.generate_plan)

        action_layout.addWidget(preview_button)
        action_layout.addWidget(report_button)
        action_layout.addStretch()
        root_layout.addWidget(action_group)

        self.banner_label = QLabel("等待数据目录。")
        self.banner_label.setObjectName("vizBanner")
        self.banner_label.setWordWrap(True)
        root_layout.addWidget(self.banner_label)

        preview_group = QGroupBox("可视化预览")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.setContentsMargins(20, 24, 20, 20)
        preview_layout.setSpacing(12)

        self.preview_text = QPlainTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMinimumHeight(220)
        preview_layout.addWidget(self.preview_text)
        root_layout.addWidget(preview_group)
        root_layout.addStretch()

    def _create_metric_card(self, title: str):
        card = QFrame()
        card.setObjectName("summaryCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setObjectName("metricTitle")
        value_label = QLabel("--")
        value_label.setObjectName("metricValue")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        return card, value_label

    def select_dataset(self):
        path = QFileDialog.getExistingDirectory(self, "选择数据目录")
        if not path:
            return
        self.dataset_path = Path(path)
        self.path_label.setText(str(self.dataset_path))
        self.refresh_preview()

    def refresh_preview(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "提示", "请先选择数据目录。")
            return

        stats = self._scan_dataset(self.dataset_path)
        chart_name = self.chart_combo.currentText()
        self.metric_labels["图像总量"].setText(str(stats["images"]))
        self.metric_labels["标注总量"].setText(str(stats["labels"]))
        self.metric_labels["推荐主图"].setText(chart_name)
        self.metric_labels["输出说明"].setText("轻量预览")

        self.banner_label.setText(f"已根据当前目录刷新预览建议，推荐主图为“{chart_name}”。")
        self.preview_text.setPlainText(self._build_preview_text(stats, chart_name))

    def generate_plan(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "提示", "请先选择数据目录。")
            return

        stats = self._scan_dataset(self.dataset_path)
        chart_name = self.chart_combo.currentText()
        plan_lines = [
            "可视化输出方案",
            f"数据目录: {self.dataset_path}",
            f"主图类型: {chart_name}",
            f"图像数量: {stats['images']}",
            f"标注数量: {stats['labels']}",
            "建议搭配: 1 张主图 + 1 段摘要说明 + 1 份处理备注",
        ]
        self.preview_text.setPlainText("\n".join(plan_lines))
        self.banner_label.setText("可视化方案已生成，当前页面为轻量预览版。")

    def _scan_dataset(self, root: Path):
        image_files = [item for item in root.rglob("*") if item.is_file() and item.suffix.lower() in self.IMAGE_EXTENSIONS]
        label_files = [
            item
            for item in root.rglob("*")
            if item.is_file() and item.suffix.lower() in {".txt", ".json", ".xml"}
        ]
        return {"images": len(image_files), "labels": len(label_files)}

    def _build_preview_text(self, stats, chart_name):
        lines = [
            "可视化预览说明",
            f"数据目录: {self.dataset_path}",
            f"主图类型: {chart_name}",
            f"图像总量: {stats['images']}",
            f"标注总量: {stats['labels']}",
            "",
            "推荐展示顺序",
            "1. 顶部放一张主图，先交代整体规模。",
            "2. 中部放 2 到 3 条关键结论，避免信息过密。",
            "3. 底部保留处理备注，说明异常值或缺失情况。",
        ]
        return "\n".join(lines)

    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#vizIntro {
                color: #6d8198;
                font-size: 13px;
                line-height: 1.6;
                padding: 0 4px 2px 4px;
            }

            QLabel#vizBanner {
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
                font-size: 24px;
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
