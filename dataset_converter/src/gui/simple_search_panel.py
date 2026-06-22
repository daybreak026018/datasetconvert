"""
Light-green dataset search panel.
"""

from pathlib import Path

from PyQt5.QtWidgets import (
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class SimpleSearchPanel(QWidget):
    """Dataset file search page."""

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
    LABEL_EXTENSIONS = {".txt", ".json", ".xml"}

    def __init__(self, parent=None):
        super().__init__(parent)
        self.dataset_path = None
        self._build_ui()

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(6, 6, 6, 6)
        root_layout.setSpacing(22)

        intro = QLabel("用关键词、文件类型和子集目录快速筛选内容，减少手动翻找文件的时间。")
        intro.setObjectName("searchIntro")
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        path_group = QGroupBox("搜索目录")
        path_layout = QVBoxLayout(path_group)
        path_layout.setContentsMargins(20, 24, 20, 20)
        path_layout.setSpacing(14)

        self.path_label = QLabel("未选择搜索目录")
        self.path_label.setWordWrap(True)
        select_button = QPushButton("选择搜索目录")
        select_button.setMinimumHeight(42)
        select_button.clicked.connect(self.select_dataset)

        path_row = QHBoxLayout()
        path_row.setSpacing(16)
        path_row.addWidget(self.path_label, 1)
        path_row.addWidget(select_button)
        path_layout.addLayout(path_row)
        root_layout.addWidget(path_group)

        filter_group = QGroupBox("筛选条件")
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.setContentsMargins(20, 24, 20, 20)
        filter_layout.setSpacing(12)

        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("输入文件名关键词")
        self.keyword_input.setMinimumHeight(40)

        self.type_combo = QComboBox()
        self.type_combo.addItems(["全部类型", "图像文件", "标注文件"])
        self.type_combo.setMinimumHeight(40)

        self.split_combo = QComboBox()
        self.split_combo.addItems(["全部子集", "train", "val", "test"])
        self.split_combo.setMinimumHeight(40)

        search_button = QPushButton("开始搜索")
        search_button.setProperty("buttonType", "success")
        search_button.setMinimumHeight(42)
        search_button.clicked.connect(self.run_search)

        clear_button = QPushButton("清空结果")
        clear_button.setMinimumHeight(42)
        clear_button.clicked.connect(self.clear_results)

        filter_layout.addWidget(self.keyword_input, 2)
        filter_layout.addWidget(self.type_combo, 1)
        filter_layout.addWidget(self.split_combo, 1)
        filter_layout.addWidget(search_button)
        filter_layout.addWidget(clear_button)
        root_layout.addWidget(filter_group)

        self.status_label = QLabel("等待执行搜索。")
        self.status_label.setObjectName("searchBanner")
        root_layout.addWidget(self.status_label)

        results_group = QGroupBox("搜索结果")
        results_layout = QVBoxLayout(results_group)
        results_layout.setContentsMargins(20, 24, 20, 20)
        results_layout.setSpacing(12)

        self.results_table = QTableWidget(0, 4)
        self.results_table.setHorizontalHeaderLabels(["文件名", "类型", "子集", "路径"])
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setMinimumHeight(260)
        results_layout.addWidget(self.results_table)

        root_layout.addWidget(results_group)
        root_layout.addStretch()

    def select_dataset(self):
        path = QFileDialog.getExistingDirectory(self, "选择搜索目录")
        if not path:
            return
        self.dataset_path = Path(path)
        self.path_label.setText(str(self.dataset_path))
        self.status_label.setText("目录已选择，可以开始搜索。")

    def run_search(self):
        if not self.dataset_path:
            QMessageBox.warning(self, "提示", "请先选择搜索目录。")
            return

        keyword = self.keyword_input.text().strip().lower()
        type_filter = self.type_combo.currentText()
        split_filter = self.split_combo.currentText()

        results = []
        for item in self.dataset_path.rglob("*"):
            if not item.is_file():
                continue

            file_type = self._detect_type(item)
            if type_filter == "图像文件" and file_type != "图像":
                continue
            if type_filter == "标注文件" and file_type != "标注":
                continue

            subset = self._detect_subset(item)
            if split_filter != "全部子集" and subset != split_filter:
                continue

            if keyword and keyword not in item.name.lower():
                continue

            results.append((item.name, file_type, subset or "-", str(item)))
            if len(results) >= 500:
                break

        self.results_table.setRowCount(len(results))
        for row, values in enumerate(results):
            for column, value in enumerate(values):
                self.results_table.setItem(row, column, QTableWidgetItem(value))

        self.status_label.setText(f"搜索完成，共匹配 {len(results)} 条结果。")

    def clear_results(self):
        self.results_table.setRowCount(0)
        self.status_label.setText("结果已清空。")

    def _detect_type(self, path: Path):
        suffix = path.suffix.lower()
        if suffix in self.IMAGE_EXTENSIONS:
            return "图像"
        if suffix in self.LABEL_EXTENSIONS:
            return "标注"
        return "其他"

    def _detect_subset(self, path: Path):
        for part in path.parts:
            lowered = part.lower()
            if lowered in {"train", "val", "test"}:
                return lowered
        return ""

    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#searchIntro {
                color: #6d8198;
                font-size: 13px;
                line-height: 1.6;
                padding: 0 4px 2px 4px;
            }

            QLabel#searchBanner {
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
