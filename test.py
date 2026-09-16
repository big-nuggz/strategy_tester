from os.path import join as path_join
from datetime import datetime

import numpy as np

from constants import *
from data import load_sp500, get_slices
from markdown import generate_table, get_best_indices
from strategy.buy_and_hold import BuyAndHold
from strategy.dca import DCA
from strategy.timed_dca import TimedDCA
from strategy.reverse_timed_dca import ReverseTimedDCA


def print_result(results: list, period: int, prefix=None) -> None:
    if prefix:
        print(prefix)

    mean_return, low, high, std, cagr = get_result_metrics(results, period)

    print(f'mean return: {mean_return * 100:.2f}%, mean CAGR: {cagr * 100:.2f}%')
    print(f'low: {low * 100:.2f}%, high: {high * 100:.2f}%, std: {std * 100:.2f}%')

    return

def get_result_metrics(results: list, period: int):
    mean_return = np.mean(results)
    low = np.min(results)
    high = np.max(results)
    std = np.std(results)
    cagr = (mean_return + 1) ** (1 / period) - 1

    return (mean_return, low, high, std, cagr)

def generate_report(
        path: str, 
        results_price_only: list, 
        results_total_return: list, 
        period: int, 
        prefixes: list, 
        date: datetime):
    """
    generates and writes a neat markdown result
    """
    date_text = date.isoformat()
    
    # table headers
    header = ['Strategy', 'Mean 10 Year Return', 'Minimum 10 Year Return', 'Maximum 10 Year Return', 'Std. Deviation', 'Mean CAGR']

    units = ['', '%', '%', '%', '%', '%']
    evaluators=[None, np.argmax, np.argmax, np.argmax, np.argmin, np.argmax]

    data_price_only = [header]
    for result, prefix in zip(results_price_only, prefixes):
        mean_return, low, high, std, cagr = get_result_metrics(result, period)
        data_price_only += [[
            prefix, 
            float(mean_return * 100), 
            float(low * 100), 
            float(high * 100), 
            float(std * 100), 
            float(cagr * 100)]]

    data_total_return = [header]
    for result, prefix in zip(results_total_return, prefixes):
        mean_return, low, high, std, cagr = get_result_metrics(result, period)
        data_total_return += [[
            prefix, 
            float(mean_return * 100), 
            float(low * 100), 
            float(high * 100), 
            float(std * 100), 
            float(cagr * 100)]]

    table_price_only = generate_table(
        data_price_only, 
        units=units, 
        highlights=get_best_indices(data_price_only, evaluators))

    table_total_return = generate_table(
        data_total_return, 
        units=units, 
        highlights=get_best_indices(data_total_return, evaluators))

    with open(path, 'w', encoding='utf8') as f:
        f.write(f'# Test Result Report (run: {date_text})')
        f.write('\n' * 2)
        f.write(f'## S&P 500 Price Only')
        f.write('\n' * 2)
        f.write(table_price_only)
        f.write('\n' * 2)
        f.write(f'## S&P 500 Total Return')
        f.write('\n' * 2)
        f.write(table_total_return)
        f.write('\n')

def run_test(slices: list, strategies: list, parameters: list):
    results = []
    for sliced_data in slices:
        # initialize the strategies
        active_strategies = [
            strategy(**parameter) 
            for strategy, parameter in zip(strategies, parameters)]

        for row in sliced_data.itertuples():
            date, open_, high, low, close = row[:5]
            for strategy in active_strategies:
                strategy(date, open_, high, low, close)

        run = []
        for strategy in active_strategies:
            run.append(strategy.get_results()[1])
        results.append(run)

    results = np.array(results).T
    return results


# run with: python -m test
if __name__ == '__main__':
    # add strategies and their initializing parameters here
    strategies = [
        BuyAndHold, 
        DCA, 
        TimedDCA, 
        ReverseTimedDCA
    ]

    parameters = [
        {'budget': BUDGET}, 
        {'budget': BUDGET, 'years': 5}, 
        {'budget': BUDGET, 'years': 5, 'dca_portion': 0.80, 'threshold': 0.99}, 
        {'budget': BUDGET, 'years': 5, 'dca_portion': 0.80, 'threshold': 0.95}
    ]

    starting_time = datetime.now()

    slices_price_only = get_slices(load_sp500(path=PATH_SP500), YEAR_START, YEAR_END)
    results_price_only = run_test(slices_price_only, strategies, parameters)

    slices_total_return = get_slices(load_sp500(path=PATH_SP500_TR), YEAR_START_TOTAL_RETURN, YEAR_END)
    results_total_return = run_test(slices_total_return, strategies, parameters)

    # show and save results
    prefixes = [strategy.name for strategy in strategies]

    print('S&P 500 price only')
    print(f'{TESTING_PERIOD} year testing period, number of samples = {len(slices_price_only)}')
    print('=' * 40)
    
    for result, prefix in zip(results_price_only, prefixes):
        print('-' * 40)
        print_result(result, TESTING_PERIOD, prefix)

    print('S&P 500 total return')
    print(f'{TESTING_PERIOD} year testing period, number of samples = {len(slices_total_return)}')
    print('=' * 40)
    
    for result, prefix in zip(results_total_return, prefixes):
        print('-' * 40)
        print_result(result, TESTING_PERIOD, prefix)

    report_path = path_join(PATH_REPORT_ROOT, 'result.md')
    generate_report(
        report_path, 
        results_price_only, 
        results_total_return,
        TESTING_PERIOD, 
        prefixes, 
        starting_time)

    print('=' * 40)
    print(f'report generated in {report_path}')