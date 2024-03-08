#!/usr/bin/env python
# -*- coding: utf-8 -*-s

import io
import time
from PIL import Image, ImageTk
import tkinter as tk
import threading
import requests
from utils.speech import Speaker


class FrontEndWin:
    '''
    前端窗口
    包含两个功能：
    1. 视频播放
    2. 弹窗显示+语音播报
    '''
    def __init__(self, master):
        self.master = master
        self.master.withdraw()  # 隐藏主窗口

        self.screen_w = self.master.winfo_screenwidth()
        self.screen_h = self.master.winfo_screenheight()

        self.popup_w = 800
        self.popup_h = 450

        self.play_thread = None  # 初始化线程
        self.break_sign = False  # 初始化线程结束标志

        self.speaker = Speaker(language=0, speed=200, volume=0.9)

    # 视频播放
    def play_streams(self, video_url):
        if self.play_thread is None:
            self.break_sign = False
            self.play_thread = threading.Thread(target=self.show_stream, args=(video_url,))
            self.play_thread.start()
            return '成功启动视频播放'
        else:
            return "视频播放线程已经存在"

    # 弹窗和语音播报
    def popup(self, source, type, event):
        show_thread = threading.Thread(target=self.show_img, args=(source, type))
        show_thread.start()
        threading.Thread(target=self.speaker, args=(event,)).start()

    def show_stream(self, video_url):
        stream_window = tk.Toplevel(self.master)  # 创建子窗口
        # stream_window.geometry(f"{self.screen_w}x{self.screen_h}")  # 初始化位置
        # stream_window.overrideredirect(True)  # 无边框
        stream_window.attributes("-topmost", True)  # 保持窗口在顶部
        stream_window.attributes("-fullscreen", True)  # 全屏

        canvas = tk.Canvas(stream_window, width=self.screen_w, height=self.screen_h)
        canvas.pack()

        response = requests.get(video_url, stream=True)
        byte_data = b''
        for chunk in response.iter_content(chunk_size=1024):  # 2073600
            if self.break_sign:
                break
            byte_data += chunk
            start = byte_data.find(b'\xff\xd8')
            end = byte_data.find(b'\xff\xd9')
            if start != -1 and end != -1:
                img = byte_data[start:end+2]
                # byte_data = byte_data[end+2:]
                byte_data = b''

                img = Image.open(io.BytesIO(img))
                img = self.keep_scale_resize(self.screen_w, self.screen_h, img)
                img = ImageTk.PhotoImage(img)
                canvas.create_image(0, 0, anchor='nw', image=img)
                _ = img  # 防止img_on_canvas被Python自动回收
        print("show_stream end")
        stream_window.destroy()

    # 停止窗口的代码
    def stop_stream(self):
        if self.break_sign is False:
            # if self.play_thread is not None:
            # self.move_window(0.0, 'down')
            self.break_sign = True
            self.play_thread.join()  # 等待线程结束
            self.play_thread = None
            # self.child_window.destroy()
        return "成功停止视频播放"

    def show_img(self, source, type):
        if type == "img":
            img = Image.open(source)
            img = self.keep_scale_resize(self.popup_w, self.popup_h, img)
            new_w, new_h = img.size
            img = ImageTk.PhotoImage(img)

            child_window = tk.Toplevel(self.master)  # 创建子窗口
            child_window.withdraw()  # 隐藏窗口
            child_window.overrideredirect(True)  # 移除窗口装饰
            child_window.geometry(f"{new_w}x{new_h}+{self.screen_w-new_w}+{self.screen_h}")  # 初始化位置，右下角屏幕之外
            child_window.attributes("-topmost", True)  # 保持窗口在顶部
            child_window.deiconify()  # 显示窗口
            canvas = tk.Canvas(child_window, width=new_w, height=new_h, background='black')
            canvas.pack()

            canvas.create_image(0, 0, anchor='nw', image=img)
            self.move_window(child_window, 0.0, 'up')

            # 5秒后下降并关闭窗口
            time.sleep(5)
            self.move_window(child_window, 0.0, 'down')
            child_window.destroy()
        print("show_imgs end")

    # 不拉伸缩放
    def keep_scale_resize(self, max_w, max_h, img: Image.Image):
        ori_w, ori_h = img.size
        scale = min(max_w / ori_w, max_h / ori_h)
        new_shape = (int(ori_w * scale), int(ori_h * scale))
        return img.resize(new_shape, Image.ANTIALIAS)

    # 窗口上升下降
    def move_window(self, window, sleep_time=0.005, direction='up'):
        win_w, win_h = window.winfo_width(), window.winfo_height()
        _range = range(0, win_h, 1) if direction == 'up' else range(win_h, 0, -2)
        for i in _range:  # 从屏幕底部开始，每次上移n像素
            window.geometry(f"{win_w}x{win_h}+{self.screen_w-win_w}+{self.screen_h-i}")
            time.sleep(sleep_time)  # 暂停0.05秒，可以调整这个值来改变窗口的速度


if __name__ == '__main__':
    root = tk.Tk()
    FrontEndWin(root)
    root.mainloop()
