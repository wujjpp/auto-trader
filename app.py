"""
Created by 满仓干 on - 2025/03/10.
使用本程序造成的投资上的任何损失与程序作者无任何关系，同意才能使用

重要的事说三遍:

股市有风险，打板需谨慎
股市有风险，打板需谨慎
股市有风险，打板需谨慎

"""

from time import sleep
from libs.quote import Quote
from libs.trader import Trader
import backend


Trader.get_instance().start()
sleep(5)  # 稍微等一下，只是让日志输出更加有序
Quote.get_instance().start()
backend.start()
