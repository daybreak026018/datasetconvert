# DataForge v2.0 / DataForge v2.0

🚀 **专业级数据集处理工具套件** - 一个功能完整、界面现代化的桌面应用程序，专为计算机视觉项目的数据集管理而设计。

🚀 **Professional Dataset Processing Toolkit** - A comprehensive desktop application designed for computer vision dataset management with modern UI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

---

## 📖 目录 / Table of Contents

### 🇨🇳 中文文档
- [主要特性](#主要特性)
- [快速开始](#快速开始)
- [安装指南](#安装指南)
- [项目结构](#项目结构)
- [核心功能](#核心功能)
- [使用示例](#使用示例)
- [支持的数据格式](#支持的数据格式)
- [界面特色](#界面特色)
- [更新日志](#更新日志)
- [贡献指南](#贡献指南)

### 🇺🇸 English Documentation
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Installation Guide](#installation-guide)
- [Project Structure](#project-structure)
- [Core Functions](#core-functions)
- [Usage Examples](#usage-examples)
- [Supported Data Formats](#supported-data-formats)
- [Interface Features](#interface-features)
- [Version History](#version-history)
- [Contributing](#contributing)

---

# 🇨🇳 中文文档

## ✨ 主要特性

### 🔄 格式转换
- **5种主流格式支持**: YOLO检测、YOLO分割、VOC、JSON、自定义格式
- **智能转换**: 支持矩形框和多边形标注的混合处理
- **无损转换**: 保持标注精度和完整性
- **批量处理**: 高效处理大规模数据集

### 🤖 AI质量检测
- **智能质量分析**: 自动检测标注质量问题
- **图像质量评估**: 检测模糊、过暗、过亮等图像问题
- **标注质量验证**: 检测边界框重叠、超出范围等问题
- **质量评分系统**: 提供0-100分的质量评分
- **详细报告**: 生成完整的质量检测报告

### 🖼️ 批量图片处理
- **多种处理操作**: 调整尺寸、裁剪、旋转、翻转等
- **图像增强**: 亮度、对比度、饱和度调整
- **格式转换**: 支持JPEG、PNG、BMP等格式互转
- **预设配置**: 网页优化、缩略图生成等预设
- **批量处理**: 高效处理大量图片文件

### 👥 协作标注管理
- **数据集划分**: 将数据集按人头数智能划分给多个标注员
- **多种分配方式**: 支持按序号顺序、随机分配、按文件夹名称分配
- **自定义命名**: 支持person_1、annotator_1或完全自定义的文件夹命名
- **实时预览**: 显示每个标注员将分配到的文件数量和占比
- **进度跟踪**: 实时显示划分进度，支持取消操作
- **完整复制**: 自动复制对应的标签文件（txt、xml、json格式）

### 📊 数据分析
- **全面统计**: 图片数量、标注分布、类别统计
- **质量评估**: 自动检测数据问题，生成健康度评分
- **可视化展示**: 直观的标注可视化和数据集预览
- **详细报告**: 生成专业的HTML分析报告

### 🛠️ 数据处理
- **自动修复**: 智能修复坐标错误、重复文件等问题
- **数据增强**: 7种图像增强方法，支持自定义组合
- **数据整理**: 批量重命名、数据集划分、多数据集合并
- **格式标准化**: 统一文件命名和目录结构

### 🎨 现代化界面
- **Material Design**: 现代化的用户界面设计
- **响应式布局**: 支持滚动，适配不同屏幕尺寸
- **统一风格**: 所有窗口采用一致的设计语言
- **用户友好**: 直观的操作流程和清晰的状态反馈

## 🚀 快速开始

### 环境要求
- Python 3.8+
- PyQt5 5.15+
- Pillow 10.0+

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/dataset-converter.git
cd dataset-converter
```

2. **安装依赖**
```bash
pip install -r dataset_converter/requirements.txt
```

3. **启动程序**
```bash
python dataset_converter/main.py
```

## 📦 安装指南

### 系统要求

- **操作系统**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 或更高版本
- **内存**: 建议 4GB 以上
- **存储**: 至少 100MB 可用空间

### 方法1: 直接安装（推荐）

1. **下载项目**
```bash
git clone https://github.com/your-username/dataset-converter.git
cd dataset-converter
```

2. **安装Python依赖**
```bash
pip install -r dataset_converter/requirements.txt
```

3. **启动程序**
```bash
python dataset_converter/main.py
```

### 方法2: 虚拟环境安装

1. **创建虚拟环境**
```bash
python -m venv dataset_converter_env

# Windows
dataset_converter_env\Scripts\activate

# macOS/Linux  
source dataset_converter_env/bin/activate
```

2. **安装依赖并启动**
```bash
pip install -r dataset_converter/requirements.txt
python dataset_converter/main.py
```

### 依赖包说明

| 包名 | 版本 | 用途 |
|------|------|------|
| PyQt5 | ≥5.15.0 | GUI界面框架 |
| Pillow | ≥10.0.0 | 图像处理 |
| pyyaml | ≥6.0 | 配置文件解析 |
| lxml | ≥5.1.0 | XML文件处理 |

### 常见问题

#### Q: 提示"No module named 'PyQt5'"
**A**: 安装PyQt5依赖
```bash
pip install PyQt5>=5.15.0
```

#### Q: 提示"No module named 'PIL'"  
**A**: 安装Pillow依赖
```bash
pip install Pillow>=10.0.0
```

#### Q: Windows上PowerShell执行策略错误
**A**: 使用CMD而不是PowerShell，或者设置执行策略
```cmd
# 使用CMD运行
python dataset_converter/main.py
```

#### Q: 程序启动后界面显示不完整
**A**: 确保屏幕分辨率至少为1200x800，程序会自动调整布局

### 验证安装

运行以下命令验证安装是否成功：

```bash
python -c "
import sys
print(f'Python版本: {sys.version}')

try:
    import PyQt5
    print('✓ PyQt5 已安装')
except ImportError:
    print('✗ PyQt5 未安装')

try:
    from PIL import Image
    print('✓ Pillow 已安装')
except ImportError:
    print('✗ Pillow 未安装')

try:
    import yaml
    print('✓ PyYAML 已安装')
except ImportError:
    print('✗ PyYAML 未安装')

print('安装验证完成！')
"
```

### 故障排除

#### 常见问题解决

**Q: 数据可视化时程序闪退**
**A**: 确保数据集符合标准目录结构，检查图片和标签文件是否完整
```bash
# 检查数据集结构
数据集名称/
├── images/train/  # 确保有图片文件
├── images/test/
├── images/val/
├── labels/train/  # 确保有对应的标签文件
├── labels/test/
└── labels/val/
```

**Q: 统计图表中文显示为方块**
**A**: 系统缺少中文字体，程序会自动尝试多种字体，如仍有问题请安装SimSun字体

**Q: 数据搜索功能选择数据集后闪退**
**A**: 此问题已在v2.1.1版本中完全修复。如仍遇到问题，请确保：
- 使用最新版本的应用程序
- 数据集采用标准目录结构
- 在进度条运行时避免频繁切换菜单

**Q: 数据搜索显示0个标注**
**A**: 检查数据集是否使用标准目录结构，标签文件是否与图片文件名匹配

**Q: 数据集分析无结果**
**A**: 确保选择的是数据集根目录（包含images和labels文件夹），而不是子目录

**Q: 界面显示不完整或有滚动问题**
**A**: 调整窗口大小或使用全屏模式，程序支持响应式布局

## 📁 项目结构

```
dataset_converter/
├── 📄 README.md                    # 项目说明文档
├── 📄 requirements.txt             # 依赖包列表
├── 📄 main.py                      # 程序入口
├── 📁 src/                         # 源代码目录
│   ├── 📁 core/                    # 核心功能模块
│   │   ├── 📄 base_parser.py       # 基础解析器
│   │   ├── 📄 converter.py         # 格式转换器
│   │   ├── 📄 yolo_parser.py       # YOLO检测解析器
│   │   ├── 📄 yolo_seg_parser.py   # YOLO分割解析器
│   │   ├── 📄 voc_parser.py        # VOC格式解析器
│   │   ├── 📄 json_parser.py       # JSON格式解析器
│   │   ├── 📄 dataset_analyzer.py  # 数据集分析器
│   │   ├── 📄 dataset_validator.py # 数据集验证器
│   │   ├── 📄 data_augmentation.py # 数据增强器
│   │   ├── 📄 dataset_organizer.py # 数据集整理器
│   │   ├── 📄 annotation_visualizer.py # 标注可视化器
│   │   ├── 📄 dataset_comparator.py # 数据集比较器
│   │   ├── 📄 annotation_fixer.py  # 标注修复器
│   │   └── 📄 dataset_exporter.py  # 数据集导出器
│   ├── 📁 gui/                     # 图形界面模块
│   │   ├── 📄 styles.py            # 统一样式管理
│   │   ├── 📄 home_window.py       # 主窗口
│   │   ├── 📄 converter_panel.py   # 转换面板
│   │   ├── 📄 analysis_panel.py    # 分析面板
│   │   ├── 📄 splitting_panel.py   # 分割面板
│   │   └── 📁 widgets/             # 自定义控件
│   └── 📁 utils/                   # 工具函数
│       ├── 📄 file_utils.py        # 文件操作工具
│       ├── 📄 xml_utils.py         # XML处理工具
│       ├── 📄 label_utils.py       # 标签处理工具
│       └── 📄 logger.py            # 日志工具
├── 📁 data/                        # 数据目录
│   ├── 📁 input/                   # 输入数据
│   └── 📁 output/                  # 输出数据
├── 📁 configs/                     # 配置文件
│   └── 📄 config.yaml              # 主配置文件
└── 📁 resources/                   # 资源文件
    └── 🖼️ icon.png                 # 应用图标
```

## 🎯 核心功能

### 1. 数据集格式转换
- **YOLO检测** ↔ **VOC** ↔ **JSON**
- **YOLO分割** ↔ **JSON**
- **YOLO分割** → **YOLO检测** (保留矩形框)
- 支持自定义标签映射和批量转换

### 2. 数据集分析
- 📈 **统计分析**: 全面的数据集统计信息
- 🔍 **质量检查**: 自动检测和评估数据质量
- 📊 **可视化**: 标注可视化和数据集预览
- 📋 **报告生成**: 专业的HTML分析报告

### 3. 数据集处理
- 🔧 **自动修复**: 修复坐标错误、重复文件等问题
- 🎨 **数据增强**: 亮度、对比度、旋转、翻转等增强
- 📂 **数据整理**: 重命名、划分、合并数据集
- ⚖️ **数据比较**: 多数据集对比分析

### 4. 数据导出
- 📦 **ZIP打包**: 完整数据集打包导出
- 🏷️ **COCO格式**: 导出为COCO标准格式
- ⚙️ **训练配置**: 生成YOLO训练配置文件
- 📄 **详细报告**: HTML格式的分析报告

## 💡 使用示例

### 数据准备

#### 标准数据集目录结构
```
my_dataset/                    # 数据集根目录
├── images/                    # 图片目录
│   ├── train/                 # 训练集图片
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   ├── test/                  # 测试集图片
│   │   ├── img101.jpg
│   │   └── ...
│   └── val/                   # 验证集图片
│       ├── img201.jpg
│       └── ...
└── labels/                    # 标签目录
    ├── train/                 # 训练集标签
    │   ├── img001.txt         # 与图片同名
    │   ├── img002.txt
    │   └── ...
    ├── test/                  # 测试集标签
    │   ├── img101.txt
    │   └── ...
    └── val/                   # 验证集标签
        ├── img201.txt
        └── ...
```

#### YOLO检测格式示例
```
# 文件: labels/train/img001.txt
0 0.5 0.5 0.3 0.4              # 类别0: 中心点(0.5,0.5), 宽高(0.3,0.4)
1 0.2 0.3 0.1 0.2              # 类别1: 中心点(0.2,0.3), 宽高(0.1,0.2)
```

#### YOLO分割格式示例
```
# 文件: labels/train/img002.txt
0 0.5 0.5 0.3 0.4                           # 矩形框
1 0.1 0.1 0.2 0.1 0.2 0.2 0.1 0.2           # 四边形
2 0.7 0.7 0.8 0.7 0.8 0.8 0.7 0.8 0.75 0.75 # 五边形
```

### GUI使用步骤

1. **启动程序**
   ```bash
   python dataset_converter/main.py
   ```

2. **选择功能**
   - 点击左侧导航栏选择功能模块

3. **数据集格式转换**
   - 点击"数据集格式转换"
   - 选择输入目录（数据集根目录，包含images和labels文件夹）
   - 选择输出目录
   - 选择转换格式并点击对应按钮

4. **数据集可视化**
   - 点击"数据集可视化"
   - 选择数据集根目录
   - 点击"生成统计仪表板"查看详细分析

5. **数据搜索**
   - 点击"数据搜索"
   - 选择数据集目录
   - 设置筛选条件
   - 点击"开始搜索"并可导出结果

6. **数据集分析**
   - 点击"数据集分析"
   - 选择数据集目录
   - 使用各种分析功能（统计、验证、增强等）

7. **设置主题**
   - 点击"设置"
   - 在主题选项卡中选择喜欢的主题
   - 点击"应用主题"

### 基本转换
1. 启动程序，选择"数据集格式转换"
2. 选择输入目录（包含图片和标注文件）
3. 选择输出目录
4. 点击对应的转换按钮（如"YOLO检测 → JSON"）
5. 查看转换日志和结果

### 数据集分析
1. 选择"数据集分析"面板
2. 选择数据集目录
3. 点击"统计分析"查看详细统计
4. 点击"质量检查"评估数据质量
5. 点击"生成报告"创建HTML报告

### 数据增强
1. 在分析面板中选择数据集
2. 选择需要的增强方法（亮度、对比度等）
3. 设置增强倍数
4. 点击"开始增强"生成增强数据

### 命令行使用 (高级)

```python
from pathlib import Path
from dataset_converter.src.core.converter import convert

# YOLO分割 → JSON
convert(
    input_dir=Path("input_data"),
    input_format="yolo_seg", 
    output_dir=Path("output_data"),
    output_format="json"
)
```

## 🔧 支持的数据格式

### YOLO检测格式
```
# 每行格式: class_id center_x center_y width height (归一化坐标)
0 0.5 0.5 0.3 0.4
1 0.2 0.3 0.1 0.2
```

### YOLO分割格式
```
# 矩形框: class_id center_x center_y width height
0 0.5 0.5 0.3 0.4
# 多边形: class_id x1 y1 x2 y2 ... xn yn
1 0.1 0.1 0.2 0.1 0.2 0.2 0.1 0.2
```

### JSON格式
```json
{
  "file_name": "image.jpg",
  "width": 800,
  "height": 600,
  "annotations": [
    {"label": "cat", "bbox": [100, 100, 200, 200]},
    {"label": "dog", "polygon": [0.1, 0.1, 0.2, 0.1, 0.2, 0.2]}
  ]
}
```

## 🎨 界面特色

### 🎯 现代化设计
- **Material Design**: 现代化的用户界面设计风格
- **统一主题系统**: 4种内置主题（浅色、深色、蓝色、绿色）可选
- **SimSun字体**: 统一使用宋体，完美支持中文显示
- **无焦点虚线框**: 清洁的视觉体验，无干扰元素

### ⚡ 性能优化
- **集中式样式管理**: 统一的样式管理架构，避免冲突
- **防闪烁机制**: 优化的渲染机制，界面切换更流畅
- **样式继承**: 高效的样式继承系统，减少重复计算
- **快速响应**: 优化的界面加载和切换速度

### 🎨 用户体验
- **响应式布局**: 支持滚动，适配不同屏幕尺寸
- **直观操作**: 颜色编码的按钮（绿色=执行，橙色=警告，蓝色=主要）
- **实时反馈**: 详细的日志输出和进度显示
- **流畅切换**: 主题和面板切换无卡顿

### 🛡️ 稳定性保障
- **样式一致性**: 所有面板采用统一的设计语言
- **无界面闪烁**: 彻底解决界面异常显示问题
- **稳定渲染**: 优化的样式应用机制
- **长期稳定**: 经过优化的界面架构，确保长时间使用稳定

## 📝 更新日志

### [2.2.0] - 2026-01-12

#### 🚀 重大功能更新
- **高级功能面板**: 新增专门的高级功能模块，集成AI质量检测和批量图片处理
- **AI质量检测系统**: 智能检测标注质量问题，包括图像质量、边界框质量、类别平衡等
- **批量图片处理工具**: 支持调整尺寸、格式转换、图像增强等多种批量操作
- **协作标注管理**: 数据集智能划分功能，支持多人协作标注项目

#### 🤖 AI质量检测功能
- **图像质量分析**: 检测图片亮度、对比度、模糊度等问题
- **标注质量验证**: 检测边界框超出范围、重叠度过高、尺寸异常等问题
- **类别平衡检查**: 分析数据集中各类别的分布情况
- **质量评分系统**: 提供0-100分的综合质量评分
- **详细报告导出**: 生成Markdown格式的质量检测报告

#### 🖼️ 批量图片处理功能
- **多种处理操作**: 调整尺寸、裁剪、旋转、翻转、亮度/对比度/饱和度调整
- **图像滤镜**: 模糊、锐化、灰度转换、标准化等处理
- **格式转换**: 支持JPEG、PNG、BMP、TIFF、WEBP等格式互转
- **预设配置**: 网页优化、缩略图生成、图像增强、数据集准备等预设
- **批量处理**: 高效处理大量图片文件，支持进度显示和状态回调

#### 👥 协作标注功能
- **数据集智能划分**: 按人头数将数据集划分给多个标注员，支持2-20人的团队协作
- **多种分配策略**: 按序号顺序分配、随机分配、按文件夹名称分配三种方式
- **灵活命名方案**: 支持person_1/person_2、annotator_1/annotator_2或完全自定义的文件夹命名
- **实时预览功能**: 显示每个标注员将分配到的文件数量、占比，便于调整分配方案
- **完整文件复制**: 自动复制图片文件和对应的标签文件（支持txt、xml、json格式）
- **标准目录结构**: 为每个标注员创建images和labels子目录，便于后续管理

#### 🛠️ 技术改进
- **新增依赖**: 添加opencv-python支持，用于图像质量分析
- **模块化设计**: 高级功能采用选项卡式界面，便于功能扩展
- **异常处理**: 完善的错误处理机制，确保功能稳定性
- **进度反馈**: 所有长时间操作都提供进度条和状态反馈

### [2.1.1] - 2026-01-12

#### 🔧 重要修复
- **搜索面板闪退修复**: 彻底解决数据搜索功能选择数据集后闪退的问题
- **线程安全优化**: 改进工作线程和进度对话框的生命周期管理
- **菜单切换安全**: 修复在进度条运行时切换菜单导致的资源冲突问题
- **AttributeError消除**: 解决进度更新时的 `'NoneType' object has no attribute 'setLabelText'` 错误

#### 🛠️ 技术改进

**进度管理器优化**
- 在搜索面板中添加 `progress_manager` 实例变量保持对进度管理器的引用
- 改进 `ProgressDialog` 的资源清理机制，确保线程和对话框正确销毁
- 使用队列连接 (`Qt.QueuedConnection`) 确保UI更新在主线程中进行
- 添加异常安全的UI更新机制，防止访问已销毁的对话框

**主窗口资源管理**
- 改进菜单切换逻辑，在切换前清理正在运行的任务
- 添加窗口关闭事件处理器，确保应用程序关闭时所有任务被正确清理
- 防止面板销毁时工作线程仍在运行导致的闪退问题

**工作线程改进**
- 完善线程取消和清理机制，支持超时强制终止
- 改进信号连接和断开机制，防止内存泄漏
- 添加析构函数确保资源在对象销毁时被正确清理

#### ✅ 修复效果
- **消除闪退**: 数据搜索功能在进度条运行时不再闪退
- **菜单切换安全**: 用户可以在任何时候安全地切换菜单，正在运行的任务会被正确取消
- **资源管理**: 所有工作线程和进度对话框都能被正确清理
- **线程安全**: 使用队列连接确保UI更新在主线程中进行
- **无错误输出**: 彻底消除AttributeError等异常输出

### [2.1.0] - 2026-01-09

#### 🎉 重大更新
- **应用重命名**: 从"数据集转换工具"更名为"DataForge"，体现专业的数据锻造理念
- **标准目录结构**: 统一采用 `images/` 和 `labels/` 的标准数据集结构，支持 `train/test/val` 子集
- **智能格式检测**: 自动识别数据集格式，减少用户操作复杂度
- **主题系统**: 完整的主题管理系统，支持4种内置主题
- **界面优化**: 移除所有焦点虚线框，提供更清洁的视觉体验
- **UI架构重构**: 全面优化界面渲染机制，彻底解决界面闪烁问题
- **数据集重新划分**: 支持对已有数据集进行重新划分（如8:1:1 → 6:2:2）

#### ✨ 新增功能

**数据集验证与管理**
- 新增数据集验证器 (`dataset_validator.py`)，支持标准目录结构验证
- 智能格式检测，自动识别YOLO、VOC、JSON等格式
- 数据集健康度评分系统，全面评估数据质量
- 标准目录结构创建工具

**增强的数据可视化**
- 双重可视化系统：`EnhancedVisualizer` (matplotlib) 和 `SimpleVisualizer` (HTML/Plotly)
- 9图表统计仪表板：类别分布、尺寸统计、密度热力图等
- 交互式HTML报告，支持响应式设计
- 专业级数据分析图表，完美支持中文字体显示

**数据搜索与过滤**
- 全新的数据搜索面板 (`search_panel.py`)
- 多维度筛选：文件名、类别、尺寸、标注数量
- 筛选结果导出功能，支持实际文件复制
- 详细统计报告生成和保存

**主题与界面优化**
- 完整的主题管理系统 (`theme_manager.py`)
- 4种内置主题：浅色、深色、蓝色、绿色
- 设置面板 (`settings_panel.py`) 支持主题切换和界面配置
- 统一的Material Design风格，使用SimSun(宋体)字体

**UI架构重构**
- 集中式样式管理：统一由主窗口管理所有样式
- 样式继承机制：子面板自动继承主窗口样式
- 防闪烁优化：使用`setUpdatesEnabled`机制防止界面闪烁
- 渲染性能提升：优化样式应用时机和重绘机制

**数据集重新划分**
- 智能检测标准目录结构数据集
- 支持重新划分已有数据集比例（如8:1:1 → 6:2:2）
- 自动合并所有子集后按新比例重新分配
- 完整的数据验证和错误处理机制

#### 🔧 重大改进

**标准目录结构支持**
- 所有解析器完全适配新的标准目录结构
- 支持 `train/test/val` 子集自动识别和处理
- 图片和标签文件分离管理，提高数据组织效率
- 跨子集的统一处理和验证机制

**用户体验优化**
- 移除所有界面焦点虚线框（QTabWidget、QListWidget等）
- 中文字体完美支持，解决matplotlib图表文字显示为正方形的问题
- 响应式布局改进，支持滚动和动态调整
- 统一的错误处理和用户反馈机制

**功能完善**
- 数据集分析功能完全重构，支持标准目录结构
- 数据搜索功能修复，正确显示标注数量和统计信息
- 可视化功能增强，支持中文标题和标签，添加字体缓存刷新
- 所有导出功能适配新的数据结构

**技术架构升级**
- 统一的样式管理系统，替代旧的AppStyles
- 模块化的主题系统，支持动态切换
- 改进的错误处理和调试信息
- 更好的跨平台兼容性和字体支持

#### 🐛 修复问题
- **界面闪烁异常**: 彻底解决界面上方出现三个点等异常显示问题
- **样式系统冲突**: 统一样式管理，移除新旧样式系统混用导致的冲突
- **UI渲染优化**: 优化样式应用机制，防止界面加载时的闪烁和延迟
- **数据可视化闪退**: 修复选择数据集后程序闪退的问题，添加延迟初始化和错误处理
- **搜索功能零标注**: 修复数据搜索功能显示0个标注的问题，更新为新的验证系统
- **分析功能无结果**: 修复数据集分析功能无结果的问题，完全适配标准目录结构
- **中文字体显示**: 修复统计仪表板中文字显示为正方形的问题，添加跨平台字体配置
- **界面焦点框**: 移除所有界面焦点虚线框，提供更清洁的视觉体验
- **目录结构适配**: 修复所有功能对新标准目录结构的适配问题

#### 📊 数据集格式规范

**标准目录结构**
```
数据集名称/
├── images/
│   ├── train/          # 训练集图片
│   ├── test/           # 测试集图片
│   └── val/            # 验证集图片
└── labels/
    ├── train/          # 训练集标签
    ├── test/           # 测试集标签
    └── val/            # 验证集标签
```

**支持的格式**
- **图片格式**: .jpg, .jpeg, .png, .bmp, .tiff, .webp
- **标签格式**: 
  - YOLO: .txt (归一化坐标)
  - VOC: .xml (Pascal VOC格式)
  - JSON: .json (自定义JSON格式)

#### 🎨 界面改进
- 应用名称更新为"DataForge v2.0"
- 统一的SimSun(宋体)字体支持，解决中文显示问题
- 4种主题可选：浅色、深色、蓝色、绿色
- 移除所有焦点虚线框，包括选项卡和列表控件
- 改进的按钮和控件样式，更现代化的视觉效果

#### 📋 使用说明更新

**新的数据集准备方式**
1. 创建主数据集文件夹（如 `my_dataset`）
2. 在其中创建 `images` 和 `labels` 两个子文件夹
3. 在每个子文件夹中创建 `train`、`test`、`val` 子目录
4. 将对应的图片和标签文件放入相应目录
5. 确保图片和标签文件名一致（扩展名不同）

**功能使用建议**
- 使用"数据集可视化"前，确保数据集符合标准目录结构
- 利用"数据搜索"功能快速筛选和导出特定条件的数据
- 通过"数据集分析"获取详细的数据质量报告
- 在"设置"中选择合适的主题以获得最佳视觉体验

### [2.0.0] - 2024-01-07

#### 🎉 重大更新
- 完全重构的现代化界面设计
- 新增YOLO分割格式支持
- 完整的数据集分析和处理功能

#### ✨ 新增功能

**格式转换**
- 新增YOLO分割格式解析器 (`yolo_seg_parser.py`)
- 支持矩形框和多边形混合标注
- 扩展JSON解析器支持分割标注
- 新增12种转换路径

**数据分析**
- 数据集统计分析器 (`dataset_analyzer.py`)
- 数据质量验证器 (`dataset_validator.py`)
- 标注可视化器 (`annotation_visualizer.py`)
- 数据集比较器 (`dataset_comparator.py`)
- HTML报告生成功能

**数据处理**
- 自动修复器 (`annotation_fixer.py`)
- 数据增强器 (`data_augmentation.py`)
- 数据集整理器 (`dataset_organizer.py`)
- 多格式导出器 (`dataset_exporter.py`)

**界面优化**
- 统一样式管理系统 (`styles.py`)
- Material Design风格界面
- 响应式布局和滚动支持
- 三个主要功能面板：转换、分析、分割

#### 🔧 改进

**用户体验**
- 重新设计的主窗口布局
- 颜色编码的功能按钮
- 实时进度显示和日志输出
- 直观的状态反馈

**技术架构**
- 模块化的核心功能设计
- 统一的解析器接口
- 可扩展的插件架构
- 改进的错误处理机制

**性能优化**
- 优化大文件处理性能
- 改进内存使用效率
- 支持批量操作
- 异步处理支持

#### 🐛 修复
- 修复YOLO坐标解析精度问题
- 修复JSON文件编码问题
- 修复界面在不同分辨率下的显示问题
- 修复文件路径处理的跨平台兼容性

### [2.0.0] - 2024-01-07

#### 🎉 重大更新
- 完全重构的现代化界面设计
- 新增YOLO分割格式支持
- 完整的数据集分析和处理功能

#### ✨ 新增功能

**格式转换**
- 新增YOLO分割格式解析器 (`yolo_seg_parser.py`)
- 支持矩形框和多边形混合标注
- 扩展JSON解析器支持分割标注
- 新增12种转换路径

**数据分析**
- 数据集统计分析器 (`dataset_analyzer.py`)
- 数据质量验证器 (`dataset_validator.py`)
- 标注可视化器 (`annotation_visualizer.py`)
- 数据集比较器 (`dataset_comparator.py`)
- HTML报告生成功能

**数据处理**
- 自动修复器 (`annotation_fixer.py`)
- 数据增强器 (`data_augmentation.py`)
- 数据集整理器 (`dataset_organizer.py`)
- 多格式导出器 (`dataset_exporter.py`)

**界面优化**
- 统一样式管理系统 (`styles.py`)
- Material Design风格界面
- 响应式布局和滚动支持
- 三个主要功能面板：转换、分析、分割

#### 🔧 改进

**用户体验**
- 重新设计的主窗口布局
- 颜色编码的功能按钮
- 实时进度显示和日志输出
- 直观的状态反馈

**技术架构**
- 模块化的核心功能设计
- 统一的解析器接口
- 可扩展的插件架构
- 改进的错误处理机制

**性能优化**
- 优化大文件处理性能
- 改进内存使用效率
- 支持批量操作
- 异步处理支持

#### 🐛 修复
- 修复YOLO坐标解析精度问题
- 修复JSON文件编码问题
- 修复界面在不同分辨率下的显示问题
- 修复文件路径处理的跨平台兼容性

### [1.0.0] - 2023-12-01

#### ✨ 初始版本
- 基础的YOLO、VOC、JSON格式转换功能
- 简单的PyQt5 GUI界面
- 基本的文件选择和转换操作
- 日志输出功能

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - 强大的GUI框架
- [Pillow](https://pillow.readthedocs.io/) - Python图像处理库
- [Material Design](https://material.io/design) - 现代化设计指南


### 注意事项

1. **文件命名**: 标注文件必须与图片文件同名
2. **坐标格式**: YOLO格式使用归一化坐标 (0-1)
3. **多边形要求**: 至少需要3个点 (6个坐标值)
4. **格式兼容**: YOLO分割格式向下兼容YOLO检测格式

---

⭐ 如果这个项目对你有帮助，请给它一个星标！

---

# 🇺🇸 English Documentation

## ✨ Key Features

### 🔄 Format Conversion
- **5 mainstream formats**: YOLO Detection, YOLO Segmentation, VOC, JSON, Custom formats
- **Smart conversion**: Mixed processing of bounding boxes and polygon annotations
- **Lossless conversion**: Maintains annotation precision and completeness
- **Batch processing**: Efficient handling of large-scale datasets

### 🤖 AI Quality Detection
- **Intelligent quality analysis**: Automatic detection of annotation quality issues
- **Image quality assessment**: Detect blur, darkness, brightness and other image problems
- **Annotation quality validation**: Detect bounding box overlap, out-of-bounds and other issues
- **Quality scoring system**: Provide 0-100 quality scores
- **Detailed reports**: Generate comprehensive quality detection reports

### 🖼️ Batch Image Processing
- **Multiple processing operations**: Resize, crop, rotate, flip, etc.
- **Image enhancement**: Brightness, contrast, saturation adjustment
- **Format conversion**: Support JPEG, PNG, BMP and other format conversion
- **Preset configurations**: Web optimization, thumbnail generation and other presets
- **Batch processing**: Efficiently process large numbers of image files

### 👥 Collaborative Annotation Management
- **Dataset Splitting**: Intelligently split datasets among multiple annotators by headcount
- **Multiple Assignment Methods**: Support sequential, random, and folder-name-based assignment
- **Custom Naming**: Support person_1, annotator_1, or completely custom folder naming
- **Real-time Preview**: Display file count and percentage for each annotator
- **Progress Tracking**: Real-time progress display with cancellation support
- **Complete Copy**: Automatically copy corresponding label files (txt, xml, json formats)

### 📊 Data Analysis
- **Comprehensive statistics**: Image count, annotation distribution, class statistics
- **Quality assessment**: Automatic problem detection with health scoring
- **Visualization**: Intuitive annotation visualization and dataset preview
- **Detailed reports**: Professional HTML analysis reports

### 🛠️ Data Processing
- **Auto-repair**: Smart fixing of coordinate errors, duplicate files, etc.
- **Data augmentation**: 7 image enhancement methods with custom combinations
- **Data organization**: Batch renaming, dataset splitting, multi-dataset merging
- **Format standardization**: Unified file naming and directory structure

### 🎨 Modern Interface
- **Material Design**: Modern user interface design
- **Responsive layout**: Scroll support, adapts to different screen sizes
- **Unified style**: Consistent design language across all windows
- **User-friendly**: Intuitive operation flow and clear status feedback

## 🚀 Quick Start

### Requirements
- Python 3.8+
- PyQt5 5.15+
- Pillow 10.0+

### Installation

1. **Clone the project**
```bash
git clone https://github.com/your-username/dataset-converter.git
cd dataset-converter
```

2. **Install dependencies**
```bash
pip install -r dataset_converter/requirements.txt
```

3. **Launch the application**
```bash
python dataset_converter/main.py
```

## 📦 Installation Guide

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **Memory**: 4GB+ recommended
- **Storage**: At least 100MB available space

### Method 1: Direct Installation (Recommended)

1. **Download the project**
```bash
git clone https://github.com/your-username/dataset-converter.git
cd dataset-converter
```

2. **Install Python dependencies**
```bash
pip install -r dataset_converter/requirements.txt
```

3. **Launch the application**
```bash
python dataset_converter/main.py
```

### Method 2: Virtual Environment Installation

1. **Create virtual environment**
```bash
python -m venv dataset_converter_env

# Windows
dataset_converter_env\Scripts\activate

# macOS/Linux  
source dataset_converter_env/bin/activate
```

2. **Install dependencies and launch**
```bash
pip install -r dataset_converter/requirements.txt
python dataset_converter/main.py
```

### Dependencies Overview

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt5 | ≥5.15.0 | GUI framework |
| Pillow | ≥10.0.0 | Image processing |
| pyyaml | ≥6.0 | Configuration file parsing |
| lxml | ≥5.1.0 | XML file processing |

### Common Issues

#### Q: "No module named 'PyQt5'" error
**A**: Install PyQt5 dependency
```bash
pip install PyQt5>=5.15.0
```

#### Q: "No module named 'PIL'" error  
**A**: Install Pillow dependency
```bash
pip install Pillow>=10.0.0
```

#### Q: PowerShell execution policy error on Windows
**A**: Use CMD instead of PowerShell, or set execution policy
```cmd
# Use CMD to run
python dataset_converter/main.py
```

#### Q: Incomplete interface display after startup
**A**: Ensure screen resolution is at least 1200x800, the program will automatically adjust layout

### Installation Verification

Run the following command to verify successful installation:

```bash
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    import PyQt5
    print('✓ PyQt5 installed')
except ImportError:
    print('✗ PyQt5 not installed')

try:
    from PIL import Image
    print('✓ Pillow installed')
except ImportError:
    print('✗ Pillow not installed')

try:
    import yaml
    print('✓ PyYAML installed')
except ImportError:
    print('✗ PyYAML not installed')

print('Installation verification complete!')
"
```

### Troubleshooting

#### Common Issues Resolution

**Q: Program crashes during data visualization**
**A**: Ensure dataset follows standard directory structure, check if image and label files are complete
```bash
# Check dataset structure
dataset_name/
├── images/train/  # Ensure image files exist
├── images/test/
├── images/val/
├── labels/train/  # Ensure corresponding label files exist
├── labels/test/
└── labels/val/
```

**Q: Chinese text displays as squares in charts**
**A**: System lacks Chinese fonts, program will automatically try multiple fonts, install SimSun font if issues persist

**Q: Data search crashes after selecting dataset**
**A**: This issue has been completely fixed in v2.1.1. If you still encounter problems, please ensure:
- Use the latest version of the application
- Dataset follows standard directory structure
- Avoid frequent menu switching while progress bar is running

**Q: Data search shows 0 annotations**
**A**: Check if dataset uses standard directory structure, ensure label files match image filenames

**Q: Dataset analysis shows no results**
**A**: Ensure you select the dataset root directory (containing images and labels folders), not subdirectories

**Q: Interface display incomplete or scroll issues**
**A**: Adjust window size or use fullscreen mode, program supports responsive layout

## 📁 Project Structure

```
dataset_converter/
├── 📄 README.md                    # Project documentation
├── 📄 requirements.txt             # Dependencies list
├── 📄 main.py                      # Application entry point
├── 📁 src/                         # Source code directory
│   ├── 📁 core/                    # Core functionality modules
│   │   ├── 📄 base_parser.py       # Base parser
│   │   ├── 📄 converter.py         # Format converter
│   │   ├── 📄 yolo_parser.py       # YOLO detection parser
│   │   ├── 📄 yolo_seg_parser.py   # YOLO segmentation parser
│   │   ├── 📄 voc_parser.py        # VOC format parser
│   │   ├── 📄 json_parser.py       # JSON format parser
│   │   ├── 📄 dataset_analyzer.py  # Dataset analyzer
│   │   ├── 📄 dataset_validator.py # Dataset validator
│   │   ├── 📄 data_augmentation.py # Data augmentor
│   │   ├── 📄 dataset_organizer.py # Dataset organizer
│   │   ├── 📄 annotation_visualizer.py # Annotation visualizer
│   │   ├── 📄 dataset_comparator.py # Dataset comparator
│   │   ├── 📄 annotation_fixer.py  # Annotation fixer
│   │   └── 📄 dataset_exporter.py  # Dataset exporter
│   ├── 📁 gui/                     # GUI modules
│   │   ├── 📄 styles.py            # Unified style management
│   │   ├── 📄 home_window.py       # Main window
│   │   ├── 📄 converter_panel.py   # Conversion panel
│   │   ├── 📄 analysis_panel.py    # Analysis panel
│   │   ├── 📄 splitting_panel.py   # Splitting panel
│   │   └── 📁 widgets/             # Custom widgets
│   └── 📁 utils/                   # Utility functions
│       ├── 📄 file_utils.py        # File operation utilities
│       ├── 📄 xml_utils.py         # XML processing utilities
│       ├── 📄 label_utils.py       # Label processing utilities
│       └── 📄 logger.py            # Logging utilities
├── 📁 data/                        # Data directory
│   ├── 📁 input/                   # Input data
│   └── 📁 output/                  # Output data
├── 📁 configs/                     # Configuration files
│   └── 📄 config.yaml              # Main configuration
└── 📁 resources/                   # Resource files
    └── 🖼️ icon.png                 # Application icon
```

## 🎯 Core Functions

### 1. Dataset Format Conversion
- **YOLO Detection** ↔ **VOC** ↔ **JSON**
- **YOLO Segmentation** ↔ **JSON**
- **YOLO Segmentation** → **YOLO Detection** (keep bounding boxes)
- Support for custom label mapping and batch conversion

### 2. Dataset Analysis
- 📈 **Statistical analysis**: Comprehensive dataset statistics
- 🔍 **Quality check**: Automatic detection and assessment of data quality
- 📊 **Visualization**: Annotation visualization and dataset preview
- 📋 **Report generation**: Professional HTML analysis reports

### 3. Dataset Processing
- 🔧 **Auto-repair**: Fix coordinate errors, duplicate files, etc.
- 🎨 **Data augmentation**: Brightness, contrast, rotation, flip, etc.
- 📂 **Data organization**: Rename, split, merge datasets
- ⚖️ **Data comparison**: Multi-dataset comparison analysis

### 4. Data Export
- 📦 **ZIP packaging**: Complete dataset packaging and export
- 🏷️ **COCO format**: Export to COCO standard format
- ⚙️ **Training config**: Generate YOLO training configuration files
- 📄 **Detailed reports**: HTML format analysis reports

## 💡 Usage Examples

### Data Preparation

#### Standard Dataset Directory Structure
```
my_dataset/                    # Dataset root directory
├── images/                    # Images directory
│   ├── train/                 # Training set images
│   │   ├── img001.jpg
│   │   ├── img002.jpg
│   │   └── ...
│   ├── test/                  # Test set images
│   │   ├── img101.jpg
│   │   └── ...
│   └── val/                   # Validation set images
│       ├── img201.jpg
│       └── ...
└── labels/                    # Labels directory
    ├── train/                 # Training set labels
    │   ├── img001.txt         # Same name as image
    │   ├── img002.txt
    │   └── ...
    ├── test/                  # Test set labels
    │   ├── img101.txt
    │   └── ...
    └── val/                   # Validation set labels
        ├── img201.txt
        └── ...
```

#### YOLO Detection Format Example
```
# File: labels/train/img001.txt
0 0.5 0.5 0.3 0.4              # Class 0: center(0.5,0.5), size(0.3,0.4)
1 0.2 0.3 0.1 0.2              # Class 1: center(0.2,0.3), size(0.1,0.2)
```

#### YOLO Segmentation Format Example
```
# File: labels/train/img002.txt
0 0.5 0.5 0.3 0.4                           # Bounding box
1 0.1 0.1 0.2 0.1 0.2 0.2 0.1 0.2           # Quadrilateral
2 0.7 0.7 0.8 0.7 0.8 0.8 0.7 0.8 0.75 0.75 # Pentagon
```

### GUI Usage Steps

1. **Launch the application**
   ```bash
   python dataset_converter/main.py
   ```

2. **Select function**
   - Click on the left navigation bar to select function modules

3. **Dataset Format Conversion**
   - Click "Dataset Format Conversion"
   - Select input directory (dataset root containing images and labels folders)
   - Select output directory
   - Choose conversion format and click corresponding button

4. **Dataset Visualization**
   - Click "Dataset Visualization"
   - Select dataset root directory
   - Click "Generate Statistical Dashboard" for detailed analysis

5. **Data Search**
   - Click "Data Search"
   - Select dataset directory
   - Set filter conditions
   - Click "Start Search" and export results

6. **Dataset Analysis**
   - Click "Dataset Analysis"
   - Select dataset directory
   - Use various analysis functions (statistics, validation, augmentation, etc.)

7. **Theme Settings**
   - Click "Settings"
   - Select preferred theme in theme tab
   - Click "Apply Theme"

### Basic Conversion
1. Launch the application, select "Dataset Format Conversion"
2. Select input directory (containing images and annotation files)
3. Select output directory
4. Click the corresponding conversion button (e.g., "YOLO Detection → JSON")
5. View conversion logs and results

### Dataset Analysis
1. Select "Dataset Analysis" panel
2. Select dataset directory
3. Click "Statistical Analysis" to view detailed statistics
4. Click "Quality Check" to assess data quality
5. Click "Generate Report" to create HTML report

### Data Augmentation
1. In the analysis panel, select dataset
2. Choose desired augmentation methods (brightness, contrast, etc.)
3. Set augmentation multiplier
4. Click "Start Augmentation" to generate augmented data

### Command Line Usage (Advanced)

```python
from pathlib import Path
from dataset_converter.src.core.converter import convert

# YOLO Segmentation → JSON
convert(
    input_dir=Path("input_data"),
    input_format="yolo_seg", 
    output_dir=Path("output_data"),
    output_format="json"
)
```

## 🔧 Supported Data Formats

### YOLO Detection Format
```
# Format: class_id center_x center_y width height (normalized coordinates)
0 0.5 0.5 0.3 0.4
1 0.2 0.3 0.1 0.2
```

### YOLO Segmentation Format
```
# Bounding box: class_id center_x center_y width height
0 0.5 0.5 0.3 0.4
# Polygon: class_id x1 y1 x2 y2 ... xn yn
1 0.1 0.1 0.2 0.1 0.2 0.2 0.1 0.2
```

### JSON Format
```json
{
  "file_name": "image.jpg",
  "width": 800,
  "height": 600,
  "annotations": [
    {"label": "cat", "bbox": [100, 100, 200, 200]},
    {"label": "dog", "polygon": [0.1, 0.1, 0.2, 0.1, 0.2, 0.2]}
  ]
}
```

## 🎨 Interface Features

### 🎯 Modern Design
- **Material Design**: Modern user interface design style
- **Unified Theme System**: 4 built-in themes (light, dark, blue, green) available
- **SimSun Font**: Unified use of SimSun font with perfect Chinese character support
- **No Focus Rectangles**: Clean visual experience without distracting elements

### ⚡ Performance Optimization
- **Centralized Style Management**: Unified style management architecture avoiding conflicts
- **Anti-Flicker Mechanism**: Optimized rendering mechanism for smoother interface transitions
- **Style Inheritance**: Efficient style inheritance system reducing redundant calculations
- **Fast Response**: Optimized interface loading and switching speed

### 🎨 User Experience
- **Responsive Layout**: Scroll support, adapts to different screen sizes
- **Intuitive Operation**: Color-coded buttons (green=execute, orange=warning, blue=primary)
- **Real-time Feedback**: Detailed log output and progress display
- **Smooth Transitions**: Theme and panel switching without lag

### 🛡️ Stability Assurance
- **Style Consistency**: All panels adopt unified design language
- **No Interface Flicker**: Completely resolved interface anomaly display issues
- **Stable Rendering**: Optimized style application mechanism
- **Long-term Stability**: Optimized interface architecture ensuring stable long-term use

## 📝 Version History

### [2.2.0] - 2026-01-12

#### 🚀 Major Feature Updates
- **Advanced Features Panel**: New dedicated advanced features module integrating AI quality detection and batch image processing
- **AI Quality Detection System**: Intelligent detection of annotation quality issues including image quality, bounding box quality, class balance, etc.
- **Batch Image Processing Tool**: Support for resizing, format conversion, image enhancement and other batch operations
- **Collaborative Annotation Management**: Intelligent dataset splitting functionality for multi-user collaborative annotation projects

#### 🤖 AI Quality Detection Features
- **Image Quality Analysis**: Detect image brightness, contrast, blur and other issues
- **Annotation Quality Validation**: Detect bounding boxes out of bounds, excessive overlap, abnormal sizes, etc.
- **Class Balance Check**: Analyze distribution of various classes in dataset
- **Quality Scoring System**: Provide comprehensive quality scores from 0-100
- **Detailed Report Export**: Generate quality detection reports in Markdown format

#### 🖼️ Batch Image Processing Features
- **Multiple Processing Operations**: Resize, crop, rotate, flip, brightness/contrast/saturation adjustment
- **Image Filters**: Blur, sharpen, grayscale conversion, normalization, etc.
- **Format Conversion**: Support conversion between JPEG, PNG, BMP, TIFF, WEBP and other formats
- **Preset Configurations**: Web optimization, thumbnail generation, image enhancement, dataset preparation presets
- **Batch Processing**: Efficiently process large numbers of image files with progress display and status callbacks

#### 👥 Collaborative Annotation Features
- **Intelligent Dataset Splitting**: Split datasets among multiple annotators by headcount, supporting teams of 2-20 people
- **Multiple Assignment Strategies**: Sequential assignment, random assignment, and folder-name-based assignment
- **Flexible Naming Schemes**: Support person_1/person_2, annotator_1/annotator_2, or completely custom folder naming
- **Real-time Preview**: Display file count and percentage for each annotator to facilitate assignment adjustment
- **Complete File Copying**: Automatically copy image files and corresponding label files (supports txt, xml, json formats)
- **Standard Directory Structure**: Create images and labels subdirectories for each annotator for easy management

#### 🛠️ Technical Improvements
- **New Dependencies**: Added opencv-python support for image quality analysis
- **Modular Design**: Advanced features use tabbed interface for easy feature expansion
- **Exception Handling**: Comprehensive error handling mechanisms ensuring feature stability
- **Progress Feedback**: All long-running operations provide progress bars and status feedback

### [2.1.1] - 2026-01-12

#### 🔧 Critical Fixes
- **Search Panel Crash Fix**: Completely resolved data search functionality crashing after dataset selection
- **Thread Safety Optimization**: Improved lifecycle management of worker threads and progress dialogs
- **Menu Switching Safety**: Fixed resource conflicts when switching menus while progress bar is running
- **AttributeError Elimination**: Resolved `'NoneType' object has no attribute 'setLabelText'` errors during progress updates

#### 🛠️ Technical Improvements

**Progress Manager Optimization**
- Added `progress_manager` instance variable in search panel to maintain reference to progress manager
- Improved `ProgressDialog` resource cleanup mechanism ensuring proper thread and dialog destruction
- Used queued connections (`Qt.QueuedConnection`) to ensure UI updates occur in main thread
- Added exception-safe UI update mechanism preventing access to destroyed dialogs

**Main Window Resource Management**
- Improved menu switching logic to cleanup running tasks before switching
- Added window close event handler ensuring all tasks are properly cleaned up when application closes
- Prevented crashes caused by worker threads still running when panels are destroyed

**Worker Thread Improvements**
- Enhanced thread cancellation and cleanup mechanism with timeout forced termination support
- Improved signal connection and disconnection mechanism preventing memory leaks
- Added destructor to ensure resources are properly cleaned up when objects are destroyed

#### ✅ Fix Results
- **Eliminated Crashes**: Data search functionality no longer crashes while progress bar is running
- **Safe Menu Switching**: Users can safely switch menus at any time, running tasks will be properly cancelled
- **Resource Management**: All worker threads and progress dialogs are properly cleaned up
- **Thread Safety**: Used queued connections to ensure UI updates occur in main thread
- **No Error Output**: Completely eliminated AttributeError and other exception outputs

### [2.1.0] - 2026-01-09

#### 🎉 Major Updates
- **Application Rename**: Renamed from "Dataset Conversion Tool" to "DataForge" for a more professional identity
- **Standard Directory Structure**: Unified adoption of `images/` and `labels/` standard dataset structure with `train/test/val` subsets
- **Smart Format Detection**: Automatic dataset format recognition to reduce user operation complexity
- **Theme System**: Complete theme management system with 4 built-in themes
- **Interface Optimization**: Removed all focus outline rectangles for a cleaner visual experience
- **UI Architecture Refactoring**: Comprehensive interface rendering mechanism optimization, completely resolved interface flicker issues
- **Dataset Re-splitting**: Support for re-splitting existing datasets (e.g., 8:1:1 → 6:2:2)

#### ✨ New Features

**Dataset Validation & Management**
- New dataset validator (`dataset_validator.py`) supporting standard directory structure validation
- Smart format detection automatically recognizing YOLO, VOC, JSON formats
- Dataset health scoring system for comprehensive data quality assessment
- Standard directory structure creation tools

**Enhanced Data Visualization**
- Dual visualization system: `EnhancedVisualizer` (matplotlib) and `SimpleVisualizer` (HTML/Plotly)
- 9-chart statistical dashboard: class distribution, size statistics, density heatmaps, etc.
- Interactive HTML reports with responsive design
- Professional-grade data analysis charts with perfect Chinese font support

**Data Search & Filtering**
- Brand new data search panel (`search_panel.py`)
- Multi-dimensional filtering: filename, class, size, annotation count
- Filter result export functionality with actual file copying
- Detailed statistical report generation and saving

**Theme & Interface Optimization**
- Complete theme management system (`theme_manager.py`)
- 4 built-in themes: light, dark, blue, green
- Settings panel (`settings_panel.py`) supporting theme switching and interface configuration
- Unified Material Design style with SimSun font support

#### 🔧 Major Improvements

**Standard Directory Structure Support**
- All parsers fully adapted to new standard directory structure
- Support for automatic `train/test/val` subset recognition and processing
- Separated image and label file management for improved data organization
- Unified processing and validation mechanisms across subsets

**User Experience Optimization**
- Removed all interface focus outline rectangles (QTabWidget, QListWidget, etc.)
- Perfect Chinese font support, fixed matplotlib chart text displaying as squares
- Improved responsive layout with scroll support and dynamic adjustment
- Unified error handling and user feedback mechanisms

**Feature Enhancement**
- Dataset analysis functionality completely reconstructed to support standard directory structure
- Data search functionality fixed to correctly display annotation counts and statistics
- Enhanced visualization with Chinese title and label support, added font cache refresh
- All export functions adapted to new data structure

**Technical Architecture Upgrade**
- Unified style management system replacing old AppStyles
- Modular theme system supporting dynamic switching
- Improved error handling and debugging information
- Better cross-platform compatibility and font support

#### 🐛 Bug Fixes
- **Data Visualization Crash**: Fixed program crash when selecting dataset, added delayed initialization and error handling
- **Search Zero Annotations**: Fixed data search showing 0 annotations, updated to new validation system
- **Analysis No Results**: Fixed dataset analysis showing no results, fully adapted to standard directory structure
- **Chinese Font Display**: Fixed statistical dashboard text displaying as squares, added cross-platform font configuration
- **Interface Focus Rectangles**: Removed all interface focus outline rectangles for cleaner visual experience
- **Directory Structure Adaptation**: Fixed all functionality adaptation issues with new standard directory structure

#### 📊 Dataset Format Standards

**Standard Directory Structure**
```
dataset_name/
├── images/
│   ├── train/          # Training set images
│   ├── test/           # Test set images
│   └── val/            # Validation set images
└── labels/
    ├── train/          # Training set labels
    ├── test/           # Test set labels
    └── val/            # Validation set labels
```

**Supported Formats**
- **Image formats**: .jpg, .jpeg, .png, .bmp, .tiff, .webp
- **Label formats**: 
  - YOLO: .txt (normalized coordinates)
  - VOC: .xml (Pascal VOC format)
  - JSON: .json (custom JSON format)

#### 🎨 Interface Improvements
- Application name updated to "DataForge v2.0"
- Unified SimSun font support, solving Chinese display issues
- 4 selectable themes: light, dark, blue, green
- Removed all focus outline rectangles including tabs and list controls
- Improved button and control styles with more modern visual effects

#### 📋 Updated Usage Instructions

**New Dataset Preparation Method**
1. Create main dataset folder (e.g., `my_dataset`)
2. Create `images` and `labels` subfolders within it
3. Create `train`, `test`, `val` subdirectories in each subfolder
4. Place corresponding image and label files in respective directories
5. Ensure image and label filenames match (different extensions)

**Feature Usage Recommendations**
- Before using "Dataset Visualization", ensure dataset follows standard directory structure
- Use "Data Search" functionality to quickly filter and export data meeting specific conditions
- Get detailed data quality reports through "Dataset Analysis"
- Select appropriate theme in "Settings" for optimal visual experience

### [2.0.0] - 2024-01-07

#### 🎉 Major Updates
- Complete redesign with modern interface
- Added YOLO segmentation format support
- Comprehensive dataset analysis and processing features

#### ✨ New Features

**Format Conversion**
- New YOLO segmentation format parser (`yolo_seg_parser.py`)
- Support for mixed bounding box and polygon annotations
- Extended JSON parser with segmentation annotation support
- Added 12 conversion pathways

**Data Analysis**
- Dataset statistical analyzer (`dataset_analyzer.py`)
- Data quality validator (`dataset_validator.py`)
- Annotation visualizer (`annotation_visualizer.py`)
- Dataset comparator (`dataset_comparator.py`)
- HTML report generation functionality

**Data Processing**
- Auto-repair tool (`annotation_fixer.py`)
- Data augmentation engine (`data_augmentation.py`)
- Dataset organizer (`dataset_organizer.py`)
- Multi-format exporter (`dataset_exporter.py`)

**Interface Improvements**
- Unified style management system (`styles.py`)
- Material Design interface
- Responsive layout with scroll support
- Three main functional panels: conversion, analysis, splitting

#### 🔧 Improvements

**User Experience**
- Redesigned main window layout
- Color-coded functional buttons
- Real-time progress display and log output
- Intuitive status feedback

**Technical Architecture**
- Modular core functionality design
- Unified parser interface
- Extensible plugin architecture
- Improved error handling mechanisms

**Performance Optimization**
- Optimized large file processing performance
- Improved memory usage efficiency
- Support for batch operations
- Asynchronous processing support

#### 🐛 Bug Fixes
- Fixed YOLO coordinate parsing precision issues
- Fixed JSON file encoding problems
- Fixed interface display issues on different resolutions
- Fixed cross-platform compatibility for file path handling

#### ✨ New Features

**Format Conversion**
- New YOLO segmentation format parser (`yolo_seg_parser.py`)
- Support for mixed bounding box and polygon annotations
- Extended JSON parser with segmentation annotation support
- Added 12 conversion pathways

**Data Analysis**
- Dataset statistical analyzer (`dataset_analyzer.py`)
- Data quality validator (`dataset_validator.py`)
- Annotation visualizer (`annotation_visualizer.py`)
- Dataset comparator (`dataset_comparator.py`)
- HTML report generation functionality

**Data Processing**
- Auto-repair tool (`annotation_fixer.py`)
- Data augmentation engine (`data_augmentation.py`)
- Dataset organizer (`dataset_organizer.py`)
- Multi-format exporter (`dataset_exporter.py`)

**Interface Improvements**
- Unified style management system (`styles.py`)
- Material Design interface
- Responsive layout with scroll support
- Three main functional panels: conversion, analysis, splitting

#### 🔧 Improvements

**User Experience**
- Redesigned main window layout
- Color-coded functional buttons
- Real-time progress display and log output
- Intuitive status feedback

**Technical Architecture**
- Modular core functionality design
- Unified parser interface
- Extensible plugin architecture
- Improved error handling mechanisms

**Performance Optimization**
- Optimized large file processing performance
- Improved memory usage efficiency
- Support for batch operations
- Asynchronous processing support

#### 🐛 Bug Fixes
- Fixed YOLO coordinate parsing precision issues
- Fixed JSON file encoding problems
- Fixed interface display issues on different resolutions
- Fixed cross-platform compatibility for file path handling

### [1.0.0] - 2023-12-01

#### ✨ Initial Release
- Basic YOLO, VOC, JSON format conversion functionality
- Simple PyQt5 GUI interface
- Basic file selection and conversion operations
- Log output functionality

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) - Powerful GUI framework
- [Pillow](https://pillow.readthedocs.io/) - Python imaging library
- [Material Design](https://material.io/design) - Modern design guidelines

[GitHub Discussions](https://github.com/your-username/dataset-converter/discussions)

### Important Notes

1. **File naming**: Annotation files must have the same name as image files
2. **Coordinate format**: YOLO format uses normalized coordinates (0-1)
3. **Polygon requirements**: At least 3 points required (6 coordinate values)
4. **Format compatibility**: YOLO segmentation format is backward compatible with YOLO detection format

---

⭐ If this project helps you, please give it a star!
