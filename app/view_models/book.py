# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/5 14:52
# @Author  : lemon


class BookSingleModel:

    def __init__(self,book):
        '''
        解析单本书
        '''
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '、'.join(book['author'])
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.isbn = book['isbn']
        self.pages = book['pages']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros =  filter(lambda x:x if True else False,
                      [self.author,self.publisher,self.price])
        return '/'.join(intros)



class BookCollectionModel:
    '''
    解析多本书
    '''
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self,yushu_book,keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookSingleModel(book) for book in yushu_book.books]


