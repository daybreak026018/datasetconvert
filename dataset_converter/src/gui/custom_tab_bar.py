"""
自定义选项卡栏 - 解决中文文本省略问题
"""

from PyQt5.QtWidgets import QTabBar, QTabWidget
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QFontMetrics


class CustomTabBar(QTabBar):
    """自定义选项卡栏，确保中文文本不被省略"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setElideMode(Qt.ElideNone)
        self.setExpanding(True)
        self.setUsesScrollButtons(False)
        
        # 延迟配置定时器
        self.config_timer = QTimer()
        self.config_timer.setSingleShot(True)
        self.config_timer.timeout.connect(self._force_configure)
        
        # 记录最小宽度要求
        self.min_width_required = 0
        
    def addTab(self, *args, **kwargs):
        """重写添加选项卡方法"""
        result = super().addTab(*args, **kwargs)
        # 立即计算并设置最小宽度
        self._calculate_minimum_width()
        # 延迟配置以确保文本正确显示
        self.config_timer.start(50)
        return result
    
    def insertTab(self, *args, **kwargs):
        """重写插入选项卡方法"""
        result = super().insertTab(*args, **kwargs)
        # 立即计算并设置最小宽度
        self._calculate_minimum_width()
        # 延迟配置以确保文本正确显示
        self.config_timer.start(50)
        return result
    
    def _calculate_minimum_width(self):
        """计算所有选项卡需要的最小总宽度"""
        if self.count() == 0:
            return
            
        font_metrics = QFontMetrics(self.font())
        total_width = 0
        
        for i in range(self.count()):
            tab_text = self.tabText(i)
            if tab_text:
                # 计算文本宽度，为中文字符留出更多空间
                text_width = font_metrics.width(tab_text)
                # 每个选项卡需要的宽度：文本宽度 + 内边距 + 边框 + 间距
                tab_width = text_width + 60  # 60像素用于内边距、边框等
                total_width += tab_width
        
        # 添加选项卡之间的间距
        total_width += (self.count() - 1) * 4  # 每个间距4像素
        
        self.min_width_required = total_width
        
        # 设置选项卡栏的最小宽度
        self.setMinimumWidth(total_width)
        
        # 通知父控件更新最小宽度
        if self.parent():
            self.parent().setMinimumWidth(total_width + 20)  # 额外20像素边距
    
    def _force_configure(self):
        """强制配置选项卡显示"""
        try:
            # 设置基本属性
            self.setElideMode(Qt.ElideNone)
            self.setExpanding(True)
            self.setUsesScrollButtons(False)
            
            # 重新计算最小宽度
            self._calculate_minimum_width()
            
            # 计算并设置每个选项卡的最小宽度
            font_metrics = QFontMetrics(self.font())
            
            for i in range(self.count()):
                tab_text = self.tabText(i)
                if tab_text:
                    # 计算文本宽度，为中文字符留出更多空间
                    text_width = font_metrics.width(tab_text)
                    min_width = text_width + 60  # 额外60像素用于边距和图标
                    
                    # 清除可能导致省略的按钮
                    self.setTabButton(i, QTabBar.LeftSide, None)
                    self.setTabButton(i, QTabBar.RightSide, None)
            
            # 强制更新布局和重绘
            self.updateGeometry()
            self.update()
            
        except Exception as e:
            print(f"配置选项卡时出错: {e}")
    
    def resizeEvent(self, event):
        """重写大小调整事件"""
        super().resizeEvent(event)
        # 确保有足够空间显示所有选项卡
        if event.size().width() < self.min_width_required:
            # 如果当前宽度不足，设置最小宽度
            self.setMinimumWidth(self.min_width_required)
        # 在大小调整后重新配置
        self.config_timer.start(10)
    
    def showEvent(self, event):
        """重写显示事件"""
        super().showEvent(event)
        # 在显示时重新配置
        self._calculate_minimum_width()
        self.config_timer.start(10)
    
    def sizeHint(self):
        """重写尺寸提示"""
        hint = super().sizeHint()
        # 确保宽度足够显示所有选项卡
        if self.min_width_required > 0:
            hint.setWidth(max(hint.width(), self.min_width_required))
        return hint
    
    def minimumSizeHint(self):
        """重写最小尺寸提示"""
        hint = super().minimumSizeHint()
        # 确保最小宽度足够显示所有选项卡
        if self.min_width_required > 0:
            hint.setWidth(max(hint.width(), self.min_width_required))
        return hint


class CustomTabWidget(QTabWidget):
    """自定义选项卡控件，使用自定义选项卡栏"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 使用自定义选项卡栏
        self.custom_tab_bar = CustomTabBar()
        self.setTabBar(self.custom_tab_bar)
        
        # 设置基本属性
        self.setTabsClosable(False)
        self.setMovable(False)
        self.setUsesScrollButtons(False)
        self.setElideMode(Qt.ElideNone)
        
        # 延迟配置定时器
        self.config_timer = QTimer()
        self.config_timer.setSingleShot(True)
        self.config_timer.timeout.connect(self._configure_display)
        
        # 设置选项卡位置，确保有足够空间
        self.setTabPosition(QTabWidget.North)
    
    def addTab(self, widget, label):
        """重写添加选项卡方法"""
        result = super().addTab(widget, label)
        # 延迟配置以确保显示正确
        self.config_timer.start(50)
        return result
    
    def insertTab(self, index, widget, label):
        """重写插入选项卡方法"""
        result = super().insertTab(index, widget, label)
        # 延迟配置以确保显示正确
        self.config_timer.start(50)
        return result
    
    def _configure_display(self):
        """配置选项卡显示"""
        try:
            if hasattr(self.custom_tab_bar, '_force_configure'):
                self.custom_tab_bar._force_configure()
        except Exception as e:
            print(f"配置选项卡控件时出错: {e}")
    
    def showEvent(self, event):
        """重写显示事件"""
        super().showEvent(event)
        # 在显示时配置
        self.config_timer.start(10)
    
    def resizeEvent(self, event):
        """重写大小调整事件"""
        super().resizeEvent(event)
        # 确保选项卡栏有足够空间
        if hasattr(self.custom_tab_bar, 'min_width_required'):
            min_width = self.custom_tab_bar.min_width_required
            if event.size().width() < min_width:
                # 如果窗口宽度不足，设置最小宽度
                self.setMinimumWidth(min_width + 40)  # 额外40像素边距
        # 在大小调整后配置
        self.config_timer.start(10)
    
    def sizeHint(self):
        """重写尺寸提示"""
        hint = super().sizeHint()
        # 确保宽度足够显示所有选项卡
        if hasattr(self.custom_tab_bar, 'min_width_required'):
            min_width = self.custom_tab_bar.min_width_required
            if min_width > 0:
                hint.setWidth(max(hint.width(), min_width + 40))
        return hint
    
    def minimumSizeHint(self):
        """重写最小尺寸提示"""
        hint = super().minimumSizeHint()
        # 确保最小宽度足够显示所有选项卡
        if hasattr(self.custom_tab_bar, 'min_width_required'):
            min_width = self.custom_tab_bar.min_width_required
            if min_width > 0:
                hint.setWidth(max(hint.width(), min_width + 40))
        return hint