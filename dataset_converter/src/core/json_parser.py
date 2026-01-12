import json
from pathlib import Path
from typing import List, Optional, Callable

from .base_parser import BaseParser, ImageAnnotation, BBox, Polygon


class JSONParser(BaseParser):
    format_name = "json"

    def parse_with_progress(self, input_dir: Path, 
                           progress_callback: Optional[Callable[[int, int, str], None]] = None,
                           status_callback: Optional[Callable[[str], None]] = None,
                           cancel_callback: Optional[Callable[[], bool]] = None) -> List[ImageAnnotation]:
        """带进度回调的JSON解析"""
        results: List[ImageAnnotation] = []
        
        # 检查标准目录结构
        images_dir = input_dir / "images"
        labels_dir = input_dir / "labels"
        
        if not images_dir.exists() or not labels_dir.exists():
            raise ValueError(f"数据集目录结构不正确。需要包含 'images' 和 'labels' 文件夹。\n当前目录: {input_dir}")
        
        # 收集所有JSON文件
        all_json_files = []
        subsets = ["train", "test", "val"]
        
        if status_callback:
            status_callback("扫描JSON数据集文件...")
        
        for subset in subsets:
            img_subset_dir = images_dir / subset
            label_subset_dir = labels_dir / subset
            
            if not img_subset_dir.exists() or not label_subset_dir.exists():
                continue
            
            # 首先尝试读取 annotations.json (批量格式)
            batch_fp = label_subset_dir / "annotations.json"
            if batch_fp.exists():
                all_json_files.append((batch_fp, img_subset_dir, True))  # True表示批量格式
            
            # 然后扫描目录中的所有 .json 文件 (单文件格式)
            json_files = list(label_subset_dir.glob("*.json"))
            for json_file in json_files:
                if json_file.name == "annotations.json":
                    continue  # 跳过批量文件
                all_json_files.append((json_file, img_subset_dir, False))  # False表示单文件格式
        
        total_files = len(all_json_files)
        if total_files == 0:
            return results
        
        # 处理文件
        for i, (json_file, img_subset_dir, is_batch) in enumerate(all_json_files):
            # 检查是否取消
            if cancel_callback and cancel_callback():
                break
            
            # 更新进度
            if progress_callback:
                progress_callback(i, total_files, f"解析 {json_file.name}")
            
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                
                if is_batch:
                    # 批量格式处理
                    images = data.get("images", [])
                    for im in images:
                        ann = self._parse_single_image(im, img_subset_dir)
                        if ann:
                            results.append(ann)
                else:
                    # 单文件格式处理
                    ann = self._parse_single_image(data, img_subset_dir)
                    if ann:
                        results.append(ann)
            except Exception:
                continue
        
        # 完成进度
        if progress_callback:
            progress_callback(total_files, total_files, "JSON解析完成")
        
        return results

    def parse(self, input_dir: Path) -> List[ImageAnnotation]:
        """原始解析方法，保持向后兼容"""
        return self.parse_with_progress(input_dir)

    def export_with_progress(self, annotations: List[ImageAnnotation], output_dir: Path,
                            progress_callback: Optional[Callable[[int, int, str], None]] = None,
                            status_callback: Optional[Callable[[str], None]] = None,
                            cancel_callback: Optional[Callable[[], bool]] = None) -> None:
        """带进度回调的JSON导出"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        total_annotations = len(annotations)
        
        if status_callback:
            status_callback("导出JSON格式...")
        
        for i, ann in enumerate(annotations):
            # 检查是否取消
            if cancel_callback and cancel_callback():
                break
            
            # 更新进度
            if progress_callback:
                progress_callback(i, total_annotations, f"导出 {ann.image_path.name}")
            
            annotations_list = []
            # 添加矩形框标注
            for b in ann.boxes:
                annotations_list.append({"label": b.label, "bbox": [b.xmin, b.ymin, b.xmax, b.ymax]})
            # 添加分割标注
            if ann.polygons:
                for p in ann.polygons:
                    annotations_list.append({"label": p.label, "polygon": p.points})
            
            entry = {
                "file_name": str(ann.image_path),
                "width": ann.width,
                "height": ann.height,
                "annotations": annotations_list,
            }
            out_name = Path(ann.image_path).with_suffix(".json").name or "annotation.json"
            (output_dir / out_name).write_text(
                json.dumps(entry, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        
        # 完成进度
        if progress_callback:
            progress_callback(total_annotations, total_annotations, "JSON导出完成")

    def export(self, annotations: List[ImageAnnotation], output_dir: Path) -> None:
        """导出为JSON格式"""
        self.export_with_progress(annotations, output_dir)
    
    def _parse_single_image(self, im_data: dict, img_dir: Path = None) -> ImageAnnotation:
        """解析单个图片的标注数据"""
        file_name = im_data.get("file_name")
        width = int(im_data.get("width", 0))
        height = int(im_data.get("height", 0))
        annos = im_data.get("annotations", [])
        boxes: List[BBox] = []
        polygons: List[Polygon] = []
        
        for a in annos:
            label = str(a.get("label", "")).strip()
            if "bbox" in a:
                bbox = a.get("bbox", [0, 0, 0, 0])
                xmin, ymin, xmax, ymax = map(int, bbox)
                boxes.append(BBox(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax, label=label))
            elif "polygon" in a:
                polygon = a.get("polygon", [])
                if len(polygon) >= 6 and len(polygon) % 2 == 0:
                    polygons.append(Polygon(points=polygon, label=label))
        
        # 构建完整的图片路径
        if file_name and img_dir:
            img_path = img_dir / file_name
            if not img_path.exists():
                # 如果指定的文件不存在，尝试查找同名文件
                stem = Path(file_name).stem
                img_path = self._find_image_in_dir(img_dir, stem)
                if img_path is None:
                    img_path = Path(file_name)  # 使用原始文件名
        else:
            img_path = Path(file_name) if file_name else Path("unknown.jpg")
        
        return ImageAnnotation(
            image_path=img_path,
            width=width, 
            height=height, 
            boxes=boxes, 
            polygons=polygons
        )
    
    def _find_image_in_dir(self, img_dir: Path, stem: str) -> Path:
        """在指定目录中查找同名图片文件"""
        exts = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
        for ext in exts:
            img_path = img_dir / f"{stem}{ext}"
            if img_path.exists():
                return img_path
        return None

    def export(self, annotations: List[ImageAnnotation], output_dir: Path) -> None:
        """导出为JSON格式"""
        self.export_with_progress(annotations, output_dir)