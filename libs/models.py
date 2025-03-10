"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

import datetime
import json
from typing import Dict, Optional
from terminaltables3 import AsciiTable


class QuoteOnline:
    def __init__(self):

        self.stock_code = ""
        """
        证券代码
        """
        self.datetime = ""
        """
        行情时间(包含日期)
        """
        self.time = ""
        """
        行情时间
        """
        self.price = 0
        """
        最新价格
        """
        self.open = 0
        """
        开盘价
        """
        self.high = 0
        """
        最高价
        """
        self.low = 0
        """
        最低价
        """
        self.last_close = 0
        """
        昨收
        """
        self.amount = 0
        """
        总成交额
        """
        self.volume = 0
        """
        总成交量（股）
        """
        self.ask1 = 0
        """
        卖一价
        """
        self.ask2 = 0
        """
        卖二价
        """
        self.ask3 = 0
        """
        卖三价
        """
        self.ask4 = 0
        """
        卖四价
        """
        self.ask5 = 0
        """
        卖五价
        """
        self.ask_vol1 = 0
        """
        卖一量（股）
        """
        self.ask_vol2 = 0
        """
        卖二量（股）
        """
        self.ask_vol3 = 0
        """
        卖三量（股）
        """
        self.ask_vol4 = 0
        """
        卖四量（股）
        """
        self.ask_vol5 = 0
        """
        卖五量（股）
        """
        self.bid1 = 0
        """
        买一价
        """
        self.bid2 = 0
        """
        买二价
        """
        self.bid3 = 0
        """
        买三价
        """
        self.bid4 = 0
        """
        买四价
        """
        self.bid5 = 0
        """
        买五价
        """
        self.bid_vol1 = 0
        """
        买一量（股）
        """
        self.bid_vol2 = 0
        """
        买二量（股）
        """
        self.bid_vol3 = 0
        """
        买三量（股）
        """
        self.bid_vol4 = 0
        """
        买四量（股）
        """
        self.bid_vol5 = 0
        """
        买五量（股）
        """
        self.stockStatus = 0
        """
        证券状态: 来自官网
        0,10 - 默认为未知
        11 - 开盘前S
        12 - 集合竞价时段C
        13 - 连续交易T
        14 - 休市B
        15 - 闭市E
        16 - 波动性中断V
        17 - 临时停牌P
        18 - 收盘集合竞价U
        19 - 盘中集合竞价M
        20 - 暂停交易至闭市N
        21 - 获取字段异常
        22 - 盘后固定价格行情
        23 - 盘后固定价格行情完毕
        """

    def __str__(self) -> str:
        r = {}
        attrs = list(
            filter(
                lambda s: not s.startswith("__") and s != "load_from_dict", dir(self)
            )
        )
        for attr in attrs:
            r[attr] = getattr(self, attr)

        return json.dumps(r, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_dict(cls, stock_code: str, data: Dict) -> Optional["QuoteOnline"]:
        if data != None:
            o = QuoteOnline()
            o.stock_code = stock_code
            o.datetime = datetime.datetime.fromtimestamp(data.get("time") / 1000).strftime("%Y-%m-%d %H:%M:%S")  # type: ignore
            o.time = datetime.datetime.fromtimestamp(data.get("time") / 1000).strftime("%H:%M:%S")  # type: ignore
            o.price = data.get("lastPrice")
            o.open = data.get("open")
            o.high = data.get("high")
            o.low = data.get("low")
            o.last_close = data.get("lastClose")
            o.amount = data.get("amount")
            o.volume = data.get("volume") * 100  # type: ignore

            [ask1, ask2, ask3, ask4, ask5] = list(data.get("askPrice"))  # type: ignore
            o.ask1 = ask1
            o.ask2 = ask2
            o.ask3 = ask3
            o.ask4 = ask4
            o.ask5 = ask5

            [ask_vol1, ask_vol2, ask_vol3, ask_vol4, ask_vol5] = list(data.get("askVol"))  # type: ignore
            o.ask_vol1 = ask_vol1 * 100
            o.ask_vol2 = ask_vol2 * 100
            o.ask_vol3 = ask_vol3 * 100
            o.ask_vol4 = ask_vol4 * 100
            o.ask_vol5 = ask_vol5 * 100

            [bid1, bid2, bid3, bid4, bid5] = list(data.get("bidPrice"))  # type: ignore
            o.bid1 = bid1
            o.bid2 = bid2
            o.bid3 = bid3
            o.bid4 = bid4
            o.bid5 = bid5

            [bid_vol1, bid_vol2, bid_vol3, bid_vol4, bid_vol5] = list(data.get("bidVol"))  # type: ignore
            o.bid_vol1 = bid_vol1 * 100
            o.bid_vol2 = bid_vol2 * 100
            o.bid_vol3 = bid_vol3 * 100
            o.bid_vol4 = bid_vol4 * 100
            o.bid_vol5 = bid_vol5 * 100

            o.stockStatus = data.get("stockStatus")

            return o

        return None


class Order:
    def __init__(self):
        self.account_id = ""
        self.account_type = 0
        self.account_type_name = "股票"
        self.direction = 0
        self.direction_name = ""
        self.offset_flag = 0
        self.offset_flag_name = ""
        self.order_id = 0
        self.order_remark = ""
        self.order_status = 0
        self.order_status_name = ""
        self.order_sysid = ""
        self.order_time = 0
        self.order_type = 0
        self.order_type_name = ""
        self.order_volume = 0
        self.price = 0
        self.price_type = 0
        self.price_type_name = 0
        self.status_msg = ""
        self.stock_code = ""
        self.strategy_name = ""
        self.traded_price = 0
        self.traded_volume = 0

    def __str__(self) -> str:
        r = {}
        attrs = list(
            filter(
                lambda s: not s.startswith("__") and s != "load_from_dict", dir(self)
            )
        )
        for attr in attrs:
            r[attr] = getattr(self, attr)

        return json.dumps(r, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_dict(cls, data: Dict) -> Optional["Order"]:
        if data != None:
            o = Order()
            o.account_id = data.get("account_id")
            o.account_type = data.get("account_type")
            o.account_type_name = data.get("account_type_name")
            o.direction = data.get("direction")
            o.direction_name = data.get("direction_name")
            o.offset_flag = data.get("offset_flag")
            o.offset_flag_name = data.get("offset_flag_name")
            o.order_id = data.get("order_id")
            o.order_remark = data.get("order_remark")
            o.order_status = data.get("order_status")
            o.order_status_name = data.get("order_status_name")
            o.order_sysid = data.get("order_sysid")
            o.order_time = data.get("order_time")
            o.order_type = data.get("order_type")
            o.order_type_name = data.get("order_type_name")
            o.order_volume = data.get("order_volume")
            o.price = data.get("price")
            o.price_type = data.get("price_type")
            o.price_type_name = data.get("price_type_name")
            o.status_msg = data.get("status_msg")
            o.stock_code = data.get("stock_code")
            o.strategy_name = data.get("strategy_name")
            o.traded_price = data.get("traded_price")
            o.traded_volume = data.get("traded_volume")

            return o

        return None


class Trade:
    def __init__(self):
        self.account_id = ""
        self.account_type = 0
        self.account_type_name = ""
        self.direction = 0
        self.direction_name = ""
        self.offset_flag = 0
        self.offset_flag_name = ""
        self.order_id = 0
        self.order_remark = ""
        self.order_sysid = ""
        self.order_type = 0
        self.order_type_name = ""
        self.stock_code = ""
        self.strategy_name = ""
        self.traded_amount = 0
        self.traded_id = ""
        self.traded_price = 0
        self.traded_time = 0
        self.traded_volume = 0

    def __str__(self) -> str:
        r = {}
        attrs = list(
            filter(
                lambda s: not s.startswith("__") and s != "load_from_dict", dir(self)
            )
        )
        for attr in attrs:
            r[attr] = getattr(self, attr)

        return json.dumps(r, ensure_ascii=False, indent=2)

    @classmethod
    def load_from_dict(cls, data: Dict) -> Optional["Trade"]:
        if data != None:
            o = Trade()
            o.account_id = data.get("account_id")
            o.account_type = data.get("account_type")
            o.account_type_name = data.get("account_type_name")
            o.direction = data.get("direction")
            o.direction_name = data.get("direction_name")
            o.offset_flag = data.get("offset_flag")
            o.offset_flag_name = data.get("offset_flag_name")
            o.order_id = data.get("order_id")
            o.order_remark = data.get("order_remark")
            o.order_sysid = data.get("order_sysid")
            o.order_type = data.get("order_type")
            o.order_type_name = data.get("order_type_name")
            o.stock_code = data.get("stock_code")
            o.strategy_name = data.get("strategy_name")
            o.traded_amount = data.get("traded_amount")
            o.traded_id = data.get("traded_id")
            o.traded_price = data.get("traded_price")
            o.traded_time = data.get("traded_time")
            o.traded_volume = data.get("traded_volume")

            return o

        return None


class TemporaryOrder:
    def __init__(self, stock_code: str):
        self.stock_code = stock_code
        self.order_time = datetime.datetime.now()


class AccountAsset:
    def __init__(self) -> None:
        self.account_id = ""
        """
        账户ID
        """
        self.account_type = 2
        """
        账户类型
        """
        self.cash = 0
        """
        账户现金
        """
        self.frozen_cash = 0
        """
        冻结资金
        """
        self.market_value = 0
        """
        持仓市值
        """
        self.total_asset = 0
        """
        总资产
        """
        self.account_type_name = ""
        """
        账户类型名称
        """

    def print(self) -> None:
        table_data = []
        table_data.append(["账户", self.account_id])
        table_data.append(["账户类型", self.account_type_name])
        table_data.append(["现金", self.cash])
        table_data.append(["冻结资金", self.frozen_cash])
        table_data.append(["持仓市值", self.market_value])
        table_data.append(["总资产", self.total_asset])
        table = AsciiTable(table_data)
        table.inner_heading_row_border = False
        table.title = "账户信息"
        print(table.table)

    @classmethod
    def load_from_dict(cls, data: Dict) -> Optional["AccountAsset"]:
        if data != None:
            acc = AccountAsset()
            acc.account_id = data.get("account_id")
            acc.account_type = data.get("account_type")
            acc.cash = data.get("cash")
            acc.frozen_cash = data.get("frozen_cash")
            acc.market_value = data.get("market_value")
            acc.total_asset = data.get("total_asset")
            acc.account_type_name = data.get("account_type_name")
            return acc

        return None
