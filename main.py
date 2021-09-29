import datetime
import backtrader as bt
import pandas as pd
import backtrader.analyzers as btanalyzers

import strategy as yt_strategy


class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volume
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

    def next(self):
        close_last_100 = self.dataclose.get(size=100)
        volume_last_100 = self.datavolume.get(size=100)
        high_last_100 = self.datahigh.get(size=100)
        low_last_100 = self.datalow.get(size=100)
        if len(close_last_100) and len(volume_last_100) > 0:
            fund_index_hist_sina_df = pd.DataFrame(
                {"close": close_last_100, 'amount': volume_last_100, "high": high_last_100, "low": low_last_100})
            strategy_new_result = yt_strategy.strategy_combine(fund_index_hist_sina_df)
            percent = ((strategy_new_result.count('buy')) / len(strategy_new_result))
            print(percent)
    # Simply log the closing price of the series from the reference
    # self.log('Close, %.2f' % self.dataclose[0])
    # 数据切片
    # myslice = self.dataclose.get(size=5)
    # self.order = self.order_target_percent(target=5)
    # self.buy()
    # print(self.position)
    # if len(myslice) > 0:
    #     print(myslice)


class Strategy_percent(bt.Strategy):
    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavolume = self.datas[0].volume
        self.datahigh = self.datas[0].high
        self.datalow = self.datas[0].low

    def log(self, txt, dt=None, doprint=False):
        '''log记录'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):

        if self.order:
            return  # pending order execution

        close_last_100 = self.dataclose.get(size=100)
        volume_last_100 = self.datavolume.get(size=100)
        high_last_100 = self.datahigh.get(size=100)
        low_last_100 = self.datalow.get(size=100)
        if len(close_last_100) and len(volume_last_100) > 0:
            fund_index_hist_sina_df = pd.DataFrame(
                {"close": close_last_100, 'amount': volume_last_100, "high": high_last_100, "low": low_last_100})
            strategy_new_result = yt_strategy.strategy_combine(fund_index_hist_sina_df)
            percent = ((strategy_new_result.count('buy')) / len(strategy_new_result))
            self.order = self.order_target_percent(target=percent)

    def stop(self):
        data_value = self.broker.get_value([self.data])
        dt = self.data.datetime.date()
        portfolio_value = self.broker.get_value()
        print('%04d - %s - Position Size:     %02d - Value %.2f' %
              (len(self), dt.isoformat(), self.position.size, portfolio_value))
        print('data_value', data_value)
        # self.log("最大回撤:-%.2f%%" % self.stats.drawdown.maxdrawdown[-1], doprint=True)


def runstart():
    # Create a cerebro entity
    cerebro = bt.Cerebro()

    # Add a strategy
    # cerebro.addstrategy(TestStrategy)
    cerebro.addstrategy(Strategy_percent)
    # Get a pandas dataframe
    dt_start = datetime.datetime.strptime("20100101", "%Y%m%d")
    dt_end = datetime.datetime.strptime("20210927", "%Y%m%d")
    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.GenericCSVData(
        dataname=r'./399006.csv',
        fromdate=dt_start,  # 起止日期
        todate=dt_end,
        nullvalue=0.0,
        dtformat=('%Y-%m-%d'),  # 日期列的格式
        datetime=0,  # 各列的位置，从0开始，如列缺失则为None，-1表示自动根据列名判断
        high=3,
        low=4,
        open=1,
        close=2,
        volume=6,
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    # 手续费
    cerebro.broker.setcommission(commission=0.0003)
    # 滑点
    cerebro.broker.set_slippage_fixed(0.01)
    cerebro.addobserver(bt.observers.DrawDown)
    # Run over everything
    # cerebro.run()
    # Plot the result
    # cerebro.plot(style='bar')
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name="AR")
    cerebro.addanalyzer(btanalyzers.DrawDown, _name="DD")
    cerebro.addanalyzer(btanalyzers.Returns, _name="RE")
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name="TA")
    cerebro.addanalyzer(btanalyzers.SQN, _name="SQN")
    results = cerebro.run()
    thestrat = results[0]
    #
    print("年化收益率:", thestrat.analyzers.AR.get_analysis())
    print("最大回撤:%.2f，最大回撤周期%d" % (
        thestrat.analyzers.DD.get_analysis().max.drawdown, thestrat.analyzers.DD.get_analysis().max.len))
    print("总收益率:%.2f" % (thestrat.analyzers.RE.get_analysis()["rtot"]))
    trade_info = results[0].analyzers.TA.get_analysis()
    total_trade_num = trade_info["total"]["total"]
    win_num = trade_info["won"]["total"]
    lost_num = trade_info["lost"]["total"]
    pnl_won = trade_info['won']['pnl']['total']
    pnl_lost = trade_info['lost']['pnl']['total']
    print('交易次数:', total_trade_num)
    print('胜率:', win_num / total_trade_num,'败率:', lost_num / total_trade_num,'盈亏比:', pnl_won / - pnl_lost)
    print('SQN:',thestrat.analyzers.SQN.get_analysis().sqn)
    # print('败率:', lost_num / total_trade_num)
    # print('盈亏比:', pnl_won / - pnl_lost)


if __name__ == '__main__':
    runstart()
