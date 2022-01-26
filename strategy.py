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


def po_strategy(ohlcv: pd.DataFrame, short=20, long=9):
    po_value = indicator.po(ohlcv=ohlcv, short_n=short, long_n=long)
    direct = 'buy' if po_value > 0 else 'sell'
    return direct


def pos_strategy(ohlcv: pd.DataFrame, n=100):
    direct = ''
    back_day = -1
    pos_value = indicator.pos(ohlcv=ohlcv, n=n)
    if pos_value > 80:
        direct = 'buy'
    if pos_value < 20:
        direct = 'sell'
    while direct == '':
        pos_value = indicator.pos(ohlcv=ohlcv[:back_day], n=n)
        if pos_value > 80:
            direct = 'buy'
        if pos_value < 20:
            direct = 'sell'
        back_day = back_day - 1
    return direct


def adtm_strategy(ohlcv: pd.DataFrame, n=20):
    direct = ''
    back_day = -1
    adtm_value = indicator.adtm(ohlcv=ohlcv, n=n)
    if adtm_value > 0.5:
        direct = 'buy'
    if adtm_value < -0.5:
        direct = 'sell'
    while direct == '':
        adtm_value = indicator.adtm(ohlcv=ohlcv[:back_day], n=n)
        if adtm_value > 0.5:
            direct = 'buy'
        if adtm_value < -0.5:
            direct = 'sell'
        back_day = back_day - 1
    return direct


def ma_strategy(ohlcv: pd.DataFrame, slow=20, fast=5):
    ma1 = indicator.ma(ohlcv=ohlcv, n=slow)
    ma2 = indicator.ma(ohlcv=ohlcv, n=fast)
    direct = 'buy' if ma2 > ma1 else 'sell'
    return direct


def ma_cross_strategy(ohlcv: pd.DataFrame, n=5):
    ma = indicator.ma(ohlcv=ohlcv, n=n)
    close = ohlcv['close'].tolist()[-1]
    direct = 'buy' if close > ma else 'sell'
    return direct


def macd_strategy(ohlcv: pd.DataFrame):
    macdhist = indicator.macd(ohlcv=ohlcv)
    direct = 'buy' if macdhist > 0 else 'sell'
    return direct


def strategy_combine(etf_data: pd.DataFrame):
    # tii = tii_strategy(etf_data)
    # er = er_strategy(etf_data)
    # macd = macd_strategy(etf_data)
    maamt = maamt_strategy(etf_data)
    dpo = dpo_strategy(etf_data)
    # ma5ma20 = ma_strategy(etf_data, slow=20, fast=5)
    # ma5 = ma_cross_strategy(etf_data, n=5)
    # adtm = adtm_strategy(ohlcv=etf_data)
    # pos = pos_strategy(ohlcv=etf_data)
    # po = po_strategy(ohlcv=etf_data)


    mesa = mesa_strategy(etf_data=etf_data)
    # return [tii, maamt, dpo]
    # 1.6
    # return [tii, er, maamt, dpo]  #胜率: 0.3739130434782609 败率: 0.6260869565217392 盈亏比: 2.2802850351731516
    # 1.5
    # return [er, maamt, dpo] # 胜率: 0.371900826446281 败率: 0.628099173553719 盈亏比: 2.1608333617392135
    # 1.81742
    # return [tii, maamt, dpo]  # 胜率: 0.3816793893129771 败率: 0.6183206106870229 盈亏比: 2.3604458652855973
    # .53
    # 胜率: 0.3235294117647059 败率: 0.6764705882352942 盈亏比: 2.0789329373182297
    # return [tii, er, dpo]
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
    # return [tii, er] # 胜率: 0.3108108108108108 败率: 0.6891891891891891 盈亏比: 1.909201015635396
    # 1.75
    # return [dpo, tii]  # 胜率: 0.3108108108108108 败率: 0.6891891891891891 盈亏比: 2.2012029435186897
    # 1.8319
    # return [tii, maamt]  # 胜率: 0.4268292682926829 败率: 0.573170731707317 盈亏比: 1.8585261302548868
    # 1.59
    # return [tii, er]  # 胜率: 0.30303030303030304 败率: 0.696969696969697 盈亏比: 1.9713099171089428
    # return [po]
    # -0.79
    # return [ma]
    # return [ma5]
    # return [tii, dpo, ma20]
    return [tii, dpo]
    # return [tii, dpo, macd]


