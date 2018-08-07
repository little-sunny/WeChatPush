'''
微信自动同送纯文本
推送的内容来自金山词霸的每日一句
包括英文原文，翻译，投稿人的话
过程：
准备工作，安装 wxpy第三方包
1. 通过扫描二维码登录微信
2. 从金山词霸获取每日一句
3. 查找微信好友并且将内容发送给好友

Author： litong
'''

from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests

bot = Bot(cache_path=True) # 扫描二维码登录微信，加入括号里的参数后，只有第一次登录的时候需要扫描


def get_news():

    url = "http://open.iciba.com/dsapi/"  # 获取金山词霸每日一句，content，note ，translation
    r = requests.get(url)
    contents = r.json()['content']
    note = r.json()['note']
    translation = r.json()['translation']
    return contents, note, translation


def send_news():
    try:
        zxz = bot.friends().search(u'xxx')[0] #查找好友xxx, 是微信名，不是微信号或备注
        contents, note, translation = get_news()
        zxz.send(contents)  # 发送contents
        zxz.send(note)  # 发送note
        zxz.send(translation[6:]) # 发送translation，从第6位开始
        t = Timer(86400, send_news) # 每天发一次，一天是86400秒
        t.start()
    except:
        myself = bot.friends().search(u'xxx')[0]
        myself.send("今天的消息发送失败了")


if __name__ == "__main__":
    send_news()


