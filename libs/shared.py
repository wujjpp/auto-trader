"""
Created by 满仓干 on - 2025/03/10.
"""

"""
免责声明: 
本程序仅供学习交流使用，在实盘使用本程序造成的投资上(不仅限于)的任何损失与程序作者无任何关系, 同意才能使用
运行本程序即同意上述免责声明 
"""

import datetime
import json
from typing import List
import numpy as np
import xtquant.xtconstant as xtconstant
import libs.consts as consts
import math


def json_default(v):
    if isinstance(v, datetime.datetime):
        return v.strftime("%Y-%m-%d %H:%M:%S")  # type: ignore
    if isinstance(v, (int, float)):
        if math.isnan(v):
            return None
        if math.isinf(v):
            return None
        return v

    if type(v) in [np.int32, np.int64]:
        if np.isnan(v):
            return None
        if np.isinf(v):
            return None
        return int(v)
    return str(v)


def json_dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, default=json_default)


def json_parse(s: str) -> dict:
    return json.loads(s)


def xtobject_to_dict(xtobject) -> dict:
    prop_names = list(
        filter(lambda s: not (s.startswith("__") or s.startswith("m_")), dir(xtobject))
    )
    r = {}
    for name in prop_names:
        r[name] = getattr(xtobject, name)
    return r


def xtlist_to_list(xtlist: List) -> List[dict]:
    return [xtobject_to_dict(x) for x in xtlist]


def decode_account_type(account_type) -> str:
    """
    期货 - xtconstant.FUTURE_ACCOUNT
    股票 - xtconstant.SECURITY_ACCOUNT
    信用 - xtconstant.CREDIT_ACCOUNT
    期货期权 - xtconstant.FUTURE_OPTION_ACCOUNT
    股票期权 - xtconstant.STOCK_OPTION_ACCOUNT
    沪港通 - xtconstant.HUGANGTONG_ACCOUNT
    深港通 - xtconstant.SHENGANGTONG_ACCOUNT
    """
    if account_type == xtconstant.FUTURE_ACCOUNT:
        return "期货"
    elif account_type == xtconstant.SECURITY_ACCOUNT:
        return "股票"
    elif account_type == xtconstant.CREDIT_ACCOUNT:
        return "信用"
    elif account_type == xtconstant.FUTURE_OPTION_ACCOUNT:
        return "期货期权"
    elif account_type == xtconstant.STOCK_OPTION_ACCOUNT:
        return "股票期权"
    elif account_type == xtconstant.HUGANGTONG_ACCOUNT:
        return "沪港通"
    elif account_type == xtconstant.SHENGANGTONG_ACCOUNT:
        return "深港通"
    else:
        return str(account_type)


def decode_login_status(login_status) -> str:
    """
    xtconstant.ACCOUNT_STATUS_INVALID               -1  无效
    xtconstant.ACCOUNT_STATUS_OK                    0   正常
    xtconstant.ACCOUNT_STATUS_WAITING_LOGIN         1   连接中
    xtconstant.ACCOUNT_STATUSING                    2   登陆中
    xtconstant.ACCOUNT_STATUS_FAIL                  3   失败
    xtconstant.ACCOUNT_STATUS_INITING               4   初始化中
    xtconstant.ACCOUNT_STATUS_CORRECTING            5   数据刷新校正中
    xtconstant.ACCOUNT_STATUS_CLOSED                6   收盘后
    xtconstant.ACCOUNT_STATUS_ASSIS_FAIL            7   穿透副链接断开
    xtconstant.ACCOUNT_STATUS_DISABLEBYSYS          8   系统停用（总线使用-密码错误超限）
    xtconstant.ACCOUNT_STATUS_DISABLEBYUSER         9   用户停用（总线使用）
    """

    if login_status == xtconstant.ACCOUNT_STATUS_INVALID:
        return "无效"
    elif login_status == xtconstant.ACCOUNT_STATUS_OK:
        return "正常"
    elif login_status == xtconstant.ACCOUNT_STATUS_WAITING_LOGIN:
        return "连接中"
    elif login_status == xtconstant.ACCOUNT_STATUSING:
        return "登陆中"
    elif login_status == xtconstant.ACCOUNT_STATUS_FAIL:
        return "失败"
    elif login_status == xtconstant.ACCOUNT_STATUS_INITING:
        return "初始化中"
    elif login_status == xtconstant.ACCOUNT_STATUS_CORRECTING:
        return "数据刷新校正中"
    elif login_status == xtconstant.ACCOUNT_STATUS_CLOSED:
        return "收盘后"
    elif login_status == xtconstant.ACCOUNT_STATUS_ASSIS_FAIL:
        return "穿透副链接断开"
    elif login_status == xtconstant.ACCOUNT_STATUS_DISABLEBYSYS:
        return "系统停用（总线使用-密码错误超限）"
    elif login_status == xtconstant.ACCOUNT_STATUS_DISABLEBYUSER:
        return "用户停用（总线使用）"
    else:
        return str(login_status)


