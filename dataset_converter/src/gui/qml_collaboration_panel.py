"""
QML风格协作标注面板
"""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QProgressBar, QFrame,
    QGridLayout, QLineEdit, QComboBox, QListWidget, QListWidgetItem,
    QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor

from .qml_style_window import Card


class CollaborationWorker(QThread):
    """协作工作线程"""
    progress_updated = pyqtSignal(int, str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, action, params):
        super().__init__()
        self.action = action
        self.params = params
    
    def run(self):
        try:
            self.progress_updated.emit(10, f"正在{self.action}...")
            
            # 模拟协作操作
            import time
            for i in range(10, 101, 20):
                time.sleep(0.3)
                if i == 30:
                    self.progress_updated.emit(i, "正在连接服务器...")
                elif i == 50:
                    self.progress_updated.emit(i, "正在同步数据...")
                elif i == 70:
                    self.progress_updated.emit(i, "正在更新状态...")
                elif i == 90:
                    self.progress_updated.emit(i, "正在完成操作...")
                else:
                    self.progress_updated.emit(i, f"{self.action}进度 {i}%")
            
            self.progress_updated.emit(100, f"{self.action}完成")
            self.finished.emit(True, f"{self.action}成功完成！")
            
        except Exception as e:
            self.finished.emit(False, f"{self.action}失败: {str(e)}")


class UserCard(QFrame):
    """用户卡片组件"""
    
    def __init__(self, username="", role="", status="offline", parent=None):
        super().__init__(parent)
        self.username = username
        self.role = role
        self.status = status
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # 头像
        avatar_label = QLabel("👤")
        avatar_label.setObjectName("avatar")
        avatar_label.setFixedSize(32, 32)
        avatar_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(avatar_label)
        
        # 用户信息
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # 用户名
        username_label = QLabel(self.username)
        username_label.setObjectName("username")
        info_layout.addWidget(username_label)
        
        # 角色
        role_label = QLabel(self.role)
        role_label.setObjectName("role")
        info_layout.addWidget(role_label)
        
        layout.addLayout(info_layout, 1)
        
        # 状态指示器
        self.status_indicator = QFrame()
        self.status_indicator.setObjectName("statusIndicator")
        self.status_indicator.setFixedSize(12, 12)
        layout.addWidget(self.status_indicator)
    
    def setup_style(self):
        """设置样式"""
        status_color = "#10b981" if self.status == "online" else "#6b7280"
        
        self.setStyleSheet(f"""
            UserCard {{
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }}
            
            UserCard:hover {{
                border-color: #cbd5e1;
                background-color: #f8fafc;
            }}
            
            #avatar {{
                font-size: 20px;
                color: #3b82f6;
                background-color: #eff6ff;
                border-radius: 16px;
            }}
            
            #username {{
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }}
            
            #role {{
                font-size: 12px;
                color: #6b7280;
            }}
            
            #statusIndicator {{
                background-color: {status_color};
                border-radius: 6px;
            }}
        """)


class TaskItem(QFrame):
    """任务项组件"""
    
    def __init__(self, task_data, parent=None):
        super().__init__(parent)
        self.task_data = task_data
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        
        # 任务标题和状态
        header_layout = QHBoxLayout()
        
        title_label = QLabel(self.task_data['title'])
        title_label.setObjectName("taskTitle")
        header_layout.addWidget(title_label, 1)
        
        status_label = QLabel(self.task_data['status'])
        status_label.setObjectName("taskStatus")
        header_layout.addWidget(status_label)
        
        layout.addLayout(header_layout)
        
        # 任务描述
        desc_label = QLabel(self.task_data['description'])
        desc_label.setObjectName("taskDesc")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # 任务信息
        info_layout = QHBoxLayout()
        
        assignee_label = QLabel(f"负责人: {self.task_data['assignee']}")
        assignee_label.setObjectName("taskInfo")
        info_layout.addWidget(assignee_label)
        
        info_layout.addStretch()
        
        progress_label = QLabel(f"进度: {self.task_data['progress']}%")
        progress_label.setObjectName("taskInfo")
        info_layout.addWidget(progress_label)
        
        layout.addLayout(info_layout)
    
    def setup_style(self):
        """设置样式"""
        status_colors = {
            "进行中": "#3b82f6",
            "已完成": "#10b981",
            "待开始": "#f59e0b",
            "已暂停": "#ef4444"
        }
        status_color = status_colors.get(self.task_data['status'], "#6b7280")
        
        self.setStyleSheet(f"""
            TaskItem {{
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                margin: 2px 0;
            }}
            
            TaskItem:hover {{
                border-color: #3b82f6;
                background-color: #f8fafc;
            }}
            
            #taskTitle {{
                font-size: 14px;
                font-weight: 600;
                color: #374151;
            }}
            
            #taskStatus {{
                font-size: 12px;
                font-weight: 500;
                color: {status_color};
                background-color: {status_color}20;
                padding: 4px 8px;
                border-radius: 4px;
            }}
            
            #taskDesc {{
                font-size: 13px;
                color: #6b7280;
            }}
            
            #taskInfo {{
                font-size: 12px;
                color: #9ca3af;
            }}
        """)


