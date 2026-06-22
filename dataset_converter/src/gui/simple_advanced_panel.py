"""
Light-green advanced tools panel.
"""

from collections import Counter
from pathlib import Path

from PyQt5.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class SimpleAdvancedPanel(QWidget):
    """Advanced inspection page with basic dataset checks."""

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
    LABEL_EXTENSIONS = {".txt", ".json", ".xml"}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dataset_path = None
        self.last_findings = []
        self._build_ui()

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(6, 6, 6, 6)
        root_layout.setSpacing(22)

        intro = QLabel("把常用质检项集中在同一页，先扫空标注、孤立文件和重名样本，再决定是否进入批量修复。")
        intro.setObjectName("advancedIntro")
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        path_group = QGroupBox("检查目录")
        path_layout = QVBoxLayout(path_group)
        path_layout.setContentsMargins(20, 24, 20, 20)
        path_layout.setSpacing(14)

        self.path_label = QLabel("未选择检查目录")
        self.path_label.setWordWrap(True)
        select_button = QPushButton("选择检查目录")
        select_button.setMinimumHeight(42)
        select_button.clicked.connect(self.select_dataset)

        path_row = QHBoxLayout()
        path_row.setSpacing(16)
        path_row.addWidget(self.path_label, 1)
        path_row.addWidget(select_button)
        path_layout.addLayout(path_row)
        root_layout.addWidget(path_group)

        option_group = QGroupBox("检查项")
        option_layout = QVBoxLayout(option_group)
        option_layout.setContentsMargins(20, 24, 20, 20)
        option_layout.setSpacing(12)

        self.empty_check = QCheckBox("检查空标注文件")
        self.empty_check.setChecked(True)
        self.orphan_check = QCheckBox("检查图像与标注不匹配")
        self.orphan_check.setChecked(True)
        self.duplicate_check = QCheckBox("检查同名样本")
        self.duplicate_check.setChecked(True)

        option_layout.addWidget(self.empty_check)
        option_layout.addWidget(self.orphan_check)
        option_layout.addWidget(self.duplicate_check)
        root_layout.addWidget(option_group)

        action_group = QGroupBox("执行动作")
        action_layout = QHBoxLayout(action_group)
        action_layout.setContentsMargins(20, 22, 20, 20)
        action_layout.setSpacing(12)

        inspect_button = QPushButton("执行检查")
        inspect_button.setProperty("buttonType", "success")
        inspect_button.setMinimumHeight(46)
        inspect_button.clicked.connect(self.run_inspection)

        suggest_button = QPushButton("生成修复建议")
        suggest_button.setMinimumHeight(46)
        suggest_button.clicked.connect(self.generate_suggestions)

        clear_button = QPushButton("清空结果")
        clear_button.setMinimumHeight(46)
        clear_button.clicked.connect(self.clear_results)

        action_layout.addWidget(inspect_button)
        action_layout.addWidget(suggest_button)
        action_layout.addWidget(clear_button)
        action_layout.addStretch()
        root_layout.addWidget(action_group)

        self.banner_label = QLabel("等待执行高级检查。")
        self.banner_label.setObjectName("advancedBanner")
        root_layout.addWidget(self.banner_label)

        result_group = QGroupBox("检查结果")
        result_layout = QVBoxLayout(result_group)
        result_layout.setContentsMargins(20, 24, 20, 20)
        result_layout.setSpacing(12)

        self.result_view = QPlainTextEdit()
        self.result_view.setReadOnly(True)
        self.result_view.setMinimumHeight(240)
        result_layout.addWidget(self.result_view)
        root_layout.addWidget(result_group)
        root_layout.addStretch()

    def select_dataset(self):
        path = QFileDialog.getExistingDirectory(self, "选择检查目录")
        if not path:
            return
        self.dataset_path = Path(path)
        self.path_label.setText(str(self.dataset_path))
        self.banner_label.setText("目录已选择，可以执行质检。")

    def run_inspection(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "提示", "请先选择检查目录。")
            return

        findings = []
        image_files = [item for item in self.dataset_path.rglob("*") if item.is_file() and item.suffix.lower() in self.IMAGE_EXTENSIONS]
        label_files = [item for item in self.dataset_path.rglob("*") if item.is_file() and item.suffix.lower() in self.LABEL_EXTENSIONS]

        image_stems = {item.stem for item in image_files}
        label_stems = {item.stem for item in label_files}

        if self.empty_check.isChecked():
            empty_labels = [item for item in label_files if item.stat().st_size == 0]
            findings.append(f"空标注文件: {len(empty_labels)}")

        if self.orphan_check.isChecked():
            findings.append(f"缺少标注的图像: {len(image_stems - label_stems)}")
            findings.append(f"缺少图像的标注: {len(label_stems - image_stems)}")

        if self.duplicate_check.isChecked():
            image_duplicates = sum(1 for count in Counter(item.stem for item in image_files).values() if count > 1)
            label_duplicates = sum(1 for count in Counter(item.stem for item in label_files).values() if count > 1)
            findings.append(f"重名图像样本: {image_duplicates}")
            findings.append(f"重名标注样本: {label_duplicates}")

        self.last_findings = findings
        self.result_view.setPlainText("\n".join(["高级检查结果"] + findings))
        self.banner_label.setText("检查完成，结果已更新。")

    def generate_suggestions(self):
        if not self.last_findings:
            self.result_view.setPlainText("请先执行一次检查，再生成修复建议。")
            return

        suggestions = ["修复建议"]
        for item in self.last_findings:
            if "空标注文件" in item and not item.endswith(": 0"):
                suggestions.append("1. 优先清理空标注文件，避免训练阶段报错。")
            if "缺少标注的图像" in item and not item.endswith(": 0"):
                suggestions.append("2. 将缺标图像单独归档，或补齐标注后再导入。")
            if "缺少图像的标注" in item and not item.endswith(": 0"):
                suggestions.append("3. 检查标注目录是否存在过期文件或命名漂移。")
            if "重名" in item and not item.endswith(": 0"):
                suggestions.append("4. 对重名样本增加批次前缀，避免后续导出覆盖。")

        if len(suggestions) == 1:
            suggestions.append("当前未发现明显问题，可以继续进行后续处理。")

        self.result_view.setPlainText("\n".join(suggestions))
        self.banner_label.setText("修复建议已生成。")

    def clear_results(self):
        self.last_findings = []
        self.result_view.clear()
        self.banner_label.setText("结果已清空。")

    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#advancedIntro {
                color: #6d8198;
                font-size: 13px;
                line-height: 1.6;
                padding: 0 4px 2px 4px;
            }

            QLabel#advancedBanner {
                background-color: #edf5ff;
                border: 1px solid #c8dcf8;
                border-radius: 14px;
                padding: 12px 16px;
                color: #20456d;
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
