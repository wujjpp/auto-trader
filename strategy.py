"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""


import traceback
from typing import Optional

from simple_chalk import chalk
from libs.context import Context
from libs.models import QuoteOnline
from libs.trader import Trader
import libs.utils as utils
import libs.logger as logger

app_logger = logger.get_app_logger()

def action(quote: Optional[QuoteOnline]) -> None:
    """
    假如你把持仓也在stocks.csv里面，或者直接从QMT里面获取持仓，在订阅里面加入这些标的，这边可以分流出“买”和“卖”逻辑
    """
    buy(quote)

def buy(quote: Optional[QuoteOnline]) -> None:
    """
    执行买入逻辑
    """

    try:
        if quote == None:
            return

        stock_code = quote.stock_code

        price = quote.price
        last_close = quote.last_close

        trader = Trader.get_instance()
        context = Context.get_instance()

        # 看一下是不是已经下过单，下过单的就不再处理了
        if context.is_already_buy(stock_code):
            return

        # 从csv文件里面取配置的信息，你可以在csv里面增加任何你需要的字段，用于下面的辅助判断
        # detailed_info实际上就是csv文件里面对应stock的那行数据
        detailed_info = context.get_stock_detail_info(stock_code)
        if detailed_info == None:
            print(
                chalk.red(f"{stock_code} 无法在csv文件中获取标的信息")
            )  # 一般不会发生，毕竟订阅是从这个文件来的，考虑到强壮性，还是加个判断
            return

        # 价格是涨停价并且卖一的量是0，视为涨停，你也可以加入其它条件
        rise_limit = utils.get_rise_limit_by_stock_code(stock_code)
        if (round(price, 2)) >= round(
            last_close * (1 + rise_limit), 2
        ) and quote.ask_vol1 == 0:

            ######################################################################
            #      定制条件从这里开始 - 你的策略逻辑应该都写在这里                      #
            ######################################################################

            # 例如:
            #   1. 可以看一下stocks.csv里面的有个栏位叫`5涨`, 那么我们就可以增加一个“5日涨幅大于20%终止打板”的条件
            if detailed_info.get("5涨") > 20:  # type: ignore
                app_logger.info(f"{stock_code} 5日涨幅大于20%, 终止打板")
                return

            #   2. 例如：增加一个封单金额条件必须大于1000万才进行打板
            if quote.bid1 * quote.bid_vol1 < 10000000.0:
                app_logger.info(f"{stock_code} 封单金额小于1000万，终止打板")
                return

            #   3. 再举个例子：假设csv里面有个栏位叫`自由流通股本`，
            #      那么你可以通过 quote.volume * 100 / detailed_info.get("自由流通股本") 计算换手率,
            #      通过换手率参数来判断要不要继续打板

            #   4. XtQuant.XtData 提供很多数据接口，你也可以在这里调用这些模块，https://dict.thinktrader.net/nativeApi/xtdata.html?id=XM8JiS

            #   5. 你可以写很多条件在这里，自由发挥，只要有数据，一切皆有可能

            ############################ 定制条件结束 ###########################

            # 看一下账户余额，是不是资金充足
            account_info = trader.query_asset()
            if account_info == None:
                app_logger.error("无法获取账户信息")
                return

            # 你可以在这里通过account_info.cash来计算可买入的手数
            # 比如: 剩余资金的 1/4 对该标的进行打板，那么: size = int(account_info.cash / 4 / (price * 100)) * 100
            # 想这么玩，你自己看着办，但这里仅仅是用于测试，就写死了100股，即一手
            size = 100

            # 检查账户剩余现金在该价格上是不是能买入指定size
            if account_info.cash < price * size:
                app_logger.error(
                    f"终止买入{stock_code}, 账户余额不足, 需要资金: {price * size}, 剩余资金: {account_info.cash}"
                )
                account_info.print()
                return

            # 执行买入操作 - 这边就是真正的下单了
            order_id = trader.buy(stock_code, size, price, 11, "打板", detailed_info.get("备注", ""))  # type: ignore
            if order_id != -1:
                message = f"{stock_code} 下单成功，委托价: {price:.2f}, 委托量: {size}, 成本: {price * size}"
                print(chalk.yellow(message))
                # 这个是用来临时锁定用，防止在委托回调慢的情况下重复下单，有效时长1分钟
                context.set_already_buy(stock_code)
            else:
                app_logger.error(f"{stock_code} 下单失败，QMT返回的委托单号是-1")
        # else:
        #     utils.print_quote_simple(quote)

    except Exception as err:
        traceback.print_exc()
        app_logger.error(str(err))

def sell(quote: Optional[QuoteOnline]) -> None:
    """
    执行卖出操作
    """
    pass
