# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/7/1 20:35
# @Author  : lemon

from datetime import date

from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if hasattr(o,'keys') and hasattr(o,'__getitem__'):
            return dict(o)
        if isinstance(o,date):
            return o.strftime('%Y-%m-%d')

class Flask(_Flask):
    json_encoder = JSONEncoder
