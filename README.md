DataForge YOLO Studio
DataForge YOLO Studio 是一个基于 PyQt5 的桌面端 YOLO 工具箱，面向目标检测、分割和分类项目，提供从数据准备、环境检测、模型训练、模型检测到结果管理的一站式流程。

当前版本保留蓝白紧凑界面，重点围绕 YOLO 工作流重构，不再把软件定位为单纯的数据集格式转换工具。

功能概览
YOLO首页：查看环境状态、最近训练、最近检测和可用权重数量。
数据准备：包含 YOLO 数据集体检、data.yaml 生成、格式转换、数据划分、分析报告和可视化预览。
环境检测：检测 Python、PyTorch、CUDA、GPU、Ultralytics、OpenCV，并给出安装建议。
模型训练：在软件内配置 YOLO 训练参数并启动本机训练，实时查看日志。
模型检测：选择权重后对图片、目录、视频或摄像头输入进行检测。
结果管理：扫描 runs 目录，查看训练权重、预测结果和输出路径。
设置：保留 YOLO Studio 的基础说明和默认输出位置。
支持任务
YOLO 检测：detect
YOLO 分割：segment
YOLO 分类：classify
第一版暂不包含姿态估计、OBB、跟踪、ONNX/TensorRT 导出等高级能力。

环境要求
Python 3.8 或更高版本
Windows 10/11 推荐
可选 GPU：需要匹配 PyTorch 与 CUDA 版本
依赖见 requirements.txt：

PyQt5
pyyaml
lxml
Pillow
matplotlib
seaborn
numpy
opencv-python
ultralytics
安装
建议使用虚拟环境：

python -m venv .venv
.venv\Scripts\activate
python -m pip install -U pip
python -m pip install -r requirements.txt
如果需要 GPU 训练，请先根据自己的 CUDA 版本安装匹配的 PyTorch，再安装项目依赖。环境检测页会给出提示，但不会自动修改系统环境。

启动
在项目根目录运行：

python dataset_converter/main.py
启动后窗口标题为 DataForge YOLO Studio。

推荐使用流程
打开 环境检测，确认 PyTorch、CUDA、Ultralytics 是否可用。
打开 数据准备，选择数据集目录并进行 YOLO 体检。
对检测/分割数据集生成或修复 data.yaml。
如需要，使用 格式转换、数据划分、分析报告、可视化预览 等旧数据准备功能。
打开 模型训练，选择任务类型、模型、数据和训练参数。
训练完成后进入 结果管理，找到 best.pt 或 last.pt。
打开 模型检测，选择权重和输入源执行推理。
YOLO 数据集结构
检测/分割推荐结构：

dataset/
  data.yaml
  images/
    train/
    val/
    test/
  labels/
    train/
    val/
    test/
分类推荐结构：

dataset/
  train/
    class_a/
    class_b/
  val/
    class_a/
    class_b/
  test/
    class_a/
    class_b/
data.yaml 示例
path: D:/datasets/my_yolo_dataset
train: images/train
val: images/val
test: images/test
nc: 2
names:
  - person
  - car
训练说明
训练页默认参数：

epochs: 100
imgsz: 640
batch: 16
device: auto
project: runs/train
name: exp
软件会通过项目内置 runner 调用 Ultralytics Python API 执行训练，训练日志实时显示在界面中。

示例等价命令逻辑：

python -m dataset_converter.src.core.yolo_cli_runner train ^
  --task detect ^
  --model yolo26n.pt ^
  --data D:/datasets/demo/data.yaml ^
  --epochs 100 ^
  --imgsz 640 ^
  --batch 16 ^
  --device auto ^
  --project runs/train ^
  --name exp ^
  --workers 4 ^
  --patience 50
检测说明
检测页支持：

单张图片
图片目录
视频文件
摄像头编号
可配置参数：

权重路径：如 runs/train/exp/weights/best.pt
输入源：图片、目录、视频或摄像头编号
conf
iou
imgsz
device
是否保存 txt
是否保存置信度
项目结构
datasetconvert/
  README.md
  requirements.txt
  dataset_converter/
    main.py
    src/
      core/
        yolo_services.py
        yolo_cli_runner.py
        converter.py
        yolo_parser.py
        yolo_seg_parser.py
      gui/
        simple_home_window.py
        yolo_panels.py
        converter_panel.py
        simple_splitting_panel.py
        simple_analysis_panel.py
        simple_visualization_panel.py
      utils/
        worker_thread.py
当前实现状态
已完成：

YOLO Studio 主导航重构
YOLO 数据集体检
data.yaml 生成
环境检测与安装建议
本机 YOLO 训练入口
YOLO 推理检测入口
runs 结果扫描
原数据准备功能合并到 数据准备 标签页
待增强：

训练曲线图内嵌预览
检测结果缩略图浏览
权重一键带入检测页
ONNX/TensorRT 导出
姿态估计、OBB、跟踪任务
常见问题
1. 提示没有 ultralytics
执行：

python -m pip install -U ultralytics
2. GPU 不可用
先确认显卡驱动和 CUDA 环境，再安装匹配的 PyTorch。不要盲目升级 CUDA 或 torch，优先按 PyTorch 官网给出的命令安装。

3. 训练时窗口是否会卡死
不会。训练和检测通过子进程执行，日志会实时回传到界面。

4. 分类任务为什么不生成 data.yaml
Ultralytics 分类任务通常直接使用分类数据集根目录，目录名就是类别名，因此不强制需要 data.yaml。

5. 旧的格式转换和数据划分去哪了
已合并到 数据准备 页面：

格式转换
数据划分
分析报告
可视化预览
开发验证
可运行以下命令做基础检查：

python -m py_compile dataset_converter/main.py
python -m py_compile dataset_converter/src/gui/yolo_panels.py
python -m py_compile dataset_converter/src/core/yolo_services.py
python -m py_compile dataset_converter/src/core/yolo_cli_runner.py
离屏实例化检查：

set QT_QPA_PLATFORM=offscreen
python -c "import sys; from PyQt5.QtWidgets import QApplication; from dataset_converter.src.gui.simple_home_window import SimpleHomeWindow; app=QApplication(sys.argv); w=SimpleHomeWindow(); print(w.windowTitle(), len(w.panels))"

说明
本项目当前以本机桌面训练和检测为主，不包含远程服务器训练、SSH 同步、任务队列等能力。环境配置模块只做检测和引导，不会自动安装或修改用户环境。
