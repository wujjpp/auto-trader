"""
Created by 满仓干 on - 2025/03/10.

重要的事说三遍:

股市有风险，打板需谨慎
股市有风险，打板需谨慎
股市有风险，打板需谨慎
"""

from xtquant import xtdata
from libs.quote import Quote
from libs.trader import Trader

Trader.get_instance().start()
Quote.get_instance().start()

xtdata.run()
