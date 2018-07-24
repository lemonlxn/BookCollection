# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/26 11:58
# @Author  : lemon


from app.libs.json_encoder import Flask
from flask_login import LoginManager
from flask_mail import Mail

from app.models.base import db

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.secure')
    app.config.from_object('app.config.setting')
    register_blueprint(app)


    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登陆或注册'

    mail.init_app(app)

    with app.app_context():
        db.create_all()
    return app

def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)


