from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable


@dataclass
class BBox:
    xmin: int
    ymin: int
    xmax: int
    ymax: int
    label: str


@dataclass
class Polygon:
    points: List[float]  # [x1, y1, x2, y2, ..., xn, yn] 归一化坐标
    label: str


@dataclass
class ImageAnnotation:
    image_path: Path
    width: int
    height: int
    boxes: List[BBox]
    polygons: Optional[List[Polygon]] = None  # 分割标注


class BaseParser:
    """统一解析器接口：解析目录为标准注释结构、并可导出。"""

    format_name: str = "base"

    def parse(self, input_dir: Path) -> List[ImageAnnotation]:
        raise NotImplementedError
    
    def parse_with_progress(self, input_dir: Path, 
                           progress_callback: Optional[Callable[[int, int, str], None]] = None,
                           status_callback: Optional[Callable[[str], None]] = None,
                           cancel_callback: Optional[Callable[[], bool]] = None) -> List[ImageAnnotation]:
        """带进度回调的解析方法，子类可以重写以提供进度支持"""
        return self.parse(input_dir)

    def export(self, annotations: List[ImageAnnotation], output_dir: Path) -> None:
        raise NotImplementedError
    
    def export_with_progress(self, annotations: List[ImageAnnotation], output_dir: Path,
                            progress_callback: Optional[Callable[[int, int, str], None]] = None,
                            status_callback: Optional[Callable[[str], None]] = None,
                            cancel_callback: Optional[Callable[[], bool]] = None) -> None:
        """带进度回调的导出方法，子类可以重写以提供进度支持"""
        self.export(annotations, output_dir)