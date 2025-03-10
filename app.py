"""
Created by 满仓干 on - 2025/03/10.

重要的事说三遍:

股市有风险，打板需谨慎
股市有风险，打板需谨慎
股市有风险，打板需谨慎
"""

from xtquant import xtdata

from libs.models import QuoteOnline
from libs.quote import Quote
import libs.utils as utils
from libs.trader import Trader

trader = Trader()
trader.start()

def on_quote(quote: QuoteOnline) -> None:
    """
    执行逻辑
    """
    stock_code = quote.stock_code
    price = quote.price
    last_close = quote.last_close

    # 价格是涨停价并且卖一的量是0，视为涨停，你也可以加入其它条件，如：封单金额等
    # 涨停幅度可根据 stock_code前缀自行判断
    if (round(price, 2)) >= round(last_close * (1 + 0.1), 2) and quote.ask_vol1 == 0:
        print("执行打板")
        trader.buy(stock_code, 100, price, 11, "打板", "打板")
    else:
        utils.print_quote_simple(quote)
        print("")

quote = Quote()
quote.start(on_quote)

xtdata.run()


