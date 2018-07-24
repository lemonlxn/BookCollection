# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/24 12:09
# @Author  : lemon


DEBUG = True

# 配置单一数据库
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:woailxn@localhost:3306/FisherApp'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = ')uio3n^jf61*)r*s_u+nl9#4zw&8eum2q+-5#o6!8p*=_$fqzj'


MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = '819845621@qq.com'
MAIL_PASSWORD = 'pjfhdeyzetrtbefe'