def decode_order_type(order_type) -> str:
    """
    STOCK_BUY = 23
    STOCK_SELL = 24
    CREDIT_BUY = 23    #担保品买入
    CREDIT_SELL = 24   #担保品卖出
    CREDIT_FIN_BUY = 27 #融资买入
    CREDIT_SLO_SELL  = 28 #融券卖出
    CREDIT_BUY_SECU_REPAY = 29 #买券还券
    CREDIT_DIRECT_SECU_REPAY = 30 #直接还券
    CREDIT_SELL_SECU_REPAY  = 31 #卖券还款
    CREDIT_DIRECT_CASH_REPAY = 32 #直接还款
    CREDIT_FIN_BUY_SPECIAL = 40 #专项融资买入
    CREDIT_SLO_SELL_SPECIAL  = 41 #专项融券卖出
    CREDIT_BUY_SECU_REPAY_SPECIAL = 42 #专项买券还券
    CREDIT_DIRECT_SECU_REPAY_SPECIAL = 43 #专项直接还券
    CREDIT_SELL_SECU_REPAY_SPECIAL  = 44 #专项卖券还款
    CREDIT_DIRECT_CASH_REPAY_SPECIAL = 45 #专项直接还款
    """

    if order_type == xtconstant.STOCK_BUY:
        return "股票买入"
    elif order_type == xtconstant.STOCK_SELL:
        return "股票卖出"
    elif order_type == xtconstant.CREDIT_BUY:
        return "担保品买入"
    elif order_type == xtconstant.CREDIT_SELL:
        return "担保品卖出"
    elif order_type == xtconstant.CREDIT_FIN_BUY:
        return "融资买入"
    elif order_type == xtconstant.CREDIT_SLO_SELL:
        return "融券卖出"
    elif order_type == xtconstant.CREDIT_BUY_SECU_REPAY:
        return "买券还券"
    elif order_type == xtconstant.CREDIT_DIRECT_SECU_REPAY:
        return "直接还券"
    elif order_type == xtconstant.CREDIT_SELL_SECU_REPAY:
        return "卖券还款"
    elif order_type == xtconstant.CREDIT_DIRECT_CASH_REPAY:
        return "直接还款"
    elif order_type == xtconstant.CREDIT_FIN_BUY_SPECIAL:
        return "专项融资买入"
    elif order_type == xtconstant.CREDIT_SLO_SELL_SPECIAL:
        return "专项融券卖出"
    elif order_type == xtconstant.CREDIT_BUY_SECU_REPAY_SPECIAL:
        return "专项买券还券"
    elif order_type == xtconstant.CREDIT_DIRECT_SECU_REPAY_SPECIAL:
        return "专项直接还券"
    elif order_type == xtconstant.CREDIT_SELL_SECU_REPAY_SPECIAL:
        return "专项卖券还款"
    elif order_type == xtconstant.CREDIT_DIRECT_CASH_REPAY_SPECIAL:
        return "专项直接还款"
    else:
        return str(order_type)


