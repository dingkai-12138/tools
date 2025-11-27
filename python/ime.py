import sys
import threading
import time
import tkinter as tk

import keyboard
import uiautomation
import win32gui


class InputMethodMonitor:
    def __init__(self):  # self有点像Java的this
        self.root = tk.Tk()  # 创建主窗口。root只是自定义的变量名
        self.setup_window()  # 设置窗口属性
        self.last_status = None  # 记录上次输入法状态
        self.last_hwnd = None  # 记录上次窗口句柄

    def setup_window(self):
        self.root.overrideredirect(True)  # 移除窗口边框和标题栏
        self.root.attributes('-topmost', True)  # 窗口始终置顶
        self.root.attributes('-alpha', 0.8)  # 窗口始终置顶
        # self.root.configure(bg='black')
        self.root.attributes('-transparentcolor', 'gray')  # 指定一个颜色作为透明色
        self.root.configure(bg='gray')  # 设置背景为灰色（将被透明化）

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 200) // 2  # 水平居中
        y = (screen_height - 100) // 2  # 垂直居中
        self.root.geometry(f'200x100+{x}+{y}')  # 200x100像素，居中显示

        self.label = tk.Label(
            self.root,
            text='',  # 初始为空文本
            font=('Microsoft YaHei', 24, 'bold'),  # 微软雅黑字体，24号，粗体
            fg='red',  # 文字颜色为红色
            bg='gray'  # 背景为灰色（将被透明化）
            # bg='black'
        )
        self.label.pack(expand=True, fill='both')  # 填充整个窗口

    # 函数功能：在中文输入法下，获取中英文输入模式的状态
    # 返回值int：英--英文输入模式，中--中文输入模式，-1--输入模式未知
    def getInputMode(self):
        try:
            win = uiautomation.PaneControl(ClassName="Shell_TrayWnd", Name="任务栏")
            retext = win.ButtonControl(ClassName="IMEModeButton").Name
            # print("retext:", retext)
            if "英语模式" in retext:
                return '英'
            elif "中文模式" in retext:
                return '中'
            else:
                return -1
        except:  # 如果当前输入法不是中文输入法，会有异常抛出
            print(sys.exc_info()[0])
            return -1

    def get_active_window_info(self):
        """获取活动窗口信息"""
        hwnd = win32gui.GetForegroundWindow()

        # 获取窗口标题
        window_title = win32gui.GetWindowText(hwnd)

        # 获取窗口类名
        window_class = win32gui.GetClassName(hwnd)

        # 获取窗口位置和大小
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top

        return {
            'hwnd': hwnd,
            'title': window_title,
            'class': window_class,
            'position': (left, top),
            'size': (width, height)
        }

    def get_active_window_info(self):
        """获取活动窗口信息"""
        hwnd = win32gui.GetForegroundWindow()

        # 获取窗口标题
        window_title = win32gui.GetWindowText(hwnd)

        # 获取窗口类名
        window_class = win32gui.GetClassName(hwnd)

        # 获取窗口位置和大小
        rect = win32gui.GetWindowRect(hwnd)
        left, top, right, bottom = rect
        width = right - left
        height = bottom - top

        return {
            'hwnd': hwnd,
            'title': window_title,
            'class': window_class,
            'position': (left, top),
            'size': (width, height)
        }

    def window_change(self):
        current_window = self.get_active_window_info()

        # 检查窗口是否发生变化
        if current_window['hwnd'] != self.last_hwnd:
            if current_window['title']:  # 只显示有标题的窗口
                self.display(self.getInputMode())
                # print(f"切换到: {current_window['title']}")
            self.last_hwnd = current_window['hwnd']

    def update_status(self):
        current_status = self.getInputMode()
        # if current_status != self.last_status:
        self.display(current_status)

    def display(self, current_status: str | int):
        self.last_status = current_status
        color = 'red' if current_status == '中' else 'green'
        # self.label.config(text=current_status, bg=color)
        self.label.config(text=current_status)
        self.root.deiconify()  # 显示被隐藏的窗口
        # self.root.after(500, self.root.withdraw) # 定时隐藏窗口

    # 使用事件监听
    def on_shift_press(self, event):
        if event.name == 'shift':
            self.update_status()
            # print("Shift键被按下!")

    def start_monitoring(self):
        # 注册事件监听
        # keyboard.on_press(self.on_shift_press)

        def monitor():
            while True:
                self.root.after(0, self.update_status)
                # self.root.after(0, self.window_change)
                time.sleep(0.1)

        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        self.root.mainloop()


if __name__ == "__main__":
    monitor = InputMethodMonitor()
    monitor.start_monitoring()
