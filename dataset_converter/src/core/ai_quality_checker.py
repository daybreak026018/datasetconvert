"""
AI辅助标注质量检测器
使用规则和启发式算法检测标注质量问题
"""

import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from .base_parser import ImageAnnotation, BBox


class QualityIssueType(Enum):
    """质量问题类型"""
    BBOX_OUT_OF_BOUNDS = "bbox_out_of_bounds"      # 边界框超出图片范围
    BBOX_TOO_SMALL = "bbox_too_small"              # 边界框过小
    BBOX_TOO_LARGE = "bbox_too_large"              # 边界框过大
    BBOX_OVERLAP_HIGH = "bbox_overlap_high"        # 边界框重叠度过高
    BBOX_ASPECT_RATIO = "bbox_aspect_ratio"        # 边界框长宽比异常
    IMAGE_TOO_DARK = "image_too_dark"              # 图片过暗
    IMAGE_TOO_BRIGHT = "image_too_bright"          # 图片过亮
    IMAGE_BLURRY = "image_blurry"                  # 图片模糊
    IMAGE_LOW_CONTRAST = "image_low_contrast"      # 图片对比度低
    ANNOTATION_MISSING = "annotation_missing"       # 缺少标注
    ANNOTATION_TOO_MANY = "annotation_too_many"    # 标注过多
    CLASS_IMBALANCE = "class_imbalance"            # 类别不平衡


@dataclass
class QualityIssue:
    """质量问题"""
    issue_type: QualityIssueType
    severity: str  # "low", "medium", "high"
    description: str
    suggestion: str
    bbox_id: Optional[int] = None  # 相关的边界框ID
    confidence: float = 1.0  # 置信度 0-1