def decode_price_type(price_type) -> str:
    """
    LATEST_PRICE = 5                                    # 最新价
    FIX_PRICE = 11                                      # 指定价/限价
    MARKET_BEST = 18                                    # 市价最优价[郑商所][期货]
    MARKET_CANCEL = 19                                  # 市价即成剩撤[大商所][期货]
    MARKET_CANCEL_ALL = 20                              # 市价全额成交或撤[大商所][期货]
    MARKET_CANCEL_1 = 21                                # 市价最优一档即成剩撤[中金所][期货]
    MARKET_CANCEL_5 = 22                                # 市价最优五档即成剩撤[中金所][期货]
    MARKET_CONVERT_5 = 24                               # 市价最优五档即成剩转[中金所][期货]
    MARKET_SH_CONVERT_5_CANCEL = 42                     # 最优五档即时成交剩余撤销[上交所][股票]
    MARKET_SH_CONVERT_5_LIMIT = 43                      # 最优五档即时成交剩转限价[上交所][股票]
    MARKET_PEER_PRICE_FIRST = 44                        # 对手方最优价格委托[上交所[股票]][深交所[股票][期权]]
    MARKET_MINE_PRICE_FIRST = 45                        # 本方最优价格委托[上交所[股票]][深交所[股票][期权]]
    MARKET_SZ_INSTBUSI_RESTCANCEL = 46                  # 即时成交剩余撤销委托[深交所][股票][期权]
    MARKET_SZ_CONVERT_5_CANCEL = 47                     # 最优五档即时成交剩余撤销[深交所][股票][期权]
    MARKET_SZ_FULL_OR_CANCEL = 48                       # 全额成交或撤销委托[深交所][股票][期权]

    BROKER_PRICE_ANY    49                              # 市价
    BROKER_PRICE_LIMIT  50                              # 限价
    BROKER_PRICE_BEST   51                              # 最优价
    BROKER_PRICE_PROP_ALLOTMENT 52                      # 配股
    BROKER_PRICE_PROP_REFER 53                          # 转托
    BROKER_PRICE_PROP_SUBSCRIBE 54                      # 申购
    BROKER_PRICE_PROP_BUYBACK   55                      # 回购
    BROKER_PRICE_PROP_PLACING   56                      # 配售
    BROKER_PRICE_PROP_DECIDE    57                      # 指定
    BROKER_PRICE_PROP_EQUITY    58                      # 转股
    BROKER_PRICE_PROP_SELLBACK  59                      # 回售
    BROKER_PRICE_PROP_DIVIDEND  60                      # 股息
    BROKER_PRICE_PROP_SHENZHEN_PLACING  68              # 深圳配售确认
    BROKER_PRICE_PROP_CANCEL_PLACING    69              # 配售放弃
    BROKER_PRICE_PROP_WDZY  70                          # 无冻质押
    BROKER_PRICE_PROP_DJZY  71                          # 冻结质押
    BROKER_PRICE_PROP_WDJY  72                          # 无冻解押
    BROKER_PRICE_PROP_JDJY  73                          # 解冻解押
    BROKER_PRICE_PROP_ETF   81                          # ETF申购
    BROKER_PRICE_PROP_VOTE  75                          # 投票
    BROKER_PRICE_PROP_YYSGYS    92                      # 要约收购预售
    BROKER_PRICE_PROP_YSYYJC    77                      # 预售要约解除
    BROKER_PRICE_PROP_FUND_DEVIDEND 78                  # 基金设红
    BROKER_PRICE_PROP_FUND_ENTRUST  79                  # 基金申赎
    BROKER_PRICE_PROP_CROSS_MARKET  80                  # 跨市转托
    BROKER_PRICE_PROP_EXERCIS   83                      # 权证行权
    BROKER_PRICE_PROP_PEER_PRICE_FIRST  84              # 对手方最优价格
    BROKER_PRICE_PROP_L5_FIRST_LIMITPX  85              # 最优五档即时成交剩余转限价
    BROKER_PRICE_PROP_MIME_PRICE_FIRST  86              # 本方最优价格
    BROKER_PRICE_PROP_INSTBUSI_RESTCANCEL   87          # 即时成交剩余撤销
    BROKER_PRICE_PROP_L5_FIRST_CANCEL   88              # 最优五档即时成交剩余撤销
    BROKER_PRICE_PROP_FULL_REAL_CANCEL  89              # 全额成交并撤单
    BROKER_PRICE_PROP_DIRECT_SECU_REPAY 101             # 直接还券
    BROKER_PRICE_PROP_FUND_CHAIHE   90                  # 基金拆合
    BROKER_PRICE_PROP_DEBT_CONVERSION   91              # 债转股
    BROKER_PRICE_BID_LIMIT  92                          # 港股通竞价限价
    BROKER_PRICE_ENHANCED_LIMIT 93                      # 港股通增强限价
    BROKER_PRICE_RETAIL_LIMIT   94                      # 港股通零股限价
    BROKER_PRICE_PROP_INCREASE_SHARE    'j'             # 增发
    BROKER_PRICE_PROP_COLLATERAL_TRANSFER   107         # 担保品划转
    BROKER_PRICE_PROP_NEEQ_PRICING  'w'                 # 定价（全国股转 - 挂牌公司交易 - 协议转让）
    BROKER_PRICE_PROP_NEEQ_MATCH_CONFIRM    'x'         # 成交确认（全国股转 - 挂牌公司交易 - 协议转让）
    BROKER_PRICE_PROP_NEEQ_MUTUAL_MATCH_CONFIRM 'y'     # 互报成交确认（全国股转 - 挂牌公司交易 - 协议转让）
    BROKER_PRICE_PROP_NEEQ_LIMIT    'z'                 # 限价（用于挂牌公司交易 - 做市转让 - 限价买卖和两网及退市交易-限价买卖）

    """

    if price_type == xtconstant.LATEST_PRICE:
        return "最新价"
    elif price_type == xtconstant.FIX_PRICE:
        return "指定价/限价"
    elif price_type == xtconstant.MARKET_BEST:
        return "市价最优价[郑商所][期货]"
    elif price_type == xtconstant.MARKET_CANCEL:
        return "市价即成剩撤[大商所][期货]"
    elif price_type == xtconstant.MARKET_CANCEL_ALL:
        return "市价全额成交或撤[大商所][期货]"
    elif price_type == xtconstant.MARKET_CANCEL_1:
        return "市价最优一档即成剩撤[中金所][期货]"
    elif price_type == xtconstant.MARKET_CANCEL_5:
        return "市价最优五档即成剩撤[中金所][期货]"
    elif price_type == xtconstant.MARKET_CONVERT_5:
        return "市价最优五档即成剩转[中金所][期货]"
    elif price_type == xtconstant.MARKET_SH_CONVERT_5_CANCEL:
        return "最优五档即时成交剩余撤销[上交所][股票]"
    elif price_type == xtconstant.MARKET_SH_CONVERT_5_LIMIT:
        return "最优五档即时成交剩转限价[上交所][股票]"
    elif price_type == xtconstant.MARKET_PEER_PRICE_FIRST:
        return "对手方最优价格委托[上交所[股票]][深交所[股票][期权]]"
    elif price_type == xtconstant.MARKET_MINE_PRICE_FIRST:
        return "本方最优价格委托[上交所[股票]][深交所[股票][期权]]"
    elif price_type == xtconstant.MARKET_SZ_INSTBUSI_RESTCANCEL:
        return "即时成交剩余撤销委托[深交所][股票][期权]"
    elif price_type == xtconstant.MARKET_SZ_CONVERT_5_CANCEL:
        return "最优五档即时成交剩余撤销[深交所][股票][期权]"
    elif price_type == xtconstant.MARKET_SZ_FULL_OR_CANCEL:
        return "全额成交或撤销委托[深交所][股票][期权]"

    # 下面是补充的
    elif price_type == consts.BROKER_PRICE_ANY:
        return "市价"
    elif price_type == consts.BROKER_PRICE_LIMIT:
        return "限价"
    elif price_type == consts.BROKER_PRICE_BEST:
        return "最优价"
    elif price_type == consts.BROKER_PRICE_PROP_ALLOTMENT:
        return "配股"
    elif price_type == consts.BROKER_PRICE_PROP_REFER:
        return "转托"
    elif price_type == consts.BROKER_PRICE_PROP_SUBSCRIBE:
        return "申购"
    elif price_type == consts.BROKER_PRICE_PROP_BUYBACK:
        return "回购"
    elif price_type == consts.BROKER_PRICE_PROP_PLACING:
        return "配售"
    elif price_type == consts.BROKER_PRICE_PROP_DECIDE:
        return "指定"
    elif price_type == consts.BROKER_PRICE_PROP_EQUITY:
        return "转股"
    elif price_type == consts.BROKER_PRICE_PROP_SELLBACK:
        return "回售"
    elif price_type == consts.BROKER_PRICE_PROP_DIVIDEND:
        return "股息"
    elif price_type == consts.BROKER_PRICE_PROP_SHENZHEN_PLACING:
        return "深圳配售确认"
    elif price_type == consts.BROKER_PRICE_PROP_CANCEL_PLACING:
        return "配售放弃"
    elif price_type == consts.BROKER_PRICE_PROP_WDZY:
        return "无冻质押"
    elif price_type == consts.BROKER_PRICE_PROP_DJZY:
        return "冻结质押"
    elif price_type == consts.BROKER_PRICE_PROP_WDJY:
        return "无冻解押"
    elif price_type == consts.BROKER_PRICE_PROP_JDJY:
        return "解冻解押"
    elif price_type == consts.BROKER_PRICE_PROP_ETF:
        return "ETF申购"
    elif price_type == consts.BROKER_PRICE_PROP_VOTE:
        return "投票"
    elif price_type == consts.BROKER_PRICE_PROP_YYSGYS:
        return "要约收购预售"
    elif price_type == consts.BROKER_PRICE_PROP_YSYYJC:
        return "预售要约解除"
    elif price_type == consts.BROKER_PRICE_PROP_FUND_DEVIDEND:
        return "基金设红"
    elif price_type == consts.BROKER_PRICE_PROP_FUND_ENTRUST:
        return "基金申赎"
    elif price_type == consts.BROKER_PRICE_PROP_CROSS_MARKET:
        return "跨市转托"
    elif price_type == consts.BROKER_PRICE_PROP_EXERCIS:
        return "权证行权"
    elif price_type == consts.BROKER_PRICE_PROP_PEER_PRICE_FIRST:
        return "对手方最优价格"
    elif price_type == consts.BROKER_PRICE_PROP_L5_FIRST_LIMITPX:
        return "最优五档即时成交剩余转限价"
    elif price_type == consts.BROKER_PRICE_PROP_MIME_PRICE_FIRST:
        return "本方最优价格"
    elif price_type == consts.BROKER_PRICE_PROP_INSTBUSI_RESTCANCEL:
        return "即时成交剩余撤销"
    elif price_type == consts.BROKER_PRICE_PROP_L5_FIRST_CANCEL:
        return "最优五档即时成交剩余撤销"
    elif price_type == consts.BROKER_PRICE_PROP_FULL_REAL_CANCEL:
        return "全额成交并撤单"
    elif price_type == consts.BROKER_PRICE_PROP_DIRECT_SECU_REPAY:
        return "直接还券"
    elif price_type == consts.BROKER_PRICE_PROP_FUND_CHAIHE:
        return "基金拆合"
    elif price_type == consts.BROKER_PRICE_PROP_DEBT_CONVERSION:
        return "债转股"
    elif price_type == consts.BROKER_PRICE_BID_LIMIT:
        return "港股通竞价限价"
    elif price_type == consts.BROKER_PRICE_ENHANCED_LIMIT:
        return "港股通增强限价"
    elif price_type == consts.BROKER_PRICE_RETAIL_LIMIT:
        return "港股通零股限价"
    elif price_type == consts.BROKER_PRICE_PROP_INCREASE_SHARE:
        return "增发"
    elif price_type == consts.BROKER_PRICE_PROP_COLLATERAL_TRANSFER:
        return "担保品划转"
    elif price_type == consts.BROKER_PRICE_PROP_NEEQ_PRICING:
        return "定价（全国股转 - 挂牌公司交易 - 协议转让）"
    elif price_type == consts.BROKER_PRICE_PROP_NEEQ_MATCH_CONFIRM:
        return "成交确认（全国股转 - 挂牌公司交易 - 协议转让）"
    elif price_type == consts.BROKER_PRICE_PROP_NEEQ_MUTUAL_MATCH_CONFIRM:
        return "互报成交确认（全国股转 - 挂牌公司交易 - 协议转让）"
    elif price_type == consts.BROKER_PRICE_PROP_NEEQ_LIMIT:
        return "限价（用于挂牌公司交易 - 做市转让 - 限价买卖和两网及退市交易-限价买卖）"

    else:
        return str(price_type)


