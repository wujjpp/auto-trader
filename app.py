"""
Created by 满仓干 on - 2025/03/10.

重要的事说三遍:

股市有风险，打板需谨慎
股市有风险，打板需谨慎
股市有风险，打板需谨慎

"""

from time import sleep
from xtquant import xtdata
from libs.quote import Quote
from libs.trader import Trader

Trader.get_instance().start()
sleep(5) # 稍微等一下，只是让日志输出更加有序
Quote.get_instance().start()

xtdata.run()
