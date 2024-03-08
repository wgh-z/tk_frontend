import requests

# "test1.jpg", "img"

url1 = "http://localhost:3001/popup"  # 更改为你的URL
url2 = "http://localhost:3001/start"  # 更改为你的URL

data = {
    "source": "http://127.0.0.1:5000/video_feed",  # 图片或图片流的URL
    "type": "stream",  # img或stream
    "event": "打架斗殴事件"  # 事件文字
}

# data = {
#     "source": "test1.jpg",  # 图片或图片流的URL
#     "type": "img",  # img或stream
#     "event": "打架斗殴事件"  # 事件文字
# }

response = requests.post(url1, json=data)
# response = requests.post(url2)

print(response.status_code)
print(response.text)