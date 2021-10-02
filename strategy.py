import indicator
import pandas as pd


def dpo_strategy(ohlcv: pd.DataFrame, n=20):
    dpo_value = indicator.DPO(ohlcv, n=n)
    direct = 'buy' if dpo_value > 0 else 'sell'
    return direct


def maamt_strategy(ohlcv: pd.DataFrame, n=40):
    maamt, volume = indicator.MAAMT(ohlcv, n=n)
    direct = 'buy' if volume > maamt else 'sell'
    return direct


def tii_strategy(ohlcv: pd.DataFrame, n1=40, n2=9):
    tii, tii_signal = indicator.TII(ohlcv, n1=n1, n2=n2)
    direct = 'buy' if tii > tii_signal else 'sell'
    return direct


def er_strategy(ohlcv: pd.DataFrame, n=20):
    direct = ''
    back_day = -1
    bull_power, bear_power = indicator.ER(ohlcv, n=n)
    if bear_power > 0:
        direct = 'buy'
    if bull_power < 0:
        direct = 'sell'
    while direct == '':
        bull_power, bear_power = indicator.ER(ohlcv[:back_day], n=n)
        if bear_power > 0:
            direct = 'buy'
        if bull_power < 0:
            direct = 'sell'
        back_day = back_day - 1
    return direct


def ma_strategy(ohlcv: pd.DataFrame, slow=20, fast=5):
    ma1 = indicator.ma(ohlcv=ohlcv, n=slow)
    ma2 = indicator.ma(ohlcv=ohlcv, n=fast)
    direct = 'buy' if ma2 > ma1 else 'sell'
    return direct


def strategy_combine(etf_data: pd.DataFrame):
    tii = tii_strategy(etf_data)
    er = er_strategy(etf_data)
    maamt = maamt_strategy(etf_data)
    dpo = dpo_strategy(etf_data)
    # 1.6
    # return [tii, er, maamt, dpo]  #胜率: 0.3739130434782609 败率: 0.6260869565217392 盈亏比: 2.2802850351731516
    # 1.5
    # return [er, maamt, dpo] # 胜率: 0.371900826446281 败率: 0.628099173553719 盈亏比: 2.1608333617392135
    # 1.81742
    return [tii, maamt, dpo]  # 胜率: 0.3816793893129771 败率: 0.6183206106870229 盈亏比: 2.3604458652855973
    # 1.53
    # return [tii, er, dpo] # 胜率: 0.3235294117647059 败率: 0.6764705882352942 盈亏比: 2.0789329373182297
    # 1.67
    # return [tii, er, maamt]  # 胜率: 0.3793103448275862 败率: 0.6206896551724138 盈亏比: 2.1514593076326016
    # 1.34
    # return [dpo] # 胜率: 0.3291139240506329 败率: 0.6708860759493671 盈亏比: 1.9961507815587536
    # 1.0
    # return [er] #  胜率: 0.2894736842105263 败率: 0.7105263157894737 盈亏比: 1.622503803423686
    # 1.66
    # return [maamt]  # 胜率: 0.45098039215686275 败率: 0.5490196078431373 盈亏比: 1.594721787384113
    # 1.5
    # return [tii]  # 胜率: 0.4714285714285714 败率: 0.5285714285714286 盈亏比: 1.7657201588535132
    # 1.56
    # return [dpo, maamt] # 胜率: 0.391304347826087 败率: 0.6086956521739131 盈亏比: 2.1270387285995613
    # 1.26
    # return [dpo, er] # 胜率: 0.3108108108108108 败率: 0.6891891891891891 盈亏比: 1.909201015635396
    # 1.75
    # return [dpo, tii]  # 胜率: 0.3108108108108108 败率: 0.6891891891891891 盈亏比: 2.2012029435186897
    # 1.8319
    # return [tii, maamt]  # 胜率: 0.4268292682926829 败率: 0.573170731707317 盈亏比: 1.8585261302548868
    # 1.59
    # return [tii, er]  # 胜率: 0.30303030303030304 败率: 0.696969696969697 盈亏比: 1.9713099171089428


# 年化收益率: OrderedDict([(2011, 0.0), (2012, -0.059182187190000124), (2013, 0.21184097379568878), (2014, 0.1917914917428023), (2015, 0.8007249383493), (2016, -0.1507829522782037), (2017, -0.01127350180272646), (2018, -0.10268130902155193), (2019, 0.33992611896744496), (2020, 0.17938762923141116), (2021, 0.1827567250195965)])
# 夏普: 0.5257240252754136
# 最大回撤:29.56，最大回撤周期1004
# 总收益率:1.24
# 交易次数: 112
# 胜率: 0.4107142857142857 败率: 0.5892857142857143 盈亏比: 3.525653102685943


"""
bencnmark

"""
