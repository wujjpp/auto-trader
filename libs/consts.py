"""
Created by 满仓干 on - 2025/03/10.
"""

BROKER_PRICE_ANY = 49  # 市价
BROKER_PRICE_LIMIT = 50  # 限价
BROKER_PRICE_BEST = 51  # 最优价
BROKER_PRICE_PROP_ALLOTMENT = 52  # 配股
BROKER_PRICE_PROP_REFER = 53  # 转托
BROKER_PRICE_PROP_SUBSCRIBE = 54  # 申购
BROKER_PRICE_PROP_BUYBACK = 55  # 回购
BROKER_PRICE_PROP_PLACING = 56  # 配售
BROKER_PRICE_PROP_DECIDE = 57  # 指定
BROKER_PRICE_PROP_EQUITY = 58  # 转股
BROKER_PRICE_PROP_SELLBACK = 59  # 回售
BROKER_PRICE_PROP_DIVIDEND = 60  # 股息
BROKER_PRICE_PROP_SHENZHEN_PLACING = 68  # 深圳配售确认
BROKER_PRICE_PROP_CANCEL_PLACING = 69  # 配售放弃
BROKER_PRICE_PROP_WDZY = 70  # 无冻质押
BROKER_PRICE_PROP_DJZY = 71  # 冻结质押
BROKER_PRICE_PROP_WDJY = 72  # 无冻解押
BROKER_PRICE_PROP_JDJY = 73  # 解冻解押
BROKER_PRICE_PROP_ETF = 81  # ETF申购
BROKER_PRICE_PROP_VOTE = 75  # 投票
BROKER_PRICE_PROP_YYSGYS = 92  # 要约收购预售
BROKER_PRICE_PROP_YSYYJC = 77  # 预售要约解除
BROKER_PRICE_PROP_FUND_DEVIDEND = 78  # 基金设红
BROKER_PRICE_PROP_FUND_ENTRUST = 79  # 基金申赎
BROKER_PRICE_PROP_CROSS_MARKET = 80  # 跨市转托
BROKER_PRICE_PROP_EXERCIS = 83  # 权证行权
BROKER_PRICE_PROP_PEER_PRICE_FIRST = 84  # 对手方最优价格
BROKER_PRICE_PROP_L5_FIRST_LIMITPX = 85  # 最优五档即时成交剩余转限价
BROKER_PRICE_PROP_MIME_PRICE_FIRST = 86  # 本方最优价格
BROKER_PRICE_PROP_INSTBUSI_RESTCANCEL = 87  # 即时成交剩余撤销
BROKER_PRICE_PROP_L5_FIRST_CANCEL = 88  # 最优五档即时成交剩余撤销
BROKER_PRICE_PROP_FULL_REAL_CANCEL = 89  # 全额成交并撤单
BROKER_PRICE_PROP_DIRECT_SECU_REPAY = 101  # 直接还券
BROKER_PRICE_PROP_FUND_CHAIHE = 90  # 基金拆合
BROKER_PRICE_PROP_DEBT_CONVERSION = 91  # 债转股
BROKER_PRICE_BID_LIMIT = 92  # 港股通竞价限价
BROKER_PRICE_ENHANCED_LIMIT = 93  # 港股通增强限价
BROKER_PRICE_RETAIL_LIMIT = 94  # 港股通零股限价
BROKER_PRICE_PROP_INCREASE_SHARE = "j"  # 增发
BROKER_PRICE_PROP_COLLATERAL_TRANSFER = 107  # 担保品划转
BROKER_PRICE_PROP_NEEQ_PRICING = "w"  # 定价（全国股转 - 挂牌公司交易 - 协议转让）
BROKER_PRICE_PROP_NEEQ_MATCH_CONFIRM = (
    "x"  # 成交确认（全国股转 - 挂牌公司交易 - 协议转让）
)
BROKER_PRICE_PROP_NEEQ_MUTUAL_MATCH_CONFIRM = (
    "y"  # 互报成交确认（全国股转 - 挂牌公司交易 - 协议转让）
)
BROKER_PRICE_PROP_NEEQ_LIMIT = (
    "z"  # 限价（用于挂牌公司交易 - 做市转让 - 限价买卖和两网及退市交易-限价买卖）
)


# 最新价
LATEST_PRICE = 5
# 指定价/限价
FIX_PRICE = 11
# 对手方最优价格委托[上交所[股票]][深交所[股票][期权]]
MARKET_PEER_PRICE_FIRST = 44
# 本方最优价格委托[上交所[股票]][深交所[股票][期权]]
MARKET_MINE_PRICE_FIRST = 45
