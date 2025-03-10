"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

import sys
import logging
import os
from logging import handlers
from colorama import Fore, Style, init

# 初始化Colorama库
init(autoreset=True)

if not os.path.exists("logs"):
    os.makedirs("logs")

app_logger = None  # 应用日志
account_logger = None  # 账户日志
trade_logger = None  # 交易日志
error_logger = None  # 错误日志

logging.basicConfig(force=True, handlers=[])


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": Style.BRIGHT + Fore.BLUE,
        "INFO": Style.BRIGHT + Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "CRITICAL": Style.BRIGHT + Fore.RED,
    }

    def format(self, record):
        log_message = super().format(record)
        return self.COLORS.get(record.levelname, "") + log_message + Style.RESET_ALL


def get_log_file_name(name: str) -> str:
    prefix, _ = os.path.splitext(os.path.basename(sys.argv[0]))

    if not os.path.exists(f"logs/{prefix}"):
        os.makedirs(f"logs/{prefix}")

    return f"logs/{prefix}/{name}.log"


def get_app_logger() -> logging.Logger:
    """
    获取应用日志
    """
    global app_logger

    if app_logger:
        return app_logger  # type: ignore

    app_logger = logging.getLogger("App")
    app_logger.propagate = False
    app_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = handlers.RotatingFileHandler(
        get_log_file_name("app"), maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(
        ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    file_handler.setFormatter(formatter)

    # 给logger添加handler
    app_logger.addHandler(console_handler)
    app_logger.addHandler(file_handler)

    return app_logger


def get_account_logger() -> logging.Logger:
    """
    获取账户信息日志
    """
    global account_logger

    if account_logger:
        return account_logger  # type: ignore

    prefix, _ = os.path.splitext(os.path.basename(sys.argv[0]))

    account_logger = logging.getLogger("Account")
    account_logger.propagate = False
    account_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = handlers.RotatingFileHandler(
        get_log_file_name("account"),
        maxBytes=1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(ColoredFormatter("%(message)s"))
    file_handler.setFormatter(formatter)

    # 给logger添加handler
    account_logger.addHandler(console_handler)
    account_logger.addHandler(file_handler)

    return account_logger


def get_trade_logger() -> logging.Logger:
    """
    获取成功交易日志
    """
    global trade_logger

    if trade_logger:
        return trade_logger  # type: ignore

    trade_logger = logging.getLogger("Trade")
    trade_logger.propagate = False
    trade_logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    file_handler = handlers.TimedRotatingFileHandler(
        get_log_file_name("trade"),
        when="D",
        interval=1,
        backupCount=30,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(ColoredFormatter("%(message)s"))
    file_handler.setFormatter(formatter)

    # 给logger添加handler
    trade_logger.addHandler(console_handler)
    trade_logger.addHandler(file_handler)

    return trade_logger


def get_error_logger() -> logging.Logger:
    """
    获取应用日志
    """
    global error_logger

    if error_logger:
        return error_logger  # type: ignore

    error_logger = logging.getLogger("Error")
    error_logger.propagate = False
    error_logger.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)

    file_handler = handlers.RotatingFileHandler(
        get_log_file_name("error"), maxBytes=1024 * 1024 * 5, encoding="utf-8"
    )
    file_handler.setLevel(logging.ERROR)

    # 定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(
        ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    file_handler.setFormatter(formatter)

    # 给logger添加handler
    error_logger.addHandler(console_handler)
    error_logger.addHandler(file_handler)

    return error_logger
