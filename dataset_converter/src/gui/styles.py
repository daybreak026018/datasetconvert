"""
统一的GUI样式管理器
"""

class AppStyles:
    """应用程序样式定义"""
    
    # 颜色定义
    PRIMARY_COLOR = "#2ecc71"      # 主色调 - 绿色
    SUCCESS_COLOR = "#2ecc71"      # 成功色 - 绿色
    WARNING_COLOR = "#f1c40f"      # 警告色 - 黄色
    DANGER_COLOR = "#e74c3c"       # 危险色 - 红色
    BACKGROUND_COLOR = "#ecf0f1"   # 背景色 - 浅灰
    CARD_COLOR = "#ffffff"         # 卡片色 - 白色
    TEXT_COLOR = "#2c3e50"         # 文本色 - 深蓝灰
    SECONDARY_TEXT = "#7f8c8d"     # 次要文本 - 灰
    BORDER_COLOR = "#bdc3c7"       # 边框色 - 浅灰
    
    # 侧边栏和头部颜色
    SIDEBAR_BG = "#2c3e50"         # 侧边栏背景 - 深色
    SIDEBAR_TEXT = "#ecf0f1"       # 侧边栏文字 - 浅色
    HEADER_BG = "#27ae60"          # 头部背景 - 深绿色
    
    @staticmethod
    def get_main_window_style():
        """主窗口样式"""
        return f"""
        QMainWindow {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
        }}
        
        /* 侧边栏样式 */
        QFrame#sidebar {{
            background-color: {AppStyles.SIDEBAR_BG};
            border: none;
        }}
        
        /* 顶部标题栏样式 */
        QFrame#header {{
            background-color: {AppStyles.HEADER_BG};
            border: none;
        }}
        
        QLabel#headerTitle {{
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding-left: 20px;
        }}
        
        /* 导航按钮通用样式 */
        QFrame#navButton {{
            background-color: transparent;
            border: none;
            border-radius: 0px;
            margin: 0px;
            padding: 0px;
        }}
        
        QFrame#navButton:hover {{
            background-color: #34495e;  /* 稍微亮一点的深色 */
        }}
        
        /* 选中状态 */
        QFrame#navButton[selected="true"] {{
            background-color: #27ae60;  /* 绿色高亮 */
            border-left: 4px solid #2ecc71;
        }}
        
        /* 图标标签 */
        QLabel[class="navIcon"] {{
            background-color: transparent;
            padding: 0px;
        }}
        
        /* 文字标签 */
        QLabel[class="navText"] {{
            color: {AppStyles.SIDEBAR_TEXT};
            font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
            font-size: 14px;
            font-weight: 500;
        }}
        
        /* 选中状态下的文字颜色 */
        QFrame#navButton[selected="true"] QLabel[class="navText"] {{
            color: white;
            font-weight: bold;
        }}
        
        /* 内容区域卡片 */
        QGroupBox, QScrollArea, QListWidget {{
            background-color: {AppStyles.CARD_COLOR};
            border: 1px solid {AppStyles.BORDER_COLOR};
            border-radius: 4px;
        }}
        
        /* 分割线样式 */
        QFrame[class="navSeparator"] {{
            color: #D1D5DB;  /* 浅灰色 */
            border: none;
            background-color: #E9ECEF;
            width: 1px;
            margin: 0px 5px;
        }}
        """
    
    @staticmethod
    def get_panel_style():
        """面板通用样式"""
        return f"""
        QWidget {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            color: {AppStyles.TEXT_COLOR};
            font-family: "SimSun", "宋体", serif;
            font-size: 12px;
        }}
        
        QGroupBox {{
            background-color: {AppStyles.CARD_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 10px;
            margin-top: 10px;
            padding-top: 10px;
            font-weight: bold;
            font-size: 13px;
            font-family: "SimSun", "宋体", serif;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 8px 0 8px;
            color: {AppStyles.PRIMARY_COLOR};
        }}
        
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}
        
        QScrollBar:vertical {
            background-color: {AppStyles.BACKGROUND_COLOR};
            width: 10px;
            border-radius: 5px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: {AppStyles.BORDER_COLOR};
            border-radius: 5px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: {AppStyles.SECONDARY_TEXT};
        }

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }

        QScrollBar:horizontal {
            background-color: {AppStyles.BACKGROUND_COLOR};
            height: 10px;
            border-radius: 5px;
            margin: 0px;
        }
        
        QScrollBar::handle:horizontal {
            background-color: {AppStyles.BORDER_COLOR};
            border-radius: 5px;
            min-width: 20px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: {AppStyles.SECONDARY_TEXT};
        }

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
            width: 0px;
        }
        """
    
    @staticmethod
    def get_button_style(button_type="default"):
        """按钮样式"""
        styles = {
            "default": f"""
                QPushButton {{
                    background-color: {AppStyles.CARD_COLOR};
                    border: 2px solid {AppStyles.BORDER_COLOR};
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: 500;
                    font-family: "SimSun", "宋体", serif;
                    color: {AppStyles.TEXT_COLOR};
                }}
                
                QPushButton:hover {{
                    background-color: #E3F2FD;
                    border-color: {AppStyles.PRIMARY_COLOR};
                }}
                
                QPushButton:pressed {{
                    background-color: {AppStyles.PRIMARY_COLOR};
                    color: white;
                }}
            """,
            
            "primary": f"""
                QPushButton {{
                    background-color: {AppStyles.PRIMARY_COLOR};
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    font-family: "SimSun", "宋体", serif;
                    color: white;
                }}
                
                QPushButton:hover {{
                    background-color: #1976D2;
                }}
                
                QPushButton:pressed {{
                    background-color: #0D47A1;
                }}
            """,
            
            "success": f"""
                QPushButton {{
                    background-color: {AppStyles.SUCCESS_COLOR};
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 13px;
                    font-weight: bold;
                    font-family: "SimSun", "宋体", serif;
                    color: white;
                }}
                
                QPushButton:hover {{
                    background-color: #388E3C;
                }}
                
                QPushButton:pressed {{
                    background-color: #1B5E20;
                }}
            """,
            
            "warning": f"""
                QPushButton {{
                    background-color: {AppStyles.WARNING_COLOR};
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: 500;
                    font-family: "SimSun", "宋体", serif;
                    color: white;
                }}
                
                QPushButton:hover {{
                    background-color: #F57C00;
                }}
            """,
            
            "danger": f"""
                QPushButton {{
                    background-color: {AppStyles.DANGER_COLOR};
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-size: 12px;
                    font-weight: 500;
                    font-family: "SimSun", "宋体", serif;
                    color: white;
                }}
                
                QPushButton:hover {{
                    background-color: #D32F2F;
                }}
            """
        }
        
        return styles.get(button_type, styles["default"])
    
    @staticmethod
    def get_label_style(label_type="default"):
        """标签样式"""
        styles = {
            "default": f"""
                QLabel {{
                    color: {AppStyles.TEXT_COLOR};
                    font-size: 12px;
                    font-family: "SimSun", "宋体", serif;
                }}
            """,
            
            "title": f"""
                QLabel {{
                    color: {AppStyles.PRIMARY_COLOR};
                    font-size: 14px;
                    font-weight: bold;
                    font-family: "SimSun", "宋体", serif;
                    padding: 5px;
                }}
            """,
            
            "subtitle": f"""
                QLabel {{
                    color: {AppStyles.SECONDARY_TEXT};
                    font-size: 11px;
                    font-style: italic;
                    font-family: "SimSun", "宋体", serif;
                }}
            """,
            
            "status": f"""
                QLabel {{
                    background-color: {AppStyles.CARD_COLOR};
                    border: 1px solid {AppStyles.BORDER_COLOR};
                    border-radius: 6px;
                    padding: 6px 10px;
                    font-size: 12px;
                    font-family: "SimSun", "宋体", serif;
                }}
            """
        }
        
        return styles.get(label_type, styles["default"])
    
    @staticmethod
    def get_textedit_style():
        """文本编辑框样式"""
        return f"""
        QTextEdit {{
            background-color: {AppStyles.CARD_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            padding: 8px;
            font-family: "SimSun", "宋体", serif;
            font-size: 11px;
            line-height: 1.4;
        }}
        
        QTextEdit:focus {{
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        """
    
    @staticmethod
    def get_progressbar_style():
        """进度条样式"""
        return f"""
        QProgressBar {{
            background-color: {AppStyles.BACKGROUND_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 8px;
            text-align: center;
            font-size: 11px;
            font-weight: bold;
            font-family: "SimSun", "宋体", serif;
        }}
        
        QProgressBar::chunk {{
            background-color: {AppStyles.PRIMARY_COLOR};
            border-radius: 6px;
        }}
        """
    
    @staticmethod
    def get_combobox_style():
        """下拉框样式"""
        return f"""
        QComboBox {{
            background-color: {AppStyles.CARD_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 6px;
            padding: 6px 10px;
            font-size: 12px;
            font-family: "SimSun", "宋体", serif;
        }}
        
        QComboBox:hover {{
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid {AppStyles.SECONDARY_TEXT};
        }}
        """
    
    @staticmethod
    def get_checkbox_style():
        """复选框样式"""
        return f"""
        QCheckBox {{
            font-size: 12px;
            font-family: "SimSun", "宋体", serif;
            color: {AppStyles.TEXT_COLOR};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 16px;
            height: 16px;
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 3px;
            background-color: {AppStyles.CARD_COLOR};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {AppStyles.PRIMARY_COLOR};
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        """
    
    @staticmethod
    def get_spinbox_style():
        """数字输入框样式"""
        return f"""
        QSpinBox {{
            background-color: {AppStyles.CARD_COLOR};
            border: 2px solid {AppStyles.BORDER_COLOR};
            border-radius: 6px;
            padding: 6px;
            font-size: 12px;
            font-family: "SimSun", "宋体", serif;
        }}
        
        QSpinBox:focus {{
            border-color: {AppStyles.PRIMARY_COLOR};
        }}
        """