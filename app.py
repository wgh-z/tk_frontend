#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pyinstaller -F app.py

# 用户tk前端的主程序，用于启动flask服务和tk多路视频显示和tk弹窗显示
import threading
import yaml
from flask import Flask, request
from flask_cors import CORS
from tkinter import Tk
from utils.UI import FrontEndWin


app = Flask(__name__)
CORS(app, supports_credentials=True)

with open('cfg/frontend.yaml', 'r', encoding='utf-8') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

def run_tk_app():
    global frontend_win, cfg
    root = Tk()
    frontend_win = FrontEndWin(master=root, popup_w=cfg['popup_w'], popup_h=cfg['popup_h'])
    root.mainloop()

@app.route('/start', methods=['post'])
def start():
    global frontend_win
    video_url = request.json['video_url']
    # 启动UI的视频播放
    result = frontend_win.play_streams(video_url)
    return result

@app.route('/stop', methods=['post'])
def stop():
    global frontend_win
    # 停止UI的视频播放
    result = frontend_win.stop_stream()
    return result

@app.route('/popup', methods=['post'])
def popup():
    global frontend_win
    data = request.json
    # data['source']  # 图片或图片流的URL
    # data['type']  # img或stream
    # data['event']  # 事件文字
    # 启动UI的弹窗和语音播报
    frontend_win.popup(data['source'], data['type'], data['event'])
    return '成功启动弹窗'

def run_flask_app():
    global cfg
    # cfg = Path('cfg/frontend.yaml').read_text().rsplit()
    app.run(host=cfg['ip'], port=cfg['port'], debug=False)


if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    run_tk_app()
