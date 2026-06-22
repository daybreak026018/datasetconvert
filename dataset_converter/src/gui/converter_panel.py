from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..utils.label_utils import parse_label_map_txt
from ..utils.logger import get_logger


class ConverterPanel(QWidget):
    """Rebuilt spacious converter page with the original conversion logic."""

    FORMAT_LABELS = {
        "yolo": "YOLO检测",
        "yolo_seg": "YOLO分割",
        "voc": "VOC",
        "json": "JSON",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger()
        self.input_dir = None
        self.output_dir = None
        self.input_fmt = "yolo"
        self.output_fmt = "voc"
        self.label_map = {}
        self.conversion_buttons = []
        self.current_selected_button = None
        self._build_ui()
        self.set_formats("yolo", "voc", auto_select_button=True)

    def _build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(2, 2, 2, 2)
        root_layout.setSpacing(10)

        intro = QLabel("选择输入和输出目录后，再选择目标格式。页面采用更疏朗的卡片布局，减少拥挤感。")
        intro.setObjectName("converterIntro")
        intro.setWordWrap(True)
        root_layout.addWidget(intro)

        path_group = QGroupBox("路径设置")
        path_layout = QVBoxLayout(path_group)
        path_layout.setContentsMargins(12, 16, 12, 12)
        path_layout.setSpacing(8)

        self.input_label = QLabel("输入目录：未选择")
        self.input_label.setWordWrap(True)
        btn_in = QPushButton("选择输入目录")
        btn_in.setMinimumHeight(32)
        btn_in.clicked.connect(self.choose_input)
        path_layout.addLayout(self._build_path_row(self.input_label, btn_in))

        self.output_label = QLabel("输出目录：未选择")
        self.output_label.setWordWrap(True)
        btn_out = QPushButton("选择输出目录")
        btn_out.setMinimumHeight(32)
        btn_out.clicked.connect(self.choose_output)
        path_layout.addLayout(self._build_path_row(self.output_label, btn_out))
        root_layout.addWidget(path_group)

        self.label_fmt = QLabel("当前选择：YOLO检测 -> VOC")
        self.label_fmt.setObjectName("converterStatus")
        self.label_fmt.setWordWrap(True)
        root_layout.addWidget(self.label_fmt)

        basic_group = self.create_conversion_group(
            "基础格式转换",
            [
                ("YOLO检测 -> VOC", "yolo", "voc"),
                ("VOC -> YOLO检测", "voc", "yolo"),
                ("YOLO检测 -> JSON", "yolo", "json"),
                ("JSON -> YOLO检测", "json", "yolo"),
                ("JSON -> VOC", "json", "voc"),
            ],
        )
        root_layout.addWidget(basic_group)

        seg_group = self.create_conversion_group(
            "分割格式转换",
            [
                ("YOLO分割 -> JSON", "yolo_seg", "json"),
                ("JSON -> YOLO分割", "json", "yolo_seg"),
                ("YOLO分割 -> YOLO检测", "yolo_seg", "yolo"),
            ],
        )
        root_layout.addWidget(seg_group)

        tools_group = QGroupBox("操作")
        tools_layout = QHBoxLayout(tools_group)
        tools_layout.setContentsMargins(12, 16, 12, 12)
        tools_layout.setSpacing(8)

        btn_label_map = QPushButton("加载标签字典")
        btn_label_map.setProperty("buttonType", "warning")
        btn_label_map.setMinimumHeight(34)
        btn_label_map.clicked.connect(self.on_load_label_map)

        btn_convert = QPushButton("开始转换")
        btn_convert.setProperty("buttonType", "success")
        btn_convert.setMinimumHeight(34)
        btn_convert.clicked.connect(self.on_convert)

        tools_layout.addWidget(btn_label_map)
        tools_layout.addWidget(btn_convert)
        tools_layout.addStretch()
        root_layout.addWidget(tools_group)

        log_label = QLabel("日志输出")
        log_label.setObjectName("converterLogTitle")
        root_layout.addWidget(log_label)

        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMinimumHeight(100)
        root_layout.addWidget(self.log_view)
        root_layout.addStretch()

    def _build_path_row(self, label: QLabel, button: QPushButton):
        layout = QHBoxLayout()
        layout.setSpacing(8)
        label.setMinimumHeight(32)
        label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        layout.addWidget(label, 1)
        layout.addWidget(button)
        return layout

    def create_conversion_group(self, title, conversions):
        group = QGroupBox(title)
        outer_layout = QVBoxLayout(group)
        outer_layout.setContentsMargins(10, 16, 10, 10)
        outer_layout.setSpacing(8)

        option_wrap = QFrame()
        option_wrap.setObjectName("optionWrap")
        layout = QGridLayout(option_wrap)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(8)

        for i, (text, inp_fmt, out_fmt) in enumerate(conversions):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setMinimumHeight(36)
            btn.setMinimumWidth(120)
            btn.clicked.connect(
                lambda checked, i=inp_fmt, o=out_fmt, b=btn: self.set_formats(i, o, b)
            )
            btn.input_format = inp_fmt
            btn.output_format = out_fmt
            self.conversion_buttons.append(btn)

            row = i // 2
            col = i % 2
            layout.addWidget(btn, row, col)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        outer_layout.addWidget(option_wrap)
        return group

    def choose_input(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输入目录", str(Path.cwd()))
        if directory:
            self.input_dir = Path(directory)
            self.input_label.setText(f"输入目录：{directory}")

    def choose_output(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输出目录", str(Path.cwd()))
        if directory:
            self.output_dir = Path(directory)
            self.output_label.setText(f"输出目录：{directory}")

    def set_formats(self, inp: str, outp: str, selected_button=None, auto_select_button=False):
        self.input_fmt = inp
        self.output_fmt = outp

        inp_name = self.FORMAT_LABELS.get(inp, inp.upper())
        outp_name = self.FORMAT_LABELS.get(outp, outp.upper())
        self.label_fmt.setText(f"当前选择：{inp_name} -> {outp_name}")
        self.update_button_selection(inp, outp, selected_button, auto_select_button)

    def update_button_selection(self, inp_fmt, out_fmt, selected_button=None, auto_select=False):
        for btn in self.conversion_buttons:
            btn.setChecked(False)
            btn.setStyleSheet("")

        target_button = selected_button
        if not target_button or auto_select:
            for btn in self.conversion_buttons:
                if btn.input_format == inp_fmt and btn.output_format == out_fmt:
                    target_button = btn
                    break

        if target_button:
            target_button.setChecked(True)
            self.apply_selected_style(target_button)
            self.current_selected_button = target_button

    def apply_selected_style(self, button):
        from .theme_manager import theme_manager

        colors = theme_manager.get_theme_config()["colors"]
        selected_style = f"""
            QPushButton {{
                border-radius: 8px;
                padding: 7px 10px;
            }}
            QPushButton:checked {{
                background-color: {colors['primary']};
                border: 2px solid {colors.get('nav_selected_border', colors['primary'])};
                color: white;
                font-weight: bold;
            }}
            QPushButton:checked:hover {{
                background-color: {colors['selected']};
                border: 2px solid {colors.get('nav_selected_border', colors['primary'])};
            }}
            QPushButton:hover {{
                background-color: {colors['hover']};
                border: 1px solid {colors['primary']};
            }}
        """
        button.setStyleSheet(selected_style)

        for btn in self.conversion_buttons:
            if btn != button:
                self.apply_hover_style(btn)

    def apply_hover_style(self, button):
        from .theme_manager import theme_manager

        colors = theme_manager.get_theme_config()["colors"]
        hover_style = f"""
            QPushButton {{
                border-radius: 8px;
                padding: 7px 10px;
            }}
            QPushButton:hover {{
                background-color: {colors['hover']};
                border: 1px solid {colors['primary']};
            }}
        """
        button.setStyleSheet(hover_style)

    def append_log(self, msg: str):
        self.log_view.append(msg)
        self.logger.info(msg)

    def on_convert(self):
        if not self.input_dir or not self.output_dir:
            QMessageBox.warning(self, "提示", "请先选择输入目录和输出目录")
            return

        from ..utils.worker_thread import run_with_progress

        inp_name = self.FORMAT_LABELS.get(self.input_fmt, self.input_fmt)
        outp_name = self.FORMAT_LABELS.get(self.output_fmt, self.output_fmt)

        self.append_log(f"开始转换：{inp_name} -> {outp_name}")
        title = f"数据集转换：{inp_name} -> {outp_name}"
        run_with_progress(
            self,
            title,
            self._convert_with_progress,
            self.input_dir,
            self.input_fmt,
            self.output_dir,
            self.output_fmt,
            self.label_map,
        )

    def _convert_with_progress(
        self,
        input_dir,
        input_fmt,
        output_dir,
        output_fmt,
        label_map,
        progress_callback=None,
        status_callback=None,
        cancel_callback=None,
    ):
        from ..core.converter import convert_with_progress

        if output_fmt == "json" and status_callback:
            status_callback("输出说明：每张图片会导出为独立 JSON 文件")
        elif input_fmt == "yolo_seg" and status_callback:
            status_callback("输入说明：YOLO 分割支持矩形框和多边形混合标注")
        elif output_fmt == "yolo_seg" and status_callback:
            status_callback("输出说明：YOLO 分割会保留原始几何信息")

        convert_with_progress(
            input_dir,
            input_fmt,
            output_dir,
            output_fmt,
            label_map=label_map,
            progress_callback=progress_callback,
            status_callback=status_callback,
            cancel_callback=cancel_callback,
        )
        return "转换完成"

    def on_task_finished(self, result):
        self.append_log("转换完成")
        QMessageBox.information(self, "完成", "转换任务已完成")

    def on_load_label_map(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择标签字典 txt",
            str(Path.cwd()),
            "Text Files (*.txt)",
        )
        if not file_path:
            return

        try:
            self.label_map = parse_label_map_txt(Path(file_path))
            if not self.label_map:
                QMessageBox.warning(self, "提示", "未解析到有效标签映射")
                return
            self.append_log(f"已加载标签映射：{len(self.label_map)} 项")
            self.label_fmt.setText(self.label_fmt.text() + "（已加载标签映射）")
        except Exception as exc:
            QMessageBox.critical(self, "错误", f"解析失败: {exc}")

    def apply_theme(self):
        self.setStyleSheet(
            """
            QLabel#converterIntro {
                color: #6d8198;
                font-size: 11px;
                line-height: 1.6;
                padding: 0 4px 2px 4px;
                background-color: transparent;
            }

            QLabel#converterStatus {
                background-color: #edf5ff;
                border: 1px solid #c8dcf8;
                border-radius: 8px;
                padding: 8px 10px;
                color: #20456d;
                font-weight: bold;
            }

            QLabel#converterLogTitle {
                color: #20456d;
                font-size: 12px;
                font-weight: bold;
                padding-left: 2px;
                background-color: transparent;
            }

            QGroupBox {
                margin-top: 16px;
                padding-top: 12px;
            }

            QFrame#optionWrap {
                background-color: #f6faff;
                border: 1px solid #dbe7f6;
                border-radius: 8px;
            }
            """
        )

        if self.current_selected_button:
            self.apply_selected_style(self.current_selected_button)
        for btn in self.conversion_buttons:
            if btn != self.current_selected_button:
                self.apply_hover_style(btn)
