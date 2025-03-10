"""
Created by 满仓干 on - 2025/03/10.
"""

import datetime
import json
from typing import Dict, Optional

# 原始数据
# {
#   'time': 1741570265000,                                时间戳
#   'lastPrice': 18.26,                                   最新价
#   'open': 18.37,                                        开盘价
#   'high': 18.68,                                        最高价
#   'low': 18.240000000000002,                            最低价
#   'lastClose': 18.68,                                   前收盘价
#   'amount': 56091900.0,                                 成交总额
#   'volume': 30409,                                      成交总量
#   'pvolume': 3040900,                                   原始成交总量
#   'stockStatus': 0,                                     证券状态
#   'openInt': 13,                                        持仓量
#   'transactionNum': 0,                                  成交笔数
#   'lastSettlementPrice': 0.0,                           前结算
#   'settlementPrice': 0.0,
#   'pe': 0.0,
#   'askPrice': [18.26, 18.27, 18.28, 18.29, 18.3],       卖一 ~ 卖五
#   'bidPrice': [18.23, 18.22, 18.21, 18.2, 18.19],       买一 ~ 买五
#   'askVol': [47, 54, 29, 2, 327],                       卖一量 ~ 卖五量  (手)
#   'bidVol': [31, 201, 442, 265, 30],                    买一量 ~ 买五量  (手)
#   'volRatio': 0.0,
#   'speed1Min': 0.0,
#   'speed5Min': 0.0
# }


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
