"""
简洁版协作标注面板
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox
)
from PyQt5.QtCore import Qt


class SimpleCollaborationPanel(QWidget):
    """简洁版协作标注面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 功能卡片
        card = QGroupBox("协作标注")
        card_layout = QVBoxLayout(card)
        
        # 描述
        desc_label = QLabel("管理多人协作标注项目")
        desc_label.setStyleSheet("color: #6c757d; margin-bottom: 20px;")
        card_layout.addWidget(desc_label)
        
        # 功能按钮
        btn_split = QPushButton("数据集划分")
        btn_split.setProperty("buttonType", "primary")
        
        btn_manage = QPushButton("项目管理")
        btn_manage.setProperty("buttonType", "success")
        
        card_layout.addWidget(btn_split)
        card_layout.addWidget(btn_manage)
        
        layout.addWidget(card)
        layout.addStretch()