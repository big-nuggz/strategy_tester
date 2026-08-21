from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta

from data import load_sp500
from strategy.buy_and_hold import BuyAndHold
from strategy.dca import DCA


# parameters
budget = 10000 # dollars maybe
starting_date = datetime(year=1990, month=1, day=1, tzinfo=UTC)
testing_period = 10 # years

data = load_sp500()

end_date = starting_date + relativedelta(years=testing_period)
sliced_data = data.loc[starting_date: end_date]

# initialize the strategies
benchmark = BuyAndHold(budget)
dca = DCA(budget, years=5)

for row in sliced_data.itertuples():
    date, open_, high, low, close = row[:5]
    benchmark(date, open_, high, low, close)
    dca(date, open_, high, low, close)

benchmark_result = benchmark.get_results()
dca_result = dca.get_results()

print(f'initial investment ${budget:.2f} with {testing_period} year testing period')
print('-' * 40)
print('benchmark (lump sum buy and hold)')
print(f'portfolio value: ${benchmark_result[0]:.2f}, return: {benchmark_result[1] * 100:.2f}%, CAGR: {((benchmark_result[1] + 1) ** (1 / testing_period) - 1) * 100:.2f}%')

print('-' * 40)
print('DCA')
print(f'portfolio value: ${dca_result[0]:.2f}, return: {dca_result[1] * 100:.2f}%, CAGR: {((dca_result[1] + 1) ** (1 / testing_period) - 1) * 100:.2f}%')