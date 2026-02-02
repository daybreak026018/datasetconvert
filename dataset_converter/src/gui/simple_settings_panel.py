"""
简洁版设置面板
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGroupBox, 
    QComboBox, QCheckBox, QGridLayout
)
from PyQt5.QtCore import Qt


class SimpleSettingsPanel(QWidget):
    """简洁版设置面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # 界面设置卡片
        ui_card = QGroupBox("界面设置")
        ui_layout = QGridLayout(ui_card)
        ui_layout.setSpacing(15)
        
        # 主题选择
        ui_layout.addWidget(QLabel("主题:"), 0, 0)
        theme_combo = QComboBox()
        theme_combo.addItems(["浅色", "深色", "自动"])
        ui_layout.addWidget(theme_combo, 0, 1)
        
        # 语言选择
        ui_layout.addWidget(QLabel("语言:"), 1, 0)
        lang_combo = QComboBox()
        lang_combo.addItems(["中文", "English"])
        ui_layout.addWidget(lang_combo, 1, 1)
        
        layout.addWidget(ui_card)
        
        # 功能设置卡片
        func_card = QGroupBox("功能设置")
        func_layout = QVBoxLayout(func_card)
        
        # 自动保存
        auto_save_check = QCheckBox("自动保存")
        auto_save_check.setChecked(True)
        func_layout.addWidget(auto_save_check)
        
        # 显示提示
        show_tips_check = QCheckBox("显示操作提示")
        show_tips_check.setChecked(True)
        func_layout.addWidget(show_tips_check)
        
        layout.addWidget(func_card)
        
        # 操作按钮
        btn_layout = QVBoxLayout()
        
        btn_save = QPushButton("保存设置")
        btn_save.setProperty("buttonType", "primary")
        
        btn_reset = QPushButton("恢复默认")
        btn_reset.setProperty("buttonType", "warning")
        
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_reset)
        
        layout.addLayout(btn_layout)
        layout.addStretch()