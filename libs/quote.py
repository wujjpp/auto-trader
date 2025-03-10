"""
Created by 满仓干 on - 2025/03/10.
"""

from xtquant import xtdata
from libs import utils
from libs.models import QuoteOnline
import config as config
from libs.context import Context

class Quote():
    def __init__(self):
        xtdata.enable_hello = False
        self.context = Context.get_instance()
        self.callback = lambda x: utils.print_quote_simple(x)

    def on_data(self, datas):
        for stock_code in datas:
          data = datas.get(stock_code)
          quote = QuoteOnline.load_from_dict(stock_code, data)
          self.callback(quote)

    def start(self, callback):
        self.callback = callback
        xtdata.subscribe_whole_quote(self.context.candidate_stocks, callback=self.on_data)






