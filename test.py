from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta

import numpy as np

from constants import PATH_SP500, PATH_SP500_TR
from data import load_sp500
from strategy.buy_and_hold import BuyAndHold
from strategy.dca import DCA
from strategy.timed_dca import TimedDCA


# parameters
budget = 10000 # dollars maybe
# year_start = 1930
year_start = 1989
year_end = 2015 # this + testing period is the final year in dataset
testing_period = 10 # years

# data = load_sp500(PATH_SP500)
data = load_sp500(PATH_SP500_TR)

slices = []
for year in range(year_start, year_end + 1):
    starting_date = datetime(year=year, month=1, day=1, tzinfo=UTC)
    end_date = starting_date + relativedelta(years=testing_period)
    slices += [data.loc[starting_date: end_date]]

benchmark_results = []
dca_results = []
timed_dca_results = []
for sliced_data in slices:
    # initialize the strategies
    benchmark = BuyAndHold(budget)
    dca = DCA(budget, years=5)
    timed_dca = TimedDCA(budget, years=5, dca_portion=0.8, threshold=0.99)

    for row in sliced_data.itertuples():
        date, open_, high, low, close = row[:5]
        benchmark(date, open_, high, low, close)
        dca(date, open_, high, low, close)
        timed_dca(date, open_, high, low, close)

    benchmark_results += [benchmark.get_results()[1]]
    dca_results += [dca.get_results()[1]]
    timed_dca_results += [timed_dca.get_results()[1]]

benchmark_return = np.mean(benchmark_results)
dca_return = np.mean(dca_results)
timed_dca_return = np.mean(timed_dca_results)

print(f'{testing_period} year testing period, number of samples = {len(slices)}')

print('-' * 40)
print('benchmark 1 (lump sum buy and hold)')
print(f'mean return: {benchmark_return * 100:.2f}%, mean CAGR: {((benchmark_return + 1) ** (1 / testing_period) - 1) * 100:.2f}%')

print('-' * 40)
print('benchmark 2 (DCA, invested monthly in the first 5 years)')
print(f'mean return: {dca_return * 100:.2f}%, mean CAGR: {((dca_return + 1) ** (1 / testing_period) - 1) * 100:.2f}%')

print('-' * 40)
print('timed DCA')
print(f'mean return: {timed_dca_return * 100:.2f}%, mean CAGR: {((timed_dca_return + 1) ** (1 / testing_period) - 1) * 100:.2f}%')