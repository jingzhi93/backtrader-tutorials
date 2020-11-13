import math
import backtrader as bt

class GoldenCross(bt.Strategy):
    params = (('fast', 50), ('slow', 200), ('order_percentage', 0.95), ('ticker', 'SPY'))

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname="50 day moving avg")

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname="200 day moving avg")

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()} {txt}')  # Comment this line when running optimization

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # An active Buy/Sell order has been submitted/accepted - Nothing to do
            return
        #check if an order is completed
        #Note: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f"BUY EXECUTED, {order.executed.price:.2f}")
            if order.issell():
                self.log(f"SELL EXECUTED, {order.executed.price:.2f}")
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        #reset order
        self.order = None

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                # print(f"Buy {self.size} shares of {self.params.ticker} at {self.data.close[0]}")
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                # print(f"Sell {self.size} shares of {self.params.ticker} at {self.data.close[0]}")
                self.close()