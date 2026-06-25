import json
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import QSettings, Qt
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

    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
    LABEL_EXTENSIONS_BY_FORMAT = {
        "yolo": {".txt"},
        "yolo_seg": {".txt"},
        "voc": {".xml"},
        "json": {".json"},
    }
    MAX_RECENT_TASKS = 8

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
        self.conversion_groups = []
        self.current_selected_button = None
        self.settings = QSettings("DataForge", "DatasetConverter")
        self._active_task_started_at = None
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

        btn_precheck = QPushButton("转换预检")
        btn_precheck.setMinimumHeight(34)
        btn_precheck.clicked.connect(self.on_precheck)

        btn_recent = QPushButton("最近任务")
        btn_recent.setMinimumHeight(34)
        btn_recent.clicked.connect(self.show_recent_tasks)

        btn_convert = QPushButton("开始转换")
        btn_convert.setProperty("buttonType", "success")
        btn_convert.setMinimumHeight(34)
        btn_convert.clicked.connect(self.on_convert)

        tools_layout.addWidget(btn_label_map)
        tools_layout.addWidget(btn_precheck)
        tools_layout.addWidget(btn_recent)
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

        group_buttons = []
        for i, (text, inp_fmt, out_fmt) in enumerate(conversions):
            btn = QPushButton(text)
            btn.setCheckable(True)
            btn.setMinimumHeight(36)
            btn.setMinimumWidth(96)
            btn.clicked.connect(
                lambda checked, i=inp_fmt, o=out_fmt, b=btn: self.set_formats(i, o, b)
            )
            btn.input_format = inp_fmt
            btn.output_format = out_fmt
            self.conversion_buttons.append(btn)
            group_buttons.append(btn)

            row = i // 2
            col = i % 2
            layout.addWidget(btn, row, col)

        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        outer_layout.addWidget(option_wrap)
        self.conversion_groups.append((layout, group_buttons))
        return group

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_conversion_layouts()

    def update_conversion_layouts(self):
        use_single_column = self.width() < 620
        columns = 1 if use_single_column else 2

        for layout, buttons in self.conversion_groups:
            for button in buttons:
                layout.removeWidget(button)
            for index, button in enumerate(buttons):
                row = index // columns
                col = index % columns
                layout.addWidget(button, row, col)
            for column in range(2):
                layout.setColumnStretch(column, 1 if column < columns else 0)

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

    def on_precheck(self):
        if not self.input_dir:
            QMessageBox.warning(self, "提示", "请先选择输入目录")
            return

        report = self._build_precheck_report()
        self.append_log(self._format_precheck_report(report))
        if report["blockers"]:
            QMessageBox.warning(self, "预检未通过", "\n".join(report["blockers"]))
        elif report["warnings"]:
            QMessageBox.information(self, "预检完成", "发现提醒项，详情已写入日志。")
        else:
            QMessageBox.information(self, "预检完成", "未发现明显问题，可以开始转换。")

    def on_convert(self):
        if not self.input_dir or not self.output_dir:
            QMessageBox.warning(self, "提示", "请先选择输入目录和输出目录")
            return

        report = self._build_precheck_report()
        self.append_log(self._format_precheck_report(report))
        if report["blockers"]:
            QMessageBox.warning(self, "预检未通过", "\n".join(report["blockers"]))
            return
        if report["warnings"]:
            choice = QMessageBox.question(
                self,
                "预检提醒",
                "预检发现一些提醒项：\n"
                + "\n".join(report["warnings"][:6])
                + "\n\n是否继续转换？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if choice != QMessageBox.Yes:
                self.append_log("已取消转换：用户在预检提醒处停止。")
                return

        from ..utils.worker_thread import run_with_progress

        inp_name = self.FORMAT_LABELS.get(self.input_fmt, self.input_fmt)
        outp_name = self.FORMAT_LABELS.get(self.output_fmt, self.output_fmt)

        self.append_log(f"开始转换：{inp_name} -> {outp_name}")
        self._active_task_started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._upsert_recent_task(
            {
                "started_at": self._active_task_started_at,
                "input_dir": str(self.input_dir),
                "output_dir": str(self.output_dir),
                "input_format": inp_name,
                "output_format": outp_name,
                "status": "进行中",
                "summary": self._precheck_summary(report),
            }
        )
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
        if self._active_task_started_at:
            self._upsert_recent_task({"started_at": self._active_task_started_at, "status": "完成"})
            self._active_task_started_at = None
        QMessageBox.information(self, "完成", "转换任务已完成")

    def on_task_error(self, error_msg: str):
        if self._active_task_started_at:
            self._upsert_recent_task(
                {
                    "started_at": self._active_task_started_at,
                    "status": "失败",
                    "summary": f"转换失败：{error_msg}",
                }
            )
            self._active_task_started_at = None

    def _build_precheck_report(self):
        report = {
            "input_dir": str(self.input_dir) if self.input_dir else "",
            "output_dir": str(self.output_dir) if self.output_dir else "",
            "images": 0,
            "labels": 0,
            "paired_images": 0,
            "orphan_images": 0,
            "orphan_labels": 0,
            "empty_labels": 0,
            "warnings": [],
            "blockers": [],
        }

        if not self.input_dir or not self.input_dir.exists() or not self.input_dir.is_dir():
            report["blockers"].append("输入目录不存在或不可访问。")
            return report

        label_exts = self.LABEL_EXTENSIONS_BY_FORMAT.get(self.input_fmt, {".txt", ".json", ".xml"})
        image_files = [
            item
            for item in self.input_dir.rglob("*")
            if item.is_file() and item.suffix.lower() in self.IMAGE_EXTENSIONS
        ]
        label_files = [
            item
            for item in self.input_dir.rglob("*")
            if item.is_file() and item.suffix.lower() in label_exts
        ]
        image_stems = {item.stem for item in image_files}
        label_stems = {item.stem for item in label_files}

        report["images"] = len(image_files)
        report["labels"] = len(label_files)
        report["paired_images"] = len(image_stems & label_stems)
        report["orphan_images"] = len(image_stems - label_stems)
        report["orphan_labels"] = len(label_stems - image_stems)
        report["empty_labels"] = sum(1 for item in label_files if item.stat().st_size == 0)

        if not image_files and not label_files:
            report["blockers"].append("输入目录没有识别到可转换的数据文件。")
        if self.output_dir:
            output_parent = self.output_dir if self.output_dir.exists() else self.output_dir.parent
            if not output_parent.exists():
                report["blockers"].append("输出目录的上级目录不存在。")
        if not label_files:
            report["warnings"].append("未找到当前输入格式对应的标注文件。")
        if report["orphan_images"] > 0:
            report["warnings"].append(f"有 {report['orphan_images']} 张图像缺少同名标注。")
        if report["orphan_labels"] > 0:
            report["warnings"].append(f"有 {report['orphan_labels']} 个标注文件缺少同名图像。")
        if report["empty_labels"] > 0:
            report["warnings"].append(f"有 {report['empty_labels']} 个空标注文件，请确认是否为负样本。")
        if self.input_fmt in {"yolo", "yolo_seg"} and not self.label_map:
            report["warnings"].append("YOLO 输入未加载标签字典，类别名可能只能按编号处理。")

        return report

    def _format_precheck_report(self, report):
        lines = [
            "",
            "转换预检",
            f"输入目录: {report['input_dir']}",
            f"输出目录: {report['output_dir'] or '未选择'}",
            f"图像文件: {report['images']}",
            f"标注文件: {report['labels']}",
            f"完整配对: {report['paired_images']}",
            f"缺少标注的图像: {report['orphan_images']}",
            f"缺少图像的标注: {report['orphan_labels']}",
            f"空标注文件: {report['empty_labels']}",
        ]
        if report["blockers"]:
            lines.append("阻断问题:")
            lines.extend(f"- {item}" for item in report["blockers"])
        if report["warnings"]:
            lines.append("提醒:")
            lines.extend(f"- {item}" for item in report["warnings"])
        if not report["blockers"] and not report["warnings"]:
            lines.append("结果: 未发现明显问题。")
        return "\n".join(lines)

    def _precheck_summary(self, report):
        if report["blockers"]:
            return f"预检阻断 {len(report['blockers'])} 项"
        if report["warnings"]:
            return f"预检提醒 {len(report['warnings'])} 项"
        return "预检通过"

    def _load_recent_tasks(self):
        raw = self.settings.value("recent_tasks", "[]")
        try:
            tasks = json.loads(raw)
        except (TypeError, json.JSONDecodeError):
            return []
        return tasks if isinstance(tasks, list) else []

    def _save_recent_tasks(self, tasks):
        self.settings.setValue("recent_tasks", json.dumps(tasks[: self.MAX_RECENT_TASKS], ensure_ascii=False))

    def _upsert_recent_task(self, task_update):
        tasks = self._load_recent_tasks()
        started_at = task_update.get("started_at")
        for task in tasks:
            if task.get("started_at") == started_at:
                task.update(task_update)
                self._save_recent_tasks(tasks)
                return
        tasks.insert(0, task_update)
        self._save_recent_tasks(tasks)

    def show_recent_tasks(self):
        tasks = self._load_recent_tasks()
        if not tasks:
            self.append_log("\n最近任务\n暂无记录。")
            return

        lines = ["", "最近任务"]
        for index, task in enumerate(tasks[: self.MAX_RECENT_TASKS], 1):
            lines.append(
                f"{index}. {task.get('started_at', '-')}"
                f" [{task.get('status', '-')}] "
                f"{task.get('input_format', '')} -> {task.get('output_format', '')}"
            )
            lines.append(f"   输入: {task.get('input_dir', '-')}")
            lines.append(f"   输出: {task.get('output_dir', '-')}")
            if task.get("summary"):
                lines.append(f"   备注: {task['summary']}")
        self.append_log("\n".join(lines))

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
                background-color: #eaf2ff;
                border: 1px solid #c8daf1;
                border-radius: 8px;
                padding: 8px 10px;
                color: #163153;
                font-weight: bold;
            }

            QLabel#converterLogTitle {
                color: #163153;
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
                background-color: #f7fbff;
                border: 1px solid #d7e4f3;
                border-radius: 8px;
            }
            """
        )

        if self.current_selected_button:
            self.apply_selected_style(self.current_selected_button)
        for btn in self.conversion_buttons:
            if btn != self.current_selected_button:
                self.apply_hover_style(btn)
