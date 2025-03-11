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
from typing import Optional
from xtquant import xtdata
from libs.models import QuoteOnline
import config as config
from libs.context import Context
from libs.trader import Trader
import strategy

import libs.logger as logger

app_logger = logger.get_app_logger()


class Quote:
    _instance: Optional["Quote"] = None
    lock = threading.Lock()

    def __init__(self):
        xtdata.enable_hello = False
        self.context = Context.get_instance()

    def on_data(self, datas):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        # 从09:31:00开始，是为了避免涨停开盘，然后快速下杀的情况
        # 本来一字板就很难打到，这边就风控优先了
        if now <= "09:31:00" or now >= "14:55:00":
            app_logger.info(f"非交易时段, [09:31:00 ~ 14:55:00]")
            return

        trader = Trader.get_instance()
        if not trader.connected or not trader.registed:
            app_logger.error("尚未连接到QMT或回调注册尚未完成")

        for stock_code in datas:
            data = datas.get(stock_code)
            quote = QuoteOnline.load_from_dict(stock_code, data)
            self.context.quotes_onine[stock_code] = quote
            strategy.action(quote)

    def start(self):
        stock_codes = self.context.get_candidate_stock_codes()
        if len(stock_codes) > 0:
            xtdata.subscribe_whole_quote(stock_codes, callback=self.on_data)
        else:
            app_logger.warning(f"未能在csv文件中找到候选标的")

    @classmethod
    def get_instance(cls) -> "Quote":
        if cls._instance != None:
            return cls._instance

        with cls.lock:
            if not cls._instance:
                cls._instance = Quote()
            return cls._instance
