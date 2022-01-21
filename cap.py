# -*- coding=utf-8 -*-

import requests
import re
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header


url = 'http://www.sgu.edu.cn/'
noticeUrl = 'http://www.sgu.edu.cn/5m1tl.html'
today = time.strftime('%Y/%#m/%d')

print(today)

# 发送邮箱
def send(msg, title):  # 邮件内容
    # qq邮箱smtp
    HOST = 'smtp.qq.com'
    user = '你的邮箱'
    pwd = '邮箱授权码'    # 授权码，需要去自己邮箱查看并开通设置
    sender = '你的邮箱'
    receivers = ['接收人邮箱']   # 接收人信箱
    now_time = today

    # 处理内容
    msg = MIMEText(msg, 'html', 'utf8')     # 内容，格式，编码
    msg['From'] = Header(sender, 'utf8')
    msg['To'] = Header('测试用户', 'utf8')
    subject = title
    msg['Subject'] = Header(subject, 'utf8')   # 邮件标题

    try:
        smtp_obj = smtplib.SMTP_SSL(HOST, 465)
        # 此处密码需要为授权码
        res = smtp_obj.login(user=user, password=pwd)
        print('发送结果：', res)
        # 发邮件
        smtp_obj.sendmail(from_addr=sender, to_addrs=receivers, msg=msg.as_string())
        # 断开链接
        smtp_obj.quit()
    except smtplib.SMTPException:
        print('文件发送失败')
    print("sendfinish")
    pass


# 抓取页面
def capping():
    obj1 = re.compile('<div class="l_content">.*?<div class="page">', re.S)
    obj2 = re.compile('<a href="(?P<href>.*?)".*?title="(?P<title>.*?)">.*?&nbsp;(?P<date>.*?)</a>', re.S)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.sgu.edu.cn',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    }

    resp = requests.get(noticeUrl, headers=headers)
    div = obj1.findall(resp.text)[0]
    lists = obj2.findall(div)

    for li in lists:
        href = url + li[0]
        title = li[1]
        date = li[2].split('&')[0]
        print(date)
        print(date == today)
        if date == today:
            print(href, title, date)
            resp1 = requests.get(href, headers=headers)
            send(resp1.text, title)


    print("capfinish")
    pass


if __name__ == '__main__':
    capping()


