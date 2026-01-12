from pathlib import Path
from typing import List, Dict, Optional, Callable

from .base_parser import BaseParser, ImageAnnotation
from .yolo_parser import YOLOParser
from .yolo_seg_parser import YOLOSegParser
from .voc_parser import VOCParser
from .json_parser import JSONParser


PARSERS: Dict[str, BaseParser] = {
    "yolo": YOLOParser(),
    "yolo_seg": YOLOSegParser(),
    "voc": VOCParser(),
    "json": JSONParser(),
}


def convert(input_dir: Path, input_format: str, output_dir: Path, output_format: str, label_map: Optional[Dict[str, int]] = None) -> None:
    """原始转换函数，保持向后兼容"""
    convert_with_progress(input_dir, input_format, output_dir, output_format, label_map)


def convert_with_progress(input_dir: Path, input_format: str, output_dir: Path, output_format: str, 
                         label_map: Optional[Dict[str, int]] = None,
                         progress_callback: Optional[Callable[[int, int, str], None]] = None,
                         status_callback: Optional[Callable[[str], None]] = None,
                         cancel_callback: Optional[Callable[[], bool]] = None) -> None:
    """带进度回调的转换函数"""
    
    if input_format not in PARSERS:
        raise ValueError(f"Unsupported input format: {input_format}")
    if output_format not in PARSERS:
        raise ValueError(f"Unsupported output format: {output_format}")

    # 更新状态
    if status_callback:
        status_callback("初始化转换器...")
    
    # 先为解析器设置标签映射（如支持），以便在解析阶段将 id→label 反解
    parser = PARSERS[input_format]
    if hasattr(parser, "set_label_map") and label_map is not None:
        getattr(parser, "set_label_map")(label_map)

    # 解析阶段
    if status_callback:
        status_callback("解析输入数据...")
    
    # 使用带进度的解析方法
    if hasattr(parser, 'parse_with_progress'):
        annotations: List[ImageAnnotation] = parser.parse_with_progress(
            input_dir, 
            progress_callback=progress_callback,
            status_callback=status_callback,
            cancel_callback=cancel_callback
        )
    else:
        annotations: List[ImageAnnotation] = parser.parse(input_dir)

    # 检查是否被取消
    if cancel_callback and cancel_callback():
        return

    # 导出阶段
    if status_callback:
        status_callback("导出转换结果...")
    
    # 若导出器也支持标签映射（如 YOLO），同样传递以固定 label→id
    exporter = PARSERS[output_format]
    if hasattr(exporter, "set_label_map") and label_map is not None:
        getattr(exporter, "set_label_map")(label_map)
    
    # 使用带进度的导出方法
    if hasattr(exporter, 'export_with_progress'):
        exporter.export_with_progress(
            annotations, 
            output_dir,
            progress_callback=progress_callback,
            status_callback=status_callback,
            cancel_callback=cancel_callback
        )
    else:
        exporter.export(annotations, output_dir)
    
    if status_callback:
        status_callback("转换完成")