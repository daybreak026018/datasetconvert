"""
简洁版数据分析面板
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox
)
from PyQt5.QtCore import Qt


class SimpleAnalysisPanel(QWidget):
    """简洁版数据分析面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 功能卡片
        card = QGroupBox("数据集分析")
        card_layout = QVBoxLayout(card)
        
        # 描述
        desc_label = QLabel("分析数据集的统计信息、类别分布、质量评估等")
        desc_label.setStyleSheet("color: #6c757d; margin-bottom: 20px;")
        card_layout.addWidget(desc_label)
        
        # 功能按钮
        btn_stats = QPushButton("统计信息")
        btn_stats.setProperty("buttonType", "primary")
        
        btn_distribution = QPushButton("类别分布")
        btn_distribution.setProperty("buttonType", "success")
        
        btn_quality = QPushButton("质量评估")
        btn_quality.setProperty("buttonType", "warning")
        
        card_layout.addWidget(btn_stats)
        card_layout.addWidget(btn_distribution)
        card_layout.addWidget(btn_quality)
        
        layout.addWidget(card)
        layout.addStretch()