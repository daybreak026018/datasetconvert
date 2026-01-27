from .base_parser import ImageAnnotation, BBox
import copy
from pathlib import Path
from typing import List, Tuple
import random
import math
from PIL import Image, ImageEnhance, ImageFilter

class DataAugmentor:
    """数据增强器"""
    
    def __init__(self):
        self.augmentation_methods = {
            'brightness': self._adjust_brightness,
            'contrast': self._adjust_contrast,
            'saturation': self._adjust_saturation,
            'blur': self._apply_blur,
            'noise': self._add_noise,
            # flip_horizontal and rotate are handled specially to update labels
        }
    
    def augment_dataset(self, input_dir: Path, output_dir: Path, 
                       augmentations: List[str], multiplier: int = 2):
        """对数据集进行增强"""
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取所有图片文件
        image_files = list(input_dir.glob('*.jpg')) + list(input_dir.glob('*.png'))
        
        for img_file in image_files:
            # 复制原始文件
            self._copy_original(img_file, input_dir, output_dir)
            
            # 生成增强版本
            for i in range(multiplier - 1):
                self._create_augmented_version(img_file, input_dir, output_dir, 
                                             augmentations, i + 1)
    
    def _copy_original(self, img_file: Path, input_dir: Path, output_dir: Path):
        """复制原始文件"""
        # 复制图片
        img = Image.open(img_file)
        img.save(output_dir / img_file.name)
        
        # 复制标注文件
        txt_file = img_file.with_suffix('.txt')
        if txt_file.exists():
            content = txt_file.read_text(encoding='utf-8')
            (output_dir / txt_file.name).write_text(content, encoding='utf-8')
    
    def _create_augmented_version(self, img_file: Path, input_dir: Path, 
                                output_dir: Path, augmentations: List[str], version: int):
        """创建增强版本"""
        img = Image.open(img_file)
        
        # 读取标注
        txt_file = img_file.with_suffix('.txt')
        labels = []
        if txt_file.exists():
            labels = self._parse_yolo_labels(txt_file)

        # 随机选择增强方法
        selected_augs = random.sample(augmentations, 
                                    min(len(augmentations), random.randint(1, 3)))
        
        # 应用增强
        for aug in selected_augs:
            if aug == 'flip_horizontal':
                img, labels = self._apply_flip_horizontal(img, labels)
            elif aug == 'rotate':
                img, labels = self._apply_rotate(img, labels)
            elif aug in self.augmentation_methods:
                img = self.augmentation_methods[aug](img)
        
        # 保存增强后的图片
        stem = img_file.stem
        suffix = img_file.suffix
        new_name = f"{stem}_aug{version}{suffix}"
        img.save(output_dir / new_name)
        
        # 保存对应的标注文件
        if txt_file.exists():
            new_txt_name = f"{stem}_aug{version}.txt"
            self._save_yolo_labels(labels, output_dir / new_txt_name)

    def _parse_yolo_labels(self, txt_path: Path) -> List[List[float]]:
        """解析 YOLO 格式标签: class_id cx cy w h"""
        labels = []
        try:
            content = txt_path.read_text(encoding='utf-8')
            for line in content.splitlines():
                parts = line.strip().split()
                if len(parts) == 5:
                    # class_id, cx, cy, w, h
                    labels.append([float(x) for x in parts])
        except Exception:
            pass
        return labels

    def _save_yolo_labels(self, labels: List[List[float]], output_path: Path):
        """保存 YOLO 格式标签"""
        lines = []
        for l in labels:
            # class_id is int
            lines.append(f"{int(l[0])} {l[1]:.6f} {l[2]:.6f} {l[3]:.6f} {l[4]:.6f}")
        output_path.write_text("\n".join(lines), encoding='utf-8')

    def _apply_flip_horizontal(self, img: Image.Image, labels: List[List[float]]) -> Tuple[Image.Image, List[List[float]]]:
        """应用水平翻转并更新标签"""
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        new_labels = []
        for l in labels:
            # class_id, cx, cy, w, h
            cid, cx, cy, w, h = l
            new_cx = 1.0 - cx
            new_labels.append([cid, new_cx, cy, w, h])
        return img, new_labels

    def _apply_rotate(self, img: Image.Image, labels: List[List[float]]) -> Tuple[Image.Image, List[List[float]]]:
        """应用旋转并更新标签"""
        angle = random.uniform(-15, 15)
        w_old, h_old = img.size
        
        # 旋转图片
        img_new = img.rotate(angle, expand=True, fillcolor=(0, 0, 0))
        w_new, h_new = img_new.size
        
        # 转换角度为弧度 (逆时针为正)
        # PIL rotate angle is counter-clockwise degrees
        rad = -math.radians(angle) # 注意：数学坐标系旋转公式通常也是逆时针，但要确认坐标变换
        # Let's use standard rotation matrix
        # Center of rotation is (w_old/2, h_old/2)
        
        cx_old, cy_old = w_old / 2.0, h_old / 2.0
        cx_new, cy_new = w_new / 2.0, h_new / 2.0
        
        new_labels = []
        for l in labels:
            cid, cx, cy, w, h = l
            
            # Convert normalized center to absolute
            abs_cx = cx * w_old
            abs_cy = cy * h_old
            abs_w = w * w_old
            abs_h = h * h_old
            
            # Calculate 4 corners
            x1 = abs_cx - abs_w / 2
            y1 = abs_cy - abs_h / 2
            x2 = abs_cx + abs_w / 2
            y2 = abs_cy + abs_h / 2
            
            corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
            
            # Rotate corners
            rotated_corners = []
            for x, y in corners:
                # Shift to center
                dx = x - cx_old
                dy = y - cy_old
                
                # Apply rotation
                # x' = x cos θ - y sin θ
                # y' = x sin θ + y cos θ
                # Note: Y axis is down in images.
                # Standard rotation (counter-clockwise):
                # x' = x cos(-angle) - y sin(-angle) = x cos(angle) + y sin(angle)
                # y' = x sin(-angle) + y cos(-angle) = -x sin(angle) + y cos(angle)
                # Wait, let's verify PIL rotation direction.
                # PIL: positive angle is counter-clockwise.
                # Image coordinate system: Y is down.
                # If we rotate image CCW by 15 deg. A point at (1,0) goes to (cos 15, -sin 15).
                # So if Y is down, (1,0) -> (0.96, -0.25). Y decreases.
                
                # Using standard math with inverted Y:
                # It's safer to use the standard formula with the correct angle sign.
                # rad = math.radians(angle)
                # rx = dx * math.cos(rad) + dy * math.sin(rad)
                # ry = -dx * math.sin(rad) + dy * math.cos(rad)
                # Let's stick to simple geometry:
                # To rotate point (x,y) around origin by theta CCW:
                # x' = x cos theta - y sin theta
                # y' = x sin theta + y cos theta
                # This works for standard Cartesian (Y up).
                # For Image (Y down), rotating CCW means moving from +X towards -Y.
                # (1,0) -> (cos theta, -sin theta).
                # Formula:
                # x' = x cos theta + y sin theta
                # y' = -x sin theta + y cos theta
                
                rad_angle = math.radians(angle)
                cos_a = math.cos(rad_angle)
                sin_a = math.sin(rad_angle)
                
                rx = dx * cos_a + dy * sin_a
                ry = -dx * sin_a + dy * cos_a
                
                # Shift back to new center
                rotated_corners.append((rx + cx_new, ry + cy_new))
            
            # Calculate new BBox (AABB of rotated corners)
            xs = [p[0] for p in rotated_corners]
            ys = [p[1] for p in rotated_corners]
            
            min_x = max(0, min(xs))
            min_y = max(0, min(ys))
            max_x = min(w_new, max(xs))
            max_y = min(h_new, max(ys))
            
            # New normalized coordinates
            new_abs_w = max_x - min_x
            new_abs_h = max_y - min_y
            new_abs_cx = min_x + new_abs_w / 2.0
            new_abs_cy = min_y + new_abs_h / 2.0
            
            if new_abs_w > 0 and new_abs_h > 0:
                new_labels.append([
                    cid,
                    new_abs_cx / w_new,
                    new_abs_cy / h_new,
                    new_abs_w / w_new,
                    new_abs_h / h_new
                ])
                
        return img_new, new_labels

    def _adjust_brightness(self, img: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Brightness(img)
        factor = random.uniform(0.7, 1.3)
        return enhancer.enhance(factor)
    
    def _adjust_contrast(self, img: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Contrast(img)
        factor = random.uniform(0.8, 1.2)
        return enhancer.enhance(factor)
    
    def _adjust_saturation(self, img: Image.Image) -> Image.Image:
        enhancer = ImageEnhance.Color(img)
        factor = random.uniform(0.8, 1.2)
        return enhancer.enhance(factor)
    
    def _apply_blur(self, img: Image.Image) -> Image.Image:
        radius = random.uniform(0.5, 2.0)
        return img.filter(ImageFilter.GaussianBlur(radius=radius))
    
    def _add_noise(self, img: Image.Image) -> Image.Image:
        # 简单的噪声添加（实际实现可能需要numpy）
        return img
    
    def _flip_horizontal(self, img: Image.Image) -> Image.Image:
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    
    def _rotate_image(self, img: Image.Image) -> Image.Image:
        angle = random.uniform(-15, 15)
        return img.rotate(angle, expand=True, fillcolor=(0, 0, 0))

    def apply_flip_to_annotation(self, img: Image.Image, annotation: ImageAnnotation) -> Tuple[Image.Image, ImageAnnotation]:
        """应用水平翻转并更新 ImageAnnotation"""
        new_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        new_ann = copy.deepcopy(annotation)
        w = new_ann.width
        
        for box in new_ann.boxes:
            old_xmin = box.xmin
            old_xmax = box.xmax
            box.xmin = w - old_xmax
            box.xmax = w - old_xmin
            # Ensure xmin < xmax just in case
            if box.xmin > box.xmax:
                box.xmin, box.xmax = box.xmax, box.xmin
                
        return new_img, new_ann

    def apply_rotate_to_annotation(self, img: Image.Image, annotation: ImageAnnotation) -> Tuple[Image.Image, ImageAnnotation]:
        """应用旋转并更新 ImageAnnotation"""
        angle = random.uniform(-15, 15)
        new_img = img.rotate(angle, expand=True, fillcolor=(0, 0, 0))
        new_w, new_h = new_img.size
        
        new_ann = copy.deepcopy(annotation)
        new_ann.width = new_w
        new_ann.height = new_h
        
        # Center of rotation
        cx_old = annotation.width / 2.0
        cy_old = annotation.height / 2.0
        new_cx = new_w / 2.0
        new_cy = new_h / 2.0
        
        rad_angle = math.radians(angle)
        cos_a = math.cos(rad_angle)
        sin_a = math.sin(rad_angle)
        
        for box in new_ann.boxes:
            # Get corners
            corners = [
                (box.xmin, box.ymin),
                (box.xmax, box.ymin),
                (box.xmax, box.ymax),
                (box.xmin, box.ymax)
            ]
            
            new_corners = []
            for x, y in corners:
                # Shift to center
                dx = x - cx_old
                dy = y - cy_old
                
                # Rotate (CCW in Y-down)
                # x' = x cos a + y sin a
                # y' = -x sin a + y cos a
                rx = dx * cos_a + dy * sin_a
                ry = -dx * sin_a + dy * cos_a
                
                # Shift back
                new_corners.append((rx + new_cx, ry + new_cy))
            
            # AABB
            xs = [p[0] for p in new_corners]
            ys = [p[1] for p in new_corners]
            
            box.xmin = int(max(0, min(xs)))
            box.ymin = int(max(0, min(ys)))
            box.xmax = int(min(new_w, max(xs)))
            box.ymax = int(min(new_h, max(ys)))
            
        return new_img, new_ann

    def apply_flip_vertical_to_annotation(self, img: Image.Image, annotation: ImageAnnotation) -> Tuple[Image.Image, ImageAnnotation]:
        """应用垂直翻转并更新 ImageAnnotation"""
        new_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        new_ann = copy.deepcopy(annotation)
        h = new_ann.height
        
        for box in new_ann.boxes:
            old_ymin = box.ymin
            old_ymax = box.ymax
            box.ymin = h - old_ymax
            box.ymax = h - old_ymin
            if box.ymin > box.ymax:
                box.ymin, box.ymax = box.ymax, box.ymin
                
        return new_img, new_ann

    def apply_augmentation(self, img: Image.Image, annotation: ImageAnnotation, aug_name: str) -> Tuple[Image.Image, ImageAnnotation]:
        """统一的数据增强接口"""
        if aug_name == 'flip_horizontal':
            return self.apply_flip_to_annotation(img, annotation)
        elif aug_name == 'flip_vertical':
            return self.apply_flip_vertical_to_annotation(img, annotation)
        elif aug_name == 'rotate':
            return self.apply_rotate_to_annotation(img, annotation)
        
        # 对于不改变几何形状的增强，只处理图片
        if aug_name in self.augmentation_methods:
            new_img = self.augmentation_methods[aug_name](img)
            return new_img, copy.deepcopy(annotation)
            
        # 未知的增强，返回原图
        return img, copy.deepcopy(annotation)