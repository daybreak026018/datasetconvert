"""
工作线程模块 - 用于处理耗时操作，避免界面冻结
"""

from PyQt5.QtCore import QThread, pyqtSignal, QObject
from typing import Callable, Any, Dict, Optional
import traceback


class WorkerSignals(QObject):
    """工作线程信号"""
    # 进度更新信号 (当前进度, 总进度, 描述)
    progress = pyqtSignal(int, int, str)
    # 完成信号 (结果)
    finished = pyqtSignal(object)
    # 错误信号 (错误信息)
    error = pyqtSignal(str)
    # 状态更新信号 (状态描述)
    status = pyqtSignal(str)


class WorkerThread(QThread):
    """通用工作线程"""
    
    def __init__(self, func: Callable, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self._is_cancelled = False
        
    def run(self):
        """执行工作函数"""
        try:
            # 将信号传递给工作函数，让它可以更新进度
            if 'progress_callback' not in self.kwargs:
                self.kwargs['progress_callback'] = self.update_progress
            if 'status_callback' not in self.kwargs:
                self.kwargs['status_callback'] = self.update_status
            if 'cancel_callback' not in self.kwargs:
                self.kwargs['cancel_callback'] = self.is_cancelled
                
            result = self.func(*self.args, **self.kwargs)
            if not self._is_cancelled:
                self.signals.finished.emit(result)
        except Exception as e:
            error_msg = f"{str(e)}\n{traceback.format_exc()}"
            self.signals.error.emit(error_msg)
    
    def update_progress(self, current: int, total: int, description: str = ""):
        """更新进度"""
        if not self._is_cancelled:
            self.signals.progress.emit(current, total, description)
    
    def update_status(self, status: str):
        """更新状态"""
        if not self._is_cancelled:
            self.signals.status.emit(status)
    
    def is_cancelled(self) -> bool:
        """检查是否已取消"""
        return self._is_cancelled
    
    def cancel(self):
        """取消操作"""
        self._is_cancelled = True
        self.quit()
        # 等待线程结束，如果超时则强制终止
        if not self.wait(3000):  # 等待3秒
            self.terminate()
            self.wait()  # 等待终止完成


class ProgressDialog(QObject):
    """进度对话框管理器"""
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.dialog = None
        self.worker = None
        self._is_cancelled = False  # 添加取消标志
    
    def __del__(self):
        """析构函数 - 确保资源被清理"""
        try:
            self.cleanup()
        except:
            pass  # 忽略析构时的错误
        
    def start_task(self, title: str, func: Callable, *args, **kwargs):
        """启动任务"""
        from PyQt5.QtWidgets import QProgressDialog, QApplication
        from PyQt5.QtCore import Qt
        
        # 创建进度对话框
        self.dialog = QProgressDialog(title, "取消", 0, 100, self.parent)
        self.dialog.setWindowTitle("DataForge - 处理中")
        self.dialog.setWindowModality(Qt.WindowModal)
        self.dialog.setMinimumDuration(0)
        self.dialog.setValue(0)
        
        # 创建工作线程
        self.worker = WorkerThread(func, *args, **kwargs)
        
        # 连接信号 - 使用队列连接确保线程安全
        from PyQt5.QtCore import Qt
        self.worker.signals.progress.connect(self.update_progress, Qt.QueuedConnection)
        self.worker.signals.status.connect(self.update_status, Qt.QueuedConnection)
        self.worker.signals.finished.connect(self.on_finished, Qt.QueuedConnection)
        self.worker.signals.error.connect(self.on_error, Qt.QueuedConnection)
        
        # 连接取消信号
        self.dialog.canceled.connect(self.cancel_task)
        
        # 启动线程
        self.worker.start()
        
        return self.dialog
    
    def update_progress(self, current: int, total: int, description: str):
        """更新进度"""
        # 检查对话框是否仍然有效且未被取消
        if self.dialog and not self._is_cancelled and not self.dialog.wasCanceled():
            try:
                if total > 0:
                    percentage = int((current / total) * 100)
                    self.dialog.setValue(percentage)
                
                if description:
                    self.dialog.setLabelText(f"{description}\n({current}/{total})")
                
                # 处理事件，保持界面响应
                from PyQt5.QtWidgets import QApplication
                QApplication.processEvents()
            except (AttributeError, RuntimeError):
                # 对话框已被销毁，停止更新
                self._is_cancelled = True
    
    def update_status(self, status: str):
        """更新状态"""
        # 检查对话框是否仍然有效且未被取消
        if self.dialog and not self._is_cancelled and not self.dialog.wasCanceled():
            try:
                self.dialog.setLabelText(status)
            except (AttributeError, RuntimeError):
                # 对话框已被销毁，停止更新
                self._is_cancelled = True
    
    def on_finished(self, result):
        """任务完成"""
        if self.dialog:
            self.dialog.setValue(100)
            self.dialog.close()
            self.dialog = None  # 设置为 None 避免重复操作
        
        # 清理线程 - 确保线程完全结束
        self.cleanup_worker()
        
        # 发送完成信号给父对象
        if hasattr(self.parent, 'on_task_finished'):
            self.parent.on_task_finished(result)
    
    def on_error(self, error_msg: str):
        """任务出错"""
        if self.dialog:
            self.dialog.close()
            self.dialog = None  # 设置为 None 避免重复操作
        
        # 清理线程 - 确保线程完全结束
        self.cleanup_worker()
        
        # 显示错误信息
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.critical(self.parent, "错误", f"操作失败:\n{error_msg}")
        if hasattr(self.parent, 'on_task_error'):
            self.parent.on_task_error(error_msg)
    
    def cleanup_worker(self):
        """清理工作线程"""
        # 首先设置取消标志，防止进一步的UI更新
        self._is_cancelled = True
        
        if self.worker:
            if self.worker.isRunning():
                self.worker.cancel()
                # 等待线程结束，如果超时则强制终止
                if not self.worker.wait(3000):  # 等待3秒
                    self.worker.terminate()
                    self.worker.wait()  # 等待终止完成
            
            # 断开所有信号连接
            try:
                self.worker.signals.progress.disconnect()
                self.worker.signals.status.disconnect()
                self.worker.signals.finished.disconnect()
                self.worker.signals.error.disconnect()
            except:
                pass  # 忽略断开连接时的错误
            
            self.worker = None
        
        # 清理对话框引用
        if self.dialog:
            try:
                self.dialog.close()
            except:
                pass  # 忽略关闭时的错误
            self.dialog = None
    
    def cancel_task(self):
        """取消任务"""
        self._is_cancelled = True
        
        if self.worker:
            self.worker.cancel()
        
        if self.dialog:
            self.dialog.close()
            self.dialog = None  # 设置为 None 避免重复操作
        
        # 清理工作线程
        self.cleanup_worker()
    
    def cleanup(self):
        """清理资源"""
        self._is_cancelled = True
        self.cleanup_worker()
        
        # dialog 已在 cleanup_worker 中清理


def run_with_progress(parent, title: str, func: Callable, *args, **kwargs):
    """便捷函数：在进度对话框中运行函数"""
    progress_manager = ProgressDialog(parent)
    return progress_manager.start_task(title, func, *args, **kwargs)
