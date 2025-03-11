"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

"""
重要的事说三遍:

股市有风险，打板需谨慎
股市有风险，打板需谨慎
股市有风险，打板需谨慎

"""

from time import sleep
from libs.quote import Quote
from libs.trader import Trader
from libs.backend_job import BackendJob

Trader.get_instance().start()
sleep(5)  # 稍微等一下，只是让日志输出更加有序
Quote.get_instance().start()
backend_job = BackendJob.get_instance()
backend_job.start()

# 阻塞主线程，并且提供在程序运行过程中输入 “p” 打印候选标的列表、委托单、成交单功能
while True:
    s = input("")
    if s.upper() == 'P':
        print("打印候选列表、委托单、成交单")
        backend_job.print_orders_and_trades()