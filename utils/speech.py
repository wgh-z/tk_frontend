import pyttsx3


class Speaker:
    '''
    text: 阅读的文字
    language: 0-中文/1-英文 (只有这两个选择)
    speed: 语速(0-500)。50戏剧化的慢,200正常,350用心听小说,500敷衍了事
    volume: 音量(0-1)
    filename: 保存的文件名(以.mp3收尾)
    sayit: 是否发言(0否1是)
    '''
    def __init__(self,
               language:int,
               speed:int,
               volume:float,
               ):
        self.engine = pyttsx3.init()  # 初始化语音引擎
    
        self.engine.setProperty('rate', speed)  # 设置语速
        self.engine.setProperty('volume', volume)  # 设置音量
        voices = self.engine.getProperty('voices')  # 获取当前语音的详细信息
        self.engine.setProperty('voice', voices[language].id)  # 设置第语音合成器

    def save(self, text:str, filename:str):
        assert filename.endswith('.mp3'), "文件名必须以.mp3结尾"
        self.engine.save_to_file(text, filename)

    def __call__(self, text:str):
        assert text and isinstance(text, str), "输入的文本必须是非空字符串"
        self.engine.say(text)  # pyttsx3->将结果念出来
        self.engine.runAndWait() # pyttsx3结束语句(必须加)
        self.engine.stop() # pyttsx3结束语句(必须加)


if __name__ == "__main__":
    speaker = Speaker(language=0, speed=200, volume=0.9)
    speaker("我是pyttsx3, 初次见面, 给您拜个早年")
