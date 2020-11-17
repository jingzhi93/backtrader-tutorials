import pandas as pd
import backtrader as bt
import backtrader.analyzers as btanalyzers
from datetime import datetime

data1 = bt.feeds.YahooFinanceData(dataname = 'data/BTC-USD.csv', fromdate = datetime(2018, 1, 1), todate = datetime(2020, 10, 1))
data2 = bt.feeds.GenericCSVData(
    dataname='data/BTC_Gtrends.csv',
    fromdate=datetime(2018, 1, 1),
    todate=datetime(2020, 10, 1),
    nullvalue=0.0,
    dtformat=('%Y-%m'),
    datetime=0,
    time=-1,
    high=-1,
    low=-1,
    open=-1,
    close=1,
    volume=-1,
    openinterest=-1,
    timeframe=bt.TimeFrame.Weeks)

cerebro = bt.Cerebro()
cerebro.adddata(data1)
cerebro.adddata(data2)

cerebro.run()
cerebro.plot()