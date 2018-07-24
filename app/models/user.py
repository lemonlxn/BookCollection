# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/10 12:03
# @Author  : lemon
from math import floor

from flask import current_app
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app import login_manager
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin,Base):
    #__tablename__ = 'user1'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password',String(128),nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        '''
        密码读取
        '''
        return self._password

    @password.setter
    def password(self,raw):
        '''
        密码写入
        '''
        self._password = generate_password_hash(raw)

    def check_password(self,raw):
        return check_password_hash(self._password,raw)


    def can_save_to_list(self,isbn):
        '''
        根据isbn是否合法，api是否存在此书,以及既不在心愿清单也不在赠送清单时，决定是否加入到心愿清单
        '''

        # 判断是否符合isbn编号规范
        if is_isbn_or_key(isbn) != 'isbn':
            return False

        # 查看api里面是否存在这本书
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first_book:
            return False

        # 注意点有：
        # 1.不允许用户同时赠送多本相同到书；
        # 2.不允许用户既是同本书的赠送者又是索要者。
        # 以上总结为：该本书既不在与赠送清单，也不在用户心愿清单时候，才能添加到列表中。

        gifting = Gift.query.filter_by(
            uid=self.id,isbn=isbn,launched=False).first()
        wishing = Wish.query.filter_by(
            uid=self.id, isbn=isbn, launched=False).first()

        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self,expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)

        # 返回用户写入信息
        return s.dumps({'id':self.id}).decode('utf-8')



    @staticmethod
    def reset_password(token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])

        # 读取token中的信息，采取相反的方式
        try:
            date = s.loads(token.encode('utf-8'))
        except:
            return False

        uid  = date.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            if user:
                user.password = new_password
            else:
                return False
        return True


    def can_send_drift(self):

        if self.beans < 1:
            return False

        # 获取成功送出的礼物数量
        success_gifts_count = Gift.query.filter_by(uid =self.id,
                                                   launched = True).count()
        # 获取成功收到的礼物数量
        success_receive_count = Drift.query.filter_by(requester_id = self.id,
                                                    pending = PendingStatus.Success).count()

        # 每索取两本书，必须送出一本书
        return True if (
            floor(success_receive_count/2) <= success_gifts_count
        ) else False



    @property
    def summary(self):
        '''
        书籍赠送者的简要情况
        '''
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )



@login_manager.user_loader
def get_user(id):
    '''
    通过接收id号，返回一个用户模型。
    因为id是User表主键，所以不用filter_by
    flask_login 调用这个函数，生成自定义current_user
    '''

    return User.query.get(int(id))