# 年化收益率: OrderedDict([(2011, 0.0), (2012, -0.059182187190000124), (2013, 0.21184097379568878), (2014, 0.1917914917428023), (2015, 0.8007249383493), (2016, -0.1507829522782037), (2017, -0.01127350180272646), (2018, -0.10268130902155193), (2019, 0.33992611896744496), (2020, 0.17938762923141116), (2021, 0.1827567250195965)])
# 夏普: 0.5257240252754136
# 最大回撤:29.56，最大回撤周期1004
# 总收益率:1.24
# 交易次数: 112
# 胜率: 0.4107142857142857 败率: 0.5892857142857143 盈亏比: 3.525653102685943


"""[tii,dpo,ma5]
data_value 281253.2310494999
年化收益率: OrderedDict([(2011, -0.04119968818999997), (2012, 0.01882378419957842), (2013, 0.3056540618771675), (2014, 0.18181507291218213), (2015, 0.5628987980530786), (2016, -0.2019335373515344), (2017, -0.046540160086823934), (2018, -0.14016290713412827), (2019, 0.30787259960238256), (2020, 0.21976831106543226), (2021, 0.14382963124791814)])
夏普: 0.5042570018688546
最大回撤:41.18，最大回撤周期1136
总收益率:1.03
交易次数: 354
胜率: 0.307909604519774 败率: 0.6892655367231638
盈亏比: 4.043362140192906
"""
"""[tii,dpo,ma20]
data_value 321728.0673944993
年化收益率: OrderedDict([(2011, 0.0015117763999998868), (2012, -0.01369380944705234), (2013, 0.35183486619979254), (2014, 0.18701623126666966), (2015, 0.7539952210568952), (2016, -0.19125035128587353), (2017, -0.016417195509788374), (2018, -0.19681642976075064), (2019, 0.31343327359745676), (2020, 0.16737537059129148), (2021, 0.18128322009173314)])
夏普: 0.49824257496753044
最大回撤:41.58，最大回撤周期1257
总收益率:1.17
交易次数: 199
胜率: 0.2562814070351759 败率: 0.7386934673366834
盈亏比: 5.4981216797538695
"""

"""[tii,dpo,er]
data_value 358809.4218454998
年化收益率: OrderedDict([(2011, -0.02516195696000023), (2012, -0.04140536831033714), (2013, 0.43481565866040994), (2014, 0.21269079778886146), (2015, 0.8953848747353756), (2016, -0.22462050308094028), (2017, -0.029791284113337313), (2018, -0.18807871894155792), (2019, 0.3615775489491768), (2020, 0.1572913710997974), (2021, 0.2096905008009895)])
夏普: 0.4880332268041014
最大回撤:42.74，最大回撤周期1258
总收益率:1.28
交易次数: 129
胜率: 0.3178294573643411 败率: 0.6744186046511628
盈亏比: 4.451482596483896
"""

"""[tii,dpo]
data_value 370141.0625619998
年化收益率: OrderedDict([(2011, -0.02988747479000009), (2012, 0.0022234605099371585), (2013, 0.38322613327214405), (2014, 0.2746594048242117), (2015, 0.7090524305643156), (2016, -0.17215740403720592), (2017, -0.0209974934326862), (2018, -0.17705671036428083), (2019, 0.37849850519949113), (2020, 0.1298947387661049), (2021, 0.21616387105604518)])
夏普: 0.5575185272675115
最大回撤:37.36，最大回撤周期1041
总收益率:1.31
交易次数: 143
胜率: 0.3006993006993007 败率: 0.6923076923076923
盈亏比: 5.140338880809589
"""

"""[tii,dpo,maamt]
data_value 377521.50475650013
年化收益率: OrderedDict([(2011, 0.0038757196100001057), (2012, -0.01893779200814316), (2013, 0.21614413169952984), (2014, 0.22484771511394497), (2015, 0.8473751396879334), (2016, -0.14925007305987859), (2017, -0.004608291688304678), (2018, -0.11400255727688258), (2019, 0.3467077815430264), (2020, 0.1511224356620806), (2021, 0.19762171869644396)])
夏普: 0.546609622980752
最大回撤:30.29，最大回撤周期1006
总收益率:1.33
交易次数: 243
胜率: 0.4074074074074074 败率: 0.588477366255144
盈亏比: 3.503674291786867

"""

