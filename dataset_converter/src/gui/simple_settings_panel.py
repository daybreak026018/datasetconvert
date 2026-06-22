"""
Blue settings panel.
"""

from pathlib import Path

from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from .theme_manager import theme_manager


class SimpleSettingsPanel(QWidget):
    """Settings page with a fixed blue theme."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = QSettings("DataForge", "DatasetConverter")
        self.default_input_dir = self._default_data_dir("input")
        self.default_output_dir = self._default_data_dir("output")
        self._build_ui()
        self.load_settings()

    def _default_data_dir(self, name: str):
        base = Path(__file__).resolve().parents[2] / "data" / name
        return str(base)

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(6, 6, 6, 6)
        root_layout.setSpacing(22)

        banner = QLabel("界面主题已固定为白底蓝色，本页只保留常用偏好设置，不再提供主题切换。")
        banner.setObjectName("settingsBanner")
        banner.setWordWrap(True)
        root_layout.addWidget(banner)

        behavior_group = QGroupBox("使用偏好")
        behavior_layout = QVBoxLayout(behavior_group)
        behavior_layout.setContentsMargins(20, 24, 20, 20)
        behavior_layout.setSpacing(12)

        self.auto_save_check = QCheckBox("完成任务后自动保存最近一次配置")
        self.show_tips_check = QCheckBox("显示操作提示与状态提醒")
        self.open_output_check = QCheckBox("处理完成后优先定位输出目录")

        behavior_layout.addWidget(self.auto_save_check)
        behavior_layout.addWidget(self.show_tips_check)
        behavior_layout.addWidget(self.open_output_check)
        root_layout.addWidget(behavior_group)

        path_group = QGroupBox("默认目录")
        path_layout = QVBoxLayout(path_group)
        path_layout.setContentsMargins(20, 24, 20, 20)
        path_layout.setSpacing(16)

        self.input_edit = QLineEdit()
        self.input_edit.setReadOnly(True)
        input_button = QPushButton("选择默认输入目录")
        input_button.setMinimumHeight(40)
        input_button.clicked.connect(self.choose_input_dir)
        path_layout.addLayout(self._build_path_row("输入目录", self.input_edit, input_button))

        self.output_edit = QLineEdit()
        self.output_edit.setReadOnly(True)
        output_button = QPushButton("选择默认输出目录")
        output_button.setMinimumHeight(40)
        output_button.clicked.connect(self.choose_output_dir)
        path_layout.addLayout(self._build_path_row("输出目录", self.output_edit, output_button))

        root_layout.addWidget(path_group)

        action_group = QGroupBox("维护")
        action_layout = QHBoxLayout(action_group)
        action_layout.setContentsMargins(20, 22, 20, 20)
        action_layout.setSpacing(12)

        save_button = QPushButton("保存设置")
        save_button.setProperty("buttonType", "success")
        save_button.setMinimumHeight(46)
        save_button.clicked.connect(self.save_settings)

        reset_button = QPushButton("恢复默认")
        reset_button.setMinimumHeight(46)
        reset_button.clicked.connect(self.reset_settings)

        lock_button = QPushButton("重新应用蓝色主题")
        lock_button.setMinimumHeight(46)
        lock_button.clicked.connect(self.reapply_theme)

        action_layout.addWidget(save_button)
        action_layout.addWidget(reset_button)
        action_layout.addWidget(lock_button)
        action_layout.addStretch()
        root_layout.addWidget(action_group)
        root_layout.addStretch()

    def _build_path_row(self, title: str, edit: QLineEdit, button: QPushButton):
        layout = QHBoxLayout()
        layout.setSpacing(12)
        label = QLabel(title)
        label.setMinimumWidth(72)
        layout.addWidget(label)
        layout.addWidget(edit, 1)
        layout.addWidget(button)
        return layout

    def choose_input_dir(self):
        path = QFileDialog.getExistingDirectory(self, "选择默认输入目录", self.input_edit.text() or self.default_input_dir)
        if path:
            self.input_edit.setText(path)

    def choose_output_dir(self):
        path = QFileDialog.getExistingDirectory(self, "选择默认输出目录", self.output_edit.text() or self.default_output_dir)
        if path:
            self.output_edit.setText(path)

    def load_settings(self):
        self.auto_save_check.setChecked(self.settings.value("auto_save", True, type=bool))
        self.show_tips_check.setChecked(self.settings.value("show_tips", True, type=bool))
        self.open_output_check.setChecked(self.settings.value("open_output", False, type=bool))
        self.input_edit.setText(self.settings.value("default_input_dir", self.default_input_dir))
        self.output_edit.setText(self.settings.value("default_output_dir", self.default_output_dir))

    def save_settings(self):
        self.settings.setValue("auto_save", self.auto_save_check.isChecked())
        self.settings.setValue("show_tips", self.show_tips_check.isChecked())
        self.settings.setValue("open_output", self.open_output_check.isChecked())
        self.settings.setValue("default_input_dir", self.input_edit.text())
        self.settings.setValue("default_output_dir", self.output_edit.text())
        QMessageBox.information(self, "完成", "设置已保存。")

    def reset_settings(self):
        self.auto_save_check.setChecked(True)
        self.show_tips_check.setChecked(True)
        self.open_output_check.setChecked(False)
        self.input_edit.setText(self.default_input_dir)
        self.output_edit.setText(self.default_output_dir)
        self.reapply_theme()

    def reapply_theme(self):
        theme_manager.set_theme("light")
        QMessageBox.information(self, "完成", "已重新锁定蓝色界面。")

    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#settingsBanner {
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

            QLineEdit {
                border: 1px solid #dbe7f6;
                border-radius: 12px;
                background-color: #fbfdff;
                padding: 10px 12px;
            }
            """
        )
