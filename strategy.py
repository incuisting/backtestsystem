import indicator
import pandas as pd


def dpo_strategy(ohlcv: pd.DataFrame):
    dpo_value = indicator.DPO(ohlcv)
    direct = 'buy' if dpo_value > 0 else 'sell'
    return direct


def maamt_strategy(ohlcv: pd.DataFrame):
    maamt, volume = indicator.MAAMT(ohlcv)
    direct = 'buy' if volume > maamt else 'sell'
    return direct


def tii_strategy(ohlcv: pd.DataFrame):
    tii, tii_signal = indicator.TII(ohlcv, n1=40, n2=9)
    direct = 'buy' if tii > tii_signal else 'sell'
    return direct


def er_strategy(ohlcv: pd.DataFrame):
    direct = ''
    back_day = -1
    bull_power, bear_power = indicator.ER(ohlcv)
    if bear_power > 0:
        direct = 'buy'
    if bull_power < 0:
        direct = 'sell'
    while direct == '':
        bull_power, bear_power = indicator.ER(ohlcv[:back_day])
        if bear_power > 0:
            direct = 'buy'
        if bull_power < 0:
            direct = 'sell'
        back_day = back_day - 1
    return direct


def strategy_combine(etf_data: pd.DataFrame):
    tii = tii_strategy(etf_data)
    er = er_strategy(etf_data)
    maamt = maamt_strategy(etf_data)
    dpo = dpo_strategy(etf_data)
    # return [tii, er, maamt, dpo]  # 最大回撤:36.90，最大回撤周期1032 总收益率:1.05
    # return [er, maamt, dpo] # 最大回撤:38.97，最大回撤周期1121 总收益率:1.15
    # return [tii, maamt, dpo] # 最大回撤:29.76，最大回撤周期1006 总收益率:1.07
    # return [tii, er, dpo] # 最大回撤:41.67，最大回撤周期1126 总收益率:1.02
    # return [tii, er, maamt]  # 最大回撤:35.01，最大回撤周期1031 总收益率:1.03
    # return [dpo] # 最大回撤:44.72(2)，,最大回撤周期1241 总收益率:1.20(4)6
    # return [er] # 最大回撤:53.82(1)，最大回撤周期1422 总收益率:1.05(3)4
    # return [maamt]  #最大回撤:29.94(4)，最大回撤周期1117 总收益率:0.83(2)6
    # return [tii]  # 最大回撤:37.84(3)，最大回撤周期1239 总收益率:0.70(1)4
    return [dpo, maamt] # 最大回撤:31.40，最大回撤周期1013 总收益率:1.17
    # return [dpo, er] #
    # return [tii, maamt]  # 最大回撤:28.50，最大回撤周期935 总收益率:0.88
