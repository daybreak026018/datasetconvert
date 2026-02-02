"""
简洁版高级功能面板
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt


class SimpleAdvancedPanel(QWidget):
    """简洁版高级功能面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # AI功能卡片
        ai_card = QGroupBox("AI功能")
        ai_layout = QGridLayout(ai_card)
        ai_layout.setSpacing(15)
        
        # AI质量检测
        btn_quality = QPushButton("AI质量检测")
        btn_quality.setProperty("buttonType", "primary")
        ai_layout.addWidget(btn_quality, 0, 0)
        
        # 智能标注
        btn_auto_label = QPushButton("智能标注")
        btn_auto_label.setProperty("buttonType", "success")
        ai_layout.addWidget(btn_auto_label, 0, 1)
        
        layout.addWidget(ai_card)
        
        # 批处理功能卡片
        batch_card = QGroupBox("批处理功能")
        batch_layout = QGridLayout(batch_card)
        batch_layout.setSpacing(15)
        
        # 批量处理
        btn_batch = QPushButton("批量图片处理")
        btn_batch.setProperty("buttonType", "warning")
        batch_layout.addWidget(btn_batch, 0, 0)
        
        # 批量转换
        btn_batch_convert = QPushButton("批量格式转换")
        btn_batch_convert.setProperty("buttonType", "primary")
        batch_layout.addWidget(btn_batch_convert, 0, 1)
        
        layout.addWidget(batch_card)
        
        layout.addStretch()