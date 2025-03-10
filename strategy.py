"""
Created by 满仓干 on - 2025/03/10.
"""

from typing import Optional

from simple_chalk import chalk
from libs.context import Context
from libs.models import QuoteOnline
from libs.trader import Trader
import libs.utils as utils
import libs.logger as logger

app_logger = logger.get_app_logger()


def buy(quote: Optional[QuoteOnline]) -> None:
    """
    执行逻辑
    """
    if quote == None:
        return

    stock_code = quote.stock_code

    price = quote.price
    last_close = quote.last_close

    trader = Trader.get_instance()
    context = Context.get_instance()

    # 看一下是不是，已经下过单的就不再处理了
    if context.is_already_buy(stock_code):
        return

    # 从csv文件里面取配置的信息，你可以在csv里面增加任何你需要的字段，用于下面的辅助判断
    detailed_info = context.get_stock_detail_info(stock_code)

    # 价格是涨停价并且卖一的量是0，视为涨停，你也可以加入其它条件，如：封单金额等
    # 涨停幅度可根据 stock_code前缀自行判断
    if (round(price, 2)) >= round(last_close * (1 + 0.1), 2) and quote.ask_vol1 == 0:


        ################################# 您的自定义条件从这里开始 #################################
        # 例如:
        #   1. 可以看一下stocks.csv里面的`5涨`, 大于30%终止打板
        if detailed_info.get("5涨") > 30:  # type: ignore
            print(chalk.red(f"{stock_code} 5日涨幅大于30%, 终止打板"))
            return

        #   2. 等等条件，你自己看着办

        ##################################### 自定义条件结束 #####################################


        # 看一下账户余额，是不是资金充足
        account_info = trader.query_asset()
        if account_info == None:
            app_logger.error("无法获取账户信息")
            return

        # 这里写死了一手，你可以在这里通过account_info.cash来计算可买入的手数，比如: 1/4仓，随你怎么玩
        size = 100

        # 这里是检查账户现金是不是能买入指定size
        if account_info.cash < price * size:
            app_logger.error(
                f"终止买入{stock_code}, 账户余额不足, 需要资金: {price * size}"
            )
            account_info.print()
            return

        # 执行买入操作
        order_id = trader.buy(stock_code, size, price, 11, "打板", "打板")
        if order_id != -1:
            message = f"{stock_code} 下单成功，委托价: {price:.2f}, 委托量: {size}, 成本: {price * size}"
            print(chalk.yellow(message))
            context.set_already_buy(
                stock_code
            )  # 这个是用来临时锁定用，防止在委托回调慢的情况下重复下单，有效时长1分钟
        else:
            app_logger.error(f"{stock_code} 下单失败")
    else:
        utils.print_quote_simple(quote)
