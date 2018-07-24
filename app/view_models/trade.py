# /usr/bin/env python
# -*- coding:utf-8 -*-

# @Time    : 2018/5/20 12:17
# @Author  : lemon
from app.view_models.book import BookSingleModel


class TradeInfo:

    def __init__(self,goods):
        self.total  = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self,goods):
        self.total  = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self,single):

        return dict(
            user_name = single.user.nickname,
            time      = [single.create_datetime.strftime('%Y-%m-%d')
                         if single.create_datetime
                         else '未知'],
            id        = single.id
        )




class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []

        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        temp_trades = []
        for trade in self.__trades_of_mine:
            my_trade = self.__matching(trade)
            temp_trades.append(my_trade)
        return temp_trades

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade.isbn == trade_count['isbn']:
                count = trade_count['count']
        r = {
            'count': count,
            'book': BookSingleModel(trade.book),
            'id': trade.id
        }
        return r