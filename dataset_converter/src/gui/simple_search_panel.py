"""
简洁版数据搜索面板
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QLineEdit
)
from PyQt5.QtCore import Qt


class SimpleSearchPanel(QWidget):
    """简洁版数据搜索面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 搜索卡片
        card = QGroupBox("数据搜索")
        card_layout = QVBoxLayout(card)
        
        # 描述
        desc_label = QLabel("搜索和筛选数据集中的图片和标注")
        desc_label.setStyleSheet("color: #6c757d; margin-bottom: 20px;")
        card_layout.addWidget(desc_label)
        
        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入搜索关键词...")
        card_layout.addWidget(self.search_input)
        
        # 搜索按钮
        btn_search = QPushButton("开始搜索")
        btn_search.setProperty("buttonType", "primary")
        card_layout.addWidget(btn_search)
        
        layout.addWidget(card)
        layout.addStretch()