from pathlib import Path
from typing import List, Optional, Callable

from .base_parser import BaseParser, ImageAnnotation
from ..utils.xml_utils import read_xml


class VOCParser(BaseParser):
    format_name = "voc"

    def parse_with_progress(self, input_dir: Path, 
                           progress_callback: Optional[Callable[[int, int, str], None]] = None,
                           status_callback: Optional[Callable[[str], None]] = None,
                           cancel_callback: Optional[Callable[[], bool]] = None) -> List[ImageAnnotation]:
        """带进度回调的VOC解析"""
        results: List[ImageAnnotation] = []
        
        # 检查标准目录结构
        images_dir = input_dir / "images"
        labels_dir = input_dir / "labels"
        
        if not images_dir.exists() or not labels_dir.exists():
            raise ValueError(f"数据集目录结构不正确。需要包含 'images' 和 'labels' 文件夹。\n当前目录: {input_dir}")
        
        # 收集所有XML文件
        all_xml_files = []
        subsets = ["train", "test", "val"]
        
        if status_callback:
            status_callback("扫描VOC数据集文件...")
        
        for subset in subsets:
            img_subset_dir = images_dir / subset
            label_subset_dir = labels_dir / subset
            
            if not img_subset_dir.exists() or not label_subset_dir.exists():
                continue
            
            xml_files = list(label_subset_dir.glob("*.xml"))
            for xml_file in xml_files:
                all_xml_files.append((xml_file, img_subset_dir))
        
        total_files = len(all_xml_files)
        if total_files == 0:
            return results
        
        # 处理文件
        for i, (xml_file, img_subset_dir) in enumerate(all_xml_files):
            # 检查是否取消
            if cancel_callback and cancel_callback():
                break
            
            # 更新进度
            if progress_callback:
                progress_callback(i, total_files, f"解析 {xml_file.name}")
            
            stem = xml_file.stem
            
            # 在对应的图片目录中查找同名图片
            img_file = self._find_image_in_dir(img_subset_dir, stem)
            if img_file is None:
                continue
            
            try:
                # 解析XML文件 (这里需要实现XML解析逻辑)
                annotation_data = read_xml(xml_file)
                
                # 获取图片尺寸
                try:
                    from PIL import Image
                    with Image.open(img_file) as im:
                        width, height = im.size
                except Exception:
                    width, height = 0, 0
                
                # 这里应该根据XML内容创建BBox对象
                # 暂时返回空的标注作为占位符
                boxes = []
                
                results.append(ImageAnnotation(
                    image_path=img_file, 
                    width=width, 
                    height=height, 
                    boxes=boxes,
                    polygons=None
                ))
                
            except Exception:
                # XML解析失败，跳过
                continue
        
        # 完成进度
        if progress_callback:
            progress_callback(total_files, total_files, "VOC解析完成")
        
        return results

    def parse(self, input_dir: Path) -> List[ImageAnnotation]:
        """原始解析方法，保持向后兼容"""
        return self.parse_with_progress(input_dir)

    def export_with_progress(self, annotations: List[ImageAnnotation], output_dir: Path,
                            progress_callback: Optional[Callable[[int, int, str], None]] = None,
                            status_callback: Optional[Callable[[str], None]] = None,
                            cancel_callback: Optional[Callable[[], bool]] = None) -> None:
        """带进度回调的VOC导出"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        total_annotations = len(annotations)
        
        if status_callback:
            status_callback("导出VOC格式...")
        
        for i, ann in enumerate(annotations):
            # 检查是否取消
            if cancel_callback and cancel_callback():
                break
            
            # 更新进度
            if progress_callback:
                progress_callback(i, total_annotations, f"导出 {ann.image_path.name}")
            
            # 占位：写出 VOC XML（注意：VOC格式不支持分割标注，只导出矩形框）
            for _ in ann.boxes:
                pass
        
        # 完成进度
        if progress_callback:
            progress_callback(total_annotations, total_annotations, "VOC导出完成")

    def export(self, annotations: List[ImageAnnotation], output_dir: Path) -> None:
        """导出为VOC格式"""
        self.export_with_progress(annotations, output_dir)
    
    def _find_image_in_dir(self, img_dir: Path, stem: str) -> Path:
        """在指定目录中查找同名图片文件"""
        exts = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
        for ext in exts:
            img_path = img_dir / f"{stem}{ext}"
            if img_path.exists():
                return img_path
        return None

    def export(self, annotations: List[ImageAnnotation], output_dir: Path) -> None:
        """导出为VOC格式"""
        self.export_with_progress(annotations, output_dir)