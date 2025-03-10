"""
Created by 满仓干 on - 2025/03/10.
"""

from typing import Optional
from libs.context import Context
from libs.models import QuoteOnline
from libs.trader import Trader
import libs.utils as utils


def buy(quote: Optional[QuoteOnline]) -> None:
    """
    执行逻辑
    """
    if quote == None:
        return

    if quote.time <= "09:30:00" or quote.time >= "14:55:00":
        print(f"{quote.stock_code} 非交易时段")

    stock_code = quote.stock_code
    price = quote.price
    last_close = quote.last_close

    trader = Trader.get_instance()
    context = Context.get_instance()

    # 价格是涨停价并且卖一的量是0，视为涨停，你也可以加入其它条件，如：封单金额等
    # 涨停幅度可根据 stock_code前缀自行判断
    if (round(price, 2)) >= round(last_close * (1 + 0.1), 2) and quote.ask_vol1 == 0:
        print("执行打板")
        trader.buy(stock_code, 100, price, 11, "打板", "打板")
    else:
        utils.print_quote_simple(quote)
