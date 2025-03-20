"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

import threading
import time
from typing import Optional

from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from xtquant.xttype import StockAccount
from xtquant import xtconstant

import config as config
from libs.context import Context
import libs.logger as logger
from libs.errors import NotConnectError
from libs.models import AccountAsset, Order, Trade
import libs.shared as shared


app_logger = logger.get_app_logger()
trade_logger = logger.get_trade_logger()
account_logger = logger.get_account_logger()


class TraderCallback(XtQuantTraderCallback):
    def __init__(self) -> None:
        super(TraderCallback, self).__init__()

    def attach_trader(self, trader):
        self.trader = trader

    def on_disconnected(self):
        app_logger.error("connection lost")
        self.trader.connected = False
        self.trader.start()  # type: ignore

    def on_account_status(self, status):
        # 1. prepare data
        status = shared.xtobject_to_dict(status)
        status = shared.patch_xtaccountstatus(status)
        status["event_name"] = "on_account_status"

        # 2. log
        account_logger.info(f"{shared.json_dumps(status)}")

    def on_stock_asset(self, asset):
        # 1. prepare data
        asset = shared.xtobject_to_dict(asset)
        asset["event_name"] = "on_stock_asset"
        asset = shared.patch_xtasset(asset)

        # 2. log
        print(f"\n------------------ on_stock_asset ------------------")
        account_logger.info(f"{shared.json_dumps(asset)}")
        print(f"----------------------------------------------------\n")

    def on_stock_order(self, order):
        # 1. prepare data
        order = shared.xtobject_to_dict(order)
        order["event_name"] = "on_stock_order"
        order = shared.patch_xtorder(order)

        # 2. log
        print(f"\n------------------ on_stock_order ------------------")
        trade_logger.info(f"{shared.json_dumps(order)}")
        print(f"----------------------------------------------------\n")
        Context.get_instance().orders.append(Order.load_from_dict(order))  # type: ignore

    def on_stock_trade(self, trade):
        # 1. prepare data
        trade = shared.xtobject_to_dict(trade)
        trade["event_name"] = "on_stock_trade"
        trade = shared.patch_xttrade(trade)

        # 2. log
        print(f"\n------------------ on_stock_trade ------------------")
        trade_logger.info(f"{shared.json_dumps(trade)}")
        print(f"----------------------------------------------------\n")
        Context.get_instance().trades.append(Trade.load_from_dict(trade))  # type: ignore

    def on_stock_position(self, position):
        # 1. prepare data
        position = shared.xtobject_to_dict(position)
        position["event_name"] = "on_stock_position"

        # 2. log
        print(f"\n----------------- on_stock_position -----------------")
        trade_logger.info(f"{shared.json_dumps(position)}")
        print(f"-----------------------------------------------------\n")

        # 3. save data to db
        # tradedb.save_position(position)

    def on_order_error(self, order_error):
        # 1. prepare data
        order_error = shared.xtobject_to_dict(order_error)
        order_error["event_name"] = "on_order_error"
        order_error = shared.patch_xtordererror(order_error)

        # 2. log
        print(f"\n----------------- on_order_error -----------------")
        trade_logger.error(f"{shared.json_dumps(order_error)}")
        print(f"--------------------------------------------------\n")

    def on_cancel_error(self, cancel_error):
        # 1. prepare data
        cancel_error = shared.xtobject_to_dict(cancel_error)
        cancel_error["event_name"] = "on_cancel_error"
        cancel_error = shared.patch_xtcancelerror(cancel_error)

        # 2. log
        print(f"\n----------------- on_cancel_error -----------------")
        trade_logger.error(f"{shared.json_dumps(cancel_error)}")
        print(f"---------------------------------------------------\n")


