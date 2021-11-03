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
    ma_data = talib.SMA(numpy.array(close_data), timeperiod=n)  #
    dpo = close_data[-1] - ma_data[-before_day]
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
    m = int(n1 / 2) if n1 % 2 == 0 else int((n1 / 2) + 1)
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


def calc_tii_signal(etf_data: pd.DataFrame, n1=40, n2=9, signal_type: str = 'EMA'):
    tii_array = []
    for index in range(0, n2):
        data = etf_data[:-index] if index != 0 else etf_data
        tii_value = tii_line(data, n1)
        tii_array.append(tii_value)
    signal_func = getattr(talib, signal_type)
    tii_signal = signal_func(numpy.array(tii_array), n2)
    return tii_signal[-1]


def TII(ohlcv: pd.DataFrame, n1=40, n2=9, signal_type: str = 'EMA'):
    tii = tii_line(ohlcv, n1=n1)
    tii_signal = calc_tii_signal(ohlcv, n1=n1, n2=n2, signal_type=signal_type)
    return [tii, tii_signal]


def ma(ohlcv: pd.DataFrame, n=20):
    close = ohlcv['close'].tolist()
    close_ma = talib.SMA(numpy.array(close), timeperiod=n)
    return close_ma[-1]


def po(ohlcv: pd.DataFrame, short_n=9, long_n=26):
    close = ohlcv['close'].tolist()
    ema_short = talib.EMA(numpy.array(close), timeperiod=short_n)
    ema_long = talib.EMA(numpy.array(close), timeperiod=long_n)
    PO = (ema_short[-1] - ema_long[-1]) / ema_long[-1] * 100
    return PO


def pos(ohlcv: pd.DataFrame, n=100):
    close = ohlcv['close'].tolist()
    if len(close) < 2 * n:
        return 0
    n_day_price_list = []
    for day in range(1, n):
        ref_close_n = close[-(n + day + 1)]
        price = (close[-day] - ref_close_n) / ref_close_n
        n_day_price_list.append(price)
    np_price = numpy.array(n_day_price_list)
    ref_close_n = close[-(n + 1)]
    current_price = (close[-1] - ref_close_n) / ref_close_n
    POS = (current_price - np_price.min()) / (np_price.max() - np_price.min())
    return POS * 100


def adtm(ohlcv: pd.DataFrame, n=20):
    open_arr = ohlcv['open'].tolist()
    high_arr = ohlcv['high'].tolist()
    low_arr = ohlcv['low'].tolist()
    if len(low_arr) < n + 1:
        return 0
    dtm_list = []
    dbm_list = []
    for day in range(1, n + 1):
        ref_open = open_arr[-day - 1]
        open = open_arr[-day]
        high = high_arr[-day]
        low = low_arr[-day]
        dtm = max(high - open, open - ref_open) if open > ref_open else 0
        dbm = max(open - low, ref_open - open) if open < ref_open else 0
        dtm_list.append(dtm)
        dbm_list.append(dbm)
    stm = sum(dtm_list)
    sbm = sum(dbm_list)
    ADTM = (stm - sbm) / max(stm, sbm)
    return ADTM


def test_indicator():
    data = pd.read_csv('./index_history_data/399987.csv')
    TII(ohlcv=data, signal_type='EMA')


# test_indicator()
