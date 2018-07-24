# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/19 10:20
# @Author  : lemon



from flask import make_response

from app.web import web

@web.route('/set/cookie')
def set_cookie():
    response = make_response('hello lemon')
    response.set_cookie('name','lemon',100)
    return response

@web.route('/hello')
def hello():
    return 'hello'