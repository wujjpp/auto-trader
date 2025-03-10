"""
Created by 满仓干 on - 2025/03/10.
"""

import datetime
import threading
from typing import List, Optional
import pandas as pd

from libs.models import Order, TemporaryOrder, Trade


class Context:
    _instance: Optional["Context"] = None
    lock = threading.Lock()

    def __init__(self):
        self.candidate_stocks = pd.read_csv("stocks.csv")
        self.orders: List[Order] = []
        self.trades: List[Trade] = []
        self.temp_buy_orders:List[TemporaryOrder] = []

    def get_candidate_stock_codes(self) -> List[str]:
        return self.candidate_stocks["证券代码"].to_list()
    
    def get_stock_detail_info(self, stock_code:str) -> Optional[dict]:
        d = self.candidate_stocks[(self.candidate_stocks["证券代码"] == stock_code)].to_dict(orient="records")
        if len(d) > 0:
            return d[0]
        return None
    
    def is_already_buy(self, stock_code:str) -> bool:
        """
        判断是不是已经下过单
        1. 从委托列表看是不是存在该标的”股票买入“委托，这里不管状态，换句话说：假如你手动撤单了，程序也不再下单
        2. 因为每隔3秒就会收到行情数据，假如：QMT响应速度慢，可能会导致重复下单，所有在context对象里面增加了一个临时委托单的概念，用于应对这种情况
        """
        # 先看一下，委托列表里面有没有
        flag = len(list(filter(lambda x: x.stock_code == stock_code and x.order_type_name == '股票买入', self.orders))) > 0
        
        # 再看一下临时委托单里面有没有
        if not flag:
            # 先把超过一分钟的数据过滤掉
            self.temp_buy_orders = list(filter(lambda x: x.stock_code == stock_code and ((datetime.datetime.now() -  x.order_time) > datetime.timedelta(minutes=1)), self.temp_buy_orders))
            # 再看有没有
            flag = len(list(filter(lambda x: x.stock_code == stock_code, self.temp_buy_orders))) > 0

        return flag
    
    def set_already_buy(self, stock_code:str) -> None:
        self.temp_buy_orders.append(TemporaryOrder(stock_code))

    @classmethod
    def get_instance(cls) -> "Context":
        with cls.lock:
            if not cls._instance:
                cls._instance = Context()
            return cls._instance
