"""
批量图片处理工具
支持调整尺寸、格式转换、压缩、增强等操作
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from PIL import Image, ImageEnhance, ImageFilter
import json


class ProcessingOperation(Enum):
    """处理操作类型"""
    RESIZE = "resize"
    CROP = "crop"
    ROTATE = "rotate"
    FLIP = "flip"
    BRIGHTNESS = "brightness"
    CONTRAST = "contrast"
    SATURATION = "saturation"
    BLUR = "blur"
    SHARPEN = "sharpen"
    GRAYSCALE = "grayscale"
    FORMAT_CONVERT = "format_convert"
    COMPRESS = "compress"
    NORMALIZE = "normalize"


@dataclass
class ProcessingConfig:
    """处理配置"""
    operation: ProcessingOperation
    parameters: Dict
    enabled: bool = True


class BatchImageProcessor:
    """批量图片处理器"""
    
    def __init__(self):
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        self.processing_stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0
        }
    
    def process_images(self, input_dir: Path, output_dir: Path, 
                      configs: List[ProcessingConfig],
                      progress_callback: Optional[Callable] = None,
                      status_callback: Optional[Callable] = None) -> Dict:
        """批量处理图片"""
        
        # 重置统计
        self.processing_stats = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0
        }
        
        # 创建输出目录
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 获取所有图片文件
        image_files = []
        for ext in self.supported_formats:
            image_files.extend(input_dir.rglob(f"*{ext}"))
            image_files.extend(input_dir.rglob(f"*{ext.upper()}"))
        
        total_files = len(image_files)
        
        if status_callback:
            status_callback(f"找到 {total_files} 个图片文件")
        
        # 处理每个图片
        for i, image_path in enumerate(image_files):
            try:
                if progress_callback:
                    progress_callback(i, total_files, f"处理 {image_path.name}")
                
                # 处理单个图片
                success = self._process_single_image(image_path, output_dir, configs)
                
                if success:
                    self.processing_stats['successful'] += 1
                else:
                    self.processing_stats['failed'] += 1
                
                self.processing_stats['total_processed'] += 1
                
            except Exception as e:
                print(f"处理图片 {image_path} 时出错: {e}")
                self.processing_stats['failed'] += 1
                self.processing_stats['total_processed'] += 1
        
        # 生成处理报告
        report = self._generate_processing_report(input_dir, output_dir, configs)
        
        return {
            'stats': self.processing_stats,
            'report': report,
            'output_dir': output_dir
        }
    
    def _process_single_image(self, image_path: Path, output_dir: Path, 
                            configs: List[ProcessingConfig]) -> bool:
        """处理单个图片"""
        try:
            # 读取图片
            image = Image.open(image_path)
            
            # 保持相对路径结构
            relative_path = image_path.relative_to(image_path.parents[len(image_path.parents)-1])
            output_path = output_dir / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 应用所有启用的处理操作
            processed_image = image.copy()
            
            for config in configs:
                if config.enabled:
                    processed_image = self._apply_operation(processed_image, config)
            
            # 保存处理后的图片
            # 检查是否需要格式转换
            output_format = None
            for config in configs:
                if config.operation == ProcessingOperation.FORMAT_CONVERT and config.enabled:
                    output_format = config.parameters.get('format', 'JPEG')
                    # 更新输出路径的扩展名
                    new_ext = self._get_extension_for_format(output_format)
                    output_path = output_path.with_suffix(new_ext)
                    break
            
            # 保存图片
            if output_format:
                if output_format.upper() == 'JPEG' and processed_image.mode in ('RGBA', 'LA'):
                    # JPEG不支持透明度，转换为RGB
                    background = Image.new('RGB', processed_image.size, (255, 255, 255))
                    background.paste(processed_image, mask=processed_image.split()[-1] if processed_image.mode == 'RGBA' else None)
                    processed_image = background
                
                processed_image.save(output_path, format=output_format)
            else:
                processed_image.save(output_path)
            
            return True
            
        except Exception as e:
            print(f"处理图片 {image_path} 失败: {e}")
            return False
    
    def _apply_operation(self, image: Image.Image, config: ProcessingConfig) -> Image.Image:
        """应用单个处理操作"""
        
        if config.operation == ProcessingOperation.RESIZE:
            return self._resize_image(image, config.parameters)
        
        elif config.operation == ProcessingOperation.CROP:
            return self._crop_image(image, config.parameters)
        
        elif config.operation == ProcessingOperation.ROTATE:
            return self._rotate_image(image, config.parameters)
        
        elif config.operation == ProcessingOperation.FLIP:
            return self._flip_image(image, config.parameters)
        
        elif config.operation == ProcessingOperation.BRIGHTNESS:
            return self._adjust_brightness(image, config.parameters)
        
        elif config.operation == ProcessingOperation.CONTRAST:
            return self._adjust_contrast(image, config.parameters)
        
        elif config.operation == ProcessingOperation.SATURATION:
            return self._adjust_saturation(image, config.parameters)
        
        elif config.operation == ProcessingOperation.BLUR:
            return self._blur_image(image, config.parameters)
        
        elif config.operation == ProcessingOperation.SHARPEN:
            return self._sharpen_image(image, config.parameters)
        
        elif config.operation == ProcessingOperation.GRAYSCALE:
            return self._convert_grayscale(image, config.parameters)
        
        elif config.operation == ProcessingOperation.NORMALIZE:
            return self._normalize_image(image, config.parameters)
        
        else:
            return image
    
    def _resize_image(self, image: Image.Image, params: Dict) -> Image.Image:
        """调整图片尺寸"""
        width = params.get('width')
        height = params.get('height')
        mode = params.get('mode', 'exact')  # exact, keep_ratio, max_size
        
        if mode == 'exact':
            return image.resize((width, height), Image.Resampling.LANCZOS)
        
        elif mode == 'keep_ratio':
            # 保持长宽比
            image.thumbnail((width, height), Image.Resampling.LANCZOS)
            return image
        
        elif mode == 'max_size':
            # 限制最大尺寸
            w, h = image.size
            if w > width or h > height:
                image.thumbnail((width, height), Image.Resampling.LANCZOS)
            return image
        
        return image
    
    def _crop_image(self, image: Image.Image, params: Dict) -> Image.Image:
        """裁剪图片"""
        x = params.get('x', 0)
        y = params.get('y', 0)
        width = params.get('width', image.width)
        height = params.get('height', image.height)
        
        # 确保裁剪区域在图片范围内
        x = max(0, min(x, image.width))
        y = max(0, min(y, image.height))
        width = min(width, image.width - x)
        height = min(height, image.height - y)
        
        return image.crop((x, y, x + width, y + height))
    
    def _rotate_image(self, image: Image.Image, params: Dict) -> Image.Image:
        """旋转图片"""
        angle = params.get('angle', 0)
        expand = params.get('expand', True)
        
        return image.rotate(angle, expand=expand, fillcolor=(255, 255, 255))
    
    def _flip_image(self, image: Image.Image, params: Dict) -> Image.Image:
        """翻转图片"""
        direction = params.get('direction', 'horizontal')  # horizontal, vertical
        
        if direction == 'horizontal':
            return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        elif direction == 'vertical':
            return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        
        return image
    
    def _adjust_brightness(self, image: Image.Image, params: Dict) -> Image.Image:
        """调整亮度"""
        factor = params.get('factor', 1.0)  # 1.0 = 原始亮度
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    def _adjust_contrast(self, image: Image.Image, params: Dict) -> Image.Image:
        """调整对比度"""
        factor = params.get('factor', 1.0)  # 1.0 = 原始对比度
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    def _adjust_saturation(self, image: Image.Image, params: Dict) -> Image.Image:
        """调整饱和度"""
        factor = params.get('factor', 1.0)  # 1.0 = 原始饱和度
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(factor)
    
    def _blur_image(self, image: Image.Image, params: Dict) -> Image.Image:
        """模糊图片"""
        radius = params.get('radius', 1.0)
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    def _sharpen_image(self, image: Image.Image, params: Dict) -> Image.Image:
        """锐化图片"""
        factor = params.get('factor', 1.0)
        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(1.0 + factor)
    
    def _convert_grayscale(self, image: Image.Image, params: Dict) -> Image.Image:
        """转换为灰度图"""
        return image.convert('L')
    
    def _normalize_image(self, image: Image.Image, params: Dict) -> Image.Image:
        """标准化图片"""
        # 转换为numpy数组进行处理
        img_array = np.array(image)
        
        # 标准化到0-255范围
        img_array = img_array.astype(np.float32)
        img_array = (img_array - img_array.min()) / (img_array.max() - img_array.min()) * 255
        img_array = img_array.astype(np.uint8)
        
        return Image.fromarray(img_array)
    
    def _get_extension_for_format(self, format_name: str) -> str:
        """获取格式对应的文件扩展名"""
        format_map = {
            'JPEG': '.jpg',
            'PNG': '.png',
            'BMP': '.bmp',
            'TIFF': '.tiff',
            'WEBP': '.webp'
        }
        return format_map.get(format_name.upper(), '.jpg')
    
    def _generate_processing_report(self, input_dir: Path, output_dir: Path, 
                                  configs: List[ProcessingConfig]) -> str:
        """生成处理报告"""
        report_lines = []
        
        report_lines.append("# 批量图片处理报告")
        report_lines.append(f"输入目录: {input_dir}")
        report_lines.append(f"输出目录: {output_dir}")
        report_lines.append("")
        
        # 处理统计
        stats = self.processing_stats
        report_lines.append("## 处理统计")
        report_lines.append(f"- 总计处理: {stats['total_processed']} 个文件")
        report_lines.append(f"- 成功: {stats['successful']} 个")
        report_lines.append(f"- 失败: {stats['failed']} 个")
        report_lines.append(f"- 跳过: {stats['skipped']} 个")
        
        if stats['total_processed'] > 0:
            success_rate = (stats['successful'] / stats['total_processed']) * 100
            report_lines.append(f"- 成功率: {success_rate:.1f}%")
        
        report_lines.append("")
        
        # 处理操作
        report_lines.append("## 应用的处理操作")
        for i, config in enumerate(configs, 1):
            if config.enabled:
                op_name = config.operation.value.replace('_', ' ').title()
                report_lines.append(f"{i}. {op_name}")
                
                # 显示参数
                for key, value in config.parameters.items():
                    report_lines.append(f"   - {key}: {value}")
        
        return '\n'.join(report_lines)
    
    def create_preset_configs(self, preset_name: str) -> List[ProcessingConfig]:
        """创建预设配置"""
        
        if preset_name == "web_optimization":
            # 网页优化预设
            return [
                ProcessingConfig(
                    ProcessingOperation.RESIZE,
                    {'width': 1920, 'height': 1080, 'mode': 'max_size'}
                ),
                ProcessingConfig(
                    ProcessingOperation.FORMAT_CONVERT,
                    {'format': 'JPEG'}
                ),
                ProcessingConfig(
                    ProcessingOperation.COMPRESS,
                    {'quality': 85}
                )
            ]
        
        elif preset_name == "thumbnail_generation":
            # 缩略图生成预设
            return [
                ProcessingConfig(
                    ProcessingOperation.RESIZE,
                    {'width': 256, 'height': 256, 'mode': 'keep_ratio'}
                ),
                ProcessingConfig(
                    ProcessingOperation.FORMAT_CONVERT,
                    {'format': 'JPEG'}
                )
            ]
        
        elif preset_name == "image_enhancement":
            # 图像增强预设
            return [
                ProcessingConfig(
                    ProcessingOperation.BRIGHTNESS,
                    {'factor': 1.1}
                ),
                ProcessingConfig(
                    ProcessingOperation.CONTRAST,
                    {'factor': 1.2}
                ),
                ProcessingConfig(
                    ProcessingOperation.SHARPEN,
                    {'factor': 0.5}
                )
            ]
        
        elif preset_name == "dataset_preparation":
            # 数据集准备预设
            return [
                ProcessingConfig(
                    ProcessingOperation.RESIZE,
                    {'width': 640, 'height': 640, 'mode': 'exact'}
                ),
                ProcessingConfig(
                    ProcessingOperation.NORMALIZE,
                    {}
                ),
                ProcessingConfig(
                    ProcessingOperation.FORMAT_CONVERT,
                    {'format': 'JPEG'}
                )
            ]
        
        else:
            return []
    
    def save_config_preset(self, configs: List[ProcessingConfig], 
                          preset_name: str, output_path: Path):
        """保存配置预设"""
        preset_data = {
            'name': preset_name,
            'configs': []
        }
        
        for config in configs:
            config_data = {
                'operation': config.operation.value,
                'parameters': config.parameters,
                'enabled': config.enabled
            }
            preset_data['configs'].append(config_data)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(preset_data, f, indent=2, ensure_ascii=False)
    
    def load_config_preset(self, preset_path: Path) -> List[ProcessingConfig]:
        """加载配置预设"""
        with open(preset_path, 'r', encoding='utf-8') as f:
            preset_data = json.load(f)
        
        configs = []
        for config_data in preset_data['configs']:
            config = ProcessingConfig(
                operation=ProcessingOperation(config_data['operation']),
                parameters=config_data['parameters'],
                enabled=config_data['enabled']
            )
            configs.append(config)
        
        return configs