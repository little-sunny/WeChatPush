'''
微信自动推送图片
图片内容是金山词霸的每日一句
过程：
准备工作，安装 wxpy第三方包
1. 通过扫描二维码登录微信
2. 获取图片地址
3. 下载图片到本地的当前路径
4. 查找好友并发送图片

将图片保存到本地的方法有多种，
这里用到的是 urllib.request.urlretrieve

Author：litong
'''

from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests
from urllib import request
import os

bot = Bot(cache_path=True)  # 扫描二维码登录微信


def get_news():
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    image_url = r.json()['fenxiang_img']  # 获取图片地址
    return image_url


def send_news():
    try:
        cur_path = os.path.abspath(os.curdir)  # 获取当前路径
        image_path = cur_path + '\\' + 'image.jpg'
        request.urlretrieve(get_news(), image_path)  # 将图片保存到当前目录下，图片名为“image.jpg”

        friends = [u"xxx", u"xxx"]  # 想要发送的好友列表
        for i in friends:
            my_friend = bot.friends().search(i)[0]  # 查找好友
            my_friend.send('@img@image.jpg')  # 发送图片， 加上前缀 @img@， 表示发送的是图片
            my_friend.send("这条消息是自动推送，如不感兴趣请忽略！")

        t = Timer(86400, send_news)
        t.start()
    except:
        myself = bot.friends().search(u'xxx')[0]
        myself.send("今日推送失败")


if __name__ == "__main__":
    send_news()