"""ma5
data_value 147724.99977899977
年化收益率: OrderedDict([(2011, -0.022078309564999787), (2012, 0.039581128027524226), (2013, 0.149754392329017), (2014, 0.007744577452174717), (2015, 0.22502833712991643), (2016, -0.2667936049767201), (2017, -0.09471851133611842), (2018, -0.06779604298305397), (2019, 0.17328234350277105), (2020, 0.3968872102281984), (2021, 0.009497267148574906)])
夏普: 0.23471976488397983
最大回撤:55.95，最大回撤周期1539
总收益率:0.39
交易次数: 672
胜率: 0.35119047619047616 败率: 0.6473214285714286
盈亏比: 2.020116174238302

"""
"""
//@version=4
study("Trend Intensity Index With SignalLine", overlay=false)

//Inputs
SMALength = input(title = "SmaLength", type = input.integer, defval = 20)
Src = input(title = "Src", type = input.source, defval = close)
SignalType = input(title = "Signal Type?", defval = "JURIK", options = ["JURIK", "SMA", "EMA", "RMA", "VWMA"])
Sma = sma(Src, SMALength)
SignalLen = input(title = "SignalLen", defval = 20)
phase = input(title="JurikPhase", type=input.integer, defval=0)
power = input(title="JurikPower", type=input.integer, defval=2)

//Mathsshiz... calculating the TII...
Dev = Src - Sma


PosDev = 0.00
NegDev = 0.00


if Dev > 0  
    PosDev := Dev

if Dev < 0
    NegDev := abs(Dev) 

m = 0

m := (SMALength % 2 == 0) ? SMALength/2 : (SMALength + 1) / 2

Sumpos = sum(PosDev, m)
Negpos = sum(NegDev, m)

//BOOOM!

TrendIntensity = 100 * (Sumpos) / (Sumpos + Negpos)


    

//Signal Moving Averages

SignalMa = 0.00

if SignalType == "JURIK" // many thanks to the wonderful coder, Everget, for this
    /// Copyright © 2018 Alex Orekhov (everget)
    /// Copyright © 2017 Jurik Research and Consulting

    phaseRatio = phase < -100 ? 0.5 : phase > 100 ? 2.5 : phase / 100 + 1.5
    beta = 0.45 * (SignalLen - 1) / (0.45 * (SignalLen - 1) + 2)
    alpha = pow(beta, power)
    jma = 0.0
    e0 = 0.0
    e0 := (1 - alpha) * TrendIntensity + alpha * nz(e0[1])
    e1 = 0.0
    e1 := (TrendIntensity - e0) * (1 - beta) + beta * nz(e1[1])
    e2 = 0.0
    e2 := (e0 + phaseRatio * e1 - nz(jma[1])) * pow(1 - alpha, 2) + pow(alpha, 2) * nz(e2[1])
    jma := e2 + nz(jma[1])
    SignalMa := jma

if SignalType == "EMA"
    SignalMa := ema(TrendIntensity, SignalLen)

if SignalType == "SMA"
    SignalMa := sma(TrendIntensity, SignalLen)

if SignalType == "RMA"
    SignalMa := rma(TrendIntensity, SignalLen)

if SignalType == "VWMA"
    SignalMa := vwma(TrendIntensity, SignalLen)

//Lovely job... now it'd be extra nice to have a Histogram plotting the difference between the SignalLine and the TII. When this is flat, market is potentially ranging.


Dist = TrendIntensity - SignalMa
Distance = abs(Dist)

plot(Distance, style = plot.style_columns, color = TrendIntensity >= SignalMa and TrendIntensity > 2? color.green : TrendIntensity <= SignalMa and TrendIntensity < 98 ? color.red : color.green, transp = 0)
plot(TrendIntensity, style = plot.style_line, linewidth = 3, color = color.aqua)
plot(SignalMa, style = plot.style_line, linewidth = 2, color = color.maroon)

"""

"""
dpo macd tii
夏普: 0.6595065130398121
最大回撤:24.37，最大回撤周期214
总收益率:0.74
交易次数: 49
胜率: 0.3877551020408163 败率: 0.5918367346938775
盈亏比: 2.901783274178244


tii dpo
夏普: 0.6188676736173646
最大回撤:29.24，最大回撤周期287
总收益率:0.57
交易次数: 46
胜率: 0.43478260869565216 败率: 0.5434782608695652
盈亏比: 2.112487994259678
"""