class Trader:
    _instance: Optional["Trader"] = None
    lock = threading.Lock()

    def __init__(self):
        self.context = Context.get_instance()
        self.path = config.QMT_PATH
        self.connected = False
        self.registed = False
        self.account = None
        self.event_set = threading.Event()
        self.locker = threading.Lock()

    def start(self):
        t = threading.Thread(target=self._start)
        t.start()

    def _start(self):
        while True and not self.event_set.is_set():
            # 假如之前启动了，则停止
            if hasattr(self, "xt_trader") and not self.xt_trader:
                self.xt_trader.stop()

            # session_id = datetime.datetime.now().timestamp()
            # session_id = int(session_id * 1000000)
            session_id = int(time.time())
            self.xt_trader = XtQuantTrader(self.path, session_id)
            trader_callback = TraderCallback()
            trader_callback.attach_trader(self)

            self.xt_trader.register_callback(trader_callback)
            self.xt_trader.start()

            connect_result = self.xt_trader.connect()

            if connect_result == 0:
                app_logger.info("成功连接到交易终端")
                self.connected = True
            else:
                app_logger.error("无法连接到交易终端")

            if self.connected:
                account_id = config.QMT_ACCOUNT_ID
                account_type = config.QMT_ACCOUNT_TYPE
                account = StockAccount(account_id=account_id, account_type=account_type)  # type: ignore
                # 对交易回调进行订阅，订阅后可以收到交易主推，返回0表示订阅成功
                subscribe_result = self.xt_trader.subscribe(account)
                if subscribe_result == 0:
                    app_logger.info(f"资金账号 {account_id} 交易回调注册成功")
                    self.account = account

                    context = Context.get_instance()
                    context.orders = []
                    context.trades = []

                    orders = self.query_stock_orders()  # type: ignore
                    for order in orders:
                        context.orders.append(Order.load_from_dict(order))  # type: ignore

                    trades = self.query_stock_trades()  # type: ignore
                    for trade in trades:
                        context.trades.append(Trade.load_from_dict(trade))  # type: ignore

                    context.print_orders()
                    context.print_trades()

                    self.registed = True

                else:
                    app_logger.error(f"资金账号 {account_id} 交易回调注册失败")

                break  # 终止无限连接
            else:
                app_logger.info("等待2秒后重试")
                self.event_set.wait(2)

    def stop(self):
        self.event_set.set()

    def is_ready(self):
        return self.connected and self.account != None

    def _check_status(self):
        if not self.connected or not self.account:
            raise NotConnectError()

    def query_asset(self) -> Optional[AccountAsset]:
        """
        查询资金账号对应的资产
        """
        self._check_status()

        with self.locker:
            account = self.account
            r = shared.xtobject_to_dict(self.xt_trader.query_stock_asset(account))
            r["account_type_name"] = shared.decode_account_type(r["account_type"])
            return AccountAsset.load_from_dict(r)

    def query_stock_trades(self):
        """
        查询资金账号对应的当日所有成交
        """
        self._check_status()

        with self.locker:
            account = self.account
            trades = self.xt_trader.query_stock_trades(account)
            trades = shared.xtlist_to_list(trades)

            return [shared.patch_xttrade(trade) for trade in trades]

    def query_stock_orders(self, cancelable_only=False):
        """
        查询资金账号对应的当日所有委托
        cancelable_only - bool 仅查询可撤委托
        """
        self._check_status()

        with self.locker:
            account = self.account
            orders = self.xt_trader.query_stock_orders(account, cancelable_only)
            orders = shared.xtlist_to_list(orders)
            return [shared.patch_xtorder(order) for order in orders]

    def buy(
        self,
        stock_code: str,
        stock_volume,
        price,
        price_type: int = xtconstant.FIX_PRICE,
        strategy_name: str = "",
        order_remark: str = "",
    ):
        """
        `买入`: 系统生成的订单编号，成功委托后的订单编号为大于0的正整数，如果为-1表示委托失败

        `stock_code`: 股票代码

        `stock_volume`: 买入股数 - 注意: 不是手数

        `price`: 买入价格

        `price_type`: 价格类型， 5: 现价, 11: 限价

        `strategy_name`: 策略名称

        `order_remark`: 委托单备注
        """
        self._check_status()

        with self.locker:
            account: StockAccount = self.account  # type: ignore

            r = self.xt_trader.order_stock(
                account,
                stock_code,
                xtconstant.STOCK_BUY,
                stock_volume,
                price_type,
                price,
                strategy_name,
                order_remark,
            )

            order = {
                "order_id": r,
                "account_id": account.account_id,
                "account_type": account.account_type,
                "stock_code": stock_code,
                "order_type": xtconstant.STOCK_BUY,
                "stock_volume": stock_volume,
                "price_type": price_type,
                "price": price,
                "strategy_name": strategy_name,
            }

            order = shared.patch_xtorder(order)
            return order

    @classmethod
    def get_instance(cls) -> "Trader":
        if cls._instance != None:
            return cls._instance

        with cls.lock:
            if not cls._instance:
                cls._instance = Trader()
            return cls._instance
