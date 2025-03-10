"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

from typing import Optional
from .models import QuoteOnline
from terminaltables3 import AsciiTable
from simple_chalk import chalk
import libs.logger as logger

app_logger = logger.get_app_logger()


def get_number_desc(v: float) -> str:
    """
    使用用亿、万作为单位显示
    """
    if v > 100000000.0:
        return f"{round(v / 100000000.0, 2)}亿"
    elif v > 10000.0:
        return f"{round(v / 10000.0, 0)}万"
    return f"{round(v, 0)}"


def colored_value(v: float, compare_to: float, suffix: str = "") -> str:
    if v == compare_to:
        return str(round(v, 2)) + suffix
    elif v > compare_to:
        return chalk.red(str(round(v, 2)) + suffix)
    else:
        return chalk.green(str(round(v, 2)) + suffix)


def print_quote_simple(quote: Optional[QuoteOnline]) -> None:
    if quote != None:
        s2 = colored_value(
            round((quote.price - quote.last_close) * 100 / quote.last_close, 2), 0, "%"
        )
        message = f"证券代码: {chalk.blue(quote.stock_code)}, 行情时间: {chalk.yellow(quote.time)}, 现价: {colored_value(quote.price, quote.last_close)}, 涨幅: {s2}, 总量: {chalk.yellow(get_number_desc(round(quote.volume / 100, 0)))}, 总额: {chalk.magenta(get_number_desc(round(quote.amount, 2)))}"
        app_logger.info(message)


def print_quote(quote: Optional[QuoteOnline]) -> None:
    if quote != None:
        table_data = []

        table_data.append(
            [
                "现价",
                colored_value(quote.price, quote.last_close),
                "涨幅",
                colored_value(
                    round((quote.price - quote.last_close) * 100 / quote.last_close, 2),
                    0,
                    "%",
                ),
            ]
        )
        table_data.append(
            [
                "最高",
                colored_value(round(quote.high, 2), quote.last_close),
                "最低",
                colored_value(round(quote.low, 2), quote.last_close),
            ]
        )
        table_data.append(["昨收", round(quote.last_close, 2), "", ""])
        table_data.append(
            [
                "总量",
                chalk.yellow(get_number_desc(round(quote.volume / 100, 0))),
                "总额",
                chalk.magenta(get_number_desc(round(quote.amount, 2))),
            ]
        )

        table_data.append(["-" * 10, "-" * 10, "-" * 10, "-" * 10])
        table_data.append(["", "报价", "挂单量(手)", "挂单总金额"])
        table_data.append(["-" * 10, "-" * 10, "-" * 10, "-" * 10])

        table_data.append(
            [
                "卖五",
                colored_value(round(quote.ask5, 2), quote.last_close),
                chalk.yellow(int(round(quote.ask_vol5 / 100, 0))),
                chalk.magenta(get_number_desc(quote.ask5 * quote.ask_vol5)),
            ]
        )
        table_data.append(
            [
                "卖四",
                colored_value(round(quote.ask4, 2), quote.last_close),
                chalk.yellow(int(round(quote.ask_vol4 / 100, 0))),
                chalk.magenta(get_number_desc(quote.ask4 * quote.ask_vol4)),
            ]
        )
        table_data.append(
            [
                "卖三",
                colored_value(round(quote.ask3, 2), quote.last_close),
                chalk.yellow(int(round(quote.ask_vol3 / 100, 0))),
                chalk.magenta(get_number_desc(quote.ask3 * quote.ask_vol3)),
            ]
        )
        table_data.append(
            [
                "卖二",
                colored_value(round(quote.ask2, 2), quote.last_close),
                chalk.yellow(int(round(quote.ask_vol2 / 100, 0))),
                chalk.magenta(get_number_desc(quote.ask2 * quote.ask_vol2)),
            ]
        )
        table_data.append(
            [
                "卖一",
                colored_value(round(quote.ask1, 2), quote.last_close),
                chalk.yellow(int(round(quote.ask_vol1 / 100, 0))),
                chalk.magenta(get_number_desc(quote.ask1 * quote.ask_vol1)),
            ]
        )
        table_data.append(["-" * 10, "-" * 10, "-" * 10, "-" * 10])
        table_data.append(
            [
                "买一",
                colored_value(round(quote.bid1, 2), quote.last_close),
                chalk.yellow(int(round(quote.bid_vol1 / 100, 0))),
                chalk.magenta(get_number_desc(quote.bid1 * quote.bid_vol1)),
            ]
        )
        table_data.append(
            [
                "买二",
                colored_value(round(quote.bid2, 2), quote.last_close),
                chalk.yellow(int(round(quote.bid_vol2 / 100, 0))),
                chalk.magenta(get_number_desc(quote.bid2 * quote.bid_vol2)),
            ]
        )
        table_data.append(
            [
                "买三",
                colored_value(round(quote.bid3, 2), quote.last_close),
                chalk.yellow(int(round(quote.bid_vol3 / 100, 0))),
                chalk.magenta(get_number_desc(quote.bid3 * quote.bid_vol3)),
            ]
        )
        table_data.append(
            [
                "买四",
                colored_value(round(quote.bid4, 2), quote.last_close),
                chalk.yellow(int(round(quote.bid_vol4 / 100, 0))),
                chalk.magenta(get_number_desc(quote.bid4 * quote.bid_vol4)),
            ]
        )
        table_data.append(
            [
                "买五",
                colored_value(round(quote.bid5, 2), quote.last_close),
                chalk.yellow(int(round(quote.bid_vol5 / 100, 0))),
                chalk.magenta(get_number_desc(quote.bid5 * quote.bid_vol5)),
            ]
        )

        table = AsciiTable(table_data)
        table.inner_heading_row_border = False
        table.title = (
            f" {chalk.yellow(quote.stock_code)} - {chalk.yellow(quote.datetime)}"
        )
        print(table.table)

def get_rise_limit_by_stock_code(stock_code: str) -> float:
    """
    根据标的代码获取涨幅限制
    """
    if stock_code.startswith('60'): # 上证主板
        return 0.1
    if stock_code.startswith('68'): # 上证科创板
        return 0.2
    if stock_code.startswith('00'): # 深证主板
        return 0.1
    if stock_code.startswith('30'): # 深证创业板
        return 0.2
    return 0.1
