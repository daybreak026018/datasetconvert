from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QGridLayout, QProgressBar, QScrollArea, QPushButton
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen

from .styles import AppStyles

class StatsCard(QFrame):
    """统计卡片组件"""
    def __init__(self, title, value, icon_name="📊", trend="+0%", trend_color="#2ecc71", parent=None):
        super().__init__(parent)
        self.setObjectName("statsCard")
        self.setStyleSheet(f"""
            QFrame#statsCard {{
                background-color: {AppStyles.CARD_COLOR};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 8px;
            }}
            QLabel {{ border: none; background: transparent; }}
        """)
        self.setFixedSize(240, 120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 顶部：标题和图标
        top_layout = QHBoxLayout()
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {AppStyles.SECONDARY_TEXT}; font-size: 13px; font-weight: bold;")
        top_layout.addWidget(title_label)
        top_layout.addStretch()
        
        icon_label = QLabel(icon_name)
        icon_label.setStyleSheet("font-size: 18px;")
        top_layout.addWidget(icon_label)
        layout.addLayout(top_layout)
        
        # 中部：数值
        value_label = QLabel(value)
        value_label.setStyleSheet(f"color: {AppStyles.TEXT_COLOR}; font-size: 28px; font-weight: bold;")
        layout.addWidget(value_label)
        
        # 底部：趋势
        trend_label = QLabel(f"{trend} 较上周")
        trend_label.setStyleSheet(f"color: {trend_color}; font-size: 12px;")
        layout.addWidget(trend_label)

class SimpleBarChart(QFrame):
    """简单的柱状图组件 (模拟)"""
    def __init__(self, title, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setObjectName("chartCard")
        self.setStyleSheet(f"""
            QFrame#chartCard {{
                background-color: {AppStyles.CARD_COLOR};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {AppStyles.TEXT_COLOR}; font-size: 16px; font-weight: bold;")
        layout.addWidget(title_label)
        
        # 图表区域
        chart_area = QWidget()
        chart_layout = QHBoxLayout(chart_area)
        chart_layout.setAlignment(Qt.AlignBottom)
        chart_layout.setSpacing(15)
        
        max_val = max(data.values()) if data else 1
        
        colors = ["#3498db", "#e74c3c", "#f1c40f", "#2ecc71", "#9b59b6"]
        
        for i, (label, value) in enumerate(data.items()):
            bar_container = QWidget()
            bar_layout = QVBoxLayout(bar_container)
            bar_layout.setAlignment(Qt.AlignBottom)
            bar_layout.setContentsMargins(0, 0, 0, 0)
            
            # 柱子
            height = int((value / max_val) * 150)
            bar = QFrame()
            bar.setFixedSize(40, height)
            color = colors[i % len(colors)]
            bar.setStyleSheet(f"background-color: {color}; border-radius: 4px;")
            bar_layout.addWidget(bar)
            
            # 标签
            lbl = QLabel(label)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(f"color: {AppStyles.SECONDARY_TEXT}; font-size: 11px;")
            bar_layout.addWidget(lbl)
            
            chart_layout.addWidget(bar_container)
            
        layout.addWidget(chart_area)

class VisualizationPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 使用滚动区域，防止内容过多
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        
        content_widget = QWidget()
        self.layout = QVBoxLayout(content_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # 1. 统计卡片区域
        stats_layout = QGridLayout()
        stats_layout.setSpacing(20)
        
        # 模拟数据
        # 使用 2x2 网格布局，防止在小屏幕上出现水平滚动条
        stats_layout.addWidget(StatsCard("总图片数", "12,450", "🖼️", "+5%", "#2ecc71"), 0, 0)
        stats_layout.addWidget(StatsCard("已标注", "8,320", "🏷️", "+12%", "#2ecc71"), 0, 1)
        stats_layout.addWidget(StatsCard("待处理", "4,130", "⏳", "-2%", "#e74c3c"), 1, 0)
        stats_layout.addWidget(StatsCard("类别数", "15", "📦", "0%", "#95a5a6"), 1, 1)
        
        # 保持左对齐
        stats_layout.setColumnStretch(2, 1)
        
        self.layout.addLayout(stats_layout)
        
        # 2. 图表区域
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # 类别分布图
        class_data = {"Car": 450, "Pedestrian": 320, "Cyclist": 150, "Truck": 210, "Bus": 80}
        charts_layout.addWidget(SimpleBarChart("类别分布 (Top 5)", class_data))
        
        # 数据集增长图 (模拟)
        growth_data = {"Jan": 100, "Feb": 250, "Mar": 400, "Apr": 380, "May": 520}
        charts_layout.addWidget(SimpleBarChart("月度数据增长", growth_data))
        
        self.layout.addLayout(charts_layout)
        
        # 3. 最近活动列表
        recent_panel = QFrame()
        recent_panel.setObjectName("recentPanel")
        recent_panel.setStyleSheet(f"""
            QFrame#recentPanel {{
                background-color: {AppStyles.CARD_COLOR};
                border: 1px solid {AppStyles.BORDER_COLOR};
                border-radius: 8px;
            }}
        """)
        recent_layout = QVBoxLayout(recent_panel)
        
        recent_header = QLabel("最近活动")
        recent_header.setStyleSheet(f"color: {AppStyles.TEXT_COLOR}; font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        recent_layout.addWidget(recent_header)
        
        activities = [
            ("Admin", "导出数据集到 YOLO 格式", "10分钟前"),
            ("User1", "上传了 500 张新图片", "1小时前"),
            ("Admin", "完成了 'Vehicles' 数据集划分", "2小时前"),
            ("User2", "更新了标注规范", "昨天")
        ]
        
        for user, action, time in activities:
            item = QWidget()
            item_layout = QHBoxLayout(item)
            item_layout.setContentsMargins(0, 5, 0, 5)
            
            user_lbl = QLabel(user)
            user_lbl.setStyleSheet(f"color: {AppStyles.PRIMARY_COLOR}; font-weight: bold;")
            item_layout.addWidget(user_lbl)
            
            action_lbl = QLabel(action)
            action_lbl.setStyleSheet(f"color: {AppStyles.TEXT_COLOR};")
            item_layout.addWidget(action_lbl)
            
            item_layout.addStretch()
            
            time_lbl = QLabel(time)
            time_lbl.setStyleSheet(f"color: {AppStyles.SECONDARY_TEXT}; font-size: 12px;")
            item_layout.addWidget(time_lbl)
            
            recent_layout.addWidget(item)
            # 分割线
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet(f"background-color: {AppStyles.BACKGROUND_COLOR}; max-height: 1px; border: none;")
            recent_layout.addWidget(line)
            
        self.layout.addWidget(recent_panel)
        self.layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
