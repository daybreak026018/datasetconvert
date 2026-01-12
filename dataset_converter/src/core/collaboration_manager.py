"""
协作标注管理器
支持将数据集分配给多人标注，跟踪进度和质量
"""

import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = "pending"          # 待分配
    ASSIGNED = "assigned"        # 已分配
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"      # 已完成
    REVIEWED = "reviewed"        # 已审核
    REJECTED = "rejected"        # 被拒绝


class AnnotatorRole(Enum):
    """标注员角色"""
    ANNOTATOR = "annotator"      # 标注员
    REVIEWER = "reviewer"        # 审核员
    ADMIN = "admin"             # 管理员


@dataclass
class Annotator:
    """标注员信息"""
    id: str
    name: str
    email: str
    role: AnnotatorRole
    skills: List[str]  # 擅长的标注类型
    workload: int = 0  # 当前工作量
    quality_score: float = 1.0  # 质量评分 (0-1)
    created_at: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class AnnotationTask:
    """标注任务"""
    id: str
    project_id: str
    image_path: str
    assigned_to: Optional[str] = None  # 标注员ID
    reviewer_id: Optional[str] = None  # 审核员ID
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 1  # 优先级 1-5
    estimated_time: int = 10  # 预估时间(分钟)
    actual_time: Optional[int] = None  # 实际用时
    created_at: str = ""
    assigned_at: Optional[str] = None
    completed_at: Optional[str] = None
    reviewed_at: Optional[str] = None
    notes: str = ""
    quality_score: Optional[float] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class AnnotationProject:
    """标注项目"""
    id: str
    name: str
    description: str
    image_folder: str
    output_folder: str
    annotation_format: str  # yolo, voc, json等
    classes: List[str]  # 标注类别
    guidelines: str  # 标注指南
    quality_threshold: float = 0.8  # 质量阈值
    review_required: bool = True  # 是否需要审核
    created_by: str = ""
    created_at: str = ""
    deadline: Optional[str] = None
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class CollaborationManager:
    """协作标注管理器"""
    
    def __init__(self, workspace_dir: Path):
        self.workspace_dir = Path(workspace_dir)
        self.projects_dir = self.workspace_dir / "projects"
        self.annotators_file = self.workspace_dir / "annotators.json"
        self.config_file = self.workspace_dir / "collaboration_config.json"
        
        # 创建必要目录
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.projects_dir.mkdir(exist_ok=True)
        
        # 初始化数据
        self.annotators: Dict[str, Annotator] = {}
        self.projects: Dict[str, AnnotationProject] = {}
        self.config = self._load_config()
        
        self._load_annotators()
        self._load_projects()
    
    def _load_config(self) -> Dict:
        """加载配置"""
        default_config = {
            "auto_assign": True,
            "max_tasks_per_annotator": 50,
            "quality_weight": 0.7,
            "workload_weight": 0.3,
            "review_percentage": 0.2,  # 20%的任务需要审核
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    default_config.update(config)
            except Exception as e:
                print(f"加载配置失败: {e}")
        
        return default_config
    
    def _save_config(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def _load_annotators(self):
        """加载标注员信息"""
        if self.annotators_file.exists():
            try:
                with open(self.annotators_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for annotator_data in data:
                        annotator = Annotator(**annotator_data)
                        annotator.role = AnnotatorRole(annotator.role)
                        self.annotators[annotator.id] = annotator
            except Exception as e:
                print(f"加载标注员信息失败: {e}")
    
    def _save_annotators(self):
        """保存标注员信息"""
        try:
            data = []
            for annotator in self.annotators.values():
                annotator_dict = asdict(annotator)
                annotator_dict['role'] = annotator.role.value
                data.append(annotator_dict)
            
            with open(self.annotators_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存标注员信息失败: {e}")
    
    def _load_projects(self):
        """加载项目信息"""
        for project_file in self.projects_dir.glob("*/project.json"):
            try:
                with open(project_file, 'r', encoding='utf-8') as f:
                    project_data = json.load(f)
                    project = AnnotationProject(**project_data)
                    self.projects[project.id] = project
            except Exception as e:
                print(f"加载项目失败: {e}")
    
    def add_annotator(self, name: str, email: str, role: AnnotatorRole, 
                     skills: List[str] = None) -> str:
        """添加标注员"""
        annotator_id = str(uuid.uuid4())
        annotator = Annotator(
            id=annotator_id,
            name=name,
            email=email,
            role=role,
            skills=skills or []
        )
        
        self.annotators[annotator_id] = annotator
        self._save_annotators()
        return annotator_id
    
    def create_project(self, name: str, description: str, image_folder: str,
                      output_folder: str, annotation_format: str, 
                      classes: List[str], guidelines: str = "",
                      created_by: str = "", deadline: str = None) -> str:
        """创建标注项目"""
        project_id = str(uuid.uuid4())
        project = AnnotationProject(
            id=project_id,
            name=name,
            description=description,
            image_folder=image_folder,
            output_folder=output_folder,
            annotation_format=annotation_format,
            classes=classes,
            guidelines=guidelines,
            created_by=created_by,
            deadline=deadline
        )
        
        self.projects[project_id] = project
        
        # 创建项目目录
        project_dir = self.projects_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        # 保存项目信息
        with open(project_dir / "project.json", 'w', encoding='utf-8') as f:
            json.dump(asdict(project), f, indent=2, ensure_ascii=False)
        
        # 创建任务
        self._create_tasks_from_images(project_id, image_folder)
        
        return project_id
    
    def _create_tasks_from_images(self, project_id: str, image_folder: str):
        """从图片文件夹创建标注任务"""
        image_dir = Path(image_folder)
        if not image_dir.exists():
            raise ValueError(f"图片文件夹不存在: {image_folder}")
        
        # 支持的图片格式
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        
        tasks = []
        for image_path in image_dir.rglob("*"):
            if image_path.suffix.lower() in image_extensions:
                task_id = str(uuid.uuid4())
                task = AnnotationTask(
                    id=task_id,
                    project_id=project_id,
                    image_path=str(image_path)
                )
                tasks.append(task)
        
        # 保存任务
        project_dir = self.projects_dir / project_id
        tasks_file = project_dir / "tasks.json"
        
        tasks_data = [asdict(task) for task in tasks]
        for task_data in tasks_data:
            task_data['status'] = task_data['status'].value
        
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, indent=2, ensure_ascii=False)
        
        print(f"为项目 {project_id} 创建了 {len(tasks)} 个标注任务")
    
    def get_project_tasks(self, project_id: str) -> List[AnnotationTask]:
        """获取项目的所有任务"""
        project_dir = self.projects_dir / project_id
        tasks_file = project_dir / "tasks.json"
        
        if not tasks_file.exists():
            return []
        
        try:
            with open(tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                tasks = []
                for task_data in tasks_data:
                    task_data['status'] = TaskStatus(task_data['status'])
                    tasks.append(AnnotationTask(**task_data))
                return tasks
        except Exception as e:
            print(f"加载任务失败: {e}")
            return []
    
    def assign_tasks_automatically(self, project_id: str, 
                                 distribution_strategy: str = "balanced") -> Dict[str, int]:
        """自动分配任务"""
        tasks = self.get_project_tasks(project_id)
        pending_tasks = [t for t in tasks if t.status == TaskStatus.PENDING]
        
        if not pending_tasks:
            return {}
        
        # 获取可用的标注员
        available_annotators = [
            a for a in self.annotators.values() 
            if a.role in [AnnotatorRole.ANNOTATOR, AnnotatorRole.ADMIN]
            and a.workload < self.config['max_tasks_per_annotator']
        ]
        
        if not available_annotators:
            raise ValueError("没有可用的标注员")
        
        # 分配策略
        assignments = {}
        
        if distribution_strategy == "balanced":
            # 平衡分配：考虑工作量和质量
            assignments = self._balanced_assignment(pending_tasks, available_annotators)
        elif distribution_strategy == "quality_first":
            # 质量优先：优先分配给高质量标注员
            assignments = self._quality_first_assignment(pending_tasks, available_annotators)
        elif distribution_strategy == "round_robin":
            # 轮询分配：平均分配
            assignments = self._round_robin_assignment(pending_tasks, available_annotators)
        
        # 更新任务状态
        self._update_task_assignments(project_id, assignments)
        
        return {annotator_id: len(task_ids) for annotator_id, task_ids in assignments.items()}
    
    def _balanced_assignment(self, tasks: List[AnnotationTask], 
                           annotators: List[Annotator]) -> Dict[str, List[str]]:
        """平衡分配算法"""
        assignments = {a.id: [] for a in annotators}
        
        # 按质量和工作量排序标注员
        sorted_annotators = sorted(
            annotators, 
            key=lambda a: (
                a.quality_score * self.config['quality_weight'] - 
                a.workload * self.config['workload_weight']
            ),
            reverse=True
        )
        
        # 分配任务
        for i, task in enumerate(tasks):
            annotator = sorted_annotators[i % len(sorted_annotators)]
            assignments[annotator.id].append(task.id)
            annotator.workload += 1
        
        return assignments
    
    def _quality_first_assignment(self, tasks: List[AnnotationTask], 
                                annotators: List[Annotator]) -> Dict[str, List[str]]:
        """质量优先分配"""
        assignments = {a.id: [] for a in annotators}
        
        # 按质量排序
        sorted_annotators = sorted(annotators, key=lambda a: a.quality_score, reverse=True)
        
        # 优先分配给高质量标注员
        for task in tasks:
            # 选择质量最高且工作量未满的标注员
            for annotator in sorted_annotators:
                if annotator.workload < self.config['max_tasks_per_annotator']:
                    assignments[annotator.id].append(task.id)
                    annotator.workload += 1
                    break
        
        return assignments
    
    def _round_robin_assignment(self, tasks: List[AnnotationTask], 
                              annotators: List[Annotator]) -> Dict[str, List[str]]:
        """轮询分配"""
        assignments = {a.id: [] for a in annotators}
        
        for i, task in enumerate(tasks):
            annotator = annotators[i % len(annotators)]
            assignments[annotator.id].append(task.id)
        
        return assignments
    
    def _update_task_assignments(self, project_id: str, assignments: Dict[str, List[str]]):
        """更新任务分配"""
        tasks = self.get_project_tasks(project_id)
        task_dict = {t.id: t for t in tasks}
        
        current_time = datetime.now().isoformat()
        
        for annotator_id, task_ids in assignments.items():
            for task_id in task_ids:
                if task_id in task_dict:
                    task = task_dict[task_id]
                    task.assigned_to = annotator_id
                    task.status = TaskStatus.ASSIGNED
                    task.assigned_at = current_time
        
        # 保存更新后的任务
        self._save_project_tasks(project_id, list(task_dict.values()))
    
    def _save_project_tasks(self, project_id: str, tasks: List[AnnotationTask]):
        """保存项目任务"""
        project_dir = self.projects_dir / project_id
        tasks_file = project_dir / "tasks.json"
        
        tasks_data = []
        for task in tasks:
            task_data = asdict(task)
            task_data['status'] = task.status.value
            tasks_data.append(task_data)
        
        with open(tasks_file, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, indent=2, ensure_ascii=False)
    
    def get_annotator_tasks(self, annotator_id: str, project_id: str = None) -> List[AnnotationTask]:
        """获取标注员的任务"""
        all_tasks = []
        
        if project_id:
            # 获取特定项目的任务
            tasks = self.get_project_tasks(project_id)
            all_tasks.extend(tasks)
        else:
            # 获取所有项目的任务
            for pid in self.projects.keys():
                tasks = self.get_project_tasks(pid)
                all_tasks.extend(tasks)
        
        # 筛选该标注员的任务
        return [t for t in all_tasks if t.assigned_to == annotator_id]
    
    def update_task_status(self, project_id: str, task_id: str, 
                          status: TaskStatus, notes: str = ""):
        """更新任务状态"""
        tasks = self.get_project_tasks(project_id)
        
        for task in tasks:
            if task.id == task_id:
                task.status = status
                task.notes = notes
                
                current_time = datetime.now().isoformat()
                if status == TaskStatus.COMPLETED:
                    task.completed_at = current_time
                elif status == TaskStatus.REVIEWED:
                    task.reviewed_at = current_time
                
                break
        
        self._save_project_tasks(project_id, tasks)
    
    def get_project_statistics(self, project_id: str) -> Dict:
        """获取项目统计信息"""
        tasks = self.get_project_tasks(project_id)
        
        stats = {
            'total_tasks': len(tasks),
            'pending': len([t for t in tasks if t.status == TaskStatus.PENDING]),
            'assigned': len([t for t in tasks if t.status == TaskStatus.ASSIGNED]),
            'in_progress': len([t for t in tasks if t.status == TaskStatus.IN_PROGRESS]),
            'completed': len([t for t in tasks if t.status == TaskStatus.COMPLETED]),
            'reviewed': len([t for t in tasks if t.status == TaskStatus.REVIEWED]),
            'rejected': len([t for t in tasks if t.status == TaskStatus.REJECTED]),
        }
        
        # 计算进度百分比
        if stats['total_tasks'] > 0:
            stats['completion_rate'] = (stats['completed'] + stats['reviewed']) / stats['total_tasks']
            stats['assignment_rate'] = (stats['total_tasks'] - stats['pending']) / stats['total_tasks']
        else:
            stats['completion_rate'] = 0
            stats['assignment_rate'] = 0
        
        # 标注员统计
        annotator_stats = {}
        for task in tasks:
            if task.assigned_to:
                if task.assigned_to not in annotator_stats:
                    annotator_stats[task.assigned_to] = {
                        'assigned': 0, 'completed': 0, 'in_progress': 0
                    }
                
                annotator_stats[task.assigned_to]['assigned'] += 1
                if task.status == TaskStatus.COMPLETED:
                    annotator_stats[task.assigned_to]['completed'] += 1
                elif task.status == TaskStatus.IN_PROGRESS:
                    annotator_stats[task.assigned_to]['in_progress'] += 1
        
        stats['annotator_stats'] = annotator_stats
        
        return stats
    
    def export_project_data(self, project_id: str, export_path: str):
        """导出项目数据"""
        project = self.projects.get(project_id)
        if not project:
            raise ValueError(f"项目不存在: {project_id}")
        
        tasks = self.get_project_tasks(project_id)
        stats = self.get_project_statistics(project_id)
        
        export_data = {
            'project': asdict(project),
            'tasks': [asdict(task) for task in tasks],
            'statistics': stats,
            'annotators': {
                aid: asdict(annotator) for aid, annotator in self.annotators.items()
            },
            'exported_at': datetime.now().isoformat()
        }
        
        # 处理枚举类型
        for task_data in export_data['tasks']:
            task_data['status'] = task_data['status'].value
        
        for annotator_data in export_data['annotators'].values():
            annotator_data['role'] = annotator_data['role'].value
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)