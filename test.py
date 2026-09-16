from os.path import join as path_join
from datetime import datetime

import numpy as np

from constants import *
from data import load_sp500, get_slices
from results import print_result, generate_report
from strategy.buy_and_hold import BuyAndHold
from strategy.dca import DCA
from strategy.timed_dca import TimedDCA
from strategy.reverse_timed_dca import ReverseTimedDCA


def run_test(slices: list, strategies: list, parameters: list) -> np.ndarray:
    """
    does what is says

    Args:
        slices (list): data slices
        strategies (list): list of strategy classes
        parameters (list): initializing parameters for each strategy classes

    Returns:
        np.ndarray: results
    """
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