def decode_order_status(order_status) -> str:
    """
    xtconstant.ORDER_UNREPORTED 48              未报
    xtconstant.ORDER_WAIT_REPORTING	49	        待报
    xtconstant.ORDER_REPORTED   50              已报
    xtconstant.ORDER_REPORTED_CANCEL    51      已报待撤
    xtconstant.ORDER_PARTSUCC_CANCEL    52      部成待撤
    xtconstant.ORDER_PART_CANCEL    53          部撤
    xtconstant.ORDER_CANCELED   54              已撤
    xtconstant.ORDER_PART_SUCC  55              部成
    xtconstant.ORDER_SUCCEEDED  56              已成
    xtconstant.ORDER_JUNK   57                  废单
    xtconstant.ORDER_JUNK   59                  申购
    xtconstant.ORDER_UNKNOWN    255             未知

    """

    if order_status == xtconstant.ORDER_UNREPORTED:
        return "未报"
    elif order_status == xtconstant.ORDER_WAIT_REPORTING:
        return "待报"
    elif order_status == xtconstant.ORDER_REPORTED:
        return "已报"
    elif order_status == xtconstant.ORDER_REPORTED_CANCEL:
        return "已报待撤"
    elif order_status == xtconstant.ORDER_PARTSUCC_CANCEL:
        return "部成待撤"
    elif order_status == xtconstant.ORDER_PART_CANCEL:
        return "部撤"
    elif order_status == xtconstant.ORDER_CANCELED:
        return "已撤"
    elif order_status == xtconstant.ORDER_PART_SUCC:
        return "部成"
    elif order_status == xtconstant.ORDER_SUCCEEDED:
        return "已成"
    elif order_status == xtconstant.ORDER_JUNK:
        return "废单"
    elif order_status == 59:
        return "申购"
    elif order_status == xtconstant.ORDER_UNKNOWN:
        return "未知"
    else:
        return str(order_status)


