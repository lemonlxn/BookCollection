# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/28 10:44
# @Author  : lemon

from sqlalchemy import Integer, String, Column, orm, or_

from app.models.base import  Base


class Book(Base):
    id = Column(Integer,primary_key=True,autoincrement=True)
    title = Column(String(50),nullable=False)
    author = Column(String(30),default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15),nullable=False,unique=True)
    summary = Column(String(1000))
    image = Column(String(50))



    def is_save_book(self,q):
        return True if Book.query.filter(Book.isbn ==q).all() else False




