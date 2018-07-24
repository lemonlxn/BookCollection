# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/24 17:49
# @Author  : lemon


def is_isbn_or_key(word):
    '''
    判断是 isbn 还是 普通关键词搜索
    默认是key，根据条件判断更改为isbn
    '''
    isbn_or_key = 'key'
    if word.isdigit() and len(word) == 13:
        isbn_or_key = 'isbn'

    short_word = word.replace('-', '')
    if '-' in word and short_word.isdigit() and len(short_word) == 10:
        isbn_or_key = 'isbn'

    return isbn_or_key