def decode_direction(direction) -> str:
    """
    xtconstant.DIRECTION_FLAG_LONG  48  多
    xtconstant.DIRECTION_FLAG_SHORT 49  空

    xtconstant.DIRECTION_FLAG_BUY = 48 #买入
    xtconstant.DIRECTION_FLAG_SELL = 49 #卖出
    """

    if direction == xtconstant.DIRECTION_FLAG_LONG:
        return "多"
    elif direction == xtconstant.DIRECTION_FLAG_SHORT:
        return "空"
    elif direction == xtconstant.DIRECTION_FLAG_BUY:
        return "买入"
    elif direction == xtconstant.DIRECTION_FLAG_SELL:
        return "卖出"
    else:
        return str(direction)


def decode_offset_flag(offset_flag) -> str:
    """
    xtconstant.OFFSET_FLAG_OPEN 48              买入，开仓
    xtconstant.OFFSET_FLAG_CLOSE    49          卖出，平仓
    xtconstant.OFFSET_FLAG_FORCECLOSE   50      强平
    xtconstant.OFFSET_FLAG_CLOSETODAY   51      平今
    xtconstant.OFFSET_FLAG_ClOSEYESTERDAY   52  平昨
    xtconstant.OFFSET_FLAG_FORCEOFF 53          强减
    xtconstant.OFFSET_FLAG_LOCALFORCECLOSE  54  本地强平
    """

    if offset_flag == xtconstant.OFFSET_FLAG_OPEN:
        return "买入/开仓"
    elif offset_flag == xtconstant.OFFSET_FLAG_CLOSE:
        return "卖出/平仓"
    elif offset_flag == xtconstant.OFFSET_FLAG_FORCECLOSE:
        return "强平"
    elif offset_flag == xtconstant.OFFSET_FLAG_CLOSETODAY:
        return "平今"
    elif offset_flag == xtconstant.OFFSET_FLAG_ClOSEYESTERDAY:
        return "平昨"
    elif offset_flag == xtconstant.OFFSET_FLAG_FORCEOFF:
        return "强减"
    elif offset_flag == xtconstant.OFFSET_FLAG_LOCALFORCECLOSE:
        return "本地强平"
    else:
        return str(offset_flag)


