import pandas as pd
import backtrader as bt
from strategies.GoldenCross import GoldenCross
from strategies.BuyHold import BuyHold
import backtrader.analyzers as btanalyzers


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.broker.set_cash(100000)
    spy_prices = pd.read_csv('data/SPY.csv', index_col='Date', parse_dates=True)
    feed = bt.feeds.PandasData(dataname=spy_prices)
    cerebro.adddata(feed)

    cerebro.addstrategy(GoldenCross)
    # cerebro.addstrategy(BuyHold)

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name = "sharpe")
    cerebro.addanalyzer(btanalyzers.Transactions, _name = "transactions")
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name = "trades")

    back = cerebro.run()
    cerebro.plot()

    cerebro.broker.getvalue()
    sharp = back[0].analyzers.sharpe.get_analysis()
    transactions = back[0].analyzers.transactions.get_analysis()
    trades = back[0].analyzers.trades.get_analysis()

    print("#"*20)
    print(f"SharpeRatio: {sharp['sharperatio']}")