class QMLCollaborationPanel(QWidget):
    """QML风格协作标注面板"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.worker = None
        self.project_path = ""
        self.current_user = "当前用户"
        
        # 设置大小策略
        from PyQt5.QtWidgets import QSizePolicy
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.init_ui()
        self.load_sample_data()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(24)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 项目设置卡片
        project_card = Card("📁 项目设置")
        project_layout = QVBoxLayout()
        project_layout.setSpacing(12)
        
        # 项目路径
        path_layout = QHBoxLayout()
        path_layout.setSpacing(12)
        
        self.project_label = QLabel("未选择项目")
        self.project_label.setObjectName("projectLabel")
        self.project_label.setStyleSheet("""
            #projectLabel {
                background-color: white;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 12px 16px;
                color: #6b7280;
                font-style: italic;
            }
        """)
        path_layout.addWidget(self.project_label, 1)
        
        select_btn = QPushButton("选择项目")
        select_btn.setProperty("buttonType", "primary")
        select_btn.clicked.connect(self.select_project)
        path_layout.addWidget(select_btn)
        
        project_layout.addLayout(path_layout)
        
        # 用户信息
        user_layout = QHBoxLayout()
        user_layout.setSpacing(12)
        
        user_label = QLabel("当前用户:")
        user_label.setStyleSheet("font-weight: 600; color: #374151;")
        user_layout.addWidget(user_label)
        
        self.user_input = QLineEdit(self.current_user)
        self.user_input.setPlaceholderText("输入用户名...")
        user_layout.addWidget(self.user_input, 1)
        
        role_label = QLabel("角色:")
        role_label.setStyleSheet("font-weight: 600; color: #374151;")
        user_layout.addWidget(role_label)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(["标注员", "审核员", "项目经理", "管理员"])
        user_layout.addWidget(self.role_combo)
        
        project_layout.addLayout(user_layout)
        project_card.add_layout(project_layout)
        layout.addWidget(project_card)
        
        # 团队成员卡片
        team_card = Card("👥 团队成员")
        team_layout = QVBoxLayout()
        team_layout.setSpacing(12)
        
        # 成员列表
        self.team_list = QListWidget()
        self.team_list.setMinimumHeight(120)  # 设置最小高度
        self.team_list.setMaximumHeight(180)  # 增加最大高度
        self.team_list.setStyleSheet("""
            QListWidget {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 2px;
            }
        """)
        team_layout.addWidget(self.team_list)
        
        # 添加成员
        add_member_layout = QHBoxLayout()
        add_member_layout.setSpacing(8)
        
        self.member_input = QLineEdit()
        self.member_input.setPlaceholderText("输入成员用户名...")
        add_member_layout.addWidget(self.member_input, 1)
        
        add_btn = QPushButton("添加成员")
        add_btn.setProperty("buttonType", "success")
        add_btn.clicked.connect(self.add_member)
        add_member_layout.addWidget(add_btn)
        
        team_layout.addLayout(add_member_layout)
        team_card.add_layout(team_layout)
        layout.addWidget(team_card)
        
        # 任务管理卡片
        task_card = Card("📋 任务管理")
        task_layout = QVBoxLayout()
        task_layout.setSpacing(12)
        
        # 任务统计
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)
        
        for title, count, color in [("总任务", "12", "#3b82f6"), ("进行中", "5", "#f59e0b"), ("已完成", "7", "#10b981")]:
            stat_frame = QFrame()
            stat_frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {color}20;
                    border: 1px solid {color}40;
                    border-radius: 8px;
                    padding: 8px 12px;
                }}
            """)
            
            stat_layout = QVBoxLayout(stat_frame)
            stat_layout.setSpacing(2)
            
            count_label = QLabel(count)
            count_label.setAlignment(Qt.AlignCenter)
            count_label.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {color};")
            stat_layout.addWidget(count_label)
            
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("font-size: 12px; color: #6b7280;")
            stat_layout.addWidget(title_label)
            
            stats_layout.addWidget(stat_frame)
        
        stats_layout.addStretch()
        task_layout.addLayout(stats_layout)
        
        # 任务列表
        self.task_list = QListWidget()
        self.task_list.setMinimumHeight(150)  # 设置最小高度
        self.task_list.setMaximumHeight(250)  # 增加最大高度
        self.task_list.setStyleSheet("""
            QListWidget {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            
            QListWidget::item {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 2px;
            }
        """)
        task_layout.addWidget(self.task_list)
        
        task_card.add_layout(task_layout)
        layout.addWidget(task_card)
        
        # 消息中心卡片
        message_card = Card("💬 消息中心")
        message_layout = QVBoxLayout()
        message_layout.setSpacing(12)
        
        # 消息显示
        self.message_text = QTextEdit()
        self.message_text.setReadOnly(True)
        self.message_text.setMinimumHeight(100)  # 设置最小高度
        self.message_text.setMaximumHeight(150)  # 增加最大高度
        self.message_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px;
                font-size: 13px;
                color: #374151;
            }
        """)
        message_layout.addWidget(self.message_text)
        
        # 发送消息
        send_layout = QHBoxLayout()
        send_layout.setSpacing(8)
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("输入消息...")
        self.message_input.returnPressed.connect(self.send_message)
        send_layout.addWidget(self.message_input, 1)
        
        send_btn = QPushButton("发送")
        send_btn.setProperty("buttonType", "primary")
        send_btn.clicked.connect(self.send_message)
        send_layout.addWidget(send_btn)
        
        message_layout.addLayout(send_layout)
        message_card.add_layout(message_layout)
        layout.addWidget(message_card)
        
        # 操作卡片
        action_card = Card("⚡ 协作操作")
        action_layout = QVBoxLayout()
        action_layout.setSpacing(16)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        self.sync_btn = QPushButton("同步数据")
        self.sync_btn.setProperty("buttonType", "primary")
        self.sync_btn.clicked.connect(lambda: self.start_operation("同步数据"))
        button_layout.addWidget(self.sync_btn)
        
        self.backup_btn = QPushButton("备份项目")
        self.backup_btn.setProperty("buttonType", "success")
        self.backup_btn.clicked.connect(lambda: self.start_operation("备份项目"))
        button_layout.addWidget(self.backup_btn)
        
        self.export_btn = QPushButton("导出报告")
        self.export_btn.setProperty("buttonType", "warning")
        self.export_btn.clicked.connect(self.export_report)
        button_layout.addWidget(self.export_btn)
        
        button_layout.addStretch()
        action_layout.addLayout(button_layout)
        
        # 进度显示
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        action_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #6b7280; font-style: italic;")
        action_layout.addWidget(self.status_label)
        
        action_card.add_layout(action_layout)
        layout.addWidget(action_card)
        
        layout.addStretch()
    
    def load_sample_data(self):
        """加载示例数据"""
        # 示例团队成员
        members = [
            {"username": "张三", "role": "项目经理", "status": "online"},
            {"username": "李四", "role": "标注员", "status": "online"},
            {"username": "王五", "role": "审核员", "status": "offline"},
            {"username": "赵六", "role": "标注员", "status": "online"}
        ]
        
        for member in members:
            user_card = UserCard(member["username"], member["role"], member["status"])
            list_item = QListWidgetItem()
            list_item.setSizeHint(user_card.sizeHint())
            self.team_list.addItem(list_item)
            self.team_list.setItemWidget(list_item, user_card)
        
        # 示例任务
        tasks = [
            {"title": "标注汽车数据集", "description": "标注1000张汽车图片的边界框", "assignee": "李四", "status": "进行中", "progress": 65},
            {"title": "审核人物数据集", "description": "审核500张人物标注的准确性", "assignee": "王五", "status": "待开始", "progress": 0},
            {"title": "动物数据集质检", "description": "检查动物数据集的标注质量", "assignee": "赵六", "status": "已完成", "progress": 100}
        ]
        
        for task in tasks:
            task_item = TaskItem(task)
            list_item = QListWidgetItem()
            list_item.setSizeHint(task_item.sizeHint())
            self.task_list.addItem(list_item)
            self.task_list.setItemWidget(list_item, task_item)
        
        # 示例消息
        messages = [
            "系统: 欢迎使用协作标注系统",
            "张三: 大家好，今天的任务分配已经完成",
            "李四: 收到，开始标注汽车数据集",
            "王五: 人物数据集审核准备就绪"
        ]
        
        self.message_text.setPlainText("\n".join(messages))
    
    def select_project(self):
        """选择项目"""
        path = QFileDialog.getExistingDirectory(self, "选择协作项目目录")
        if path:
            self.project_path = path
            display_path = str(Path(path).name) if len(path) > 50 else path
            self.project_label.setText(display_path)
            self.project_label.setToolTip(path)
            self.project_label.setStyleSheet("""
                #projectLabel {
                    background-color: white;
                    border: 1px solid #10b981;
                    border-radius: 6px;
                    padding: 12px 16px;
                    color: #374151;
                    font-weight: 500;
                }
            """)
    
    def add_member(self):
        """添加成员"""
        username = self.member_input.text().strip()
        if not username:
            QMessageBox.warning(self, "警告", "请输入成员用户名")
            return
        
        # 创建新成员卡片
        user_card = UserCard(username, "标注员", "offline")
        list_item = QListWidgetItem()
        list_item.setSizeHint(user_card.sizeHint())
        self.team_list.addItem(list_item)
        self.team_list.setItemWidget(list_item, user_card)
        
        self.member_input.clear()
        
        # 添加消息
        current_text = self.message_text.toPlainText()
        new_message = f"系统: {username} 已加入项目"
        self.message_text.setPlainText(current_text + "\n" + new_message)
        
        # 滚动到底部
        scrollbar = self.message_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def send_message(self):
        """发送消息"""
        message = self.message_input.text().strip()
        if not message:
            return
        
        current_user = self.user_input.text() or "当前用户"
        current_text = self.message_text.toPlainText()
        new_message = f"{current_user}: {message}"
        self.message_text.setPlainText(current_text + "\n" + new_message)
        
        self.message_input.clear()
        
        # 滚动到底部
        scrollbar = self.message_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def start_operation(self, operation):
        """开始协作操作"""
        # 启动操作
        self.worker = CollaborationWorker(operation, {})
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.finished.connect(self.operation_finished)
        
        # 更新界面状态
        self.sync_btn.setEnabled(False)
        self.backup_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        self.worker.start()
    
    def update_progress(self, value, message):
        """更新进度"""
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
    
    def operation_finished(self, success, message):
        """操作完成"""
        self.reset_ui_state()
        
        if success:
            QMessageBox.information(self, "成功", message)
            self.status_label.setText("操作成功完成")
            
            # 添加系统消息
            current_text = self.message_text.toPlainText()
            new_message = f"系统: {message}"
            self.message_text.setPlainText(current_text + "\n" + new_message)
        else:
            QMessageBox.critical(self, "错误", message)
            self.status_label.setText("操作失败")
    
    def export_report(self):
        """导出协作报告"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存协作报告", 
            "collaboration_report.txt",
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("协作标注项目报告\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"项目路径: {self.project_path}\n")
                    f.write(f"当前用户: {self.user_input.text()}\n")
                    f.write(f"用户角色: {self.role_combo.currentText()}\n\n")
                    
                    f.write("团队成员:\n")
                    for i in range(self.team_list.count()):
                        item = self.team_list.item(i)
                        widget = self.team_list.itemWidget(item)
                        if isinstance(widget, UserCard):
                            f.write(f"- {widget.username} ({widget.role})\n")
                    
                    f.write("\n消息记录:\n")
                    f.write(self.message_text.toPlainText())
                
                QMessageBox.information(self, "成功", f"报告已保存到: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
    
    def reset_ui_state(self):
        """重置界面状态"""
        self.sync_btn.setEnabled(True)
        self.backup_btn.setEnabled(True)
        self.progress_bar.setVisible(False)