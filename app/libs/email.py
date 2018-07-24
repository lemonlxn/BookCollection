# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/24 21:21
# @Author  : lemon
from threading import Thread

from flask import current_app, render_template

from app import mail
from flask_mail import Message



def send_async_mail(app,msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e


def send_mail(to,subject,template,**kwargs):
    # msg = Message('测试邮件',sender='819845621@qq.com',
    #               body='test',
    #               recipients=['819845621@qq.com'])

    msg = Message('[鱼书]'+' '+subject
                  ,recipients=[to]
                  ,sender=current_app.config['MAIL_USERNAME'])
    msg.html = render_template(template,**kwargs)

    # 获取真实Flask核心对象
    app = current_app._get_current_object()
    new_thr = Thread(target=send_async_mail,args=[app,msg])
    new_thr.start()
