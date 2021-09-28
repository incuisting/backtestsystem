import numpy
import pandas as pd
import talib


# volume < maamt sell
# volume > maamt buy
def MAAMT(ohlcv: pd.DataFrame, n=40):
    volume = ohlcv['amount'].tolist()
    maamt = talib.MA(numpy.array(volume).astype(float), timeperiod=n)
    return [maamt[-1], volume[-1]]


# dpo > 0 buy
# dpo < 0 sell
def DPO(close_data: pd.DataFrame, n=20):
    before_day = int(n / 2 + 1)
    close_data = close_data['close'].tolist()
    ref_data = talib.SMA(numpy.array(close_data[:-before_day]), timeperiod=n)  #
    dpo = close_data[-1] - ref_data[-1]
    return dpo


def ER(ohlcv: pd.DataFrame, n=20):
    close = ohlcv['close'].tolist()
    close_ema = talib.EMA(numpy.array(close), timeperiod=n)
    period_ema = close_ema[-1]
    period_high = ohlcv['high'].tolist()[-1]
    period_low = ohlcv['low'].tolist()[-1]
    bull_power = period_high - period_ema
    bear_power = period_low - period_ema
    return [bull_power, bear_power]


def tii_line(etf_data: pd.DataFrame, n1=40):
    m = int((n1 / 2) + 1)
    dev_pos_m_day = []
    dev_neg_m_day = []
    close = etf_data['close'].tolist()
    close_ma = talib.MA(numpy.array(close), n1)
    dev_nd_array = numpy.subtract(close[-m:], close_ma[-m:])
    for dev in dev_nd_array:
        dev_pos = dev if dev > 0.0 else 0.0
        dev_neg = -dev if dev < 0.0 else 0.0
        dev_pos_m_day.append(dev_pos)
        dev_neg_m_day.append(dev_neg)
    sum_pos = sum(dev_pos_m_day)  # 求和 m 天的dev_pos
    sum_neg = sum(dev_neg_m_day)  # 求和 m 天的dev_neg
    tii = 0.0
    if (sum_pos + sum_neg) > 0:
        tii = 100 * sum_pos / (sum_pos + sum_neg)
    return tii


def calc_tii_signal(etf_data: pd.DataFrame, n1=40, n2=9):
    tii_array = []
    for index in range(0, n2):
        data = etf_data[:-index] if index != 0 else etf_data
        tii_value = tii_line(data, n1)
        tii_array.append(tii_value)
    tii_signal = talib.EMA(numpy.array(tii_array), n2)
    return tii_signal[-1]


def TII(ohlcv: pd.DataFrame, n1=40, n2=9):
    tii = tii_line(ohlcv, n1=n1)
    tii_signal = calc_tii_signal(ohlcv, n1=n1, n2=n2)
    return [tii, tii_signal]
