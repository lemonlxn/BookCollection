# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/4/25 17:02
# @Author  : lemon


from flask import request,render_template,flash
from flask_login import current_user

from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import TradeInfo
from . import web
from app.spider.yushu_book import YuShuBook
from app.libs.helper import is_isbn_or_key
from ..forms.book import SearchForm
from ..view_models.book import BookCollectionModel,BookSingleModel


@web.route('/book/search')
def search():
    '''
    q: 普通关键字 或 isbn
    page: 当前页数
    ?q={}&page={}  --  Request实例化的对象，可以接收问号以后的参数，Flask这里采用request进行本地代理模式。
                       request的使用，必须在 Flask上下文环境中/HTTP请求中/视图函数中 触发。
    '''
    # request.args 得到具体的q与page的值

    form = SearchForm(request.args)
    books = BookCollectionModel()

    if form.validate():
        '''
        取form验证通过的数据，如客户端传回page为空值，SearchForm里面默认设置page=1
        '''
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)

        else:
            yushu_book.search_by_keyword(q,page)

        books.fill(yushu_book, q)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')


    return render_template('search_result.html', books=books, form=form)



@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    '''
        1. 当书籍既不在心愿清单也不在礼物清单时，显示礼物清单
        2. 当书籍在心愿清单时，显示礼物清单
        3. 当书籍在礼物清单时，显示心愿清单
        4. 一本书要防止即在礼物清单，又在赠送清单，这种情况是不符合逻辑的
    '''

    has_in_gifts  = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookSingleModel(yushu_book.first_book)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    trade_gifts  = Gift.query.filter_by(isbn = isbn,launched = False).all()
    trade_wishes = Wish.query.filter_by(isbn = isbn,launched=False).all()

    trade_gifts_model  = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)


    return render_template('book_detail.html',
                           book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)



@web.route('/test1')
def test1():
    '''
    被线程隔离的对象(AppContext，RequestContext/Request，session,g)，各线程之间互不影响；
    没有被线程隔离的对象，各线程之间会受到影响。
    '''
    from flask import request
    from app.libs.none_local import n
    from flask import current_app

    print(n.v)
    n.v = 2
    app = current_app
    print('flask核心对象ID号：' + str(id(app)))
    print('-----------')
    print(getattr(request,'v',None))
    setattr(request,'v',2)
    print('flask核心对象ID号：'+ str(id(app)))
    print('--------------')
    return ''


@web.route('/test')
def test():
    r = {
        'name':'',
        'age':24
    }
    flash('hello lemon',category='error')
    flash('hello lxn')
    return render_template('test.html',data = r)