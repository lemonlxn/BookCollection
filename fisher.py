# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/24 11:07
# @Author  : lemon

from app import create_app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=5200,threaded=True)

