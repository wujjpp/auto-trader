"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

import datetime
import threading
from typing import List, Optional
import pandas as pd
from simple_chalk import chalk
from terminaltables3 import AsciiTable

from libs.models import Order, QuoteOnline, TemporaryOrder, Trade


class Context:
    _instance: Optional["Context"] = None
    lock = threading.Lock()

    def __init__(self):
        self.candidate_stocks = pd.read_csv("stocks.csv")
        self.orders: List[Order] = []
        self.trades: List[Trade] = []
        self.temp_buy_orders: List[TemporaryOrder] = []
        self.quotes_onine = {}

    def get_candidate_stock_codes(self) -> List[str]:
        return self.candidate_stocks["证券代码"].to_list()

    def get_stock_detail_info(self, stock_code: str) -> Optional[dict]:
        d = self.candidate_stocks[
            (self.candidate_stocks["证券代码"] == stock_code)
        ].to_dict(orient="records")
        if len(d) > 0:
            return d[0]
        return None

    def print_orders(self) -> None:
        table_data = []
        table_data.append(
            [
                "账户",
                "证券代码",
                "委托单类型",
                "委托价",
                "委托量",
                "报价方式",
                "成交价",
                "成交量",
                "状态",
                "下单时间",
            ]
        )
        for order in self.orders:
            table_data.append(
                [
                    order.account_id,
                    order.stock_code,
                    (
                        chalk.red(order.order_type_name)
                        if order.order_type_name == "股票买入"
                        else (
                            chalk.green(order.order_type_name)
                            if order.order_type_name == "股票卖出"
                            else chalk.blue(order.order_type_name)
                        )
                    ),
                    order.price,
                    order.order_volume,
                    order.price_type_name,
                    order.traded_price,
                    order.traded_volume,
                    order.order_status_name,
                    datetime.datetime.fromtimestamp(order.order_time).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                ]
            )
        table = AsciiTable(table_data)
        table.title = "委托列表"
        print(table.table)

    def print_candidate_stocks(self) -> None:
        table_data = []
        columns = self.candidate_stocks.columns.to_list()
        columns.append("当前涨幅")
        table_data.append(columns)
        for _, item in self.candidate_stocks.iterrows():
            values = []
            for c in columns:
                if c != "当前涨幅":
                    values.append(item.get(c))

            stock_code = item.get("证券代码")
            quote: Optional[QuoteOnline] = self.quotes_onine.get(stock_code, None)
            if quote != None:
                rise = (quote.price - quote.last_close) * 100 / quote.last_close
                rise_text = f"{round(rise, 2)}%"
                values.append(
                    chalk.red(rise_text)
                    if rise > 0
                    else (chalk.green(rise_text) if rise < 0 else rise_text)
                )
            else:
                values.append("-")

            table_data.append(values)

        table = AsciiTable(table_data)
        table.title = "候选列表"
        print(table.table)

    def print_trades(self) -> None:
        table_data = []
        table_data.append(
            [
                "账户",
                "证券代码",
                "委托单类型",
                "成交价",
                "成交量",
                "成交时间",
            ]
        )

        for trade in self.trades:
            table_data.append(
                [
                    trade.account_id,
                    trade.stock_code,
                    (
                        chalk.red(trade.order_type_name)
                        if trade.order_type_name == "股票买入"
                        else (
                            chalk.green(trade.order_type_name)
                            if trade.order_type_name == "股票卖出"
                            else chalk.blue(trade.order_type_name)
                        )
                    ),
                    trade.traded_price,
                    trade.traded_volume,
                    datetime.datetime.fromtimestamp(trade.traded_time).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                ]
            )
        table = AsciiTable(table_data)
        table.title = "成交列表"
        print(table.table)

    def is_already_buy(self, stock_code: str) -> bool:
        """
        判断是不是已经下过单
        1. 从委托列表看是不是存在该标的”股票买入“委托，这里不管状态，换句话说：假如你手动撤单了，程序也不再下单了
        2. 因为每隔3秒就会收到行情数据，假如：QMT回调速度慢的话，可能会导致重复下单，所以在context对象里面增加了一个临时委托单的概念，用于应对这种情况，数据保存1分钟
        """
        # 先看一下，委托列表里面有没有
        flag = (
            len(
                list(
                    filter(
                        lambda x: x.stock_code == stock_code
                        and x.order_type_name == "股票买入",
                        self.orders,
                    )
                )
            )
            > 0
        )

        # 再看一下临时委托单里面有没有
        if not flag:
            # 先把超过一分钟的数据过滤掉
            self.temp_buy_orders = list(
                filter(
                    lambda x: x.stock_code == stock_code
                    and (
                        (datetime.datetime.now() - x.order_time)
                        > datetime.timedelta(minutes=1)
                    ),
                    self.temp_buy_orders,
                )
            )
            # 再看有没有
            flag = (
                len(
                    list(
                        filter(
                            lambda x: x.stock_code == stock_code, self.temp_buy_orders
                        )
                    )
                )
                > 0
            )

        return flag

    def set_already_buy(self, stock_code: str) -> None:
        self.temp_buy_orders.append(TemporaryOrder(stock_code))

    @classmethod
    def get_instance(cls) -> "Context":
        if cls._instance != None:
            return cls._instance

        with cls.lock:
            if not cls._instance:
                cls._instance = Context()
            return cls._instance
