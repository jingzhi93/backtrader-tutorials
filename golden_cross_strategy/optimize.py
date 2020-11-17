import datetime
import backtrader as bt
import pandas as pd
from strategies.GoldenCross import GoldenCross

cerebro = bt.Cerebro(optreturn=False)

#Set data parameters and add to Cerebro
spy_prices = pd.read_csv('data/SPY.csv', index_col='Date', parse_dates=True)
feed = bt.feeds.PandasData(dataname=spy_prices)
cerebro.adddata(feed)

#Add strategy to Cerebro
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
cerebro.optstrategy(GoldenCross, fast=range(30, 60), slow=range(150, 250))

#Default position size
cerebro.addsizer(bt.sizers.SizerFix, stake=3)

if __name__ == '__main__':
    optimized_runs = cerebro.run()

    final_results_list = []
    for run in optimized_runs:
        print(f"Run {run}")
        for strategy in run:
            PnL = round(strategy.broker.get_value() - 10000,2)
            sharpe = strategy.analyzers.sharpe_ratio.get_analysis()
            final_results_list.append([strategy.params.fast,
                strategy.params.slow, PnL, sharpe['sharperatio']])

            print(f"Fast SMA: {strategy.params.fast} Slow SMA: {strategy.params.slow} Sharpe Ratio: {sharpe['sharperatio']}")

    sort_by_sharpe = sorted(final_results_list, key=lambda x: x[3],
                             reverse=True)
    for line in sort_by_sharpe[:5]:
        print(line)