def safe_append_name(obj: dict, prop_name: str, applyer) -> dict:
    v = obj.get(prop_name)
    if v != None:
        obj[f"{prop_name}_name"] = applyer(obj[prop_name])
    return obj


def patch_xtasset(asset: dict) -> dict:
    asset = safe_append_name(asset, "account_type", decode_account_type)
    return asset


def patch_xtorder(order: dict) -> dict:
    order = safe_append_name(order, "account_type", decode_account_type)
    order = safe_append_name(order, "order_type", decode_order_type)
    order = safe_append_name(order, "price_type", decode_price_type)
    order = safe_append_name(order, "order_status", decode_order_status)
    order = safe_append_name(order, "direction", decode_direction)
    order = safe_append_name(order, "offset_flag", decode_offset_flag)

    return order


def patch_xttrade(trade):
    trade = safe_append_name(trade, "account_type", decode_account_type)
    trade = safe_append_name(trade, "order_type", decode_order_type)
    trade = safe_append_name(trade, "direction", decode_direction)
    trade = safe_append_name(trade, "offset_flag", decode_offset_flag)
    return trade


def patch_xtposition(position):
    position = safe_append_name(position, "account_type", decode_account_type)
    position = safe_append_name(position, "direction", decode_direction)
    if math.isnan(position.get("avg_price", 0)) or position.get("volume", 0) == 0:
        position["avg_price"] = 0
        position["open_price"] = 0
    return position


def patch_xtaccountinfo(account):
    account = safe_append_name(account, "account_type", decode_account_type)
    account = safe_append_name(account, "login_status", decode_login_status)
    return account


def patch_xtaccountstatus(account):
    account = safe_append_name(account, "account_type", decode_account_type)
    account = safe_append_name(account, "status", decode_login_status)
    return account


def patch_xtordererror(order_error):
    order_error = safe_append_name(order_error, "account_type", decode_account_type)
    return order_error


def patch_xtcancelerror(cancel_error):
    cancel_error = safe_append_name(cancel_error, "account_type", decode_account_type)
    market = cancel_error.get("market")
    if market == 0:
        cancel_error["market_name"] = "上海"
    elif market == 1:
        cancel_error["market_name"] = "深圳"
    else:
        cancel_error["market_name"] = "未知"
    return cancel_error
