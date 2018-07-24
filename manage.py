# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/20 14:39
# @Author  : lemon

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from fisher import app
from app.models.base import db

migrate = Migrate(app,db)

manage = Manager(app)
manage.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manage.run()