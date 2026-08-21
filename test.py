from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta

import numpy as np

from constants import PATH_SP500, PATH_SP500_TR
from data import load_sp500
from strategy.buy_and_hold import BuyAndHold
from strategy.dca import DCA
from strategy.timed_dca import TimedDCA


def print_result(results: list, period: int, prefix=None) -> None:
    if prefix:
        print(prefix)

    mean_return = np.mean(results)
    low = np.min(results)
    high = np.max(results)
    std = np.std(results)
    cagr = (mean_return + 1) ** (1 / period) - 1
    print(f'mean return: {mean_return * 100:.2f}%, mean CAGR: {cagr * 100:.2f}%')
    print(f'low: {low * 100:.2f}%, high: {high * 100:.2f}%, std: {std * 100:.2f}%')

    return

if __name__ == '__main__':
    # parameters
    budget = 10000 # dollars maybe
    year_start = 1928
    # year_start = 1989
    year_end = 2015 # this + testing period is the final year in dataset
    testing_period = 10 # years

    data = load_sp500(PATH_SP500)
    # data = load_sp500(PATH_SP500_TR)

    slices = []
    for year in range(year_start, year_end + 1):
        starting_date = datetime(year=year, month=1, day=1, tzinfo=UTC)
        end_date = starting_date + relativedelta(years=testing_period)
        slices += [data.loc[starting_date: end_date]]

    # generate parameter grid for the timed dca
    param_dca_portion = np.linspace(0.2, 0.8, 7)
    param_threshold = np.linspace(0.95, 0.99, 5)
    param_grid = [(round(dca_portion, 2), round(threshold, 2)) for dca_portion in param_dca_portion for threshold in param_threshold]

    results = []
    for sliced_data in slices:
        # initialize the strategies
        strategies = [
            BuyAndHold(budget), 
            DCA(budget, years=5)
        ] + [
            TimedDCA(budget, years=5, dca_portion=dca_portion, threshold=threshold) for dca_portion, threshold in param_grid
        ]

        for row in sliced_data.itertuples():
            date, open_, high, low, close = row[:5]
            for strategy in strategies:
                strategy(date, open_, high, low, close)

        run = []
        for strategy in strategies:
            run.append(strategy.get_results()[1])
        results.append(run)

    results = np.array(results).T

    print(f'{testing_period} year testing period, number of samples = {len(slices)}')

    prefixes = [
        'benchmark 1 (Buy and Hold)', 
        'benchmark 2 (DCA, invested monthly in the first 5 years)'
    ] + [
        f'Timed DCA ({int(dca_portion*100)}%, {int(threshold*100)}%)' for dca_portion, threshold in param_grid 
    ] 
    for result, prefix in zip(results, prefixes):
        print('-' * 40)
        print_result(result, testing_period, prefix)

    # chart it out
    import matplotlib.pyplot as plt

    timed_dca_returns = np.mean(results[2:], axis=1)

    Z = timed_dca_returns.reshape(len(param_dca_portion), len(param_threshold)).T
    fig, ax = plt.subplots()

    cax = ax.imshow(
        Z * 100, 
        cmap='viridis',
        origin='lower',
        extent=[param_dca_portion[0] * 100, param_dca_portion[-1] * 100, param_threshold[0] * 100, param_threshold[-1] * 100],
        aspect='auto'
    )

    fig.colorbar(cax, label='Mean 10 Year Returns (%)')
    ax.set_xlabel('Regular Contribution Portion (%)')
    ax.set_ylabel('Market Dip Threshold (%)')
    ax.set_title('Timed DCA Parameter Sweep')

    ax.set_xticks(param_dca_portion * 100)
    ax.set_yticks(param_threshold * 100)

    plt.tight_layout()
    plt.show()