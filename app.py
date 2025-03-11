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
import logging
import signal
from libs.quote import Quote
from libs.trader import Trader
from libs.backend_job import BackendJob
import libs.logger as logger

def before_exit(a, b):
    logger.get_app_logger().info("正在关闭服务, 请稍后...")
    try:
        BackendJob.get_instance().stop()
    except:
        pass
    try:
        logging.shutdown()
    except:
        pass

    exit(0)

signal.signal(signal.SIGINT, before_exit)  # type: ignore

Trader.get_instance().start()
sleep(5)  # 稍微等一下，只是让日志输出更加有序
Quote.get_instance().start()
backend_job = BackendJob.get_instance()
backend_job.start()

while True:
    s = input("")
    if s == 'p':
        print("打印候选列表、委托单、成交单")
        backend_job.print_orders_and_trades()