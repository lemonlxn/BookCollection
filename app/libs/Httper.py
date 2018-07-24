# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/25 10:32
# @Author  : lemon

import requests

class Http:
    @staticmethod
    def get(url,return_json=True):
        r = requests.get(url)
        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text

