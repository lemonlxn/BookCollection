# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/26 11:58
# @Author  : lemon

from flask import Blueprint,render_template

web = Blueprint('web',__name__)

@web.app_errorhandler(404)
def not_found(e):
    # AOP 面向切面编程
    return render_template('404.html'),404

from app.web import book,auth,main,drift,gift,wish,test


