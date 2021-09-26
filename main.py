import datetime

import backtrader as bt


class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    # def next(self):
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
    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):
        dt = self.data.datetime.date()

        portfolio_value = self.broker.get_value()
        print('%04d - %s - Position Size:     %02d - Value %.2f' %
              (len(self), dt.isoformat(), self.position.size, portfolio_value))

        data_value = self.broker.get_value([self.data])

        # if self.p.use_target_value:
        #     print('%04d - %s - data value %.2f' %
        #           (len(self), dt.isoformat(), data_value))
        #
        # elif self.p.use_target_percent:
        #     port_perc = data_value / portfolio_value
        #     print('%04d - %s - data percent %.2f' %
        #           (len(self), dt.isoformat(), port_perc))
        print('data_value', data_value)
        if self.order:
            return  # pending order execution

        size = dt.day
        if (dt.month % 2) == 0:
            size = 31 - size

        percent = size / 100.0

        print('%04d - %s - Order Target Percent: %.2f' %
              (len(self), dt.isoformat(), percent))

        self.order = self.order_target_percent(target=percent)


def runstart():
    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    # cerebro.addstrategy(TestStrategy)
    cerebro.addstrategy(Strategy_percent)
    # Get a pandas dataframe
    dt_start = datetime.datetime.strptime("20100101", "%Y%m%d")
    dt_end = datetime.datetime.strptime("20210923", "%Y%m%d")
    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.GenericCSVData(
        dataname=r'./000300.csv',
        fromdate=dt_start,  # 起止日期
        todate=dt_end,
        nullvalue=0.0,
        dtformat=('%Y-%m-%d'),  # 日期列的格式
        datetime=0,  # 各列的位置，从0开始，如列缺失则为None，-1表示自动根据列名判断
        high=3,
        low=4,
        open=1,
        close=2,
        volume=5,
        openinterest=-1
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)
    # 手续费
    cerebro.broker.setcommission(commission=0.0003)
    # 滑点
    cerebro.broker.set_slippage_fixed(0.01)
    # Run over everything
    cerebro.run()
    # Plot the result
    # cerebro.plot(style='bar')


if __name__ == '__main__':
    runstart()
