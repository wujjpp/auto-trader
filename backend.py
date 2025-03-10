"""
Created by 满仓干 on - 2025/03/10.
"""

import os
import sys
from time import sleep
from pytz import timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from libs.context import Context


def _restart():
    """
    重新启动自己
    """
    seconds = 5
    while seconds > 0:
        print(f"{seconds}秒后系统自重启")
        sleep(1)
        seconds = seconds - 1

    os.execl(sys.executable, sys.executable, *sys.argv)

def _print_orders_and_trades():
    context = Context.get_instance()
    context.print_orders()
    context.print_trades()

def start() -> None:
    jobstores = {"default": MemoryJobStore()}
    executors = {"default": ThreadPoolExecutor(5)}
    job_defaults = {"coalesce": True, "max_instances": 1}
    scheduler = BlockingScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone=timezone("Asia/Shanghai"),
    )

    # 应用自重启
    scheduler.add_job(
        _restart,
        trigger="cron",
        day="*",
        hour=9,
        minute=0,
        second=0,
        name=f"【系统】09:00:00 应用自重启",
    )

    # 每隔1分钟打印委托和成交
    scheduler.add_job(
        _print_orders_and_trades,
        trigger="cron",
        day="*",
        hour="*",
        minute="*",
        second=0,
        name=f"【系统】每隔1分钟打印委托和成交信息",
    )

    
