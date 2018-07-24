# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/25 12:05
# @Author  : lemon


from app.libs.Httper import Http
from flask import current_app


class YuShuBook:
    '''
    描述相关书相关的特征，储存一个集合类型的数据。
    '''
    isbn_url    = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        '''
        不建议保存查询参数，因为YuShuBook主要保存的是书相关的信息。
        如果将查询参数，查询页数之类的都保存，这个类太过具体，以后不方便调整。如果有业务需要，可将此类封装。
        '''
        self.total = 0
        self.books = []


    def search_by_isbn(self,isbn):
        url = self.isbn_url.format(isbn)
        result = Http.get(url)
        self.__fill__single(result)


    def search_by_keyword(self,keyword,page=1):
        url = self.keyword_url.format(keyword,
                                     current_app.config['PER_PAGE'],
                                     self.calculate_start(page))
        result = Http.get(url)
        self.__fill__collection(result)



    def calculate_start(self,page):
        # 起始start设为0
        return (page-1) * current_app.config['PER_PAGE']


    def __fill__single(self,result):
        if result:
            self.total = 1
            self.books.append(result)



    def __fill__collection(self,result):
        self.books = result['books']
        self.total = result['total']

    @property
    def first_book(self):
        return self.books[0] if self.total >= 1 else None






