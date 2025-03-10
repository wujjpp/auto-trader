"""
Created by 满仓干 on - 2025/03/10.
"""

import threading
from typing import Optional
from xtquant import xtdata
from libs.models import QuoteOnline
import config as config
from libs.context import Context
import strategy


class Quote:
    _instance: Optional["Quote"] = None
    lock = threading.Lock()

    def __init__(self):
        xtdata.enable_hello = False
        self.context = Context.get_instance()

    def on_data(self, datas):
        for stock_code in datas:
            data = datas.get(stock_code)
            quote = QuoteOnline.load_from_dict(stock_code, data)
            strategy.buy(quote)

    def start(self):
        xtdata.subscribe_whole_quote(
            self.context.candidate_stocks, callback=self.on_data
        )

    @classmethod
    def get_instance(cls) -> "Quote":
        with cls.lock:
            if not cls._instance:
                cls._instance = Quote()
            return cls._instance
