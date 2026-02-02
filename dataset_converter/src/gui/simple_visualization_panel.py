"""
简洁版数据可视化面板
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox
)
from PyQt5.QtCore import Qt


class SimpleVisualizationPanel(QWidget):
    """简洁版数据可视化面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 功能卡片
        card = QGroupBox("数据可视化")
        card_layout = QVBoxLayout(card)
        
        # 描述
        desc_label = QLabel("生成数据集的可视化图表和报告")
        desc_label.setStyleSheet("color: #6c757d; margin-bottom: 20px;")
        card_layout.addWidget(desc_label)
        
        # 功能按钮
        btn_charts = QPushButton("生成图表")
        btn_charts.setProperty("buttonType", "primary")
        
        btn_report = QPushButton("生成报告")
        btn_report.setProperty("buttonType", "success")
        
        card_layout.addWidget(btn_charts)
        card_layout.addWidget(btn_report)
        
        layout.addWidget(card)
        layout.addStretch()