from pathlib import Path

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QGroupBox,
    QGridLayout,
)
from PyQt5.QtCore import Qt

from ..core.converter import convert
from ..utils.logger import get_logger
from ..utils.label_utils import parse_label_map_txt


class ConverterPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.logger = get_logger()
        
        # 存储所有转换按钮的引用
        self.conversion_buttons = []
        self.current_selected_button = None

        main_layout = QVBoxLayout(self)

        # 输入输出路径 - 固定在顶部
        path_group = QWidget()
        path_layout = QVBoxLayout(path_group)
        
        # 输入目录
        input_layout = QHBoxLayout()
        self.input_label = QLabel("输入目录: 未选择")
        self.input_label.setWordWrap(True)
        btn_in = QPushButton("选择输入目录")
        btn_in.setMaximumWidth(120)
        input_layout.addWidget(self.input_label, 1)
        input_layout.addWidget(btn_in)
        
        # 输出目录
        output_layout = QHBoxLayout()
        self.output_label = QLabel("输出目录: 未选择")
        self.output_label.setWordWrap(True)
        btn_out = QPushButton("选择输出目录")
        btn_out.setMaximumWidth(120)
        output_layout.addWidget(self.output_label, 1)
        output_layout.addWidget(btn_out)
        
        btn_in.clicked.connect(self.choose_input)
        btn_out.clicked.connect(self.choose_output)
        
        path_layout.addLayout(input_layout)
        path_layout.addLayout(output_layout)
        main_layout.addWidget(path_group)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(2)  # 总是显示垂直滚动条
        scroll_area.setHorizontalScrollBarPolicy(1)  # 根据需要显示水平滚动条
        
        # 创建滚动内容容器
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 当前格式显示
        self.label_fmt = QLabel("当前格式: YOLO检测 → VOC")
        self.label_fmt.setWordWrap(True)
        self.label_fmt.setProperty("labelType", "status")
        scroll_layout.addWidget(self.label_fmt)
        
        # 基础格式转换组
        basic_group = self.create_conversion_group("基础格式转换", [
            ("YOLO检测 → VOC", "yolo", "voc"),
            ("VOC → YOLO检测", "voc", "yolo"),
            ("YOLO检测 → JSON", "yolo", "json"),
            ("JSON → YOLO检测", "json", "yolo"),
            ("JSON → VOC", "json", "voc"),
        ])
        scroll_layout.addWidget(basic_group)
        
        # 分割格式转换组
        seg_group = self.create_conversion_group("分割格式转换", [
            ("YOLO分割 → JSON", "yolo_seg", "json"),
            ("JSON → YOLO分割", "json", "yolo_seg"),
            ("YOLO分割 → YOLO检测", "yolo_seg", "yolo"),
        ])
        scroll_layout.addWidget(seg_group)

        # 工具按钮组
        tools_group = self.create_tools_group()
        scroll_layout.addWidget(tools_group)
        
        # 设置滚动内容
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)

        # 日志输出 - 固定在底部
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setMaximumHeight(150)  # 限制高度
        
        log_label = QLabel("日志输出:")
        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log_view)

        self.input_dir = None
        self.output_dir = None
        self.input_fmt = "yolo"
        self.output_fmt = "voc"
        self.label_map = {}
        
        # 设置默认选中的按钮（YOLO检测 → VOC）
        self.set_formats("yolo", "voc", auto_select_button=True)
    
    def create_conversion_group(self, title, conversions):
        """创建转换按钮组"""
        group = QGroupBox(title)
        layout = QGridLayout(group)
        
        # 每行最多2个按钮，防止超出窗口
        for i, (text, inp_fmt, out_fmt) in enumerate(conversions):
            btn = QPushButton(text)
            btn.setMaximumWidth(200)  # 限制按钮宽度
            btn.setCheckable(True)  # 设置按钮可选中
            btn.clicked.connect(lambda checked, i=inp_fmt, o=out_fmt, b=btn: self.set_formats(i, o, b))
            
            # 存储按钮引用和对应的格式信息
            btn.input_format = inp_fmt
            btn.output_format = out_fmt
            self.conversion_buttons.append(btn)
            
            row = i // 2
            col = i % 2
            layout.addWidget(btn, row, col)
        
        return group
    
    def create_tools_group(self):
        """创建工具按钮组"""
        group = QGroupBox("工具")
        layout = QVBoxLayout(group)
        
        # 标签字典按钮
        btn_label_map = QPushButton("加载标签字典")
        btn_label_map.setMaximumWidth(200)
        btn_label_map.setProperty("buttonType", "warning")
        btn_label_map.clicked.connect(self.on_load_label_map)
        layout.addWidget(btn_label_map)
        
        # 转换按钮
        btn_convert = QPushButton("开始转换")
        btn_convert.setMaximumWidth(200)
        btn_convert.setProperty("buttonType", "success")
        btn_convert.clicked.connect(self.on_convert)
        layout.addWidget(btn_convert)
        
        return group

    def choose_input(self):
        d = QFileDialog.getExistingDirectory(self, "选择输入目录", str(Path.cwd()))
        if d:
            self.input_dir = Path(d)
            self.input_label.setText(f"输入目录: {d}")

    def choose_output(self):
        d = QFileDialog.getExistingDirectory(self, "选择输出目录", str(Path.cwd()))
        if d:
            self.output_dir = Path(d)
            self.output_label.setText(f"输出目录: {d}")

    def set_formats(self, inp: str, outp: str, selected_button=None, auto_select_button=False):
        """设置转换格式并更新按钮高亮状态"""
        self.input_fmt = inp
        self.output_fmt = outp
        
        # 格式名称映射
        format_names = {
            "yolo": "YOLO检测",
            "yolo_seg": "YOLO分割", 
            "voc": "VOC",
            "json": "JSON"
        }
        
        inp_name = format_names.get(inp, inp.upper())
        outp_name = format_names.get(outp, outp.upper())
        
        # 使用更醒目的格式显示
        format_text = f"✓ 当前选择: {inp_name} → {outp_name}"
        self.label_fmt.setText(format_text)
        
        # 更新按钮选中状态
        self.update_button_selection(inp, outp, selected_button, auto_select_button)
    
    def update_button_selection(self, inp_fmt, out_fmt, selected_button=None, auto_select=False):
        """更新按钮选中状态和高亮效果"""
        # 清除所有按钮的选中状态
        for btn in self.conversion_buttons:
            btn.setChecked(False)
            btn.setStyleSheet("")  # 清除自定义样式
        
        # 设置当前选中的按钮
        target_button = selected_button
        
        # 如果没有指定按钮，自动查找匹配的按钮
        if not target_button or auto_select:
            for btn in self.conversion_buttons:
                if (hasattr(btn, 'input_format') and hasattr(btn, 'output_format') and
                    btn.input_format == inp_fmt and btn.output_format == out_fmt):
                    target_button = btn
                    break
        
        # 应用选中状态和高亮样式
        if target_button:
            target_button.setChecked(True)
            self.apply_selected_style(target_button)
            self.current_selected_button = target_button
    
    def apply_selected_style(self, button):
        """应用选中按钮的高亮样式"""
        # 获取当前主题的颜色
        from .theme_manager import theme_manager
        current_theme = theme_manager.get_current_theme()
        
        if current_theme == "dark":
            # 深色主题的高亮样式
            selected_style = """
                QPushButton:checked {
                    background-color: #0078d4;
                    border: 2px solid #106ebe;
                    color: white;
                    font-weight: bold;
                    border-radius: 4px;
                }
                QPushButton:checked:hover {
                    background-color: #106ebe;
                    border: 2px solid #005a9e;
                }
                QPushButton:hover {
                    background-color: #404040;
                    border: 1px solid #606060;
                }
            """
        elif current_theme == "blue":
            # 蓝色主题的高亮样式
            selected_style = """
                QPushButton:checked {
                    background-color: #2196F3;
                    border: 2px solid #1976D2;
                    color: white;
                    font-weight: bold;
                    border-radius: 4px;
                }
                QPushButton:checked:hover {
                    background-color: #1976D2;
                    border: 2px solid #1565C0;
                }
                QPushButton:hover {
                    background-color: #E3F2FD;
                    border: 1px solid #2196F3;
                }
            """
        elif current_theme == "green":
            # 绿色主题的高亮样式
            selected_style = """
                QPushButton:checked {
                    background-color: #4CAF50;
                    border: 2px solid #388E3C;
                    color: white;
                    font-weight: bold;
                    border-radius: 4px;
                }
                QPushButton:checked:hover {
                    background-color: #388E3C;
                    border: 2px solid #2E7D32;
                }
                QPushButton:hover {
                    background-color: #E8F5E8;
                    border: 1px solid #4CAF50;
                }
            """
        else:
            # 浅色主题的高亮样式
            selected_style = """
                QPushButton:checked {
                    background-color: #0078d4;
                    border: 2px solid #106ebe;
                    color: white;
                    font-weight: bold;
                    border-radius: 4px;
                }
                QPushButton:checked:hover {
                    background-color: #106ebe;
                    border: 2px solid #005a9e;
                }
                QPushButton:hover {
                    background-color: #f0f0f0;
                    border: 1px solid #0078d4;
                }
            """
        
        button.setStyleSheet(selected_style)
        
        # 为所有其他按钮应用悬停效果
        for btn in self.conversion_buttons:
            if btn != button:
                self.apply_hover_style(btn)

    def append_log(self, msg: str):
        self.log_view.append(msg)
        self.logger.info(msg)

    def on_convert(self):
        if not self.input_dir or not self.output_dir:
            QMessageBox.warning(self, "提示", "请先选择输入与输出目录")
            return
            
        # 使用进度对话框执行转换
        from ..utils.worker_thread import run_with_progress
        
        format_names = {
            "yolo": "YOLO检测",
            "yolo_seg": "YOLO分割", 
            "voc": "VOC",
            "json": "JSON"
        }
        inp_name = format_names.get(self.input_fmt, self.input_fmt)
        outp_name = format_names.get(self.output_fmt, self.output_fmt)
        
        self.append_log(f"开始转换: {inp_name} → {outp_name}")
        
        # 启动带进度条的转换任务
        title = f"数据集转换: {inp_name} → {outp_name}"
        run_with_progress(
            self, 
            title, 
            self._convert_with_progress,
            self.input_dir,
            self.input_fmt,
            self.output_dir, 
            self.output_fmt,
            self.label_map
        )
    
    def _convert_with_progress(self, input_dir, input_fmt, output_dir, output_fmt, label_map, 
                              progress_callback=None, status_callback=None, cancel_callback=None):
        """带进度回调的转换函数"""
        try:
            if output_fmt == "json":
                if status_callback:
                    status_callback("导出说明：将为每张图片生成一个独立的 JSON 文件")
            elif input_fmt == "yolo_seg":
                if status_callback:
                    status_callback("输入说明：YOLO分割格式支持矩形框和多边形混合标注")
            elif output_fmt == "yolo_seg":
                if status_callback:
                    status_callback("输出说明：YOLO分割格式将保留原有的矩形框和多边形标注")
            
            # 执行转换（使用带进度回调的转换函数）
            from ..core.converter import convert_with_progress
            convert_with_progress(
                input_dir, input_fmt, output_dir, output_fmt, 
                label_map=label_map,
                progress_callback=progress_callback,
                status_callback=status_callback,
                cancel_callback=cancel_callback
            )
            
            return "转换完成"
            
        except Exception as e:
            raise e
    
    def on_task_finished(self, result):
        """转换任务完成回调"""
        self.append_log("转换完成")
        QMessageBox.information(self, "完成", "转换完成！")

    def on_load_label_map(self):
        fp, _ = QFileDialog.getOpenFileName(self, "选择标签字典 txt", str(Path.cwd()), "Text Files (*.txt)")
        if not fp:
            return
        try:
            self.label_map = parse_label_map_txt(Path(fp))
            if not self.label_map:
                QMessageBox.warning(self, "提示", "未解析到有效标签映射")
                return
            self.append_log(f"已加载标签映射：{len(self.label_map)}项（将在解析与导出阶段生效）")
            self.label_fmt.setText(self.label_fmt.text() + "（已加载标签映射）")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"解析失败: {e}")
    
    def apply_hover_style(self, button):
        """为未选中的按钮应用悬停样式"""
        from .theme_manager import theme_manager
        current_theme = theme_manager.get_current_theme()
        
        if current_theme == "dark":
            hover_style = """
                QPushButton:hover {
                    background-color: #404040;
                    border: 1px solid #606060;
                    border-radius: 4px;
                }
            """
        elif current_theme == "blue":
            hover_style = """
                QPushButton:hover {
                    background-color: #E3F2FD;
                    border: 1px solid #2196F3;
                    border-radius: 4px;
                }
            """
        elif current_theme == "green":
            hover_style = """
                QPushButton:hover {
                    background-color: #E8F5E8;
                    border: 1px solid #4CAF50;
                    border-radius: 4px;
                }
            """
        else:
            hover_style = """
                QPushButton:hover {
                    background-color: #f0f0f0;
                    border: 1px solid #0078d4;
                    border-radius: 4px;
                }
            """
        
        button.setStyleSheet(hover_style)

    def apply_theme(self):
        """应用主题时更新选中按钮的样式"""
        if self.current_selected_button:
            self.apply_selected_style(self.current_selected_button)
        
        # 为所有未选中的按钮应用悬停样式
        for btn in self.conversion_buttons:
            if btn != self.current_selected_button:
                self.apply_hover_style(btn)