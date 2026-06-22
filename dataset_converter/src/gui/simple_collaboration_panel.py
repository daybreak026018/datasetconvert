"""
Light-green collaboration panel.
"""

from PyQt5.QtWidgets import (
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class SimpleCollaborationPanel(QWidget):
    """Collaboration dashboard with a lightweight task board."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.metric_labels = {}
        self._build_ui()
        self._seed_tables()

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(6, 6, 6, 6)
        root_layout.setSpacing(22)

        intro = QLabel("用轻量看板管理标注分工、任务状态和交接说明，避免多人协作时界面过挤。")
        intro.setObjectName("collabIntro")
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        metrics_group = QGroupBox("协作概览")
        metrics_layout = QGridLayout(metrics_group)
        metrics_layout.setContentsMargins(20, 24, 20, 20)
        metrics_layout.setHorizontalSpacing(18)
        metrics_layout.setVerticalSpacing(18)

        for index, title in enumerate(["进行中任务", "待复核", "成员数量", "今日更新"]):
            card, value_label = self._create_metric_card(title)
            self.metric_labels[title] = value_label
            metrics_layout.addWidget(card, index // 2, index % 2)

        root_layout.addWidget(metrics_group)

        table_group = QGroupBox("任务看板")
        table_layout = QVBoxLayout(table_group)
        table_layout.setContentsMargins(20, 24, 20, 20)
        table_layout.setSpacing(12)

        button_row = QHBoxLayout()
        button_row.setSpacing(12)

        add_button = QPushButton("新增任务")
        add_button.setProperty("buttonType", "success")
        add_button.setMinimumHeight(42)
        add_button.clicked.connect(self.add_task)

        done_button = QPushButton("标记完成")
        done_button.setMinimumHeight(42)
        done_button.clicked.connect(self.mark_done)

        handoff_button = QPushButton("生成交接备注")
        handoff_button.setMinimumHeight(42)
        handoff_button.clicked.connect(self.generate_handoff)

        button_row.addWidget(add_button)
        button_row.addWidget(done_button)
        button_row.addWidget(handoff_button)
        button_row.addStretch()
        table_layout.addLayout(button_row)

        self.task_table = QTableWidget(0, 4)
        self.task_table.setHorizontalHeaderLabels(["任务", "负责人", "状态", "备注"])
        self.task_table.verticalHeader().setVisible(False)
        self.task_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.task_table.setAlternatingRowColors(True)
        self.task_table.setMinimumHeight(220)
        table_layout.addWidget(self.task_table)
        root_layout.addWidget(table_group)

        notes_group = QGroupBox("交接说明")
        notes_layout = QVBoxLayout(notes_group)
        notes_layout.setContentsMargins(20, 24, 20, 20)
        notes_layout.setSpacing(12)

        self.notes_view = QPlainTextEdit()
        self.notes_view.setReadOnly(False)
        self.notes_view.setPlaceholderText("在这里记录批次边界、审核标准或异常样本说明。")
        self.notes_view.setMinimumHeight(180)
        notes_layout.addWidget(self.notes_view)
        root_layout.addWidget(notes_group)
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

    def _seed_tables(self):
        rows = [
            ("批次 A 清洗", "张三", "进行中", "检查图像命名"),
            ("批次 B 复核", "李四", "待复核", "关注漏标样本"),
            ("批次 C 导出", "王五", "已排期", "等待格式统一"),
        ]
        self.task_table.setRowCount(len(rows))
        for row_index, row_values in enumerate(rows):
            for column_index, value in enumerate(row_values):
                self.task_table.setItem(row_index, column_index, QTableWidgetItem(value))

        self.metric_labels["进行中任务"].setText("2")
        self.metric_labels["待复核"].setText("1")
        self.metric_labels["成员数量"].setText("3")
        self.metric_labels["今日更新"].setText("4")

    def add_task(self):
        row = self.task_table.rowCount()
        self.task_table.insertRow(row)
        default_values = ["新任务", "待分配", "待开始", "补充说明"]
        for column, value in enumerate(default_values):
            self.task_table.setItem(row, column, QTableWidgetItem(value))
        self.notes_view.appendPlainText("新增任务: 已添加一条待分配记录。")

    def mark_done(self):
        row = self.task_table.currentRow()
        if row < 0:
            self.notes_view.appendPlainText("未选择任务，无法标记完成。")
            return
        self.task_table.setItem(row, 2, QTableWidgetItem("已完成"))
        self.notes_view.appendPlainText(f"任务完成: 第 {row + 1} 行已更新为已完成。")

    def generate_handoff(self):
        lines = [
            "交接摘要",
            f"任务总数: {self.task_table.rowCount()}",
            "建议下一位处理人优先检查待复核任务。",
            "如需导出正式交接单，可复用当前看板内容继续扩展。",
        ]
        self.notes_view.setPlainText("\n".join(lines))

    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#collabIntro {
                color: #6d8198;
                font-size: 13px;
                line-height: 1.6;
                padding: 0 4px 2px 4px;
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

            QTableWidget,
            QPlainTextEdit {
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