class AIQualityChecker:
    """AI辅助质量检测器"""
    
    def __init__(self):
        # 质量检测阈值
        self.thresholds = {
            'min_bbox_size': 10,           # 最小边界框尺寸
            'max_bbox_ratio': 0.8,         # 最大边界框占图片比例
            'max_overlap_ratio': 0.7,      # 最大重叠比例
            'min_aspect_ratio': 0.1,       # 最小长宽比
            'max_aspect_ratio': 10.0,      # 最大长宽比
            'min_brightness': 30,          # 最小亮度
            'max_brightness': 225,         # 最大亮度
            'min_contrast': 20,            # 最小对比度
            'blur_threshold': 100,         # 模糊阈值
            'max_annotations': 50,         # 单图最大标注数
        }
    
    def check_annotation_quality(self, annotation: ImageAnnotation) -> List[QualityIssue]:
        """检查单个标注的质量"""
        issues = []
        
        # 检查图片质量
        if annotation.image_path.exists():
            image_issues = self._check_image_quality(annotation.image_path)
            issues.extend(image_issues)
        
        # 检查边界框质量
        bbox_issues = self._check_bbox_quality(annotation)
        issues.extend(bbox_issues)
        
        # 检查标注数量
        annotation_count_issues = self._check_annotation_count(annotation)
        issues.extend(annotation_count_issues)
        
        return issues
    
    def _check_image_quality(self, image_path: Path) -> List[QualityIssue]:
        """检查图片质量"""
        issues = []
        
        try:
            # 读取图片
            image = cv2.imread(str(image_path))
            if image is None:
                return [QualityIssue(
                    QualityIssueType.IMAGE_TOO_DARK,
                    "high",
                    "无法读取图片文件",
                    "检查图片文件是否损坏或格式不支持"
                )]
            
            # 转换为灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 检查亮度
            mean_brightness = np.mean(gray)
            if mean_brightness < self.thresholds['min_brightness']:
                issues.append(QualityIssue(
                    QualityIssueType.IMAGE_TOO_DARK,
                    "medium",
                    f"图片过暗，平均亮度: {mean_brightness:.1f}",
                    "考虑调整图片亮度或使用图像增强技术",
                    confidence=min(1.0, (self.thresholds['min_brightness'] - mean_brightness) / 50)
                ))
            elif mean_brightness > self.thresholds['max_brightness']:
                issues.append(QualityIssue(
                    QualityIssueType.IMAGE_TOO_BRIGHT,
                    "medium",
                    f"图片过亮，平均亮度: {mean_brightness:.1f}",
                    "考虑调整图片亮度或曝光设置",
                    confidence=min(1.0, (mean_brightness - self.thresholds['max_brightness']) / 50)
                ))
            
            # 检查对比度
            contrast = np.std(gray)
            if contrast < self.thresholds['min_contrast']:
                issues.append(QualityIssue(
                    QualityIssueType.IMAGE_LOW_CONTRAST,
                    "medium",
                    f"图片对比度过低: {contrast:.1f}",
                    "考虑使用直方图均衡化或对比度增强",
                    confidence=min(1.0, (self.thresholds['min_contrast'] - contrast) / 20)
                ))
            
            # 检查模糊度（使用拉普拉斯算子）
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            if laplacian_var < self.thresholds['blur_threshold']:
                issues.append(QualityIssue(
                    QualityIssueType.IMAGE_BLURRY,
                    "high",
                    f"图片可能模糊，清晰度: {laplacian_var:.1f}",
                    "考虑重新拍摄或使用锐化滤镜",
                    confidence=min(1.0, (self.thresholds['blur_threshold'] - laplacian_var) / 100)
                ))
            
        except Exception as e:
            issues.append(QualityIssue(
                QualityIssueType.IMAGE_TOO_DARK,
                "high",
                f"图片质量检测失败: {e}",
                "检查图片文件完整性"
            ))
        
        return issues
    
    def _check_bbox_quality(self, annotation: ImageAnnotation) -> List[QualityIssue]:
        """检查边界框质量"""
        issues = []
        
        if not annotation.boxes:
            issues.append(QualityIssue(
                QualityIssueType.ANNOTATION_MISSING,
                "medium",
                "图片没有标注",
                "检查是否需要添加标注"
            ))
            return issues
        
        image_area = annotation.width * annotation.height
        
        for i, bbox in enumerate(annotation.boxes):
            # 检查边界框是否超出图片范围
            if (bbox.xmin < 0 or bbox.ymin < 0 or 
                bbox.xmax > annotation.width or bbox.ymax > annotation.height):
                issues.append(QualityIssue(
                    QualityIssueType.BBOX_OUT_OF_BOUNDS,
                    "high",
                    f"边界框 {i} 超出图片范围",
                    "调整边界框坐标使其在图片范围内",
                    bbox_id=i
                ))
            
            # 检查边界框尺寸
            bbox_width = bbox.xmax - bbox.xmin
            bbox_height = bbox.ymax - bbox.ymin
            bbox_area = bbox_width * bbox_height
            
            if bbox_width < self.thresholds['min_bbox_size'] or bbox_height < self.thresholds['min_bbox_size']:
                issues.append(QualityIssue(
                    QualityIssueType.BBOX_TOO_SMALL,
                    "medium",
                    f"边界框 {i} 过小 ({bbox_width}x{bbox_height})",
                    "检查标注是否准确，考虑扩大边界框",
                    bbox_id=i
                ))
            
            # 检查边界框占图片比例
            area_ratio = bbox_area / image_area
            if area_ratio > self.thresholds['max_bbox_ratio']:
                issues.append(QualityIssue(
                    QualityIssueType.BBOX_TOO_LARGE,
                    "medium",
                    f"边界框 {i} 过大，占图片 {area_ratio:.1%}",
                    "检查边界框是否过大，考虑调整尺寸",
                    bbox_id=i
                ))
            
            # 检查长宽比
            aspect_ratio = bbox_width / bbox_height if bbox_height > 0 else float('inf')
            if (aspect_ratio < self.thresholds['min_aspect_ratio'] or 
                aspect_ratio > self.thresholds['max_aspect_ratio']):
                issues.append(QualityIssue(
                    QualityIssueType.BBOX_ASPECT_RATIO,
                    "low",
                    f"边界框 {i} 长宽比异常: {aspect_ratio:.2f}",
                    "检查边界框比例是否合理",
                    bbox_id=i,
                    confidence=0.5
                ))
        
        # 检查边界框重叠
        overlap_issues = self._check_bbox_overlaps(annotation.boxes)
        issues.extend(overlap_issues)
        
        return issues
    
    def _check_bbox_overlaps(self, boxes: List[BBox]) -> List[QualityIssue]:
        """检查边界框重叠"""
        issues = []
        
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                overlap_ratio = self._calculate_overlap_ratio(boxes[i], boxes[j])
                
                if overlap_ratio > self.thresholds['max_overlap_ratio']:
                    issues.append(QualityIssue(
                        QualityIssueType.BBOX_OVERLAP_HIGH,
                        "medium",
                        f"边界框 {i} 和 {j} 重叠度过高: {overlap_ratio:.1%}",
                        "检查是否为重复标注或调整边界框位置",
                        confidence=min(1.0, overlap_ratio)
                    ))
        
        return issues
    
    def _calculate_overlap_ratio(self, bbox1: BBox, bbox2: BBox) -> float:
        """计算两个边界框的重叠比例"""
        # 计算交集
        x1 = max(bbox1.xmin, bbox2.xmin)
        y1 = max(bbox1.ymin, bbox2.ymin)
        x2 = min(bbox1.xmax, bbox2.xmax)
        y2 = min(bbox1.ymax, bbox2.ymax)
        
        if x2 <= x1 or y2 <= y1:
            return 0.0
        
        intersection = (x2 - x1) * (y2 - y1)
        
        # 计算并集
        area1 = (bbox1.xmax - bbox1.xmin) * (bbox1.ymax - bbox1.ymin)
        area2 = (bbox2.xmax - bbox2.xmin) * (bbox2.ymax - bbox2.ymin)
        union = area1 + area2 - intersection
        
        return intersection / union if union > 0 else 0.0
    
    def _check_annotation_count(self, annotation: ImageAnnotation) -> List[QualityIssue]:
        """检查标注数量"""
        issues = []
        
        total_annotations = len(annotation.boxes)
        if annotation.polygons:
            total_annotations += len(annotation.polygons)
        
        if total_annotations > self.thresholds['max_annotations']:
            issues.append(QualityIssue(
                QualityIssueType.ANNOTATION_TOO_MANY,
                "medium",
                f"标注数量过多: {total_annotations}",
                "检查是否有重复或不必要的标注"
            ))
        
        return issues
    
    def check_dataset_quality(self, annotations: List[ImageAnnotation]) -> Dict:
        """检查整个数据集的质量"""
        all_issues = []
        issue_stats = {}
        
        # 检查每个标注
        for annotation in annotations:
            issues = self.check_annotation_quality(annotation)
            all_issues.extend(issues)
        
        # 统计问题类型
        for issue in all_issues:
            issue_type = issue.issue_type.value
            if issue_type not in issue_stats:
                issue_stats[issue_type] = {'count': 0, 'severity': {}}
            
            issue_stats[issue_type]['count'] += 1
            severity = issue.severity
            if severity not in issue_stats[issue_type]['severity']:
                issue_stats[issue_type]['severity'][severity] = 0
            issue_stats[issue_type]['severity'][severity] += 1
        
        # 检查类别平衡
        class_balance_issues = self._check_class_balance(annotations)
        all_issues.extend(class_balance_issues)
        
        # 计算质量评分
        quality_score = self._calculate_quality_score(all_issues, len(annotations))
        
        return {
            'total_images': len(annotations),
            'total_issues': len(all_issues),
            'issue_stats': issue_stats,
            'quality_score': quality_score,
            'issues': all_issues,
            'recommendations': self._generate_recommendations(issue_stats)
        }
    
    def _check_class_balance(self, annotations: List[ImageAnnotation]) -> List[QualityIssue]:
        """检查类别平衡"""
        issues = []
        
        # 统计类别分布
        class_counts = {}
        for annotation in annotations:
            for bbox in annotation.boxes:
                class_counts[bbox.label] = class_counts.get(bbox.label, 0) + 1
        
        if not class_counts:
            return issues
        
        total_annotations = sum(class_counts.values())
        max_count = max(class_counts.values())
        min_count = min(class_counts.values())
        
        # 检查类别不平衡（最大类别数量是最小类别的10倍以上）
        if max_count / min_count > 10:
            issues.append(QualityIssue(
                QualityIssueType.CLASS_IMBALANCE,
                "medium",
                f"类别分布不平衡，最大类别 {max_count} 个，最小类别 {min_count} 个",
                "考虑使用数据增强或重新采样来平衡类别分布"
            ))
        
        return issues
    
    def _calculate_quality_score(self, issues: List[QualityIssue], total_images: int) -> float:
        """计算质量评分 (0-100)"""
        if total_images == 0:
            return 0.0
        
        # 根据问题严重程度计算扣分
        penalty = 0
        for issue in issues:
            if issue.severity == "high":
                penalty += 10
            elif issue.severity == "medium":
                penalty += 5
            else:  # low
                penalty += 2
        
        # 平均到每张图片
        avg_penalty = penalty / total_images
        
        # 计算评分 (最低10分)
        score = max(10, 100 - avg_penalty)
        
        return round(score, 1)
    
    def _generate_recommendations(self, issue_stats: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 根据问题统计生成建议
        if 'image_too_dark' in issue_stats or 'image_too_bright' in issue_stats:
            recommendations.append("建议调整图片亮度，使用自动曝光或手动调整相机设置")
        
        if 'image_blurry' in issue_stats:
            recommendations.append("建议检查相机对焦设置，避免拍摄时抖动")
        
        if 'bbox_out_of_bounds' in issue_stats:
            recommendations.append("建议检查标注工具设置，确保边界框在图片范围内")
        
        if 'bbox_overlap_high' in issue_stats:
            recommendations.append("建议检查重复标注，合并或删除重叠的边界框")
        
        if 'class_imbalance' in issue_stats:
            recommendations.append("建议使用数据增强技术平衡类别分布")
        
        if not recommendations:
            recommendations.append("数据集质量良好，建议继续保持标注标准")
        
        return recommendations
    
    def export_quality_report(self, quality_result: Dict, output_path: Path):
        """导出质量报告"""
        report_lines = []
        
        report_lines.append("# 数据集质量检测报告")
        report_lines.append(f"生成时间: {Path().cwd()}")
        report_lines.append("")
        
        # 总体统计
        report_lines.append("## 总体统计")
        report_lines.append(f"- 图片总数: {quality_result['total_images']}")
        report_lines.append(f"- 问题总数: {quality_result['total_issues']}")
        report_lines.append(f"- 质量评分: {quality_result['quality_score']}/100")
        report_lines.append("")
        
        # 问题统计
        if quality_result['issue_stats']:
            report_lines.append("## 问题统计")
            for issue_type, stats in quality_result['issue_stats'].items():
                issue_name = issue_type.replace('_', ' ').title()
                report_lines.append(f"- {issue_name}: {stats['count']} 个")
                
                severity_info = []
                for severity, count in stats['severity'].items():
                    severity_info.append(f"{severity}: {count}")
                report_lines.append(f"  - 严重程度: {', '.join(severity_info)}")
            report_lines.append("")
        
        # 改进建议
        if quality_result['recommendations']:
            report_lines.append("## 改进建议")
            for i, rec in enumerate(quality_result['recommendations'], 1):
                report_lines.append(f"{i}. {rec}")
            report_lines.append("")
        
        # 详细问题列表
        if quality_result['issues']:
            report_lines.append("## 详细问题列表")
            for i, issue in enumerate(quality_result['issues'][:50], 1):  # 限制显示前50个
                report_lines.append(f"{i}. {issue.description}")
                report_lines.append(f"   - 类型: {issue.issue_type.value}")
                report_lines.append(f"   - 严重程度: {issue.severity}")
                report_lines.append(f"   - 建议: {issue.suggestion}")
                if issue.bbox_id is not None:
                    report_lines.append(f"   - 相关边界框: {issue.bbox_id}")
                report_lines.append("")
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report_lines))