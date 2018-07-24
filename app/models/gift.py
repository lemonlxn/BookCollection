# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/10 12:03
# @Author  : lemon

from flask import current_app

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship


from app.models.base import Base, db

from app.spider.yushu_book import YuShuBook


class Gift(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')    # 引用模型与模型之间的关系
    uid  = Column(Integer,ForeignKey('user.id'))
    isbn = Column(String(15),nullable=False)
    launched = Column(Boolean, default=False)


    def is_yourself_gift(self,uid):
        '''
        根据uid，判断是否向自己索要书籍。True为向自己索要，False相反。
        '''
        return True if self.uid == uid else False

    @classmethod
    def recent_gifts(cls):
        recent_gift = Gift.query.filter_by(launched=False).group_by(
                                            Gift.isbn).order_by(
                                            desc(Gift.create_time)).limit(
                                            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first_book

    @classmethod
    def get_user_gifts(cls,uid):
        gifts = Gift.query.filter_by(uid=uid,launched=False).order_by(
            desc(Gift.create_time)).all()

        return gifts

    @classmethod
    def get_wish_counts(cls,isbn_list):
        from app.models.wish import Wish
        # 查询主体，条件表达式
        # 跨表查询的时候，可以尝试db.session.query。
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
                                                                            Wish.launched == False,
                                                                            Wish.isbn.in_(isbn_list),
                                                                            Wish.status == 1).group_by(
                                                                            Wish.isbn).all()

        count_list = [{'count':i[0],'isbn':i[1]} for i in count_list]

        return count_list








