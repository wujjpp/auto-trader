"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

import os
import sys
import threading
from time import sleep
from typing import Optional
from pytz import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from libs.context import Context
import libs.logger as logger

app_logger = logger.get_app_logger()



class BackendJob:
    _instance: Optional["BackendJob"] = None
    lock = threading.Lock()

    def __init__(self) -> None:
        jobstores = {"default": MemoryJobStore()}
        job_defaults = {"coalesce": True, "max_instances": 1}

        self.executors = {"default": ThreadPoolExecutor(5)}
        self.scheduler = BackgroundScheduler(
            jobstores=jobstores,
            executors=self.executors,
            job_defaults=job_defaults,
            timezone=timezone("Asia/Shanghai"),
        )

        # 应用自重启
        self.scheduler.add_job(
            self.restart,
            trigger="cron",
            day="*",
            hour=9,
            minute=0,
            second=0,
            name=f"【系统】09:00:00 应用自重启",
        )

        # # 每隔1分钟打印委托和成交
        # self.scheduler.add_job(
        #     self.print_orders_and_trades,
        #     trigger="cron",
        #     day="*",
        #     hour="*",
        #     minute="*",
        #     second=0,
        #     name=f"【系统】每隔1分钟打印委托和成交信息",
        # )

    def start(self):
        """
        启动调度器
        """
        self.scheduler.start()

    def stop(self):
        """
        关闭调度器
        """
        self.scheduler.shutdown(False)
        for exec in self.executors.values():
            try:
                exec.shutdown(False)
            except:
                pass

    def print_orders_and_trades(self):
        app_logger.info("定时打印候选列表、委托单、成交单")
        context = Context.get_instance()
        context.print_candidate_stocks()
        context.print_orders()
        context.print_trades()

    
    def restart(self):
        """
        重新启动自己
        """
        seconds = 5
        while seconds > 0:
            print(f"{seconds}秒后系统自重启")
            sleep(1)
            seconds = seconds - 1
        os.execl(sys.executable, sys.executable, *sys.argv)

    @classmethod
    def get_instance(cls) -> "BackendJob":
        if cls._instance != None:
            return cls._instance

        with cls.lock:
            if not cls._instance:
                cls._instance = BackendJob()
            return cls._instance
